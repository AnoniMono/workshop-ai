#!/usr/bin/env python3
"""Pinza a ingranaggi e parallelogramma: un'unica fonte di misure per DXF, PDF, OpenSCAD e anteprima 3D.

Solo libreria standard. Tutte le parti sono piastre estruse, stampabili in piano senza supporti.
Convenzione: Y verso le punte, X laterale, Z spessore. Misure in mm.
"""
import json
import math
import os

# ---------- parametri ----------
MODULE, TEETH, PRESSURE = 1.0, 20, 20.0
BACKLASH = 0.15
CRANK, RAIL = 40.0, 22.0          # lunghezza delle bielle, passo fra i perni
HALF_GEAR = MODULE * TEETH / 2    # gli assi degli ingranaggi stanno a x = +/-10
PAD_X = -17.0                     # faccia di presa rispetto al perno del dito
TH_OPEN, TH_CLOSED, TH_GRIP = 35.0, 79.0, None
PIN_D, PILOT_D = 3.2, 1.8
HUB_D, SLOT_W, SEAT = 7.5, 6.0, 2.0
Z = {"crank": (0, 5), "jaw": (5.5, 11.5), "idler": (12, 17), "low": (-4.5, -0.5), "up": (17.5, 21.5), "post": (-0.5, 17.5)}
RHO, FILL = 1.24, 0.6
SERVO_NM = 0.216                  # MG90S, valore tipico da scheda
SERVO_G = 13.4
OBJ = 30.0
POSTS = [(-18, -20), (18, -20), (0, 27)]
POST_R = 4.0

# ---------- geometria di base ----------


