import type { ReactNode } from 'react';

export interface PanelProps {
  /** titolo del pannello (Fredoka) */
  title?: string;
  /** light = bianco con bordo, dark = navy */
  tone?: 'light' | 'dark';
  children: ReactNode;
}

/** Pannello arrotondato (16px) che contiene spiegazioni, controlli o dati accanto a una demo. */
export function Panel({ title, tone = 'light', children }: PanelProps) {
  return (
    <div className={`ws-panel ws-panel--${tone}`}>
      {title && <h3 className="ws-panel__title">{title}</h3>}
      {children}
    </div>
  );
}
