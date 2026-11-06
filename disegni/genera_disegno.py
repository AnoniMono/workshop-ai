#!/usr/bin/env python3
"""Genera il disegno G-02 (dito della pinza, gara del Modulo 3) in DXF e PDF, in scala 1:1 su foglio A3.

Solo libreria standard. La forma di riferimento arriva da pinza/genera_pinza.py.
"""
import math
import os

# Requisiti della gara, in mm: gli stessi controllati nel deck
T = 6
HOLE_D = 3.2
HOLES = [(0, 0), (0, 22)]
FACE_X, FACE_Y = -17, (44, 73)
ENV_X, ENV_Y = (-17.3, 9), (-8, 82)
MASS_MAX, RHO, FILL = 4.6, 1.24, 0.6
FLEX_MAX, FORCE, FORCE_Y = 1, 3.2, 58

_here = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(_here, "pinza", "genera_pinza.py"), encoding="utf-8").read().split("# ---------- verifiche ed esportazione")[0]
_g = {}
exec(compile(_src, "genera_pinza", "exec"), _g)
JAW = _g["PARTS"]["jaw"]

SHEET_W, SHEET_H = 420, 297
ents = []


def line(x1, y1, x2, y2, layer="GEOM"):
    ents.append(("line", layer, x1, y1, x2, y2))


def circle(cx, cy, r, layer="GEOM"):
    ents.append(("circle", layer, cx, cy, r))


def arc(cx, cy, r, a0, a1, layer="GEOM"):
    ents.append(("arc", layer, cx, cy, r, a0, a1))


def text(x, y, h, s, center=False, layer="TESTO"):
    ents.append(("text", layer, x, y, h, s, center))


def rect(x0, y0, x1, y1, layer="GEOM"):
    line(x0, y0, x1, y0, layer)
    line(x1, y0, x1, y1, layer)
    line(x1, y1, x0, y1, layer)
    line(x0, y1, x0, y0, layer)


def arrow(x, y, ang):
    for d in (160, 200):
        a = math.radians(ang + d)
        line(x, y, x + 2.6 * math.cos(a), y + 2.6 * math.sin(a), "QUOTE")


def hdim(x1, x2, y_from, y_dim, label):
    """Quota orizzontale fra x1 e x2, sulla linea y_dim."""
    s = 1 if y_dim > y_from else -1
    line(x1, y_from + s, x1, y_dim + s, "QUOTE")
    line(x2, y_from + s, x2, y_dim + s, "QUOTE")
    line(x1, y_dim, x2, y_dim, "QUOTE")
    tight = abs(x2 - x1) < 7  # quota stretta: frecce all'esterno
    arrow(x1, y_dim, 0 if tight else 180)
    arrow(x2, y_dim, 180 if tight else 0)
    if label:
        text((x1 + x2) / 2, y_dim + 1.2, 3, label, center=True, layer="QUOTE")


def vdim(y1, y2, x_from, x_dim, label):
    """Quota verticale fra y1 e y2, sulla linea x_dim. Testo a fianco della linea."""
    s = 1 if x_dim > x_from else -1
    line(x_from + s, y1, x_dim + s, y1, "QUOTE")
    line(x_from + s, y2, x_dim + s, y2, "QUOTE")
    line(x_dim, y1, x_dim, y2, "QUOTE")
    tight = abs(y2 - y1) < 7
    arrow(x_dim, y1, 90 if tight else 270)
    arrow(x_dim, y2, 270 if tight else 90)
    tx = x_dim + 1.5 if s > 0 else x_dim - 1.5 - 1.7 * len(label)
    text(tx, (y1 + y2) / 2 - 1.5, 3, label, layer="QUOTE")


def leader(x1, y1, x2, y2, label):
    line(x1, y1, x2, y2, "QUOTE")
    line(x2, y2, x2 + 1.8 * len(label) + 2, y2, "QUOTE")
    text(x2 + 1, y2 + 1, 3, label, layer="QUOTE")


