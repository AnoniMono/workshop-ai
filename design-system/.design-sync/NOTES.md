# design-sync notes: workshop-ai-ds

- The package lives in `design-system/` of the workshop repo (AnoniMono/workshop-ai); run every sync command from inside `design-system/`.
- Build: `npm run build` (esbuild → `dist/index.js` + `dist/styles.css`, then `tsc` for `.d.ts`). React is external.
- `src/styles.css` `@import`s `../tokens.css` and `../eras.css`; esbuild inlines them into `dist/styles.css`, which is `cfg.cssEntry`.
- No local Playwright browser: the render check and capture use the installed Chrome via
  `DS_CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"`. Install playwright in `.ds-sync/` with `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`.
- Card layout overrides: `ExplainCard` single (700x560, it's an overlay); `PhoneFrame`, `BeforeAfterBar`, `Panel`, `StatCompare` column (wider than grid cells).
- Fixed during first sync: `BeforeAfterBar` used an auto-sized label column, so stacked bars didn't line up; it now uses a fixed 7em label column with ellipsis.

## Known render warns
- `[FONT_REMOTE]` Fredoka / Nunito Sans / Inter (and the era fonts) load from Google Fonts at runtime, same as the deck. Expected.

## Re-sync risks
- Tokens are duplicated: the deck (`ai-workshop.html`) still has its own `:root` block and era classes. A colour change made only in `tokens.css` won't reach the deck until the deck is switched to import it.
- Fonts depend on Google Fonts being reachable; offline renders fall back to system fonts.
- Previews were graded against the Windows Chrome build on the author's machine; another machine's Chrome may render fonts slightly differently.
