# Workshop AI: how to build with this kit

An interactive workshop on AI for Italian high-school students (projector + students' phones). All UI copy is **Italian**, friendly and concrete ("Hai messo like!", "Ok, continua ▶").

## Setup
No provider or wrapper is needed: components read CSS custom properties from `styles.css` (which `@import`s `_ds_bundle.css`; tokens, era themes and component classes all live there). Fonts load from Google Fonts at runtime. Components are on `window.WorkshopDS`:

```jsx
const { Button, TabBar, Badge, ExplainCard, BeforeAfterBar, StatCompare, EraFrame, PhoneFrame, Panel } = window.WorkshopDS;
```

## Styling idiom: tokens, never hard-coded values
Use `var(--*)` tokens for your own layout glue:
- **Colour**: `--navy` (text, dark surfaces), `--orange` (the ONE main action per screen), `--cyan` / `--cyan2` (secondary), `--light` (page background), `--card` (white surfaces), `--border`, `--gray` (secondary text), `--green` / `--red` (feedback).
- **Type**: `--ff-head` (Fredoka: titles and big numbers) and `--ff-body` (Nunito Sans: text); sizes `--fs-h2`, `--fs-h3`, `--fs-body`, `--fs-small`, `--fs-num`.
- **Space / shape / depth**: `--sp-1`…`--sp-7` (4px grid), `--r-md` 10px, `--r-lg` 16px, `--r-xl` 20px, `--r-pill`, shadows `--sh-1`…`--sh-3`, `--sh-pop`.
- Component classes use the `ws-` prefix (`ws-btn`, `ws-panel`…); don't reuse them for new elements, use the components.

## Patterns that make it feel like the workshop
- **Explain after every action.** When a student does something, show an `ExplainCard` with three rows: what was recorded (`kind:"data"`), how the AI uses it (`kind:"ai"`), and what maths decides (`kind:"math"`), plus a `BeforeAfterBar` showing the effect.
- **Always say whether it's AI or maths** with `Badge` (`ai`, `math`, `data`, `idea`, `mech`, `fun`). The colours are fixed meanings.
- **Simulated apps go inside `PhoneFrame`**; demo switches go in `TabBar` (labels may start with an emoji).
- **History screens**: `EraFrame era={1739|1950|1966|1997|2016|2022}` dresses content in that decade's style (print, typescript, green terminal, Windows 95, Material, today). The same look is available on any container via class `era-0` … `era-5`.
- Big comparisons (brain vs machine) use `StatCompare`; side information goes in `Panel` (`tone="light"` or `"dark"`).

## Example
```jsx
<Panel title="🧠 Cosa pensa l'algoritmo di te">
  <TabBar active="tt" tabs={[{ id: 'tt', label: '📱 TikTok' }, { id: 'sp', label: '🎵 Spotify' }]} />
  <div style={{ display: 'flex', gap: 'var(--sp-3)', alignItems: 'center' }}>
    <Button>Invia il segnale</Button>
    <Badge kind="ai" />
  </div>
  <BeforeAfterBar label="😂 Comedy" from={13} to={39} />
</Panel>
```