def poly(pts, ox, oy, layer):
    for a, b in zip(pts, pts[1:] + pts[:1]):
        line(ox + a[0], oy + a[1], ox + b[0], oy + b[1], layer)


# ---------- foglio ----------
rect(10, 10, SHEET_W - 10, SHEET_H - 10, "FOGLIO")
tb_x = 250
rect(tb_x, 10, SHEET_W - 10, 52, "FOGLIO")
line(tb_x, 40, SHEET_W - 10, 40, "FOGLIO")
line(tb_x, 28, SHEET_W - 10, 28, "FOGLIO")
text(tb_x + 4, 44, 5, "G-02  DITO DELLA PINZA - GARA")
text(tb_x + 4, 32, 3, "Scala 1:1 su A3   -   Misure in mm   -   Materiale PLA")
text(tb_x + 4, 21, 3, "Il profilo tratteggiato e' un riferimento: la forma e' libera")
text(tb_x + 4, 14, 3, "Workshop Stampa 3D e Robotica - SAIHUB School")


# ---------- vista in pianta (X-Y): l'origine e' il foro inferiore ----------
ox, oy = 95, 90
text(ox - 60, oy + ENV_Y[1] + 28, 4, "VISTA IN PIANTA (X-Y)")
poly(JAW["outline"], ox, oy, "NASCOSTE")
for c in JAW["cut"]:
    poly(c, ox, oy, "NASCOSTE")
rect(ox + ENV_X[0], oy + ENV_Y[0], ox + ENV_X[1], oy + ENV_Y[1], "ASSI")
for hx, hy in HOLES:
    circle(ox + hx, oy + hy, HOLE_D / 2)
    line(ox + hx - 4, oy + hy, ox + hx + 4, oy + hy, "ASSI")
    line(ox + hx, oy + hy - 4, ox + hx, oy + hy + 4, "ASSI")
line(ox + FACE_X, oy + FACE_Y[0], ox + FACE_X, oy + FACE_Y[1], "GEOM")
vdim(oy, oy + HOLES[1][1], ox, ox + 24, str(HOLES[1][1]))
vdim(oy, oy + FACE_Y[0], ox + FACE_X, ox - 32, str(FACE_Y[0]))
vdim(oy, oy + FACE_Y[1], ox + FACE_X, ox - 44, str(FACE_Y[1]))
vdim(oy, oy + ENV_Y[1], ox, ox + 36, str(ENV_Y[1]))
vdim(oy + ENV_Y[0], oy, ox, ox + 14, str(-ENV_Y[0]))
hdim(ox + FACE_X, ox, oy + ENV_Y[0], oy + ENV_Y[0] - 10, str(-FACE_X))
hdim(ox + ENV_X[0], ox, oy + ENV_Y[0], oy + ENV_Y[0] - 20, str(-ENV_X[0]))
hdim(ox, ox + ENV_X[1], oy + ENV_Y[0], oy + ENV_Y[0] - 10, str(ENV_X[1]))
leader(ox + HOLE_D / 2, oy + HOLES[1][1] + HOLE_D / 2, ox + 13, oy + HOLES[1][1] + 10, f"2 x %%c{HOLE_D} passanti")
text(ox - 10, oy - 1, 2.6, "(0,0)", layer="QUOTE")
leader(ox + FACE_X, oy + 58, ox - 28, oy + 86, "faccia di presa piana")
leader(ox + ENV_X[1], oy + ENV_Y[1], ox + 15, oy + ENV_Y[1] + 7, "ingombro massimo")


# ---------- vista di fianco: lo spessore ----------
sx, sy = 190, 90
text(sx - 8, oy + ENV_Y[1] + 28, 4, "SPESSORE (Z)")
rect(sx, sy + ENV_Y[0], sx + T, sy + ENV_Y[1], "NASCOSTE")
hdim(sx, sx + T, sy + ENV_Y[1], sy + ENV_Y[1] + 5, "")
leader(sx + T, sy + ENV_Y[1] + 5, sx + 10, sy + ENV_Y[1] + 5, f"{T}  (da z=0 a z={T})")


