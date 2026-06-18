# Earnings Review

Dashboard **standalone** de acompanhamento de resultados trimestrais de empresas
listadas. A cada trimestre extraímos os números do *release* e do ITR/DFP da
companhia, montamos a série financeira de longo prazo e escrevemos uma **leitura
qualitativa** dos trends operacionais — com gráficos que chamam atenção para a
tendência.

> Projeto independente. Não tem relação com o monitor de insiders/tesouraria da CVM.

## Uso

```bash
python build.py            # gera output/earnings_review.html (todas as empresas em data/)
python build.py RENT3      # restringe/ordena pelos tickers passados
make build                 # idem (todas)
make serve                 # serve output/ em http://127.0.0.1:8780
make publish               # regenera docs/index.html (publicado via GitHub Pages)
```

**Publicação:** GitHub Pages servindo `docs/` na branch `main` (deploy from branch).
Para atualizar o site (no Windows não há `make` — use o copy direto):

```bash
python build.py
cp output/earnings_review.html docs/index.html   # Windows: copy output\earnings_review.html docs\index.html
git add docs/index.html && git commit -m "atualiza dashboard" && git push
```

(Não usa GitHub Actions: o token de push não tem o escopo `workflow`. Se quiser CI,
conceda o escopo `workflow` e mova o build para `.github/workflows/`.)

Saída: um HTML **autossuficiente** (SVG inline, sem CDN de JS; fontes via Google
Fonts com fallback de sistema). Abre direto no navegador.

## Dados (`data/<TICKER>.json`)

Uma empresa por arquivo. É a **fonte da verdade** do dashboard.

```jsonc
{
  "ticker": "RENT3", "nome": "Localiza", "setor": "...",
  "ref": "1T26",
  "ref_data": "2026-03-31",            // data-base do trimestre (fim do período)
  "data_divulgacao": "2026-05-07",     // DIA em que o resultado foi divulgado
  "divulgacao_nota": "após o fechamento",  // opcional

  "quarters": [                         // série COMPLETA; gráficos plotam tudo
    {"periodo":"1T10","ref":"2010-03-31",
     "financ":{"receita_liq":..,"receita_aluguel":..,"ebitda":..,
               "margem_ebitda":..,"lucro_liquido":..,"result_fin":..}},  // R$ mi
    ...
  ],
  "operacional": [                       // KPIs do trimestre de referência
    {"label":"Frota total","valor":"645.854","unidade":"carros",
     "yoy":2.8,"qoq":-1.9,"nota":"..."}
  ],
  "trends":   [{"tom":"pos|neg|neu","titulo":"...","texto":"..."}],
  "veredito": {"tom":"positivo|misto|negativo","resumo":"..."},
  "fontes":   [{"label":"Release 1T26","url":"https://..."}]
}
```

- **YoY/QoQ dos KPIs financeiros** são derivados da série em runtime (último vs
  4 trimestres atrás / vs anterior). Os do `operacional[]` são curados no JSON.
- **Margem EBITDA** = EBITDA / receita líquida de aluguel.
- A **leitura (`trends`/`veredito`) é um rascunho gerado no processamento** —
  revisar antes de circular.

## Rotina trimestral

1. Virou o trimestre → pegar os números na **fonte primária**. A melhor é a
   **planilha de séries históricas do RI da companhia** (o Excel de "dados
   históricos"/"central de resultados", atualizado a cada tri) — primária e já
   traz a série longa inteira. Conferir contra o *release*/ITR.
2. Acrescentar o(s) trimestre(s) em `quarters[]` e atualizar `operacional[]`/`ref`/
   `data_divulgacao` (lida do release/protocolo CVM, não de notícia).
3. Rascunhar `trends[]` + `veredito` a partir dos dados, com juízo próprio; **revisar**.
4. `make build` e publicar o HTML.

> Exemplo: Localiza → planilha `localiza_1t26.xlsx` do RI (aba Consolidado / Dados
> Operacionais), de onde saiu a série 1T10–1T26.

## Adicionar uma empresa

Procurar o Excel de séries históricas no RI da empresa, extrair a série e soltar um
novo `data/<TICKER>.json` no formato acima. Sem refactor; o seletor de empresa
aparece automaticamente quando há mais de uma.

## Convenções

- **Só fontes primárias.** Os números e a leitura saem do *release* da companhia e do
  ITR/DFP na CVM — **nada de notícia/sell-side**, pra não enviesar a análise. Fatos
  pontuais (ex.: data de divulgação) também se leem do release/protocolo CVM. As
  `fontes[]` devem citar apenas a fonte oficial.
- **Sem dependência externa no HTML.** Gráficos são SVG inline. Não reintroduzir
  `<script src=...>` externo.
- Templates com CSS/JS usam `.replace(sentinela)`, não `str.format()`.
- Cabeçalho sempre com **chip de versão** (`v1.0 · data`).
- Gráficos sempre com a **série mais longa disponível**, sem seletor de janela.
