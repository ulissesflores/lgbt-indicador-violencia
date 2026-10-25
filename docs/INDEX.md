# Documentos

| Pasta | Conteúdo |
| --- | --- |
| [`dossies/`](dossies/) | `DOSSIE-CONSOLIDADO-2026-10-12.md` (versão vigente, com as revisões de 2026-10-21/22/23), partes 1 e 2 e o plano da parte 2 |
| [`laudos/`](laudos/INDEX.md) | laudos das frentes: GGB (o que é, séries), mortalidade, governos, mídia, F2 custos, F3 GGB, F5 economia política, F6 Ásia/África, F8 literatura, ideologia |
| [`PRE-REGISTROS/`](PRE-REGISTROS/) | pré-registros de governos, mortalidade e mídia, com hash gravado antes da coleta |
| [`briefings/`](briefings/) | briefings de pesquisa por rodada (método) |

Convenções dos dossiês: ✅ conferido na fonte primária · ⚠️ resumo/secundário/não revisado · 🚫 não encontrado após busca enumerada.

Fora de `docs/`, no mesmo nível de documentação: [`../paper/`](../paper/) (figuras e testes de figura; o artigo entra depois, fora do selo) e
[`../research-2026-10-21-rodada3/escrutinio/`](../research-2026-10-21-rodada3/escrutinio/) (revisões hostis, triagem, reanálises, simetria).

## Termos internos que ficaram em arquivos com hash gravado

Pré-registros e critérios foram gravados com sha256 ANTES dos dados; reescrevê-los quebraria a prova de anterioridade, então ficam byte a byte.
Neles aparecem termos de operação do projeto: "coordenadora" (a coordenação do projeto, que decidia o que ia para o navegador real),
"dono" (o autor), `fila-chrome.jsonl` (fila de páginas que exigiam navegador real, não distribuída), "entregues-pelo-ulisses" (pasta de PDFs
obtidos pelo autor por acesso institucional, não distribuída), "F-M4" (rótulo da família de hipóteses M4 de mortalidade, não um sistema) e
um caminho de pasta da máquina do autor em `PRE-REGISTROS/midia/PRE-REGISTRO{,.original}.md` (linha 76) e em
`../research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md` (linha 3). Nos demais arquivos esses termos foram trocados por termos neutros
(`../manifest/MODIFICACOES.tsv`).

Na v0.3, os pré-registros `../dados/presidencia/PREREGISTRO-C09.md` e `../dados/exposicao/PREREGISTRO-C10.md` (também com hash gravado) citam,
na linha 3, a pasta de trabalho de origem (`research-2026-10-24-presidencia/`, `research-2026-10-24-exposicao/`, hoje `dados/presidencia/` e
`dados/exposicao/`), e o de C09 cita `ASTRA-B-lacunas.md`: "Astra" é o modelo de linguagem de outra família usado como revisor externo hostil
da v0.2 (o arquivo, um levantamento de lacunas, não é distribuído). Em `../dados/painel/R6-PREREGISTRO-FORMA.md` vale a mesma regra.
O pré-registro `../dados/disque100/PREREGISTRO-D100.md` (v0.3, hash do corpo gravado antes das contagens) também cita, na linha 3, a pasta de trabalho de origem
(`research-2026-10-24-disque100/`, hoje `dados/disque100/`) e o briefing interno da frente, que não é distribuído ("frente D" é a divisão do trabalho do autor,
não um sistema); o balanço oficial que ele cita está em `../dados/disque100/entradas/`.