def arc(cx, cy, r, a0, a1, n=16):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def spline(pts, closed=False, n=10):
    """Catmull-Rom passante per i punti."""
    out, m = [], len(pts)
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        if closed:
            p0, p1, p2, p3 = pts[(i - 1) % m], pts[i], pts[(i + 1) % m], pts[(i + 2) % m]
        else:
            p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, m - 1)]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (p2[j] - p0[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t + (3 * p1[j] - p0[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    if not closed:
        out.append(pts[-1])
    return out


def rrect(x0, y0, x1, y1, r):
    return arc(x1 - r, y0 + r, r, -90, 0, 8) + arc(x1 - r, y1 - r, r, 0, 90, 8) + arc(x0 + r, y1 - r, r, 90, 180, 8) + arc(x0 + r, y0 + r, r, 180, 270, 8)


def stadium(ax, ay, bx, by, r):
    ang = math.degrees(math.atan2(by - ay, bx - ax))
    return arc(bx, by, r, ang - 90, ang + 90) + arc(ax, ay, r, ang + 90, ang + 270)


def tf(poly, x=0, y=0, rot=0, mirror=False):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for px, py in poly:
        qx, qy = px * c - py * s, px * s + py * c
        out.append((x - qx if mirror else x + qx, y + qy))
    return out


def area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))) / 2


def inv(a):
    return math.tan(a) - a


def gear_outline(phase, skip=None):
    """Profilo a evolvente. phase = angolo del centro del primo dente. skip = settore (a0,a1) occupato dalla biella."""
    rp = MODULE * TEETH / 2
    rb = rp * math.cos(math.radians(PRESSURE))
    ra, rf = rp + MODULE, rp - 1.25 * MODULE
    psi_p = (math.pi * MODULE / 2 - BACKLASH) / 2 / rp + inv(math.radians(PRESSURE))
    pitch = 360.0 / TEETH
    pts = []
    for k in range(TEETH):
        c = phase + k * pitch
        flank = []
        for i in range(7):
            r = rb + max(0.0, ra - rb) * i / 6
            a = math.acos(rb / r) if r > rb else 0.0
            flank.append((r, math.degrees(psi_p - inv(a))))
        tooth = [(rf, -flank[0][1] - 1.5)] + [(r, -p) for r, p in flank] + [(r, p) for r, p in reversed(flank)] + [(rf, flank[0][1] + 1.5)]
        pts += [(r * math.cos(math.radians(c + a)), r * math.sin(math.radians(c + a))) for r, a in tooth]
    if skip:
        def ang(p):
            return math.degrees(math.atan2(p[1], p[0])) % 360
        pts = [p for p in pts if not (ang(p) > skip[1] or ang(p) < skip[0])]
    return pts


# ---------- parti (coordinate locali) ----------

def crank_part(phase):
    """Ingranaggio con biella lungo +X. phase = fase dei denti rispetto alla biella."""
    half = 5.2
    sector = math.degrees(math.asin(half / 8.5)) + 3
    teeth = gear_outline(phase, skip=(sector, 360 - sector))
    # ordina partendo dal primo punto dopo la biella
    teeth = sorted(teeth, key=lambda p: math.degrees(math.atan2(p[1], p[0])) % 360)
    arm = [(8.2, -half)] + arc(CRANK, 0, 6, -90, 90) + [(8.2, half)]
    return {"outline": arm + teeth, "holes": [((0, 0), PIN_D), ((CRANK, 0), PIN_D)],
            "cut": [stadium(16, 0, 29, 0, 2.3)]}


def idler_part():
    return {"outline": stadium(0, 0, CRANK, 0, 5.5), "holes": [((0, 0), PIN_D), ((CRANK, 0), PIN_D)], "cut": [stadium(10, 0, 30, 0, 2.2)]}


def jaw_part():
    outer = spline([(6.0, 0), (6.6, 12), (6.4, 26), (4.2, 42), (-1.5, 58), (-9.0, 72), (-14.2, 77.2)])
    tip = arc(-15.2, 75.6, 1.9, 58, 180, 8)
    serr = []
    y = 73.5
    while y > 43:
        serr += [(PAD_X, y), (PAD_X + 0.9, y - 1.0), (PAD_X, y - 2.4)]
        y -= 2.4
    inner = spline([(PAD_X, y), (-15.4, 34), (-11.2, 22), (-7.2, 10), (-5.8, 1), (-3.2, -4.8), (0, -6)])
    closing = arc(0, 0, 6, -90, 0, 8)
    window = spline([(-12.8, 45), (-12.8, 62), (-9.6, 64), (-4.4, 52), (-2.6, 40), (-5.4, 32), (-9.4, 33), (-12.0, 39)], closed=True, n=6)
    return {"outline": outer + tip + serr + inner + closing[1:], "holes": [((0, 0), PIN_D), ((0, RAIL), PIN_D)], "cut": [window]}


SERVO_Y = -5.9   # centro del corpo rispetto all'albero
SERVO_EARS = 27.7


def low_plate():
    o = rrect(-26, -38, 26, 33, 7)
    h = [((-10, 0), PIN_D), ((10, 0), 12.0), ((10, SERVO_Y + SERVO_EARS / 2), PILOT_D), ((10, SERVO_Y - SERVO_EARS / 2), PILOT_D)]
    h += [((x, y), PIN_D) for x, y in POSTS]
    h += [((x, y), PIN_D) for x in (-16, 16) for y in (-33,)]
    return {"outline": o, "holes": h, "cut": [rrect(-15, 11, 5, 19, 3)]}


def up_plate():
    o = rrect(-26, -28, 26, 33, 7)
    h = [((x, 0), PIN_D) for x in (-10, 10)] + [((x, RAIL), PIN_D) for x in (-10, 10)] + [((x, y), PIN_D) for x, y in POSTS]
    return {"outline": o, "holes": h, "cut": [rrect(-14, 6, 14, 15, 3), rrect(-16, -22, 16, -9, 4)]}


def post_part():
    return {"outline": arc(0, 0, POST_R, 0, 360, 32)[:-1], "holes": [((0, 0), PIN_D)], "cut": []}


# Il dente della destra sta in presa dove la sinistra ha un vano: serve per specchiare le bielle.
TH_MESH = (TH_OPEN + TH_CLOSED) / 2
PHASE_R = (-TH_MESH) % 18.0
PHASE_L = (9.0 - TH_MESH) % 18.0
PARTS = {"crankR": crank_part(PHASE_R), "crankL": crank_part(PHASE_L), "idler": idler_part(), "jaw": jaw_part(),
         "low": low_plate(), "up": up_plate(), "post": post_part()}


def volume(name):
    p = PARTS[name]
    a = area(p["outline"]) - sum(area(c) for c in p["cut"]) - sum(math.pi * d * d / 4 for _, d in p["holes"])
    return a * (Z[name.replace("R", "").replace("L", "") if name.startswith("crank") else name][1] - Z[name.replace("R", "").replace("L", "") if name.startswith("crank") else name][0]) / 1000


# ---------- cinematica ----------

def world(theta):
    """Contorni nel piano per ogni strato alla posizione theta."""
    jx, jy = HALF_GEAR + CRANK * math.cos(math.radians(theta)), CRANK * math.sin(math.radians(theta))
    # la biella locale punta lungo +X; la sinistra e' la specchiata
    out = {
        "crankR": tf(PARTS["crankR"]["outline"], HALF_GEAR, 0, theta),
        "crankL": tf(PARTS["crankL"]["outline"], -HALF_GEAR, 0, theta, mirror=True) if False else [(-HALF_GEAR - (px * math.cos(math.radians(theta)) - py * math.sin(math.radians(theta))), px * math.sin(math.radians(theta)) + py * math.cos(math.radians(theta))) for px, py in PARTS["crankL"]["outline"]],
        "idlerR": tf(PARTS["idler"]["outline"], HALF_GEAR, RAIL, theta),
        "idlerL": tf(PARTS["idler"]["outline"], -HALF_GEAR, RAIL, 180 - theta),
        "jawR": tf(PARTS["jaw"]["outline"], jx, jy),
        "jawL": [(-(x + jx), y + jy) for x, y in PARTS["jaw"]["outline"]],
    }
    return out, jx, jy


def seg_cross(a, b, c, d):
    def o(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


def inside(pt, poly):
    x, y, hit = pt[0], pt[1], False
    for i in range(len(poly)):
        x1, y1, x2, y2 = poly[i][0], poly[i][1], poly[(i + 1) % len(poly)][0], poly[(i + 1) % len(poly)][1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


def clash(a, b):
    if inside(a[0], b) or inside(b[0], a):
        return True
    for i in range(len(a)):
        for j in range(len(b)):
            if seg_cross(a[i], a[(i + 1) % len(a)], b[j], b[(j + 1) % len(b)]):
                return True
    return False


def gap_at(theta):
    return 2 * (HALF_GEAR + CRANK * math.cos(math.radians(theta)) + PAD_X)


def theta_for_gap(g):
    return math.degrees(math.acos((g / 2 - HALF_GEAR - PAD_X) / CRANK))


def checks():
    posts = [tf(PARTS["post"]["outline"], x, y) for x, y in POSTS]
    rows = []
    steps = 45
    for i in range(steps + 1):
        th = TH_OPEN + (TH_CLOSED - TH_OPEN) * i / steps
        w, jx, jy = world(th)
        pairs = [("ingranaggio/ingranaggio", w["crankR"], w["crankL"]), ("dito/dito", w["jawR"], w["jawL"]), ("leva/leva", w["idlerR"], w["idlerL"])]
        for nm in ("crankR", "crankL", "jawR", "jawL", "idlerR", "idlerL"):
            for k, p in enumerate(posts):
                pairs.append((f"{nm}/colonnina{k}", w[nm], p))
        for nm, a, b in pairs:
            if clash(a, b):
                rows.append((round(th, 1), nm))
    return rows


# ---------- esportazione: OpenSCAD ----------

def scad_part(name):
    p = PARTS[name]
    fmt = lambda poly: "[" + ",".join(f"[{x:.3f},{y:.3f}]" for x, y in poly) + "]"
    body = f"polygon({fmt(p['outline'])});"
    holes = "".join(f"translate([{x},{y}]) circle(d={d});\n" for (x, y), d in p["holes"]) + "".join(f"polygon({fmt(c)});\n" for c in p["cut"])
    return f"difference() {{ {body}\n{holes}}}\n"


def write_scad(path):
    s = ["// Pinza a ingranaggi e parallelogramma. Generato da genera_pinza.py: modifica li' le misure.", "$fn=48;", "parte = \"dito\"; // dito, biella_motore, biella_folle, leva, piastra_bassa, piastra_alta, colonnina", ""]
    names = {"jaw": "dito", "crankR": "biella_motore", "crankL": "biella_folle", "idler": "leva", "low": "piastra_bassa", "up": "piastra_alta", "post": "colonnina"}
    for n, it in names.items():
        z = Z["crank" if n.startswith("crank") else n]
        s.append(f"module {it}() linear_extrude({z[1] - z[0]})\n{scad_part(n)}")
    # Sede della squadretta del servo sulla biella motore
    s.append(f"module sede() translate([0,0,-1]) linear_extrude({SEAT + 1}) union() {{ circle(d={HUB_D}); translate([0,-{SLOT_W / 2}]) square([18,{SLOT_W}]); }}")
    s.append("module biella_motore_finita() difference() { biella_motore(); sede(); }")
    s.append("if (parte==\"dito\") dito(); if (parte==\"biella_motore\") biella_motore_finita(); if (parte==\"biella_folle\") biella_folle(); if (parte==\"leva\") leva(); if (parte==\"piastra_bassa\") piastra_bassa(); if (parte==\"piastra_alta\") piastra_alta(); if (parte==\"colonnina\") colonnina();")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(s) + "\n")


# ---------- esportazione: DXF con i contorni 1:1 ----------

def write_dxf(path):
    lines = []

    def w(c, v):
        lines.append(f"{c}\n{v}")

    w(0, "SECTION"); w(2, "HEADER"); w(9, "$ACADVER"); w(1, "AC1009"); w(0, "ENDSEC")
    layers = {"CONTORNI": 7, "FORI": 1, "SCRITTE": 5}
    w(0, "SECTION"); w(2, "TABLES"); w(0, "TABLE"); w(2, "LAYER"); w(70, len(layers))
    for n, c in layers.items():
        w(0, "LAYER"); w(2, n); w(70, 0); w(62, c); w(6, "CONTINUOUS")
    w(0, "ENDTAB"); w(0, "ENDSEC"); w(0, "SECTION"); w(2, "ENTITIES")

    def poly(pts, x0, y0, layer):
        w(0, "POLYLINE"); w(8, layer); w(66, 1); w(70, 1)
        for x, y in pts:
            w(0, "VERTEX"); w(8, layer); w(10, round(x + x0, 4)); w(20, round(y + y0, 4)); w(30, 0)
        w(0, "SEQEND"); w(8, layer)

    layout = [("jaw", 40, 30, "DITO x2 (specchiato) - sp. 6"), ("crankR", 95, 50, "BIELLA MOTORE - sp. 5"), ("crankL", 95, 100, "BIELLA FOLLE - sp. 5"),
              ("idler", 190, 50, "LEVA x2 - sp. 5"), ("low", 195, 150, "PIASTRA BASSA - sp. 4"), ("up", 285, 150, "PIASTRA ALTA - sp. 4"), ("post", 290, 50, "COLONNINA x3 - h 18")]
    for name, x0, y0, label in layout:
        p = PARTS[name]
        poly(p["outline"], x0, y0, "CONTORNI")
        for c in p["cut"]:
            poly(c, x0, y0, "FORI")
        for (x, y), d in p["holes"]:
            w(0, "CIRCLE"); w(8, "FORI"); w(10, x + x0); w(20, y + y0); w(30, 0); w(40, d / 2)
        w(0, "TEXT"); w(8, "SCRITTE"); w(10, x0 - 15); w(20, y0 - 14 if name not in ("low", "up") else y0 - 46); w(30, 0); w(40, 3); w(1, label)
    w(0, "ENDSEC"); w(0, "EOF")
    with open(path, "w", encoding="ascii", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")


# ---------- esportazione: PDF multi-foglio ----------
MM = 72 / 25.4


class Sheet:
    def __init__(self):
        self.ops = [f"{MM:.5f} 0 0 {MM:.5f} 0 0 cm", "1 J 1 j"]
        self.frame()

    def stroke(self, w=0.35, rgb="0 0 0"):
        self.ops.append(f"{w:.3f} w {rgb} RG")

    def poly(self, pts, x0=0, y0=0, w=0.35, rgb="0 0 0", close=True):
        self.stroke(w, rgb)
        p = [(x + x0, y + y0) for x, y in pts]
        self.ops.append(f"{p[0][0]:.3f} {p[0][1]:.3f} m " + " ".join(f"{x:.3f} {y:.3f} l" for x, y in p[1:]) + (" h S" if close else " S"))

    def circ(self, x, y, d, w=0.3, rgb="0 0 0"):
        self.poly(arc(x, y, d / 2, 0, 360, 28), w=w, rgb=rgb)

    def text(self, x, y, h, s, rgb="0 0 0"):
        s = s.replace("(", "\\(").replace(")", "\\)")
        out = "".join(c if ord(c) < 127 else "\\%03o" % c.encode("cp1252")[0] for c in s)
        self.ops.append(f"BT /F1 {h / 0.72:.2f} Tf {rgb} rg {x:.2f} {y:.2f} Td ({out}) Tj ET")

    def part(self, name, x0, y0, tf_fn=None, w=0.35, rgb="0 0 0"):
        p = PARTS[name]
        fn = tf_fn or (lambda q: q)
        self.poly(fn(p["outline"]), x0, y0, w, rgb)
        for c in p["cut"]:
            self.poly(fn(c), x0, y0, w * .7, rgb)
        for (x, y), d in p["holes"]:
            q = fn([(x, y)])[0]
            self.circ(q[0] + x0, q[1] + y0, d, w * .7, rgb)

    def dim_h(self, x1, x2, y, label):
        c = "0.05 0.2 0.55"
        self.poly([(x1, y), (x2, y)], w=.2, rgb=c, close=False)
        for x, s in ((x1, 1), (x2, -1)):
            self.poly([(x + s * 2.2, y + .7), (x, y), (x + s * 2.2, y - .7)], w=.2, rgb=c, close=False)
        self.text((x1 + x2) / 2 - .8 * len(label), y + 1, 2.8, label, c)

    def dim_v(self, y1, y2, x, label):
        c = "0.05 0.2 0.55"
        self.poly([(x, y1), (x, y2)], w=.2, rgb=c, close=False)
        for y, s in ((y1, 1), (y2, -1)):
            self.poly([(x - .7, y + s * 2.2), (x, y), (x + .7, y + s * 2.2)], w=.2, rgb=c, close=False)
        self.text(x + 1.4, (y1 + y2) / 2 - 1, 2.8, label, c)

    def frame(self):
        self.poly(rrect(10, 10, 410, 287, .1), w=.5, rgb="0.35 0.35 0.35")

    def title(self, n, name):
        self.poly(rrect(250, 10, 410, 40, .1), w=.5, rgb="0.35 0.35 0.35")
        self.text(254, 30, 5, name)
        self.text(254, 22, 3, f"Foglio {n} di 2 - Scala 1:1 su A3 - Misure in mm - PLA")
        self.text(254, 15, 3, "BOZZA rev. A - Da verificare sui componenti reali")


def write_pdf(path, report):
    a = Sheet()
    a.title(1, "PINZA - ASSIEME")
    ops_for = {"crankR": "0.55 0.55 0.6", "crankL": "0.55 0.55 0.6", "idlerR": "0.1 0.45 0.45", "idlerL": "0.1 0.45 0.45", "jawR": "0.75 0.2 0.1", "jawL": "0.75 0.2 0.1"}
    for (cx, th, lab) in ((75, TH_OPEN, f"APERTA: {gap_at(TH_OPEN):.0f} mm"), (195, theta_for_gap(OBJ), f"IN PRESA SUL BLOCCO: {OBJ:.0f} mm")):
        cy = 95
        a.text(cx - 36, 262, 4, lab)
        a.poly(PARTS["up"]["outline"], cx, cy, .2, "0.65 0.65 0.65")
        w, _, _ = world(th)
        for k, v in w.items():
            a.poly(v, cx, cy, .4, ops_for[k])
        for x, y in POSTS:
            a.circ(cx + x, cy + y, POST_R * 2, .25, "0.4 0.4 0.4")
    a.dim_h(75 - gap_at(TH_OPEN) / 2, 75 + gap_at(TH_OPEN) / 2, 250, f"{gap_at(TH_OPEN):.1f}")
    y = 275
    a.text(250, y, 4, "DISTINTA")
    bom = ["Biella motore x1, biella folle x1: modulo 1, 20 denti, sp. 5",
           "Leva x2: passo 40, sp. 5", "Dito x2 (uno specchiato): sp. 6",
           "Piastra bassa x1, piastra alta x1: sp. 4", "Colonnina x3: h 18",
           "Servo MG90S x1, squadretta a braccio singolo", "Perni M3 e viti: da definire sulla stampa"]
    for s in bom:
        y -= 6.6
        a.text(250, y, 3.2, s)
    y -= 12
    a.text(250, y, 4, "VERIFICHE CALCOLATE")
    for s in report:
        y -= 6.6
        a.text(250, y, 3.2, s)
    b = Sheet()
    b.title(2, "PINZA - PARTI")
    # dito
    b.text(20, 272, 4, "DITO")
    x0, y0 = 45, 165
    b.part("jaw", x0, y0)
    b.dim_v(y0, y0 + RAIL, x0 + 14, f"{RAIL:.0f}")
    b.dim_h(x0 + PAD_X, x0, y0 - 11, f"{-PAD_X:.0f}")
    b.dim_v(y0 + 43, y0 + 73.5, x0 - 30, "30")
    b.text(20, 145, 2.8, f"Fori d{PIN_D} - Spessore {Z['jaw'][1] - Z['jaw'][0]:.0f}")
    # biella
    b.text(95, 272, 4, "BIELLA MOTORE")
    b.part("crankR", 115, 240)
    b.dim_h(115, 115 + CRANK, 225, f"{CRANK:.0f}")
    b.text(95, 215, 2.8, f"m={MODULE:.0f}, z={TEETH}, a={PRESSURE:.0f} gradi, De=22, Dp=20, sp. 5")
    b.text(95, 209, 2.8, f"Sotto: sede d{HUB_D} e scanalatura {SLOT_W:.0f}, prof. {SEAT:.0f}, lungo la biella")
    b.text(95, 196, 4, "BIELLA FOLLE")
    b.part("crankL", 115, 172)
    b.dim_h(115, 115 + CRANK, 157, f"{CRANK:.0f}")
    b.text(95, 147, 2.8, f"Stessi dati; denti sfasati di 9 gradi per l'ingranamento")
    b.text(95, 128, 4, "LEVA")
    b.part("idler", 110, 112)
    b.dim_h(110, 110 + CRANK, 98, f"{CRANK:.0f}")
    b.text(180, 272, 4, "COLONNINA")
    b.part("post", 195, 255)
    b.text(205, 254, 2.8, f"d{POST_R * 2:.0f}, h 18, foro d{PIN_D}")
    b.text(250, 272, 4, "PIASTRA BASSA")
    b.part("low", 285, 225)
    b.dim_h(285 - 26, 285 + 26, 182, "52")
    b.text(350, 272, 4, "PIASTRA ALTA")
    b.part("up", 378, 225)
    b.dim_h(378 - 26, 378 + 26, 192, "52")
    b.text(250, 170, 2.8, f"Foro servo d12 in (10, 0); viti servo d{PILOT_D} a interasse {SERVO_EARS} lungo Y.")
    b.text(250, 164, 2.8, "Origine delle piastre: centro fra gli assi degli ingranaggi.")
    b.text(250, 158, 2.8, f"Assi ingranaggi (+/-10, 0). Assi leve (+/-10, {RAIL:.0f}). Colonnine: (+/-18, -20), (0, 27).")
    pages = [a, b]
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", None]
    kids = []
    font_id = 3
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    for sh in pages:
        s = ("q\n" + "\n".join(sh.ops) + "\nQ").encode("latin-1")
        objs.append(b"<< /Length " + str(len(s)).encode() + b" >>\nstream\n" + s + b"\nendstream")
        content = len(objs)
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {420 * MM:.2f} {297 * MM:.2f}] /Contents {content} 0 R /Resources << /Font << /F1 {font_id} 0 R >> >> >>".encode())
        kids.append(f"{len(objs)} 0 R")
    objs[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>".encode()
    buf = bytearray(b"%PDF-1.4\n")
    off = []
    for i, o in enumerate(objs, 1):
        off.append(len(buf))
        buf += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    x = len(buf)
    buf += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for o in off:
        buf += f"{o:010d} 00000 n \n".encode()
    buf += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n".encode()
    with open(path, "wb") as f:
        f.write(buf)


# ---------- anteprima 3D ----------
HTML = r"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Anteprima Pinza</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400&family=Source+Sans+3:wght@400;600&display=swap">
<style>:root{--p:#ECEAE4;--i:#151B2C;--m:#5C6170}html,body{height:100%;margin:0}body{background:var(--p);color:var(--i);font:16px 'Source Sans 3',sans-serif;overflow:hidden}canvas{position:fixed;inset:0;display:block}
#ui{position:fixed;left:28px;bottom:24px;width:min(360px,calc(100vw - 56px))}h1{font:400 34px/1.1 Newsreader,serif;margin:0 0 4px}p{margin:0 0 10px;color:var(--m)}input{width:100%;accent-color:var(--i)}label{display:flex;justify-content:space-between}</style>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script></head><body>
<div id="ui"><h1>Pinza a ingranaggi</h1><p>Bozza del progetto: due ingranaggi, due leve, le dita restano parallele.</p><label for="g">Apertura <output id="o"></output></label><input id="g" type="range" step="0.5"></div>
<script type="module">
import * as THREE from 'three';import {OrbitControls} from 'three/addons/controls/OrbitControls.js';import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
const D=__DATA__;
const r=new THREE.WebGLRenderer({antialias:true});r.setPixelRatio(Math.min(devicePixelRatio,2));r.setSize(innerWidth,innerHeight);r.shadowMap.enabled=true;r.shadowMap.type=THREE.PCFSoftShadowMap;r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=.72;document.body.prepend(r.domElement);
const s=new THREE.Scene();s.background=new THREE.Color(0xECEAE4);s.environment=new THREE.PMREMGenerator(r).fromScene(new RoomEnvironment(),.04).texture;s.environmentIntensity=.55;
const c=new THREE.PerspectiveCamera(30,innerWidth/innerHeight,1,4000);c.position.set(95,-135,215);c.up.set(0,0,1);const ct=new OrbitControls(c,r.domElement);ct.target.set(0,36,6);ct.update();
const sun=new THREE.DirectionalLight(0xffffff,2);sun.position.set(90,-70,260);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-150,right:150,top:150,bottom:-150,near:1,far:600});sun.shadow.bias=-.0004;s.add(sun);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(2000,2000),new THREE.ShadowMaterial({opacity:.16}));fl.position.z=-36;fl.receiveShadow=true;s.add(fl);
const M={red:new THREE.MeshPhysicalMaterial({color:0xA3200F,roughness:.38,clearcoat:.35,clearcoatRoughness:.5}),gear:new THREE.MeshStandardMaterial({color:0xB9BEC6,metalness:.75,roughness:.32}),teal:new THREE.MeshStandardMaterial({color:0x2F7F86,roughness:.45,metalness:.12}),plate:new THREE.MeshStandardMaterial({color:0x2A2F3A,roughness:.5,metalness:.25}),post:new THREE.MeshStandardMaterial({color:0x8D929B,metalness:.8,roughness:.3}),servo:new THREE.MeshStandardMaterial({color:0x151820,roughness:.55}),block:new THREE.MeshStandardMaterial({color:0xE8E2D2,roughness:.7})};
function geo(p,h,mir){const f=mir?q=>new THREE.Vector2(-q[0],q[1]):q=>new THREE.Vector2(q[0],q[1]);let o=p.outline.map(f);const sh=new THREE.Shape(o);
 const add=a=>{sh.holes.push(new THREE.Path(a.map(f)))};p.cut.forEach(add);p.holes.forEach(([c,d])=>{const a=[];for(let i=0;i<32;i++){const t=i/32*Math.PI*2;a.push([c[0]+d/2*Math.cos(t),c[1]+d/2*Math.sin(t)])}add(a)});
 return new THREE.ExtrudeGeometry(sh,{depth:h-.5,bevelEnabled:true,bevelThickness:.25,bevelSize:.25,bevelOffset:-.25,bevelSegments:2,curveSegments:8})}
function mesh(n,mat,mir){const m=new THREE.Mesh(geo(D.parts[n],D.z[n.startsWith('crank')?'crank':n][1]-D.z[n.startsWith('crank')?'crank':n][0],mir),mat);m.castShadow=m.receiveShadow=true;m.position.z=D.z[n.startsWith('crank')?'crank':n][0]+.25;return m}
const root=new THREE.Group();s.add(root);
root.add(mesh('low',M.plate));const up=mesh('up',M.plate);up.material=M.plate.clone();up.material.transparent=true;up.material.opacity=.14;up.castShadow=false;root.add(up);
D.posts.forEach(([x,y])=>{const m=mesh('post',M.post);m.position.x=x;m.position.y=y;root.add(m)});
const crR=mesh('crankR',M.gear),crL=mesh('crankL',M.gear,true);crR.position.x=D.g;crL.position.x=-D.g;root.add(crR,crL);
const idR=mesh('idler',M.teal),idL=mesh('idler',M.teal,true);idR.position.set(D.g,D.rail,D.z.idler[0]+.25);idL.position.set(-D.g,D.rail,D.z.idler[0]+.25);root.add(idR,idL);
const jR=mesh('jaw',M.red),jL=mesh('jaw',M.red,true);root.add(jR,jL);
const sv=new THREE.Mesh(new THREE.BoxGeometry(12.4,22.8,22.7),M.servo);sv.position.set(D.g,D.servoY,-16);sv.castShadow=true;root.add(sv);const ear=new THREE.Mesh(new THREE.BoxGeometry(12.4,32.5,2.5),M.servo);ear.position.set(D.g,D.servoY,-5.8);ear.castShadow=true;root.add(ear);
const pin=(x,y,z0,z1)=>{const m=new THREE.Mesh(new THREE.CylinderGeometry(1.55,1.55,z1-z0,20),M.post);m.rotation.x=Math.PI/2;m.position.set(x,y,(z0+z1)/2);m.castShadow=true;root.add(m);return m};
[[-D.g,0],[D.g,0]].forEach(([x,y])=>pin(x,y,-.5,17.5));[[-D.g,D.rail],[D.g,D.rail]].forEach(([x,y])=>pin(x,y,12,21.5));
const p1=[pin(0,0,0,11.5),pin(0,0,0,11.5)],p2=[pin(0,0,5.5,17),pin(0,0,5.5,17)];
function set(g){const th=Math.acos((g/2-D.g-D.pad)/D.crank),jx=D.g+D.crank*Math.cos(th),jy=D.crank*Math.sin(th);crR.rotation.z=th;crL.rotation.z=-th;idR.rotation.z=th;idL.rotation.z=-th;jR.position.set(jx,jy,D.z.jaw[0]+.25);jL.position.set(-jx,jy,D.z.jaw[0]+.25);
 p1[0].position.x=jx;p1[0].position.y=jy;p1[1].position.x=-jx;p1[1].position.y=jy;p2[0].position.x=jx;p2[0].position.y=jy+D.rail;p2[1].position.x=-jx;p2[1].position.y=jy+D.rail;}
const sl=document.getElementById('g'),o=document.getElementById('o');sl.min=D.gmin;sl.max=D.gmax;const q=new URLSearchParams(location.search);sl.value=q.get('g')||38;const up_=()=>{set(+sl.value);o.textContent=(+sl.value).toFixed(1)+' mm'};sl.oninput=up_;up_();
addEventListener('resize',()=>{c.aspect=innerWidth/innerHeight;c.updateProjectionMatrix();r.setSize(innerWidth,innerHeight)});
r.setAnimationLoop(()=>{ct.update();r.render(s,c)});window.__ok=true;
</script></body></html>"""


def write_preview(path):
    data = {"parts": PARTS, "z": Z, "g": HALF_GEAR, "rail": RAIL, "crank": CRANK, "pad": PAD_X, "posts": POSTS, "servoY": SERVO_Y,
            "gmin": round(gap_at(TH_CLOSED), 1), "gmax": round(gap_at(TH_OPEN), 1)}
    with open(path, "w", encoding="utf-8") as f:
        f.write(HTML.replace("__DATA__", json.dumps(data, separators=(",", ":"))))


# ---------- verifiche ed esportazione ----------
here = os.path.dirname(os.path.abspath(__file__))
bad = checks()
th_grip = theta_for_gap(OBJ)
# Ogni dito riceve meta' coppia. Forza orizzontale in punta da lavoro virtuale: F = (T/2)/(R sin theta)
force = (SERVO_NM / 2) / (CRANK / 1000 * math.sin(math.radians(th_grip)))
counts = {"jaw": 2, "crankR": 1, "crankL": 1, "idler": 2, "low": 1, "up": 1, "post": 3}
grams = {k: volume(k) * RHO * FILL * n for k, n in counts.items()}
print_g = sum(grams.values())
total_g = print_g + SERVO_G
jaw_g = grams["jaw"] / 2
# trave incastrata sulla sezione minima del dito
span = 73.5 - RAIL
rep = [
    f"Apertura da {gap_at(TH_OPEN):.1f} a {gap_at(TH_CLOSED):.1f} mm, corsa servo {TH_CLOSED - TH_OPEN:.0f} gradi",
    f"Forza di stallo per dito sul blocco da {OBJ:.0f} mm: {force:.1f} N (teorica)",
    f"Avanzamento delle punte in chiusura: {CRANK * (math.sin(math.radians(TH_CLOSED)) - math.sin(math.radians(TH_OPEN))):.1f} mm",
    f"Plastica stampata {print_g:.0f} g, dito singolo {jaw_g:.1f} g (riempimento {int(FILL * 100)}%)",
    f"Totale con servo {total_g:.0f} g, viti escluse",
    f"Collisioni su {46} posizioni della corsa: {len(bad)}",
]
write_scad(os.path.join(here, "pinza.scad"))
write_dxf(os.path.join(here, "pinza-parti.dxf"))
write_pdf(os.path.join(here, "pinza-disegni.pdf"), rep)
write_preview(os.path.join(here, "anteprima.html"))
print("\n".join(rep))
print("grams", {k: round(v, 1) for k, v in grams.items()})
print("clashes", bad[:20])
