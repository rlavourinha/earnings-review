"""
Earnings Review — dashboard standalone de acompanhamento de resultados.

A cada trimestre: extrair os números do release/ITR da companhia, atualizar
data/<TICKER>.json (série financeira + KPIs operacionais) e rascunhar a leitura
qualitativa dos trends. Este script lê os JSONs e gera um HTML autossuficiente
(SVG inline, sem CDN de JS) com:

  · veredito do trimestre        · KPIs financeiros com Δ YoY/QoQ
  · gráficos da SÉRIE COMPLETA   · leitura qualitativa (trends) + KPIs operacionais

Uso:
  python build.py            -> output/earnings_review.html (todas as empresas em data/)
  python build.py RENT3      -> idem, mas restrito/ordenado pelos tickers passados

Sem str.format() onde há CSS/JS: o script JS é montado com .replace(sentinela).
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import theme

VERSION = "1.0"
BASE = Path(__file__).resolve().parent
DATA_DIR = BASE / "data"
OUT_DIR = BASE / "output"
OUT_DIR.mkdir(exist_ok=True)


def load(order: list[str] | None = None) -> dict:
    data = {}
    for fp in sorted(DATA_DIR.glob("*.json")):
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[earnings] ignorando {fp.name}: {e}")
            continue
        data[obj.get("ticker") or fp.stem] = obj
    if order:
        data = {t: data[t] for t in order if t in data} or data
    return data


# ---------------------------------------------------------------------------
def _script(data: dict, default: str) -> str:
    js = r"""<script>(()=>{
  const DATA = __PAYLOAD__;
  const sel = document.getElementById('co'); if(!sel) return;
  const $ = id => document.getElementById(id);

  const dec=(v,n=1)=>(v==null||isNaN(v))?'—':v.toFixed(n).replace('.',',');
  const fmtMi=v=>{ if(v==null||isNaN(v))return '—'; const a=Math.abs(v);
    return a>=1000 ? 'R$ '+dec(v/1000,2)+' bi' : 'R$ '+dec(v,0)+' mi'; };
  const chg=(c,p)=>(p==null||p<=0||isNaN(p)||c==null)?null:(c/p-1)*100;
  // comparativos por rótulo de trimestre (robusto p/ série curta ou com lacunas)
  const yoyP=p=>p.slice(0,2)+String(+p.slice(2)-1).padStart(2,'0');           // 1T26 -> 1T25
  const qoqP=p=>{const t=+p[0],y=+p.slice(2);                                  // 1T26 -> 4T25
    return t===1?('4T'+String(y-1).padStart(2,'0')):((t-1)+'T'+p.slice(2));};

  function chip(v,unit){
    if(v==null||isNaN(v)) return '<span class="chip flat">—</span>';
    const flat=Math.abs(v)<0.05, up=v>0, arr=flat?'→':(up?'▲':'▼');
    const cls=flat?'flat':(up?'up':'down'), u=unit==='pp'?' p.p.':'%';
    return `<span class="chip ${cls}">${arr} ${(up?'+':'')}${dec(v,1)}${u}</span>`;
  }

  // série curta (ex.: review via release, só YoY): barras por trimestre
  function chartBars(vals, labels, fmt, zeroBase){
    const W=400,H=212,padL=10,padR=12,padT=22,padB=26, n=vals.length;
    const plotW=W-padL-padR, plotH=H-padT-padB;
    let mn=Math.min(...vals), mx=Math.max(...vals);
    if(zeroBase||mn>0){ mn=Math.min(0,mn); } mx=Math.max(0,mx);
    const span=(mx-mn)||1, y=v=>padT+plotH*(mx-v)/span, yz=y(0);
    const slot=plotW/n, bw=Math.min(slot*0.5,64);
    let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="comparativo por trimestre">`;
    s+=`<line class="gl" x1="${padL}" y1="${yz.toFixed(1)}" x2="${W-padR}" y2="${yz.toFixed(1)}"/>`;
    for(let i=0;i<n;i++){ const xc=padL+slot*i+slot/2, v=vals[i], yv=y(v);
      const top=Math.min(yv,yz), h=Math.max(Math.abs(yv-yz),1.5), last=i===n-1;
      const fill=last?'var(--accent)':(v<0?'var(--down)':'var(--muted)');
      s+=`<rect x="${(xc-bw/2).toFixed(1)}" y="${top.toFixed(1)}" width="${bw.toFixed(1)}" height="${h.toFixed(1)}" rx="3" fill="${fill}" opacity="${last?'1':'.5'}"/>`;
      s+=`<text class="last-lbl" x="${xc.toFixed(1)}" y="${(top-6).toFixed(1)}" text-anchor="middle">${fmt(v)}</text>`;
      s+=`<text class="ax" x="${xc.toFixed(1)}" y="${(H-8).toFixed(1)}" text-anchor="middle">${labels[i]}</text>`;
    }
    s+=`</svg>`; return s;
  }
  // gráfico de série completa: área + linha, último ponto destacado, ticks por ano
  function chartArea(vals, labels, fmt, zeroBase){
    if(vals.length<=6) return chartBars(vals, labels, fmt, zeroBase);
    const W=400,H=212,padL=10,padR=12,padT=18,padB=26;
    const plotW=W-padL-padR, plotH=H-padT-padB, n=vals.length;
    let mn=Math.min(...vals), mx=Math.max(...vals);
    if(zeroBase){ mn=Math.min(0,mn); mx=Math.max(0,mx); }
    const span=(mx-mn)||1; const x=i=>padL+plotW*i/(n-1); const y=v=>padT+plotH*(mx-v)/span;
    let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="série histórica">`;
    if(zeroBase && mn<0){ const yz=y(0); s+=`<line class="gl" x1="${padL}" y1="${yz.toFixed(1)}" x2="${W-padR}" y2="${yz.toFixed(1)}"/>`; }
    const pts=vals.map((v,i)=>`${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
    const baseY=zeroBase&&mn<0?y(0):(padT+plotH);
    s+=`<polygon points="${padL},${baseY.toFixed(1)} ${pts} ${(W-padR)},${baseY.toFixed(1)}" fill="rgba(79,195,224,.10)"/>`;
    s+=`<polyline points="${pts}" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round"/>`;
    // ticks de ano (todo 1T) — rótulo de 2 dígitos
    for(let i=0;i<n;i++){ if(String(labels[i]).slice(0,2)==='1T'){
      s+=`<text class="ax" x="${x(i).toFixed(1)}" y="${(H-8).toFixed(1)}" text-anchor="middle">${labels[i].slice(2)}</text>`; } }
    const li=n-1, lv=vals[li];
    s+=`<circle cx="${x(li).toFixed(1)}" cy="${y(lv).toFixed(1)}" r="3.4" fill="var(--accent)" stroke="var(--bg)" stroke-width="1.5"/>`;
    s+=`<text class="last-lbl" x="${(W-padR).toFixed(1)}" y="${(padT-5).toFixed(1)}" text-anchor="end">${fmt(lv)}</text>`;
    s+=`</svg>`; return s;
  }
  const card=(t,m,svg)=>`<section class="card"><div class="card-h"><h2>${t}</h2><span class="m">${m}</span></div><div class="chart-box">${svg}</div></section>`;

  function render(tk){
    const c=DATA[tk]; if(!c) return;
    const qs=c.quarters||[], L=qs.map(q=>q.periodo), N=qs.length;
    const F=k=>qs.map(q=>(q.financ||{})[k]);
    const rec=F('receita_liq'), ebt=F('ebitda'), mg=F('margem_ebitda'), ll=F('lucro_liquido');
    const byP={}; qs.forEach(q=>byP[q.periodo]=q.financ||{});
    const cp=(qs[N-1]||{}).periodo||'';
    const fc=byP[cp]||{}, fy=byP[yoyP(cp)]||{}, fq=byP[qoqP(cp)]||{};

    const brDate = s => s ? s.split('-').reverse().join('/') : '';
    $('h-co').innerHTML = (c.nome||tk)+' · <em>'+(c.ref||'')+'</em>';
    $('h-sub').innerHTML = `<span>${c.setor||''}</span>`
      + (c.data_divulgacao?`<span class="disc">Resultado divulgado em <b>${brDate(c.data_divulgacao)}</b>${c.divulgacao_nota?' ('+c.divulgacao_nota+')':''}</span>`:'')
      + (c.ref_data?`<span>data-base <b>${brDate(c.ref_data)}</b></span>`:'')
      + `<span>série <b>${L[0]}–${L[N-1]}</b> (${N} tri)</span>`;

    const vd=c.veredito||{}, tom=vd.tom||'misto';
    $('verdict').className='verdict t-'+tom;
    $('verdict').innerHTML = vd.resumo ? `<span class="badge">Veredito · ${tom}</span><p>${vd.resumo}</p>` : '';

    const mgd=(a,b)=>(a==null||b==null)?null:(a-b);
    const KPI=(lbl,val,d1,d2,u1,foot)=>`<div class="kpi"><div class="lbl">${lbl}</div><div class="val">${val}</div>
      <div class="deltas"><span class="dl"><span class="k">YoY</span>${chip(d1,u1)}</span><span class="dl"><span class="k">QoQ</span>${chip(d2,u1)}</span></div>
      ${foot?`<div class="foot">${foot}</div>`:''}</div>`;
    $('kpis').innerHTML =
        KPI('Receita líquida', fmtMi(fc.receita_liq), chg(fc.receita_liq,fy.receita_liq), chg(fc.receita_liq,fq.receita_liq), null, c.receita_nota||'receita operacional líquida')
      + KPI('EBITDA', fmtMi(fc.ebitda), chg(fc.ebitda,fy.ebitda), chg(fc.ebitda,fq.ebitda), null, 'margem '+dec(fc.margem_ebitda,1)+'%')
      + KPI('Margem EBITDA', dec(fc.margem_ebitda,1)+'%', mgd(fc.margem_ebitda,fy.margem_ebitda), mgd(fc.margem_ebitda,fq.margem_ebitda), 'pp', 'sobre '+(c.margem_base||'a receita líquida'))
      + KPI('Lucro líquido', fmtMi(fc.lucro_liquido), chg(fc.lucro_liquido,fy.lucro_liquido), chg(fc.lucro_liquido,fq.lucro_liquido), null, 'do período');

    $('charts').innerHTML =
        card('Receita líquida', 'R$ mi', chartArea(rec,L,fmtMi,false))
      + card('Margem EBITDA', '%', chartArea(mg,L,v=>dec(v,1)+'%',false))
      + card('Lucro líquido', 'R$ mi', chartArea(ll,L,fmtMi,true));

    const ts=c.trends||[];
    $('trends').innerHTML = ts.length ? ts.map(t=>`<div class="trend t-${t.tom||'neu'}">
      <div class="trend-h"><span class="dot"></span><span class="t">${t.titulo||''}</span></div><p>${t.texto||''}</p></div>`).join('')
      : '<div class="empty">Sem leitura curada.</div>';

    const ops=c.operacional||[];
    $('oper').innerHTML = ops.length ? ops.map(o=>`<div class="ocell">
      <div class="ol">${o.label}</div>
      <div class="ov">${o.valor||'—'}<span class="un">${o.unidade||''}</span></div>
      <div class="od"><span class="dl"><span class="k">YoY</span>${chip(o.yoy)}</span><span class="dl"><span class="k">QoQ</span>${chip(o.qoq)}</span></div>
      ${o.nota?`<div class="on">${o.nota}</div>`:''}</div>`).join('')
      : '<div class="empty">Sem KPIs operacionais.</div>';

    const fs=c.fontes||[];
    $('srcs').innerHTML = fs.length ? 'Fontes: '+fs.map(f=>f.url?`<a href="${f.url}" target="_blank" rel="noopener">${f.label} ↗</a>`:f.label).join('  ·  ') : '';
  }

  const def='__DEFAULT__';
  if([...sel.options].some(o=>o.value===def)) sel.value=def;
  render(sel.value);
  sel.addEventListener('change', e=>render(e.target.value));
})();</script>"""
    return js.replace("__PAYLOAD__", json.dumps(data, ensure_ascii=False)).replace("'__DEFAULT__'", json.dumps(default))


def build(data: dict) -> str:
    tickers = list(data.keys())
    default = "RENT3" if "RENT3" in data else (tickers[0] if tickers else "")
    options = "".join(f'<option value="{t}">{t} · {data[t].get("nome", t)}</option>' for t in tickers)
    today = dt.date.today().strftime("%d/%m/%Y")
    picker = (f'<div class="picker"><label for="co">Empresa</label>'
              f'<div class="sel"><select id="co">{options}</select></div></div>')
    if not tickers:
        body = '<div class="empty">Nenhuma empresa em data/. Adicione um data/&lt;TICKER&gt;.json.</div>'
        picker = ""
    else:
        body = f"""
  <div class="verdict" id="verdict"></div>
  <section class="kpis" id="kpis"></section>
  <section class="charts" id="charts"></section>
  <div class="cols">
    <section class="card read"><div class="card-h"><h2>Leitura do trimestre</h2><span class="m">trends operacionais</span></div>
      <div id="trends"></div></section>
    <section class="card oper"><div class="card-h"><h2>Operacional</h2><span class="m">YoY · QoQ</span></div>
      <div id="oper"></div></section>
  </div>
  <p class="srcs" id="srcs"></p>
  <section class="method">
    <div><h3>O que é</h3><p>Acompanhamento <b>trimestral</b> do resultado da companhia: série financeira de longo prazo + <b>leitura qualitativa</b> dos trends operacionais que merecem atenção.</p></div>
    <div><h3>Fontes</h3><p><b>Só fontes primárias</b>: o <b>release de resultados</b> e o <b>ITR/DFP</b> da companhia. Sem notícia/sell-side — pra não enviesar a leitura. Cada KPI é conferível na fonte primária. Margem EBITDA sobre a receita de aluguel.</p></div>
    <div><h3>Método</h3><p>Juízo próprio a partir do dado primário; YoY/QoQ derivados da série; gráficos mostram o <b>histórico completo</b>, sem janela. A leitura é um <b>rascunho gerado no processamento</b> — revisar antes de circular.</p></div>
  </section>"""

    return f"""<!doctype html><html lang="pt-BR">{theme.head('Earnings Review')}
<body><div class="wrap">
  <header>
    <div>
      <div class="brand">Earnings Review</div>
      <h1 id="h-co">—</h1>
      <div class="sub" id="h-sub"></div>
    </div>
    <div class="head-right">
      <span class="ver">v<b>{VERSION}</b> · {today}</span>
      {picker}
    </div>
  </header>
  {body}
  <footer><span>earnings-review · dashboard standalone</span><span>gerado em {today}</span></footer>
</div>
{_script(data, default)}
</body></html>"""


def main() -> None:
    order = [a.upper() for a in sys.argv[1:] if not a.startswith("-")]
    data = load(order or None)
    out = OUT_DIR / "earnings_review.html"
    out.write_text(build(data), encoding="utf-8")
    print(f"[earnings] {out}  ({len(data)} empresa(s): {', '.join(data) or '—'})")


if __name__ == "__main__":
    main()
