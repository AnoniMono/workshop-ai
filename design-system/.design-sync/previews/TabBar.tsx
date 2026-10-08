import { TabBar } from 'workshop-ai-ds';

export const AppSocial = () => (
  <TabBar
    active="tt"
    tabs={[
      { id: 'tt', label: '📱 TikTok' },
      { id: 'sp', label: '🎵 Spotify' },
      { id: 'ig', label: '📸 Instagram' },
      { id: 'nf', label: '🎬 Netflix' },
      { id: 'mp', label: '🗺️ Maps' },
    ]}
  />
);

export const DueSchede = () => (
  <TabBar
    active="quiz"
    tabs={[
      { id: 'enigma', label: '1 · Enigma' },
      { id: 'quiz', label: "2 · Il gioco dell'imitazione" },
    ]}
  />
);
