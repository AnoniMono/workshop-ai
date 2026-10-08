import type { ButtonHTMLAttributes, ReactNode } from 'react';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** primary = arancione (una sola azione principale per schermata), secondary = ciano, ghost = contorno */
  variant?: 'primary' | 'secondary' | 'ghost';
  /** md per i pannelli, lg per l'azione principale di una slide */
  size?: 'md' | 'lg';
  children: ReactNode;
}

/** Pulsante del workshop. Font Fredoka, angoli 10px, leggero sollevamento al passaggio del mouse. */
export function Button({ variant = 'primary', size = 'md', className, children, ...rest }: ButtonProps) {
  const cls = ['ws-btn', `ws-btn--${variant}`, size === 'lg' ? 'ws-btn--lg' : '', className || ''].filter(Boolean).join(' ');
  return (
    <button type="button" className={cls} {...rest}>
      {children}
    </button>
  );
}
