# tpeyash.com — Peyash's Log

AstroPaper-based blog. Posts in `src/data/blog/` (`.md`/`.mdx`), deployed to GitHub Pages on push to `main`. Full workflow (frontmatter schema, build, deploy) lives in the `personal-blog` skill — use it for post/site tasks.

## Writing posts

Whenever writing, restructuring, or substantially editing a post, invoke the `blog-writing` skill first — it defines the site's voice (bench-log register, falsifiable claims, honest epistemics), the two post shapes, and the MDX component vocabulary (kickers, PostToc, trio/mini cards, step lists, figures). It composes with `no-ai-slop` (always run its pass on drafts) and `personal-blog` (mechanics).

## Diagram design language (mech-interp figures)

Inline SVG diagrams for the mechanistic-interpretability posts live in `src/assets/diagrams/*.svg`, imported as Astro components and placed inside `<figure class="fig not-prose">`. They follow the `diagram-design` skill's editorial system, adapted for in-blog theming. When creating or editing one, keep to these rules:

### Theming — CSS variables only, never hex

- Diagrams must render in both light and dark. Color exclusively through the Atlas custom properties defined in `src/styles/atlas.css` (sandboxed onto `.fig` and friends, inherited by nested SVG): `--paper`, `--card`, `--ink`, `--ink2`, `--muted`, `--hair`, `--line`, plus the blog-level `--accent` (blue `#006cac` light / ember `#ff7a1f` dark).
- **Gotcha:** `var()` does not resolve in SVG *presentation attributes* for font-family (use `style="font-family: var(--font-google-sans-code), ui-monospace, monospace"`), but works fine in `fill`/`stroke` attributes.
- The figure background is `var(--card)` (the `.fig` container), so label masks and cutouts use `--card`, not `--paper`.

### One accent, quiet structure

- `var(--accent)` marks the **focal concept only** — 1–2 elements per diagram (e.g. the virtual-weight arc; the attention arc → query → prediction chain). Never use the Atlas hue set (`--keep`, `--warn`, `--speech`, `--violet`) to color-code diagram roles.
- Everything structural is `--ink` / `--ink2` / `--line` / `--card`.

### Vocabulary

- **Node boxes:** `rx="6"`, fill `var(--paper)`, stroke `var(--line)` at 1. Emphasis variant: fill `var(--card)`, stroke `var(--ink)` at 1.2. Accent outline (1.4) reserved for the focal node.
- **Note/label chips:** `rx="4"`, fill `var(--card)`, stroke `var(--line)`, mono 9px `var(--ink2)` text. No pills.
- **Arrows:** every file defines its own `<defs>` markers — one muted (`var(--ink2)`), one accent. Draw arrows before boxes. Dashed = virtual/indirect.
- **Arrow labels:** opaque `var(--card)` mask rect (`rx="2"`, or a bordered chip when sitting on a patterned surface), 6–10px visible gap from the stroke.
- **Eyebrows / step headers:** uppercase mono 10px, `letter-spacing: 0.14em`, `var(--ink2)`, weight 600.
- **Editorial asides:** italic Literata 13px `var(--ink2)` via `style="font-family: var(--font-literata), serif"` — used for the "plain-language" gloss lines.
- **Channels/buses** (e.g. the residual stream): full-width bar `rx="8"` with a 45° alternating stripe pattern (8px bands of `--hair` at 0.9 and `--line` at 0.55 over `--card`), label in a bordered chip window.
- **Layout:** 4px grid for all coords/sizes/gaps; hairline dividers in `var(--hair)`; `viewBox` width 820.

### Root element

`<svg xmlns viewBox width="100%" role="img" aria-label="...">` — always keep the aria-label meaningful.

Reference examples: `src/assets/diagrams/residual-stream.svg`, `src/assets/diagrams/induction-mechanism.svg`.

## Interactive figures — data pipeline

Figure data is **precomputed, never computed at request time**: a script in
`scripts/figures/*.py` (run via `conda run -n mech_interp python …`) writes one
JSON to `src/data/figures/` (≤ ~200 KB, values rounded to 3 dp), consumed by a
component in `src/components/interactive/`. Contract and size budget:
`src/data/figures/README.md`. This keeps the site deployable on any static
host — the deliberate constraint behind staying on GitHub Pages.

## Technical gotchas (learned the hard way)

- **`@astrojs/mdx` must stay on the v4 line** — v5+/v7 require Astro ≥ 7; this
  project is Astro 5. `astro add mdx` will install the wrong major.
- **Never name an atlas.css class `group`** (or any Tailwind utility name).
  `.group` styled every AstroPaper header button sitewide — hence `.gcard`.
- **Atlas variables are sandboxed, not on `:root`** — `--muted` etc. collide
  with the blog's theme tokens. When adding a new Atlas component class, add it
  to *both* variable-scoping selector lists at the top of `atlas.css`.
- **`@theme inline` emits no root-level CSS vars.** Component CSS cannot use
  `var(--font-mono)` etc. — reference the Astro fonts API vars directly
  (`--font-google-sans-code`, `--font-literata`); those do exist at runtime.
  Canvas code should read `getComputedStyle(el).fontFamily` from a live element
  (loaded font-family names are hash-mangled).
- **MDX + Prettier fragmentation:** multi-line JSX text children become
  separate `<p>`s — an inline link wrapped by Prettier turns into
  `<a><p>…</p></a>` mid-sentence. For prose inside styled containers, write
  markdown-in-div (blank lines around the markdown); for structured rows, wrap
  text in `div` (valid with injected `<p>`), never `span`.
- **Drafts preview locally:** `draft: true` posts render on the dev server but
  are excluded from production builds (all routes go through
  `src/utils/postFilter.ts` — keep new routes on it, don't inline
  `!data.draft`).
- **Client scripts must handle `astro:page-load`** (ClientRouter is on;
  `DOMContentLoaded` fires once per session) and clean up on
  `astro:before-swap`. See `AttentionPattern.astro` / `PostToc.astro` for the
  mount pattern.

## What's New Daily (`/whats-new`)

Auto-curated daily digest — papers + tech updates — fed by the briefing
automation in `~/projects/automation` (its `/brief` skill writes here; see that
repo's CLAUDE.md and `.claude/skills/brief/SKILL.md` step 6).

- **Data**: one JSON per day in `src/data/daily/YYYY-MM-DD.json` — shape:
  `{ date, papers[], radar[], noted[] }` (match an existing file). Skill-managed;
  hand-edit only to fix content.
- **Pages**: `src/pages/whats-new/index.astro` (latest day + calendar) and
  `src/pages/whats-new/[date].astro` (per-day, prev/next). Shared components:
  `DailyDigest.astro`, `DailyCalendar.astro`. Nav link "Daily" in `Header.astro`.
- **Privacy rule (hard)**: only public sources appear here — Hugging Face papers
  and LinkedIn/X radar. Slack and Gmail content must never enter this repo.
- Deploys like everything else: push to `main`.