# ---------- requisiti ----------
volume_max = MASS_MAX / (RHO * FILL)
REQ = [
    "REQUISITI: UGUALI PER TUTTI",
    f"1  Piastra spessa {T} mm, da z=0 a z={T}.",
    f"2  Due fori da {HOLE_D} mm, in (0, 0) e (0, 22).",
    f"3  Faccia di presa piana a x={FACE_X}, da y={FACE_Y[0]} a y={FACE_Y[1]}.",
    f"4  Tutto dentro x da {ENV_X[0]} a {ENV_X[1]} e y da {ENV_Y[0]} a {ENV_Y[1]}.",
    f"5  Massa massima {MASS_MAX} g: volume massimo {volume_max:.2f} cm3",
    f"    (PLA {RHO} g/cm3, riempimento {int(FILL * 100)}%).",
    f"6  Flessione massima {FLEX_MAX} mm con {FORCE} N a y={FORCE_Y}.",
    "",
    "PER IL FILE DI FUSION 360",
    "Esporta lo STL in millimetri, con il pezzo disteso nel piano XY,",
    "il foro inferiore sull'origine e lo spessore da z=0.",
    "Il deck lo giudica con gli stessi controlli degli studenti.",
    "",
    "PERNO: 3 mm. I fori stampati vengono in genere piu' piccoli:",
    "prova il gioco sulla tua A1 mini prima del workshop.",
]
ry = 270
for s_ in REQ:
    head_ = s_.isupper() or s_.startswith("REQUISITI") or s_.startswith("PER IL")
    text(250, ry, 4 if head_ else 3.4, s_)
    ry -= 8.6 if head_ else 7.6

lx, ly = 250, 66
line(lx, ly, lx + 16, ly, "GEOM")
text(lx + 19, ly - 1.3, 3, "Obbligatorio")
line(lx + 56, ly, lx + 72, ly, "NASCOSTE")
text(lx + 75, ly - 1.3, 3, "Riferimento")
line(lx + 108, ly, lx + 124, ly, "ASSI")
text(lx + 127, ly - 1.3, 3, "Assi, ingombro")


# ---------- DXF R12 ----------
LAYERS = {"GEOM": (7, "CONTINUOUS"), "NASCOSTE": (8, "DASHED"), "ASSI": (1, "CENTER"),
          "QUOTE": (5, "CONTINUOUS"), "TESTO": (7, "CONTINUOUS"), "FOGLIO": (8, "CONTINUOUS")}


def write_dxf(path):
    out = []

    def w(code, value):
        out.append(f"{code}\n{value}")

    w(0, "SECTION"); w(2, "HEADER"); w(9, "$ACADVER"); w(1, "AC1009"); w(9, "$INSUNITS"); w(70, 4); w(0, "ENDSEC")
    w(0, "SECTION"); w(2, "TABLES")
    w(0, "TABLE"); w(2, "LTYPE"); w(70, 3)
    for name, desc, pat in (("CONTINUOUS", "Solid", []), ("DASHED", "Dashed", [3, -1.5]), ("CENTER", "Center", [8, -1.5, 1.5, -1.5])):
        w(0, "LTYPE"); w(2, name); w(70, 0); w(3, desc); w(72, 65); w(73, len(pat)); w(40, sum(abs(p) for p in pat))
        for p in pat:
            w(49, p)
    w(0, "ENDTAB")
    w(0, "TABLE"); w(2, "LAYER"); w(70, len(LAYERS))
    for name, (color, lt) in LAYERS.items():
        w(0, "LAYER"); w(2, name); w(70, 0); w(62, color); w(6, lt)
    w(0, "ENDTAB"); w(0, "ENDSEC")
    w(0, "SECTION"); w(2, "ENTITIES")
    for e in ents:
        kind, layer = e[0], e[1]
        w(0, kind.upper()); w(8, layer)
        if kind == "line":
            w(10, e[2]); w(20, e[3]); w(30, 0); w(11, e[4]); w(21, e[5]); w(31, 0)
        elif kind == "circle":
            w(10, e[2]); w(20, e[3]); w(30, 0); w(40, e[4])
        elif kind == "arc":
            w(10, e[2]); w(20, e[3]); w(30, 0); w(40, e[4]); w(50, e[5] % 360); w(51, e[6] % 360)
        elif kind == "text":
            w(10, e[2]); w(20, e[3]); w(30, 0); w(40, e[4]); w(1, e[5])
            if e[6]:
                w(72, 1); w(11, e[2]); w(21, e[3]); w(31, 0)
    w(0, "ENDSEC"); w(0, "EOF")
    with open(path, "w", encoding="ascii", newline="\r\n") as f:
        f.write("\n".join(out) + "\n")


