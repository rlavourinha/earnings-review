"""
Identidade visual do Earnings Review — dark, mas com personalidade própria
(distinta do monitor CVM): fundo quase-preto frio, acento ciano/azure, títulos
em Space Grotesk e números em JetBrains Mono. Tudo self-contained: SVG inline,
sem CDN de JS (fontes via Google Fonts com fallback de sistema).
"""

CSS = r"""
:root{
  --bg:#0B0C0F; --surface:#14161C; --surface2:#1B1E26; --border:#272B34;
  --ink:#ECEEF2; --muted:#969FAD; --faint:#5A636F;
  --up:#3FC08A; --down:#F0664B; --accent:#4FC3E0; --accent2:#7C8CF8;
  --glow:rgba(79,195,224,.14);
}
*{box-sizing:border-box}
body{margin:0;background:
   radial-gradient(900px 380px at 78% -8%, var(--glow), transparent 70%),
   var(--bg);
  color:var(--ink);font-family:'Inter',system-ui,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:1200px;margin:0 auto;padding:40px 28px 70px}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
code{font-family:'JetBrains Mono',monospace;font-size:.9em;color:var(--accent)}

/* header */
header{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;
  padding-bottom:22px;border-bottom:1px solid var(--border);margin-bottom:28px}
.brand{font:600 11px/1 'JetBrains Mono',monospace;letter-spacing:.34em;text-transform:uppercase;color:var(--accent);margin-bottom:14px}
h1{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:clamp(28px,4.6vw,44px);line-height:1.04;letter-spacing:-.015em;margin:0}
h1 em{font-style:normal;color:var(--accent)}
.sub{color:var(--muted);font-size:13.5px;margin-top:11px;display:flex;flex-wrap:wrap;gap:7px 16px;align-items:center}
.sub b{color:var(--ink);font-weight:600}
.sub .disc{display:inline-flex;align-items:center;gap:7px;color:var(--ink)}
.sub .disc::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 3px var(--glow)}
.sub .disc b{color:var(--accent)}
.head-right{display:flex;flex-direction:column;align-items:flex-end;gap:12px}
.ver{font:600 10.5px 'JetBrains Mono',monospace;letter-spacing:.1em;color:var(--muted);
  border:1px solid var(--border);border-radius:999px;padding:6px 13px;background:var(--surface)}
.ver b{color:var(--accent);font-weight:600}

/* seletor */
.picker{display:flex;align-items:center;gap:12px}
.picker label{font:600 10px 'Inter',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--faint)}
.sel{position:relative}
select{appearance:none;background:var(--surface);color:var(--ink);border:1px solid var(--border);border-radius:8px;
  padding:11px 38px 11px 15px;font:600 15px 'JetBrains Mono',monospace;letter-spacing:.02em;cursor:pointer;min-width:190px}
select:focus{outline:2px solid var(--accent);outline-offset:1px}
.sel::after{content:"▾";position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--accent);pointer-events:none}

/* veredito */
.verdict{display:flex;gap:16px;align-items:flex-start;margin:0 0 26px;padding:18px 22px;border-radius:12px;
  background:linear-gradient(180deg,var(--surface),var(--surface2));border:1px solid var(--border);border-left:4px solid var(--faint)}
.verdict.t-positivo{border-left-color:var(--up)} .verdict.t-negativo{border-left-color:var(--down)} .verdict.t-misto{border-left-color:var(--accent2)}
.verdict .badge{font:700 10px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;
  padding:6px 11px;border-radius:6px;white-space:nowrap;background:rgba(90,99,111,.18);color:var(--muted)}
.verdict.t-positivo .badge{background:rgba(63,192,138,.16);color:var(--up)}
.verdict.t-negativo .badge{background:rgba(240,102,75,.16);color:var(--down)}
.verdict.t-misto .badge{background:rgba(124,140,248,.16);color:var(--accent2)}
.verdict p{margin:0;font-size:15px;color:var(--ink);line-height:1.55}

/* kpis */
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:0 0 26px}
.kpi{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:18px 19px}
.kpi .lbl{font:600 10px 'Inter',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin-bottom:11px}
.kpi .val{font:600 25px 'JetBrains Mono',monospace;letter-spacing:-.01em;color:var(--ink)}
.kpi .foot{font-size:11.5px;color:var(--muted);margin-top:7px}
.deltas{display:flex;gap:8px;margin-top:11px;flex-wrap:wrap}
.dl{display:inline-flex;align-items:center;gap:5px}
.dl .k{font:600 8.5px 'Inter',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.chip{font:600 11.5px 'JetBrains Mono',monospace;padding:2px 7px;border-radius:5px;white-space:nowrap}
.chip.up{color:var(--up);background:rgba(63,192,138,.13)}
.chip.down{color:var(--down);background:rgba(240,102,75,.13)}
.chip.flat{color:var(--muted);background:rgba(90,99,111,.14)}

/* gráficos (série completa) */
.charts{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:0 0 26px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.card-h{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:15px 18px 4px}
.card-h h2{font:600 14px 'Space Grotesk',sans-serif;margin:0;letter-spacing:-.01em}
.card-h .m{font:500 10.5px 'JetBrains Mono',monospace;color:var(--faint);letter-spacing:.02em}
.chart-box{padding:6px 14px 14px}
.chart-box svg{width:100%;height:auto;display:block}
.ax{fill:var(--faint);font-family:'JetBrains Mono',monospace;font-size:9px}
.gl{stroke:var(--border);stroke-width:1}
.last-lbl{fill:var(--ink);font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600}

/* colunas leitura/operacional */
.cols{display:grid;grid-template-columns:1.3fr 1fr;gap:16px;margin:0 0 26px;align-items:start}
.read{padding:4px 0 8px}
.read .card-h{padding:16px 20px 14px;border-bottom:1px solid var(--border)}
.trend{padding:15px 20px;border-bottom:1px solid rgba(39,43,52,.6)} .trend:last-child{border-bottom:0}
.trend-h{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.dot{width:8px;height:8px;border-radius:50%;background:var(--faint);flex:none}
.trend.t-pos .dot{background:var(--up)} .trend.t-neg .dot{background:var(--down)} .trend.t-neu .dot{background:var(--accent)}
.trend-h .t{font:600 13.5px 'Inter',sans-serif;color:var(--ink)}
.trend p{margin:0;font-size:12.5px;color:var(--muted);line-height:1.55}
.oper .card-h{padding:16px 20px 14px;border-bottom:1px solid var(--border)}
.ocell{padding:15px 18px;border-bottom:1px solid rgba(39,43,52,.6)} .ocell:last-child{border-bottom:0}
.ocell .ol{font:600 10px 'Inter',sans-serif;letter-spacing:.05em;text-transform:uppercase;color:var(--faint);margin-bottom:8px}
.ocell .ov{font:600 18px 'JetBrains Mono',monospace;color:var(--ink)}
.ocell .ov .un{font-size:11px;color:var(--muted);margin-left:5px;font-weight:500}
.ocell .od{display:flex;gap:9px;margin-top:8px}
.ocell .on{font-size:11px;color:var(--muted);margin-top:8px;line-height:1.45}

/* método + rodapé */
.method{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;padding:22px 24px;background:var(--surface);
  border:1px solid var(--border);border-radius:12px;margin:0 0 14px}
.method h3{font:700 10px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0 0 8px}
.method p{margin:0;font-size:12.5px;color:var(--muted);line-height:1.55} .method b{color:var(--ink);font-weight:500}
.srcs{font:500 11.5px 'JetBrains Mono',monospace;color:var(--faint);margin:0 0 18px}
.srcs a{color:var(--accent)}
footer{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;color:var(--faint);
  font:500 11px 'JetBrains Mono',monospace;border-top:1px solid var(--border);padding-top:16px}
.empty{padding:24px;text-align:center;color:var(--faint);font-size:13px}

@media (max-width:900px){
  .kpis{grid-template-columns:repeat(2,1fr)} .charts{grid-template-columns:1fr}
  .cols{grid-template-columns:1fr} .method{grid-template-columns:1fr}
  header{align-items:flex-start} .head-right{align-items:flex-start}
}
"""


def head(title: str) -> str:
    return f"""<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>"""
