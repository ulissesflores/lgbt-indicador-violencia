Vou conferir a matriz contra o manuscrito revisado e os arquivos do repositório, sem alterar nada.Vou fechar três conferências que ainda decidem o status de células da matriz e, em seguida, escrever o parecer.## Verificação

25 linhas da matriz: 17 resolvidas, 7 resolvidas em parte, 1 refutação aceita. Nenhuma ficou não resolvida.

| ID | Status | Por quê |
|---|---|---|
| AST-01 | resolvida em parte | O §2.6 traz κ 0,91 e 0,46 e o §3.5 avisa que o Wilson mede só o sorteio. Em `research-2026-10-21-rodada3/F3-ggb/dados/kappa.json`, morte é 0,462 e LGBT+ é 0,912, ambos em 21 pares, não nos 23 casos; o corpo não diz isso. |
| AST-02 | resolvida | `dados/sinan/serie_campo55_uf_ano.py` exclui `LES_AUTOP == "1"`; `dados/sinan/resumo.md` dá 53,4% em 2015 e 44,1 / 42,5 / 44,5 em 2023–2025, com 2025 = 29,72 + 14,75. O corpo soma ignorado, branco e "não se aplica" nas fichas não autoprovocadas. |
| AST-03 | resolvida | `dados/painel/painel_c03_event_pesos.py` define a direção pelo sinal de Δ. A Tabela MC6.A10, em `paper/v05/MATERIAL-COMPLEMENTAR.md`, diz "deslocamento para a direita/esquerda". |
| AST-04 | resolvida | Corpo e Tabela 5 limitam as 38 mil a condenações de 1946 a 1991, não a pessoas, com cerca de metade por estupro ou menores. `dados/regimes/H-RELATORIO.md` traz a mesma leitura de Valodzin. |
| AST-05 | resolvida | O §3.4 dá o veredito sob a regra de periódico do primeiro quartil ("parcial") e sob a regra complementar, e diz que esta não é prospectiva. O MC1 confirma a data de 24/10. |
| AST-06 / GRO-01 | resolvida em parte | Resumo, abstract e §3.1 dizem 80% de poder só para aumento relativo de 60,7%. A linha 7 da Tabela 2 e a coluna de exibição de A15 ainda omitem o poder. `tests/test_correcoes_v03.py` trava 0,607 como aumento. |
| AST-07 | resolvida em parte | A célula de filho/enteado em `paper/v05/MATERIAL-COMPLEMENTAR.md` passou a "nenhum caso (intervalo não estimável)". A nota da mesma tabela ainda diz que os valores foram copiados sem alteração, e `dados/pns/seguro_pns2019.md` ainda tem 0,00% [0,00; 0,00]. |
| AST-08 | resolvida em parte | O §4.2 qualifica a FRA como pesquisa pela internet, sem amostra probabilística, sobre respondentes. O MC11 repete 13% a 14% sem dizer que a amostra não é probabilística. |
| AST-09 | resolvida | `dados/sim/padroniza_idade.py` soma a raça ignorada uma vez, a partir da raça conhecida. `dados/sim/asr_brasil.md` mantém os extremos 2,60 e 2,42. |
| AST-10 | resolvida em parte | A Tabela 6 diz "R$ de 2026" e a nota amarra os R$ 42 milhões ao contrato estrangeiro na PTAX de 20/10/2026, o que bate com `docs/laudos/F2-custos-README.md` e `custos-fontes.csv` (C29, C31G). A Tabela MC10.10 ainda intitula os três custos como "R$ de setembro de 2026". |
| AST-11 | resolvida | `dados/exposicao/fig_caminho_v05.py` rotula a linha como "GGB" e lê só a série do GGB. O PNG não foi aberto. |
| AST-12 | resolvida | A referência IBGE (2026) inclui a tabela 9606, e `dados/sim/padroniza_idade.py` usa `censo9606_n1_raca_sexo_idade_2010_2022.json`. |
| AST-13 | resolvida | O MC12 separa o selo da v0.4.4 do selo atual. Em `paper/v05/MATERIAL-COMPLEMENTAR.md` não há "Flores (2026)" nem "Tabela MC1.6". O corpo cita o depósito uma vez, na disponibilidade de dados. |
| GRO-02 | resolvida em parte | O §2.2 inclui "outra orientação" e o §3.1 diz que 2,68 não corrige quem deixou de se declarar. `dados/pns/seguro_pns2019.py` define LGB+ como Y008 em {2, 3, 4}. Resumo, abstract, introdução e linha 2 da Tabela 2 continuam só com "lésbicas, gays e bissexuais". O cenário quantitativo não foi feito. |
| GRO-03 | resolvida | O §2.2 e o §3.5 restringem a contradição da "lista inventada" aos 50 casos com morte violenta e vítima LGBT+; os outros 110 ficam sem verificação. |
| GRO-04 | resolvida em parte | O §3.1 diz que a fatia policial exclui o zero e se apoia em 5 vítimas LGB+. A seção 5 e a nota da Tabela 3 ainda chamam essa diferença de firme sem repetir o n. Em `dados/pns/agressor_risco_pns2019.md`, policial é 66 e 5. |
| GRO-05 | resolvida | A linha 6 da Tabela 2 lista 2,82, 2,65, 2,64 e 2,68 como ajustes separados. Os quatro batem com `dados/pns/agressor_risco_pns2019.md`. |
| GRO-06 | resolvida | O §3.2 fixa a taxa de violência em cada história e ajusta só a do registro (63,7%, 42,3% e 72,3% ao ano). |
| GRO-07 | resolvida | O §2.5 cita Goodman-Bacon como limite do estimador quando o efeito muda no tempo, e o MC6 diz que a decomposição não se aplica literalmente ao regressor contínuo. |
| GRO-08 | resolvida | A Tabela 5 traz 15 diplomatas cassados em 1969, 7 por "prática de homossexualismo". `dados/regimes/H-RELATORIO.md` tem a mesma frase. O PDF da CNV não foi reaberto. |
| GRO-09 | resolvida | O §3.3 separa 19,9 vezes (sexo e raça juntos), 10,8 (sexo) e 2,56 (raça) e avisa que 2023–2024 foram projetados do Censo de 2022. O MC4 traz os mesmos números. |
| GRO-10 | resolvida | O corpo dá o suicídio de março de 2021 a dezembro de 2023 e o aviso de que a expectativa de vida tende a superestimar. O MC4 concorda. O boletim primário da ONS não foi reaberto. |
| GRO-11 | resolvida | A seção 6 diz que 93,3% é acurácia da ligação probabilística Sinan–óbito no Rio e que isso não produz taxa de mortalidade LGBT+. O artigo de Rafael et al. (2024) não foi reaberto. |
| GRO-12 | resolvida | O §3.7 fala em 258.011 discursos baixados, remete as falhas de cobertura ao MC9 e publica κ = 0,66 (0,31 a 0,93), intervalo que inclui valores abaixo de 0,60. |
| GRO-13 | refutação aceita | A introdução não promete mais o exame das 60 buscas no corpo: diz que a busca mede atos noticiados, não crimes, e fica no MC7. "Atos estatais" no roteiro da seção 3 cabe na Tabela 5. |

