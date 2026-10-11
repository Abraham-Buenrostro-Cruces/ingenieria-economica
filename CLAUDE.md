# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Course material for an Engineering Economics class (Ingeniería Económica): four interactive slide-deck sessions plus an index page, delivered as single-file HTML that students open locally. All content, UI text and comments are in **Spanish** — keep it that way.

- Top level: `00_Indice.html` (hand-written index, not generated) and `01_…`–`04_…html` — **build outputs**, ~1.7 MB each, fully self-contained (fonts, KaTeX, Plotly, Tailwind inlined) so they work offline. Never edit these directly.
- `_fuente/`: the source. `LEEME.txt` is the author's maintenance guide.

## Build

```
cd _fuente
python build.py            # offline build (everything inlined) -> _fuente/dist/
python build.py --online   # CDN-linked build (~60 KB, faster while editing) -> _fuente/dist-online/
```

Then copy the generated files over the ones in the top-level folder. There is no test suite or linter.

**Known path mismatch:** `build.py` reads sources from `_fuente/src/sNN.html`, but the sources actually live directly in `_fuente/` (`s1.html`…`s4.html`). As-is the build silently produces nothing (it skips missing files). Either move the sources into `src/` or change `BASE / "src"` to `BASE` in `build.py` before building.

## Architecture

`build.py` wraps each `sNN.html` in a shared `SHELL` template:

- `sNN.html` starts with `<!--TITLE:…-->` (page title) and is split at the required `<!--SCRIPT-->` marker: everything above is slide markup, everything below is page-specific JS.
- The shell injects `_core.css` (shared styles, accent colors `.accent-t/-v/-r/-a`) and `_core.js` before the page JS, plus nav controls, progress bar and a link back to `00_Indice.html`.
- Offline mode inlines `_assets/` (fonts.css, tw.css, katex.css/js, katex-auto.js, plotly.js); online mode links CDNs instead.

`_core.js` is the shared engine every page relies on:
- Compound-interest factor functions `FP, PF, PA, AP, FA, AF, PG, AG, Pg(i,g,n)`, plus `npv`, `irr` (bisection) and `irrAll` (scans for multiple IRR roots).
- Formatters `money`, `money0`, `pct`, `f5`; shared Plotly layout `PL` and config `PLC`.
- Slide navigation (`initNav`, `nextSlide`, `prevSlide`); calls the page's optional `onSlideChange(k)` hook on each slide change.

Each page's script defines interactive "labs" (`lab1()`, `lab6()`, …, numbered continuously across sessions) that read inputs and redraw Plotly charts, and a `window 'load'` handler that calls `initNav()` and each lab.

## Gotchas when editing content

- Slides are `<div class="slide"><div class="slide-content">…</div></div>`; the first one has `class="slide active"`.
- `onSlideChange(k)` in each `sNN.html` maps **hard-coded slide indices** to Plotly element ids to resize charts when a hidden slide becomes visible. Inserting/removing a slide before a lab requires updating those indices.
- `_assets/tw.css` is a precompiled Tailwind subset containing only classes currently used. A new Tailwind class works in `--online` builds but not offline until `tw.css` is regenerated (`npx tailwindcss -i entrada.css -o _assets/tw.css --content "dist/*.html" --minify`). "Looks right online, wrong offline" means this.
- `_assets/katex.css` embeds only 6 KaTeX fonts (Main-Regular, Math-Italic, Size1–4); other families (bold math, calligraphic, Fraktur, AMS) fall back to substitute fonts. Math delimiters: `\( … \)` inline, `$$ … $$` display.
- Accent hex colors (`#2dd4bf`, `#a78bfa`, `#fb7185`, `#fbbf24`) are duplicated as literals inside the Plotly traces in `sNN.html`; change both places for consistency.
- `00_Indice.html` still says formulas/charts load from the internet, which is out of date for the offline build.
