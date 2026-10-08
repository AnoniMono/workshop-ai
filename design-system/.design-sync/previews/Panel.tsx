import { Panel, Badge, Button } from 'workshop-ai-ds';

export const Chiaro = () => (
  <div style={{ width: 420 }}>
    <Panel title="🧠 Cosa pensa l'algoritmo di te">
      <p style={{ margin: 0 }}>Il tuo feed è per il 34% Animali e per il 21% Comedy.</p>
      <div><Badge kind="ai" /></div>
    </Panel>
  </div>
);

export const Scuro = () => (
  <div style={{ width: 420 }}>
    <Panel title="✨ Consigliati per te" tone="dark">
      <p style={{ margin: 0 }}>Birds of a Feather, perché piace a Giulia (75% simile a te).</p>
      <div><Button variant="secondary">Ascolta</Button></div>
    </Panel>
  </div>
);
