import type { ReactNode } from 'react';

/** Il tipo di spiegazione. Ogni tipo ha sempre lo stesso colore in tutto il workshop. */
export type BadgeKind = 'ai' | 'math' | 'data' | 'idea' | 'mech' | 'fun';

export interface BadgeProps {
  kind: BadgeKind;
  /** testo personalizzato; se omesso usa l'etichetta standard del tipo */
  children?: ReactNode;
}

export const BADGE_LABELS: Record<BadgeKind, string> = {
  ai: '🧠 AI',
  math: '🧮 Matematica',
  data: '📡 Dati',
  idea: '💡 Idea',
  mech: '⚙️ Meccanismo',
  fun: '🎩 Curiosità',
};

/** Etichetta a pillola "AI o matematica?": dice se qualcosa è imparato dai dati, calcolato, registrato… */
export function Badge({ kind, children }: BadgeProps) {
  return <span className={`ws-badge ws-badge--${kind}`}>{children ?? BADGE_LABELS[kind]}</span>;
}
