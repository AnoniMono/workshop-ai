import { Button } from 'workshop-ai-ds';

export const Varianti = () => (
  <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
    <Button>Invia il segnale</Button>
    <Button variant="secondary">↺ Reset</Button>
    <Button variant="ghost">Annulla</Button>
  </div>
);

export const AzionePrincipale = () => <Button size="lg">🔬 Entriamo nell'algoritmo →</Button>;

export const Disattivato = () => (
  <div style={{ display: 'flex', gap: 12 }}>
    <Button disabled>Calcolo in corso…</Button>
    <Button variant="secondary" disabled>Allena +100</Button>
  </div>
);