# Parecer — Grok 4.7 (grok-4.7)

## Avaliação geral

A revisão r6 corrige os erros de rótulo e de inferência que a rodada anterior apontou. A razão 2,82, a não identificabilidade dos boletins, a auditoria dos 160 casos e a leitura não causal do homicídio por governo continuam de pé e conferem com os arquivos do repositório. O que sobra é propagação incompleta entre corpo, tabela e Material Complementar, mais um descompasso de contagem no roteiro. Recomendação: revisão menor.

## Críticas

### GRO-R2-01 — O roteiro anuncia três conclusões e a seção 6 enumera quatro

- Local: Introdução, parágrafo do roteiro; seção 6, primeiro parágrafo das conclusões.
- Trecho ou alegação: "A seção 6 traz as três conclusões" e "Quatro conclusões resumem o estudo."
- Problema: O roteiro promete três conclusões. A seção 6 numera quatro: violência relatada, mortes, motivo e crimes por governo. As "três mudanças" do parágrafo seguinte não são as conclusões.
- Evidência ou raciocínio verificável: `paper/v05/MANUSCRITO.md`, linha 31 e linha 385. O diff r5–r6 não alterou a frase do roteiro.
- Tipo: erro demonstrado
- Gravidade: menor
- Correção proposta: Trocar "três conclusões" por "quatro conclusões" no roteiro.
- Incerteza: Nenhuma sobre o descompasso. A frase é anterior a esta revisão e não estava na matriz.

## Pontos fortes

- Os quatro níveis impedem que prevalência, ajuste, agressor e motivo sejam lidos como a mesma pergunta.
- A reanálise da PNS reproduz as prevalências publicadas e usa razão de prevalências com o desenho amostral. O que foi feito depois de ver os dados está rotulado como exploratório.
- A Equação 1, com a taxa de violência fixada e só o registro ajustado, mostra por que a série de 783 a 3.481 boletins não separa violência de denúncia.
- A conferência do GGB recusa ao mesmo tempo "lista inventada" e "taxa nacional", e separa a incerteza do sorteio do erro de classificação.
- O homicídio por governo fica como descrição de período, com placebo em 2018 e causa indeterminada. A mortalidade fora do Brasil tem veredito explícito nas duas regras de elegibilidade.