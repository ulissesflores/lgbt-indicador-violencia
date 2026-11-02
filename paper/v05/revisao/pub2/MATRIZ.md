# Matriz da conferência pub2 (2026-10-31)

PDF conferido pelos três: `docs/paper/paper-final.pdf` sha256 `0247ec1f…` (166 páginas). Vereditos: Astra "pronto com ressalvas /
com ressalvas / DOI depois do commit limpo"; Grok "não pronto (Tabela B2 e remissões) / com ressalvas / DOI depois";
Argon "pronto com ressalvas / com ressalvas / pode cunhar" (https://gemini.google.com/app/2d6c41b037819a0c).

| Achado (IDs desta rodada) | Conferência | Resposta |
|---|---|---|
| Tabela B2 com a numeração da v0.4.4 (AST-N01, GRO-P01, ARG-N02) | lido no MC | coluna "Onde está" com seção e apêndice atuais; nota aponta Apêndices L e K e seção 6 |
| "R = I × p (seção 2.5)"; "seção 3.9" na Tabela B4; controle positivo "seção 3.4"; M1 "busca de atos: seção 3.6" (os três) | lido | Equação 1, seção 2.3; Apêndice I; seção 3.3; seções 1 e 3.7 |
| README "Em resumo" com 0,5% e 42-44% (AST-N02, GRO-N01) | README l. 79 | 0,4% a 0,5% e 42,5% a 44,5% das fichas não autoprovocadas |
| CHANGELOG: caminho antigo da LiHS e "Versão segue 0.x" (GRO-N02) | lido | corrigidos |
| REPRODUCIBILITY: data de 23/10, "Matriz (v0.3)", `paper/build/` (GRO-N03) | lido | aponta `runs/` (31/10), título sem v0.3, linha do export com `docs/paper/` e `build_v05.sh` |
| QUADRO-E2.md ainda fala em MC7 e E5 (GRO-N04) | lido | nota no topo: forma publicada é a Tabela 2; MC7 = Apêndice H |
| OSCE antes da forma expandida (GRO-N05) | lido | expandida na primeira menção |
| "het" em C1, C2, C4, C6 (AST-N03) | grep | "heterossexuais" em todos |
| modo final do auditor não checava DOI (AST-N04) | código | `--stage final` exige DOI do Zenodo em CITATION, codemeta e README e acesso aberto (hoje falha, como deve) |
| run sobre árvore suja e commit 0601c65 (AST-P01, GRO-P02) | manifesto | passo do fluxo de publicação: commit novo, `--verify` e registro de execução nesse commit, com o OK do autor |

Leitura das páginas alteradas (um leitor): linha de subcabeçalho solta na Tabela C4 (exportador passa a prendê-la à linha seguinte) e
"(27)" ambíguo (agora "27 unidades da federação"); Tabela C2 "além da margem" não procede (imagem conferida); Nota da Tabela I1 no
topo da página seguinte e carimbos partidos da Tabela B3 seguem aceitos.

Estado final: PDF `d32216bf…` (166 páginas), crivo 0/0, validador da casa 54/54, ruff e interrogate limpos, pytest 185, run_all
122/122, auditor 3 OK e release coerente (1.0.0, sem DOI), selo `52d8e1b2…` (772), `runs/20261031T235935Z`.
