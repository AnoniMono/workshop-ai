import { PhoneFrame } from 'workshop-ai-ds';

export const FeedTikTok = () => (
  <PhoneFrame title="Per te" screen="linear-gradient(160deg,#B7791F,#F6C453)">
    <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 84 }}>🐶</div>
    <div style={{ position: 'absolute', left: 14, right: 14, bottom: 16, fontSize: 14, lineHeight: 1.35 }}>
      <b>@bobby.golden</b>
      <p style={{ margin: '4px 0 0' }}>Golden retriever vede la neve</p>
    </div>
  </PhoneFrame>
);

export const Player = () => (
  <PhoneFrame title="Radio per te" screen="linear-gradient(180deg,#922B21 0%,#121212 75%)">
    <div style={{ position: 'absolute', inset: '40px 16px 16px', display: 'flex', flexDirection: 'column', gap: 12 }}>
      <div style={{ aspectRatio: '1', borderRadius: 10, background: 'linear-gradient(135deg,#7F1D1D,#E74C3C)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 72 }}>🎸</div>
      <b style={{ fontSize: 16 }}>Beggin'</b>
      <span style={{ fontSize: 13, color: '#b3b3b3' }}>Måneskin</span>
    </div>
  </PhoneFrame>
);