# ---------- PDF ----------
MM = 72 / 25.4
STYLE = {"GEOM": (0.5, "0 0 0", ""), "NASCOSTE": (0.3, "0.25 0.25 0.25", "[3 2] 0 d"), "ASSI": (0.25, "0.7 0.15 0.1", "[8 2 2 2] 0 d"),
         "QUOTE": (0.25, "0.05 0.2 0.55", ""), "TESTO": (0.3, "0 0 0", ""), "FOGLIO": (0.6, "0.3 0.3 0.3", "")}


def pdf_str(s):
    s = s.replace("%%c", "Ø")
    b = s.encode("cp1252")
    return "".join("\\" + c if c in "()\\" else c if 32 <= ord(c) < 127 else "\\%03o" % ord(c) for c in b.decode("latin-1"))


def write_pdf(path):
    ops = ["q", f"{MM:.5f} 0 0 {MM:.5f} 0 0 cm", "1 J 1 j"]
    for e in ents:
        kind, layer = e[0], e[1]
        lw, rgb, dash = STYLE[layer]
        if kind == "text":
            size = e[4] / 0.72
            x = e[2]
            if e[6]:
                x -= 0.25 * size * len(e[5].replace("%%c", "O"))
            color = rgb
            ops.append(f"BT /F1 {size:.2f} Tf {color} rg {x:.3f} {e[3]:.3f} Td ({pdf_str(e[5])}) Tj ET")
            continue
        ops.append(f"{lw / MM:.3f} w {rgb} RG {(dash.replace('[3 2]', '[1.2 0.8]').replace('[8 2 2 2]', '[3 0.8 0.8 0.8]')) if dash else '[] 0 d'}")
        if kind == "line":
            ops.append(f"{e[2]:.3f} {e[3]:.3f} m {e[4]:.3f} {e[5]:.3f} l S")
        else:
            cx, cy, r_ = e[2], e[3], e[4]
            a0, a1 = (0, 360) if kind == "circle" else (e[5], e[6])
            n = max(8, int(abs(a1 - a0) / 4))
            pts = [(cx + r_ * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r_ * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
            ops.append(f"{pts[0][0]:.3f} {pts[0][1]:.3f} m " + " ".join(f"{x:.3f} {y:.3f} l" for x, y in pts[1:]) + " S")
    ops.append("Q")
    stream = "\n".join(ops).encode("latin-1")
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {SHEET_W * MM:.2f} {SHEET_H * MM:.2f}] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>".encode(),
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    buf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, o in enumerate(objs, 1):
        offsets.append(len(buf))
        buf += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(buf)
    buf += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        buf += f"{off:010d} 00000 n \n".encode()
    buf += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    with open(path, "wb") as f:
        f.write(buf)


here = os.path.dirname(os.path.abspath(__file__))
write_dxf(os.path.join(here, "G-02-dito-gara.dxf"))
write_pdf(os.path.join(here, "G-02-dito-gara.pdf"))
print(f"entita {len(ents)} | volume max {volume_max:.2f} cm3")
