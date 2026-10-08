import { BeforeAfterBar } from 'workshop-ai-ds';

export const Aumento = () => (
  <div style={{ width: 460 }}>
    <BeforeAfterBar label="😂 Comedy" from={13} to={39} />
  </div>
);

export const Calo = () => (
  <div style={{ width: 460 }}>
    <BeforeAfterBar label="🍝 Cucina" from={22} to={9} color="#E74C3C" />
  </div>
);

export const MinutiDiViaggio = () => (
  <div style={{ width: 460, display: 'flex', flexDirection: 'column', gap: 8 }}>
    <BeforeAfterBar label="Centro" from={29} to={32} max={50} unit=" min" lowerIsBetter color="#E74C3C" />
    <BeforeAfterBar label="Tangenziale" from={19} to={22} max={50} unit=" min" lowerIsBetter color="#FFB800" />
    <BeforeAfterBar label="Campagna" from={25} to={17} max={50} unit=" min" lowerIsBetter />
  </div>
);
