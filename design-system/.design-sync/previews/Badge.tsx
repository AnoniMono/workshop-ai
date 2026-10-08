import { Badge } from 'workshop-ai-ds';

export const TuttiITipi = () => (
  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
    <Badge kind="ai" />
    <Badge kind="math" />
    <Badge kind="data" />
    <Badge kind="idea" />
    <Badge kind="mech" />
    <Badge kind="fun" />
  </div>
);

export const TestoPersonalizzato = () => (
  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
    <Badge kind="ai">🧠 AI · rete neurale</Badge>
    <Badge kind="math">🧮 Matematica · Dijkstra, 1956</Badge>
    <Badge kind="data">📡 Dati · telefoni anonimi</Badge>
  </div>
);
