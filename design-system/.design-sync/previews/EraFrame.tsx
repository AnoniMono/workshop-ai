import { EraFrame } from 'workshop-ai-ds';

export const Settecento = () => (
  <div style={{ width: 320 }}>
    <EraFrame era={1739} title="L'anatra digeritrice" meta="Jacques de Vaucanson · Parigi">
      Un'anatra di rame dorato che sembrava mangiare e digerire.
    </EraFrame>
  </div>
);

export const Terminale = () => (
  <div style={{ width: 320 }}>
    <EraFrame era={1966} title="ELIZA" meta="Joseph Weizenbaum · MIT">
      ELIZA: SALVE. COME TI SENTI OGGI?
    </EraFrame>
  </div>
);

export const Windows = () => (
  <div style={{ width: 320 }}>
    <EraFrame era={1997} title="Deep Blue" meta="IBM · New York">
      200 milioni di posizioni al secondo.
    </EraFrame>
  </div>
);

export const Oggi = () => (
  <div style={{ width: 320 }}>
    <EraFrame era={2022} title="ChatGPT" meta="OpenAI · San Francisco">
      Prevede la parola successiva, una dopo l'altra.
    </EraFrame>
  </div>
);
