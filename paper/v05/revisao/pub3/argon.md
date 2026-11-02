# Parecer de pré-publicação — Gemini 4 Argon (gemini-4-argon-high)

Conversa: https://gemini.google.com/app/a9e25290fc4b9400 (2026-11-01; anexos argon.prompt.pub3.txt, paper-final.pdf sha 62150314…, repo-lgbt-indicador.zip). Texto copiado da página, sem os marcadores de citação de anexo.

## Conferência

| ID (rodada) | Status | Por quê (1 linha) | Evidência |
|---|---|---|---|
| AST-R2-02 (r6) | resolvida | As regressões foram refeitas sem os 9 adultos de cor ou raça ignorada (C009 = 9, n = 85.904), mostrando variação máxima de 0,02 nas razões ajustadas. | PDF, p. 84 (nota da Tabela C2) e p. 90 (seção 8 do Apêndice C e Tabela C12); dados/pns/agressor_risco_pns2019.py, dados/pns/agressor_risco_pns2019.md. |
| ARG-02 (r6) | resolvida | O ajuste pela presença de cônjuge ou companheiro no domicílio (C01001) foi incluído na razão de risco por tipo de agressor e relatado no corpo e no Apêndice C. | PDF, p. 19 (seção 3.1) e p. 88 (Tabela C10: familiar 4,31; parceiro 2,42; desconhecido 1,91; amigo/colega/vizinho 1,85); dados/pns/agressor_risco_pns2019.py. |
| ARG-01 (r6) | resolvida | A capacidade dos três desenhos foi recalculada segundo a fração LGB+ de cada modo de preenchimento sobre todos os adultos do modo (1,35% com entrevistador e 3,26% com autopreenchimento). | PDF, p. 49 (nota da Tabela 6) e pp. 162–163 (Apêndice K, Tabela K2); research-2026-10-21-rodada3/F2-custos/opcoes_por_modo.csv. |
| AST-01 (r5) | resolvida em parte | Os 6 desacordos foram adjudicados por um terceiro codificador (GPT-6 Astra) e as contagens foram atualizadas de 73 para 74 no artigo e no Apêndice F, mas a seção 2.6 (p. 12) manteve a frase dizendo que o efeito não foi estimado. | PDF, pp. 8, 14, 31–32, 109–111 e 120 (atualizados para 74) vs. p. 12 (seção 2.6, frase residual contraditória); research-2026-10-21-rodada3/F3-ggb/dados/adjudicacao.json e scripts/s15_terceiro_codificador.py. |
| GRO-02 (r5) | não procedência aceita | A decisão metodológica de não simular cenários arbitrários de subdeclaração da orientação sexual está declarada de forma transparente como limite nas seções 3.1 e 5. | PDF, p. 21 (seção 3.1) e p. 45 (seção 5). |
| Diagramação | resolvida | Os carimbos da Tabela B3, os intervalos (x a y) sem sinal nas tabelas principais, o alinhamento à esquerda dos hashes longos e a paginação da nota da Tabela I1 foram corrigidos no PDF. | PDF, p. 20 (Tabela 3), p. 75 (Tabela B3), p. 121 (nota da Tabela F4), p. 154 (Tabela I1) e p. 166 (Apêndice M); paper/tools/export_v04.py. |
| Processo | resolvida | O arquivo de registro de modelos, tokens, tempo e fontes foi criado no repositório e referenciado na Tabela M1 do Apêndice M. | PDF, p. 169 (Tabela M1); docs/processo-e-custo.md. |

## Vereditos

| Pergunta | Veredito | Por quê (1 linha) |
|---|---|---|
| 1. PDF pronto | pronto com ressalvas | Todos os números, tabelas, figuras e referências APA 7 estão íntegros, exceto uma frase residual na seção 2.6 (p. 12) que contradiz a adjudicação feita em AST-01 (ARG-P01). |
| 2. Repositório atualizado | com ressalvas | Todos os caminhos novos listados na matriz e na Tabela M1 existem na árvore do .zip (incluindo runs/20261101T234846Z/), mas paper/v05/MANUSCRITO.md carrega a frase residual de ARG-P01 (conteúdo interno dos fluxos deflate não reproduzidos no PDF: não verificado). |
| 3. DOI | pode depois de corrigir os bloqueantes | Basta corrigir a frase residual da seção 2.6 (ARG-P01), regerar paper-final.pdf e atualizar paper/PAPER-SHA256.txt antes de disparar a release v1.0.0-rc1. |

## Bloqueantes

**ARG-P01 — Contradição interna na seção 2.6 sobre a estimativa do efeito dos desacordos na amostra do GGB (regressão parcial de AST-01)**

