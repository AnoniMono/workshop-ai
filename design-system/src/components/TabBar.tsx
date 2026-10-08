export interface TabItem {
  id: string;
  /** testo della scheda; può iniziare con un'emoji, es. "📱 TikTok" */
  label: string;
}

export interface TabBarProps {
  tabs: TabItem[];
  /** id della scheda attiva */
  active: string;
  onChange?: (id: string) => void;
}

/** Schede a pillola per passare tra demo della stessa slide (es. TikTok, Spotify, Instagram). */
export function TabBar({ tabs, active, onChange }: TabBarProps) {
  return (
    <div className="ws-tabs" role="tablist">
      {tabs.map((t) => (
        <button
          key={t.id}
          type="button"
          role="tab"
          aria-selected={t.id === active}
          className={'ws-tab' + (t.id === active ? ' is-on' : '')}
          onClick={() => onChange && onChange(t.id)}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}
