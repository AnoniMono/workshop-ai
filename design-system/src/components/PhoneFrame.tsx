import type { ReactNode } from 'react';

export interface PhoneFrameProps {
  /** testo nella barra in alto, es. "Per te" */
  title?: string;
  /** schermo del telefono */
  children: ReactNode;
  /** sfondo dello schermo (colore o gradiente CSS) */
  screen?: string;
}

/** Cornice di telefono scura usata per simulare le app (TikTok, Spotify, Instagram…). */
export function PhoneFrame({ title, children, screen }: PhoneFrameProps) {
  return (
    <div className="ws-phone">
      {title && <div className="ws-phone__top">{title}</div>}
      <div className="ws-phone__screen" style={screen ? { background: screen } : undefined}>
        {children}
      </div>
    </div>
  );
}
