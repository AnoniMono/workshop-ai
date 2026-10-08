# Design system: Workshop AI

These are the visual rules of `ai-workshop.html`. Use them to keep new slides consistent with the rest of the deck.

| File | Contents |
|---|---|
| `tokens.css` | Colours, fonts, sizes, spacing, radii, shadows, motion |
| `eras.css` | The six era styles of slide 3 (1739 → 2022) |
| `colors.html`, `type.html` | Previews of colours and typography |
| `buttons.html`, `popup.html`, `badges.html` | Previews of the main components |
| `eras.html` | Preview of the six eras |

Open any `.html` file in a browser to see that part of the system. Each preview starts with `<!-- @dsCard group="…" -->`, so Claude Design shows it as a card in its Design System pane.

## Rules

- **One orange action per screen.** Orange (`--orange`) marks the main action (e.g. "Invia il segnale"). Secondary actions are cyan; navigation uses pill tabs.
- **Fredoka for titles and numbers, Nunito Sans for text.** All sizes scale with screen width (`clamp`), so the deck works on both a projector and a laptop.
- **Explanations go in pop-ups.** Each pop-up covers the same three things: what was recorded (📡 Dati), how the AI uses it (🧠 AI), and the result as a before → after bar.
- **Every explanation says whether it is AI or math.** The badges in `badges.html` use the same colour everywhere in the workshop.
- **On slide 3, the page dresses in the style of its year.** The tokens in `eras.css` change background, fonts, lines and corners for each room.

## Syncing with Claude Design

In Claude Code, from this folder, run `/design-sync` and pick (or create) a Claude Design project. The tokens and preview cards in this folder become the project's design system. Changes made in Claude Design can be pulled back the same way.