- Local: PDF, página 12 (seção 2.6); paper/v05/MANUSCRITO.md.
- Trecho literal curto: "A concordância foi alta para a condição LGBT+ da vítima (κ = 0,91) e moderada para a confirmação de morte violenta (κ = 0,46; Apêndice F). O efeito dos desacordos sobre as contagens não foi estimado."
- Problema: para atender a AST-01 (r5), os 6 casos com desacordo foram submetidos a um terceiro codificador cego de outra família (GPT-6 Astra), com regra de maioria (2 de 3) conferida pelo autor, e o efeito exato foi determinado (só o caso 159 mudou; 73 -> 74; 35 -> 36; 23 -> 24; 50 de 160 inalterados). Esses números foram propagados para a seção 2.2 (p. 8), Tabela 2 (p. 14), seção 3.5 (pp. 31–32), Figura 7 (p. 32), Apêndice F (pp. 109–110), Figura F1 (p. 111) e nota da Tabela F3 (p. 120). Contudo, na seção 2.6 (p. 12) permaneceu a frase antiga, além de a frase anterior mencionar apenas um segundo codificador.
- Evidência verificável: confronto entre a p. 12 ("O efeito dos desacordos sobre as contagens não foi estimado.") e a nota da Tabela F3 na p. 120.
- Correção proposta: substituir por "Nos 6 casos com desacordo, um terceiro codificador de outra família desempatou as leituras: as mortes violentas confirmadas passaram de 73 para 74, e os 50 casos verificáveis não mudaram (Apêndice F)." Regerar DOCX/PDF e atualizar paper/PAPER-SHA256.txt.

## Não bloqueantes

**ARG-N01 — Numeração das colunas e observação sobre o tamanho amostral no texto introdutório da Tabela C10**

- Local: PDF, p. 88; dados/pns/agressor_risco_pns2019.py/.md; paper/v05/MATERIAL-COMPLEMENTAR.md.
- Trecho: "Mesmo ajuste do 2,82; segunda coluna com estado civil; terceira com cônjuge ou companheiro(a) no domicílio (a coluna n é a do ajuste sem extras; o ajuste com cônjuge usa quem respondeu C01001)."
- Problema: com "Bruta" como primeira coluna numérica, estado civil e cônjuge são a terceira e a quarta colunas de estimativas; e a ressalva sugere n menor que 85.913, mas a seção 7 (p. 89) mostra 84.359 + 1.554 = 85.913 respondentes de C01001.
- Correção proposta: "Primeira coluna ajustada com o mesmo perfil do 2,82; segunda ajustada com estado civil; terceira ajustada com cônjuge ou companheiro(a) no domicílio (n = 85.913 em todas)."

**ARG-N02 — Menção residual a 1,35% como número apenas "da versão 0.4.4" no Apêndice F**

- Local: PDF, p. 116; paper/v05/MATERIAL-COMPLEMENTAR.md.
- Trecho: "e com 1,35%, o menor valor de prevalência associado ao modo de preenchimento na conta da versão 0.4.4 (o artigo usa 1,38%, com denominador só de quem declarou orientação heterossexual ou LGB+)"
- Problema: o artigo passou a usar e explicar 1,35% (todos os adultos do modo) ao lado de 1,38%; a frase ficou defasada.
- Correção proposta: "e com 1,35%, a fração LGB+ entre todos os adultos entrevistados por outra pessoa (Tabela 6 e Tabela K2; 1,38% entre quem declarou orientação, seção 3.1)".

**ARG-N03 — Quebra de linha em intervalos [x; y] ou com sinal em tabelas de apêndice**

- Local: PDF, pp. 83 (C1), 86 (C6), 107 (E3), 135–136 (G3), 137–138 (G5), 138–140 (G6); paper/tools/export_v04.py.
- Trecho: "14,70% [10,72; / 18,67]"; "+11,9 (-4,0 a / +27,8)"; "27,9 [27,6; / 28,1]".
- Correção proposta: ampliar a expressão regular de espaços não separáveis para [x; y] e intervalos com sinal.

(Nota da auditoria sobre a Pergunta 2: a árvore do .zip foi inspecionada, com scripts, dados, tests/test_numeros_v05.py, runs/20261101T234846Z/manifest.json e docs/processo-e-custo.md presentes; o conteúdo dos fluxos comprimidos que não está espelhado no PDF fica como não verificado.)

## O que está bom

- As quatro análises pedidas (AST-R2-02, ARG-02, ARG-01 e AST-01) foram executadas e incorporadas com tabelas dedicadas (C10, C12, K2 e nota da Tabela F3).
- Propagação consistente da adjudicação do GGB (74; 84,1%; 36; 24) na seção 2.2, Tabela 2, seção 3.5, Figura 7, Apêndice F, Figura F1 e nota da Tabela F3.
- APA 7 e mapeamento dos apêndices sem vestígio da numeração MC1–MC12.
- Acabamento tipográfico: Tabela B3, notas coladas às tabelas (I1), hashes à esquerda.
- Tabela M1 mapeia os artefatos novos.
