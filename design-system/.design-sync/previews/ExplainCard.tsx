import { ExplainCard } from 'workshop-ai-ds';

export const Like = () => (
  <ExplainCard
    icon="❤️"
    title="Hai messo like!"
    rows={[
      { icon: '📡', label: 'Cosa ha registrato', kind: 'data', text: 'Un like a un video di 😂 Comedy, dopo 2,1 s di visione.' },
      { icon: '👁️', label: 'Cosa aveva "visto" nel video', kind: 'ai', text: 'Riconosce: chat 92% · notifiche 97% · risate 95% → è 😂 Comedy.' },
      { icon: '🧠', label: "Come lo usa l'AI", kind: 'ai', text: 'Il like è un segnale positivo, ma non il più forte: per TikTok conta di più quanto a lungo guardi.' },
    ]}
    barsTitle="📊 Quanto spazio avrà nel tuo feed"
    bars={[{ label: '😂 Comedy', from: 13, to: 39 }]}
  />
);

export const AIoMatematica = () => (
  <ExplainCard
    icon="☔"
    title="Sta piovendo!"
    rows={[
      { icon: '📡', label: 'Come lo sa', kind: 'data', text: 'Dai servizi meteo, e dai telefoni in strada che all\'improvviso vanno più piano.' },
      { icon: '🔮', label: "Cosa prevede l'AI", kind: 'ai', text: 'Ha imparato da anni di viaggi che con la pioggia tutti rallentano, e alcune strade più di altre.' },
      { icon: '🧮', label: 'Cosa calcola la matematica', kind: 'math', text: 'Dijkstra ricalcola tutti i percorsi: il migliore cambia da Strada di campagna a Tangenziale.' },
    ]}
  />
);
