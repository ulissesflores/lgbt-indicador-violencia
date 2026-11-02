# Matriz da rodada de pré-publicação pub1 (2026-10-31)

PDF auditado: `docs/paper/paper-final.pdf` (sha256 `5b17d4a5…de71a1`, 163 páginas). Pareceres: `astra.md` (GPT-6 Astra, 405 s),
`grok.md` (Grok 4.7, 1.043 s), `argon.md` (4 Argon pelo app, https://gemini.google.com/app/abfc7be101195042). Vereditos
unânimes na pergunta 3: **DOI só depois de corrigir os bloqueantes.** Cada item foi conferido no arquivo antes de entrar aqui.

## Procedentes (a corrigir antes da rc1)

| IDs | Achado | Conferência | Correção |
|---|---|---|---|
| AST-P02, GRO-P01, ARG-N05 | PDF diz "versão 1.0.0"; CITATION/codemeta/.zenodo/pyproject em 0.1.0, data 23/10, descrição parada na v0.3; `access_right: closed`; `check_release()` só aceita 0.x/closed | lido nos arquivos | bump 1.0.0 + data 31/10 + descrição da v0.5 nos 4 metadados; `access_right: open` só no commit da rc1 (com OK); auditor com modo final |
| AST-P04, GRO-P01, GRO-P02, ARG-P02, ARG-N02 | README/REPRODUCIBILITY/Tabela M1 apontam o artigo 0.4.4 (`paper/paper.md`, `paper/build/juiz/…`), "v0.5 em preparação", caminho `dados/lihs-checagem-ggb2016.META.md` inexistente, CHANGELOG cita PDF de 169 págs em `paper/build/v05/`; M1 sem `paper/v05/`, revisões r5–r8, C6–C11, F3–F4 | README l. 31, 264, 270, 271, 376; M1 l. 1267–1287 do MC | reescrever a face pública para a v0.5 (PDF em `docs/paper/`), Tabela M1 com caminhos e seções da v0.5, CHANGELOG sem o bullet superado |
| AST-P03 | `ruff check` = 12 erros (11 E501 + UP017) em `make_provenance.py` e `scripts/registra_run.py`; `ruff format --check` reprova `registra_run.py` | rodado: "Found 12 errors" | reformatar e quebrar linhas; reselar |
| GRO-P03 | o selo/run foi gravado sobre árvore suja do commit `0601c65` | manifesto `working_tree_dirty: true` | rc1 só sobre commit novo com `--verify` verde nesse commit (fluxo de publicação, com OK) |
| AST-P01, GRO-N01, ARG-P03 | Apêndice H: "sem instrumento normativo lido" x descrição da Portaria nº 1.576/2019 e liminar; "(Apêndice H)" dentro do próprio H; portaria fora das referências | a portaria FOI lida em 29/10 (REFERENCIAS-E4.md, tarefa 10: DOU 21/08/2019, seç. 1, p. 30) | conciliar: nas 60 consultas a fonte foi a imprensa; o instrumento foi lido depois e o texto é neutro; referência à portaria; tirar as autorremissões |
| AST-N04, ARG-P01 | "Os números dessas coortes estão no Apêndice E" — o Apêndice E não traz números de Saxby, Hsu e Clark | lido no MC | trocar por "Essas coortes são discutidas no Apêndice E" |
| AST-N01, GRO-N02, ARG-N02 | remissões herdadas que colidem com a numeração atual ("seção 3.2" = mortalidade antiga; "seção 3.1" para 3,01 milhões; "seção 3.13") | MC l. 38, 493, 607 etc. | trocar pelas seções/apêndices atuais onde houver colisão |
| ARG-N01 | o "39 denúncias" remete ao Apêndice D, que não o mostra | grep: 39 não está no D | acrescentar a frase no Apêndice D |
| ARG-N03, AST-N08 | saída bruta de script no Apêndice C ("Reprodução de seguro_pns2019.md…: divergências = 0", "(publicado: 2,82; …)", "AJUSTADA", "het"); "A reescrita deste texto (versão 0.5)" | lido | acabamento editorial |
| ARG-N04 (parte) | "nesse material" / "no mesmo material" no corpo; UNAMI & OHCHR com sigla no autor; (OSCE/ODIHR, 2025) x ODIHR | MANUSCRITO l. 282, 331 | "nesse apêndice"; nome por extenso; padronizar ODIHR |
| AST-N05 | p = 0,000 na Tabela G7 (CSV: 0,0002) | `c10_e2_resumo.csv` | "< 0,001" |
| AST-N06 | Clark, K. A. x Clark, K. D. sem iniciais nas citações | referências | iniciais na citação (APA 8.20) |
| AST-N03 | contrato estrangeiro (Gambling Survey for Great Britain, £4,5 mi) e câmbio PTAX sem referência | `custos-fontes.csv` C29 | duas referências e citação nas notas das Tabelas 6 e K1 |
| GRO-N05 | frase da TGEU sem referência | MC l. 724 | atribuir à fonte guardada ou citar a TGEU |
| AST-N07, GRO-N03 | "767 arquivos" no PAPER-SHA256; selo tem 768 | conferido | corrigir |
| AST-N02, GRO-N04, AST-N08, GRO-N06 | README da v0.5 promete mais do que o teste trava; README raiz com "42-44%" e "0,5%"; "Tabela MC5.C1" no README da v0.5 | lido | delimitar o alcance; números do PDF; "Tabela F4" |

## Não procedentes (conferidos no arquivo)

| ID | Alegação | Por que não procede |
|---|---|---|
| ARG-P04 | "(Apêndice )" sem letra na p. 46 | o PDF traz "(Apêndice B)" (pdftotext da p. 46); erro de leitura do anexo |
| ARG-N04 (parte) | "4,79 (2,58 8,90)" na Tabela 3 | a fonte e o PDF trazem "4,79 (2,58 a 8,90)" |
| ARG-N04 (parte) | URL da Lei 15.380 com "1" | a referência traz `lei/l15380` |
| ARG-N05 (parte) | `ADENDO-2.hora.txt` só com "3202" | o arquivo tem dois carimbos completos (2026-10-23T20:11:52Z e T20:16:17Z); o Argon não descomprimiu o .zip |
| ARG-P01 (parte) | QUADRO-E2.md "órfão", devia estar no Apêndice E | o QUADRO-E2 é a Tabela 2 do artigo; o achado procedente é só a frase das coortes |

## Aplicação (2026-10-31)

Tudo o que procede foi aplicado no texto r10 (`revisao/r10/MANUSCRITO.md`), nos apêndices (`monta_mc.acabamento_pub1`) e no
repositório (versão 1.0.0 nos quatro metadados; `access_right` segue `closed` até o aval do autor, e vira `open` no commit da rc1).
A leitura do PDF refeito achou ainda quatro autorremissões de apêndice ("o Apêndice B lista", "(Apêndice B)" no B, "do Apêndice C"
no C, "(Apêndice M)" no M), trocadas pela tabela certa, e o título embutido "Revisões anteriores e posteriores." passou a negrito.
GRO-P03 (commit novo antes da rc1) é passo do fluxo de publicação, com o OK do autor. PDF conferido: `docs/paper/paper-final.pdf`,
166 páginas; validador da casa 54/54; crivo 0/0; ruff e interrogate limpos; pytest 185; run_all 122/122; selo `170b0718…` (772).
