import type { ReactNode } from 'react';

/** Le sei epoche del "viaggio dell'AI". */
export type Era = 1739 | 1950 | 1966 | 1997 | 2016 | 2022;

export interface EraFrameProps {
  era: Era;
  /** titolo nello stile dell'epoca */
  title: string;
  /** riga piccola sotto il titolo (autore, luogo) */
  meta?: string;
  children?: ReactNode;
}

export const ERA_CLASS: Record<Era, string> = { 1739: 'era-0', 1950: 'era-1', 1966: 'era-2', 1997: 'era-3', 2016: 'era-4', 2022: 'era-5' };
export const ERA_STYLE: Record<Era, string> = {
  1739: 'stampa del Settecento',
  1950: 'dattiloscritto',
  1966: 'terminale a fosfori verdi',
  1997: "Windows anni '90",
  2016: 'app anni 2010',
  2022: 'interfaccia di oggi',
};

/** Riquadro vestito nello stile di un'epoca: sfondo, caratteri, linee e angoli cambiano con l'anno. */
export function EraFrame({ era, title, meta, children }: EraFrameProps) {
  return (
    <section className={`ws-era ${ERA_CLASS[era]}`}>
      <p className="ws-era__year">{era}</p>
      <h3 className="ws-era__title">{title}</h3>
      {meta && <p className="ws-era__meta">{meta}</p>}
      {children && <div className="ws-era__body">{children}</div>}
      <p className="ws-era__style">Stile: {ERA_STYLE[era]}</p>
    </section>
  );
}
