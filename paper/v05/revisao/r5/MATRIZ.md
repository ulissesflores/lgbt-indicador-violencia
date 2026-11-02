# Matriz de respostas da rodada r5 (Astra e Grok; Argon pendente de cota)

Manuscrito revisado: `paper-v05/revisao/r5/MANUSCRITO.md` (sha256 `6a4b09ea…`). Versão corrigida: `paper-v05/revisao/r6/MANUSCRITO.md` (sha256 `b7107535…`). Cada crítica foi conferida na fonte (arquivo do repositório citado pelo revisor) antes da resposta. A decisão segue a evidência, não a maioria. Trava de números, citações e legibilidade: 0 falhas nos 6 blocos. Conferência do quadro: 0 divergências.

| ID | Crítica | Conferência | Resposta | Onde |
|---|---|---|---|---|
| AST-01 | κ da conferência do GGB omitido | `kappa.json`: 23 casos; morte κ 0,462; LGBT+ κ 0,912; 2 de 6 desacordos em morte | Aceita. 2.6 declara modelos na conferência do GGB, com κ 0,91 e 0,46; 3.5 diz que Wilson mede só o sorteio; Tabela MC5.C0 nova (dupla codificação em 23 dos 32 pré-sorteados) | bloco-2, bloco-3b, MC5 |
| AST-02 | Denominador do Sinan e "vazio" | `serie_campo55_uf_ano.py` exclui `LES_AUTOP == "1"`; 2025: 29,72 + 14,75 | Aceita. "fichas de violência não autoprovocada"; a conta soma ignorado, branco e "não se aplica"; Figura 1 passa a "sem motivo útil" | bloco-3a, nota da Fig. 6, Fig. 1 |
| AST-03 | Estudo de eventos: sinal do escore ≠ troca de bloco | `painel_c03_event_pesos.py` usa só o sinal | Aceita. MC6 e Tabela MC6.A10 passam a "deslocamento para a direita/esquerda", com nota | MC6 (monta_mc.py) |
| AST-04 | 38 mil condenações soviéticas | `H-RELATORIO.md`: Valodzin "about 50/50" consensual × estupro/menores; condenações, não pessoas | Aceita. Corpo e Tabela 5 levam a ressalva | bloco-3c |
| AST-05 | Regra retrospectiva como prévia | MC1: regra complementar de 24/10, "não é prospectiva"; MC4: "parcial" na regra original | Aceita. 3.4 diz o veredito sob as duas regras | bloco-3b |
| AST-06 / GRO-01 | Efeito mínimo como "mudança" | `_mde`: só aumento, 80% de poder | Aceita. Resumo e Abstract: "80% de poder só para aumento relativo de 60,7%"; quadro A15 | bloco-1, QUADRO-E2 |
| AST-07 | IC [0,00; 0,00] | célula da Tabela MC2.A4 | Aceita. "nenhum caso (intervalo não estimável)" | MC2 |
| AST-08 | FRA sem qualificação | laudo F8: amostra não probabilística | Aceita. "pesquisa pela internet... sem amostra probabilística... respondentes" | bloco-4 |
| AST-09 | Extremos de raça contam ignorados duas vezes | `padroniza_idade.py` linhas 159–160 | Aceita. Extremos partem só da raça conhecida; saídas idênticas a 2 casas (2,60 e 2,42; `asr_brasil.md` sem diferença) | repo `dados/sim/padroniza_idade.py` |
| AST-10 | Custo estrangeiro sob "R$ de setembro" | `cenarios_custo.py:42` PTAX 2026-10-20; contrato GSGB | Aceita. Título "R$ de 2026"; nota diz contrato estrangeiro e câmbio de 20/10/2026 | bloco-4 |
| AST-11 | "GGB e ANTRA" com números só do GGB | `fig_caminho_v05.py` lê só `ggb` | Aceita. Linha rotulada "GGB" | Figura 1 |
| AST-12 | SIDRA 9606 fora da referência | `padroniza_idade.py:4`, `censo9606_…json` | Aceita. Referência IBGE (2026) inclui 9606 | referencias.md |
| AST-13 | Selo e remissões antigas no MC | MC12 citava selo `d1d2…` (724); "Tabela MC1.6" | Aceita. MC12 separa o selo da v0.4.4 do atual; remissões resolvidas pelo MC dono do rótulo (bug de raiz no `monta_mc.py`); Tabela MC0.1 mapeia seções da v0.4.4; 20 "Flores (2026)" restantes no MC viraram "este estudo" | monta_mc.py |
| GRO-02 | Modo de entrevista não corrige subdeclaração; "outra" em LGB+ | `seguro_pns2019.py`: Y008 ∈ {2, 3, 4} | Aceita em parte. Corpo define LGB+ com "outra orientação" e diz que 2,68 não corrige subdeclaração. Cenário extremo de realocação NÃO feito (análise nova; fica como limitação) | bloco-2, bloco-3a |
| GRO-03 | "Contraria lista inventada" largo demais | 50/160 com as duas confirmações | Aceita. 2.2 restringe aos 50 e diz que os demais ficam sem verificação | bloco-2 |
| GRO-04 | "Firme" com 5 vítimas | `agressor_risco_pns2019.md`: policial 66 e 5 | Aceita. "intervalo que exclui o zero... 5 vítimas LGB+" | bloco-3a |
| GRO-05 | Tabela 2 junta ajustes separados | 2,82; 2,65; 2,64; 2,68 | Aceita. Linha 6 lista os quatro ajustes separados | QUADRO-E2 (A25) |
| GRO-06 | "Melhor se ajustam" | `CENARIOS` fixos em `sim_identificabilidade.py` | Aceita. "taxa da violência fixada; a do registro é a que melhor se ajusta" | bloco-3a |
| GRO-07 | Goodman-Bacon como apoio | MC1: decomposição não se aplica literalmente | Aceita. Citado como limite do estimador | bloco-2 |
| GRO-08 | 7 diplomatas × 15 | MC8 e `H-RELATORIO.md`: 15 cassados, 7 por "prática de homossexualismo" | Aceita. Página da CNV não reaberta nesta rodada | bloco-3c (Tabela 5) |
| GRO-09 | Controle positivo empilha sexo e raça | MC4: 10,8 e 2,56; denominadores 2023–24 extrapolados | Aceita | bloco-3a |
| GRO-10 | Janela do ONS e aviso da expectativa de vida | MC4: março de 2021 a dezembro de 2023; "tendem a superestimar" | Aceita em parte. Janela e aviso no corpo; NÃO chamado de anual (o boletim de suicídio não foi reaberto) | bloco-3b |
| GRO-11 | 93,3% sem o que mede | MC4: vinculação Sinan–SIM no Rio | Aceita. Rafael et al. (2024) não reaberto | bloco-4 |
| GRO-12 | 258.011 como universo fechado; κ de fonte | MC9: até 5,1% da Câmara sem última página; Senado só 375; κ 0,66 (0,31 a 0,93) | Aceita | bloco-3c |
| GRO-13 | Introdução promete a busca de atos; resultado fora do corpo | decisão do autor de 2026-10-30: atos de governo vão para o MC7 | Refutação parcial. O resultado continua no MC7 (decisão do autor: atos noticiados não respondem à pergunta sobre crimes); a introdução deixa de prometer o exame no corpo | bloco-1 |

## Não feito nesta rodada (declarado)

- GRO-02: cenário quantitativo de subdeclaração.
- AST-09: teste automático de conservação do total de óbitos (a correção não muda as saídas publicadas).
- GRO-08, GRO-10, GRO-11: fontes primárias (CNV, boletim ONS 2025, Rafael et al. 2024) não reabertas; o texto segue o Material Complementar.
- Argon: aguarda cota do `agy` (~31/10 18:45) para ler manuscrito r6 + repositório.
