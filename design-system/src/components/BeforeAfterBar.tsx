export interface BeforeAfterBarProps {
  /** cosa misura la barra, es. "😂 Comedy" */
  label: string;
  /** valore prima dell'azione */
  from: number;
  /** valore dopo l'azione */
  to: number;
  /** valore massimo della barra (default 100) */
  max?: number;
  /** unità mostrata dopo i numeri (default "%") */
  unit?: string;
  /** true se un valore più basso è un miglioramento (es. minuti di viaggio) */
  lowerIsBetter?: boolean;
  /** colore del riempimento (default verde) */
  color?: string;
}

/** Barra "prima → dopo": mostra in un colpo d'occhio l'effetto di un'azione (es. 13% → 39%). */
export function BeforeAfterBar({ label, from, to, max = 100, unit = '%', lowerIsBetter = false, color }: BeforeAfterBarProps) {
  const better = lowerIsBetter ? to <= from : to >= from;
  const tone = to === from ? 'same' : better ? 'up' : 'down';
  const pct = Math.max(0, Math.min(100, (to / max) * 100));
  const fmt = (v: number) => String(Math.round(v * 10) / 10).replace('.', ',');
  return (
    <div className="ws-ba">
      <span className="ws-ba__label">{label}</span>
      <div className="ws-ba__track">
        <i style={{ width: pct + '%', background: color }} />
      </div>
      <b className="ws-ba__val">
        {fmt(from)}
        {unit} → <span className={`ws-ba__to is-${tone}`}>{fmt(to)}{unit}</span>
      </b>
    </div>
  );
}
