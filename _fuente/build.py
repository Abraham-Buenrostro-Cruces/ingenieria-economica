#!/usr/bin/env python3
"""Ensambla cada sesión en un HTML autocontenido.

Por defecto genera la versión SIN CONEXIÓN: tipografías, KaTeX, Plotly y
Tailwind quedan incrustados dentro del archivo. Con --online se enlazan
desde internet y los archivos pesan ~60 KB en lugar de ~1.7 MB.

    python build.py            sin conexión  (predeterminado)
    python build.py --online   enlaza a los CDN
"""
import re, sys, pathlib

BASE = pathlib.Path(__file__).parent
CSS = (BASE / "_core.css").read_text(encoding="utf-8")
JS = (BASE / "_core.js").read_text(encoding="utf-8")
A = BASE / "_assets"

ONLINE = "--online" in sys.argv

KATEX_CFG = ("{delimiters:[{left:'$$',right:'$$',display:true},"
             "{left:'\\\\[',right:'\\\\]',display:true},"
             "{left:'\\\\(',right:'\\\\)',display:false}],throwOnError:false}")

if ONLINE:
    HEAD = """<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body,%s);"></script>""" % KATEX_CFG
    TAIL = ""
else:
    def rd(n):
        return (A / n).read_text(encoding="utf-8")
    HEAD = (
        "<style>\n/* Inter + JetBrains Mono incrustadas */\n" + rd("fonts.css") + "\n</style>\n"
        "<style>\n/* Tailwind (compilado, solo las clases usadas) */\n" + rd("tw.css") + "\n</style>\n"
        "<style>\n/* KaTeX */\n" + rd("katex.css") + "\n</style>"
    )
    TAIL = (
        "<script>\n/* Plotly basic */\n" + rd("plotly.js") + "\n</script>\n"
        "<script>\n/* KaTeX */\n" + rd("katex.js") + "\n</script>\n"
        "<script>\n" + rd("katex-auto.js") + "\n</script>\n"
        "<script>renderMathInElement(document.body," + KATEX_CFG + ");</script>"
    )

SHELL = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{head}
<style>
{css}
</style>
</head>
<body>
<div id="progress-bar" style="width:0%"></div>
<a id="home-link" href="00_Indice.html">&#8592; Índice</a>
<div id="nav-controls">
  <span id="slide-counter" class="text-[11px] font-mono text-[#666] mr-2">1 / 1</span>
  <button class="nav-btn" onclick="prevSlide()">&#8592;</button>
  <button class="nav-btn" onclick="nextSlide()">&#8594;</button>
</div>
<div id="presentation">
{body}
</div>
{tail}
<script>
{core}
{page}
</script>
</body>
</html>
"""


def build(src: pathlib.Path, out: pathlib.Path):
    raw = src.read_text(encoding="utf-8")
    m = re.match(r"<!--TITLE:(.*?)-->\s*", raw)
    title = m.group(1).strip() if m else src.stem
    raw = raw[m.end():] if m else raw
    if "<!--SCRIPT-->" not in raw:
        sys.exit(f"{src.name}: falta el marcador <!--SCRIPT-->")
    body, page = raw.split("<!--SCRIPT-->", 1)
    html = SHELL.format(title=title, head=HEAD, css=CSS, body=body.strip(),
                        tail=TAIL, core=JS, page=page.strip())
    out.write_text(html, encoding="utf-8")
    n = len(re.findall(r'class="slide(?:\s|")', body))
    print(f"{out.name:44s} {len(html)/1024/1024:6.2f} MB  {n:2d} diapositivas")


if __name__ == "__main__":
    outdir = BASE / ("dist-online" if ONLINE else "dist")
    outdir.mkdir(exist_ok=True)
    print("modo:", "CON CONEXIÓN (enlaza a CDN)" if ONLINE else "SIN CONEXIÓN (todo incrustado)")
    names = {
        "s1": "01_Sesion1_Fundamentos.html",
        "s2": "02_Sesion2_Valor_Presente_Anual.html",
        "s3": "03_Sesion3_TIR_Depreciacion_BC.html",
        "s4": "04_Sesion4_Reemplazo_Costos.html",
    }
    for stem, fname in names.items():
        src = BASE / "src" / f"{stem}.html"
        if src.exists():
            build(src, outdir / fname)
