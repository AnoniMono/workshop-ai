import { StatCompare } from 'workshop-ai-ds';

export const Connessioni = () => (
  <div style={{ width: 460 }}>
    <StatCompare
      topic="Connessioni"
      brain={{ value: '100.000 miliardi', caption: 'sinapsi nel cervello, tra 86 miliardi di neuroni' }}
      machine={{ value: '175 miliardi', caption: 'parametri di GPT-3' }}
      takeaway="Il cervello ne ha circa 570 volte di più"
    />
  </div>
);

export const Energia = () => (
  <div style={{ width: 460 }}>
    <StatCompare
      topic="Energia"
      brain={{ value: '20 watt', caption: 'il cervello, giorno e notte: come una lampadina' }}
      machine={{ value: '1.287 MWh', caption: 'per addestrare GPT-3 (stima)' }}
      takeaway="Con quell'energia un cervello funzionerebbe per oltre 7.000 anni"
    />
  </div>
);
