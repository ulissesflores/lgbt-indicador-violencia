# Matriz de respostas da rodada r8 (verificação dos três)

Manuscrito verificado: `revisao/r8/MANUSCRITO.md` (sha256 `5ad6537a…`). Corrigido: `revisao/r9/MANUSCRITO.md` (sha256 `b69cf8f8…`). Recomendações: Argon, **aceitar sem novas exigências**; Grok, revisão menor, sem crítica nova; Astra, revisão menor, uma crítica nova. Trava 0 falhas nos 6 blocos; quadro 0 divergências.

| ID | O que faltava ou crítica | Conferência | Resposta | Onde |
|---|---|---|---|---|
| AST-R2-01 / ARG-R2-01 | imagem da Figura MC6.20 ("troca de controle um ano antes"); coluna "placebo" da Tabela MC6.A13; justificativa de A10 | `make_figures.py` figura 20; quadro A10 | Figura 20 regenerada ("quebra um ano antes"; "quebra em 2018: queda de 21,8%; depende da data"); textos fora da imagem atualizados em `textos_fora_da_imagem.json`; coluna e células da Tabela MC6.A13; A10 cita a queda de 2017 para 2018 e o teste como dependência da data | repo `paper/figures/`, monta_mc.py, QUADRO-E2 |
| AST-R2-07 | seção 2.2 e justificativa de A7 | — | "A busca só achou comparações de mortes noticiadas de pessoas trans, sem cobertura comum entre países" nos dois lugares | bloco-2, QUADRO-E2 |
| ARG-R2-04 | seções 4.3 e 6 sem a exceção de amigo, colega ou vizinho | razão com estado civil 1,87 (0,90 a 3,89) | "também com o estado civil"; "Para amigo, colega ou vizinho, ele só aparece sem o estado civil" nas seções 4.1, 4.3 e 6 | bloco-4 |
| AST-01 | seção 2.6 sem dizer que o efeito dos desacordos não foi estimado | — | frase acrescentada | bloco-2 |
| AST-R2-11 | extremos estaduais do Sinan em outro denominador (DF 61% com autoprovocadas) | `serie_campo55_uf_ano.csv` 2023: RR 203/1.847 = 11,0%; MS 5.275/9.741 = 54,2% | "Nas mesmas fichas, ... de 11,0% em Roraima a 54,2% em Mato Grosso do Sul" | monta_mc.py |

Pendências declaradas que seguem como limite (análise nova não feita): AST-01 (efeito dos desacordos), GRO-02 (subdeclaração), AST-R2-02 (raça ignorada), ARG-01 (Tabela 6 por modo), ARG-02 (coabitação por agressor). Os três revisores as tratam como limite declarado, não como erro.
