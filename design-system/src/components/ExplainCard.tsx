import type { ReactNode } from 'react';
import { Badge, type BadgeKind } from './Badge';
import { BeforeAfterBar, type BeforeAfterBarProps } from './BeforeAfterBar';
import { Button } from './Button';

export interface ExplainRow {
  /** emoji a sinistra della riga */
  icon?: string;
  /** titolo della riga, es. "Cosa ha registrato" */
  label: string;
  /** tipo di spiegazione: colora il bordo e il badge */
  kind: BadgeKind;
  /** testo della riga; può contenere <b> */
  text: ReactNode;
}

export interface ExplainCardProps {
  /** emoji grande in alto, es. "❤️" */
  icon: string;
  /** titolo breve, es. "Hai messo like!" */
  title: string;
  subtitle?: string;
  /** di solito tre righe: Dati → AI → Matematica */
  rows: ExplainRow[];
  /** barre prima → dopo mostrate sotto le righe */
  bars?: BeforeAfterBarProps[];
  /** titolo sopra le barre, es. "Quanto spazio avrà nel tuo feed" */
  barsTitle?: string;
  /** testo del pulsante finale (default "Ok, continua ▶") */
  actionLabel?: string;
  onAction?: () => void;
}

/**
 * Il pop-up di spiegazione: compare dopo un'azione dello studente e racconta
 * cosa è stato registrato, come lo usa l'AI e cosa è cambiato.
 */
export function ExplainCard({ icon, title, subtitle, rows, bars, barsTitle, actionLabel = 'Ok, continua ▶', onAction }: ExplainCardProps) {
  return (
    <div className="ws-explain" role="dialog" aria-label={title}>
      <div className="ws-explain__head">
        <span className="ws-explain__icon" aria-hidden="true">{icon}</span>
        <div>
          <h3 className="ws-explain__title">{title}</h3>
          {subtitle && <p className="ws-explain__sub">{subtitle}</p>}
        </div>
      </div>
      {rows.map((r, i) => (
        <div key={i} className={`ws-explain__row is-${r.kind}`}>
          {r.icon && <span className="ws-explain__ri" aria-hidden="true">{r.icon}</span>}
          <div>
            <p className="ws-explain__rl">
              {r.label} <Badge kind={r.kind} />
            </p>
            <p className="ws-explain__rt">{r.text}</p>
          </div>
        </div>
      ))}
      {bars && bars.length > 0 && (
        <div className="ws-explain__bars">
          {barsTitle && <p className="ws-explain__rl">{barsTitle}</p>}
          {bars.map((b, i) => (
            <BeforeAfterBar key={i} {...b} />
          ))}
        </div>
      )}
      <div className="ws-explain__actions">
        <Button variant="secondary" onClick={onAction}>{actionLabel}</Button>
      </div>
    </div>
  );
}
