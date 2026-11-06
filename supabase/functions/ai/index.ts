// Inoltra a Claude le richieste degli studenti del Modulo 3. La chiave resta qui, mai nella pagina.
// Pubblicazione: vedi supabase/LEGGIMI.md
import Anthropic from "npm:@anthropic-ai/sdk";

const client = new Anthropic();
const ALLOWED_ORIGINS = ["https://anonimono.github.io"];
const MAX_CHARS = 2000;
const MAX_TURNS = 6;

const COMMON = "Gli utenti sono studenti delle superiori, dai 16 ai 18 anni, durante un workshop a scuola. " +
  "Se la richiesta non riguarda il compito indicato, rispondi solo: Posso aiutarti solo con questa attivita'. " +
  "Non chiedere e non usare dati personali.";
const SYSTEM: Record<string, string> = {
  // Di proposito niente specifiche del pezzo: le deve scrivere lo studente nel prompt.
  scad: "Scrivi codice OpenSCAD valido partendo dalla descrizione dell'utente. Rispondi solo con il codice, senza spiegazioni. " + COMMON,
  explain: "Spiega in italiano componenti di elettronica, robotica e stampa 3D, in al massimo 80 parole. " + COMMON,
  code: "Scrivi il programma per un braccio simulato. Comandi: vai(\"casa\"), vai(\"sopra_blocco\"), vai(\"blocco\"), " +
    "vai(\"sopra_scatola\"), vai(\"scatola\"), apri(), chiudi(), aspetta(millisecondi). Un comando per riga, solo il codice. " + COMMON,
};

// Limite semplice per classe: vale per singola istanza della funzione, non e' un tetto di spesa.
const hits = new Map<string, { n: number; t: number }>();
function limited(room: string): boolean {
  const now = Date.now(), h = hits.get(room);
  if (!h || now - h.t > 60_000) {
    hits.set(room, { n: 1, t: now });
    return false;
  }
  h.n++;
  return h.n > 60;
}

function headers(origin: string | null) {
  return {
    "Access-Control-Allow-Origin": origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
    "Access-Control-Allow-Headers": "authorization, apikey, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
    "Content-Type": "application/json",
  };
}

Deno.serve(async (req) => {
  const origin = req.headers.get("origin");
  const H = headers(origin);
  if (req.method === "OPTIONS") return new Response(null, { headers: H });
  const reply = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: H });
  if (req.method !== "POST" || !origin || !ALLOWED_ORIGINS.includes(origin)) return reply({ error: "non consentito" }, 403);

  let body: { mode?: string; room?: string; messages?: { role: string; content: string }[] };
  try {
    body = await req.json();
  } catch {
    return reply({ error: "richiesta non valida" }, 400);
  }
  const system = SYSTEM[body.mode ?? ""];
  const msgs = body.messages;
  if (!system || !Array.isArray(msgs) || !msgs.length || msgs.length > MAX_TURNS) return reply({ error: "richiesta non valida" }, 400);
  if (msgs.some((m) => !["user", "assistant"].includes(m.role) || typeof m.content !== "string" || m.content.length > MAX_CHARS * 4)) {
    return reply({ error: "richiesta non valida" }, 400);
  }
  if (msgs[msgs.length - 1].role !== "user" || msgs[msgs.length - 1].content.length > MAX_CHARS) return reply({ error: "testo troppo lungo" }, 400);
  if (limited(String(body.room ?? "?").slice(0, 8))) return reply({ error: "troppe richieste" }, 429);

  try {
    const r = await client.beta.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 4000,
      output_config: { effort: "low" },
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      system,
      messages: msgs as Anthropic.Beta.BetaMessageParam[],
    } as never) as unknown as Anthropic.Beta.BetaMessage;
    if (r.stop_reason === "refusal") return reply({ error: "richiesta rifiutata" }, 422);
    const text = r.content.flatMap((b) => (b.type === "text" ? [b.text] : [])).join("\n");
    return reply({ text, truncated: r.stop_reason === "max_tokens" });
  } catch (e) {
    if (e instanceof Anthropic.RateLimitError) return reply({ error: "troppe richieste" }, 429);
    if (e instanceof Anthropic.APIConnectionError) return reply({ error: "AI non raggiungibile" }, 503);
    if (e instanceof Anthropic.APIError) return reply({ error: "errore dell'AI" }, 502);
    throw e;
  }
});
