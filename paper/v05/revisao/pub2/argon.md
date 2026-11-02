<!-- Transcrito de https://gemini.google.com/app/2d6c41b037819a0c (4 Argon, Thinking High), 2026-10-31, por get_page_text.
Pedido: arquivo anexo argon.prompt.pub2.txt (= argon.prompt.navegador.txt), com paper-final.pdf e o .zip do repositório.
Conferência abreviada aqui nas linhas "resolvida" (o porquê de cada uma está no app); vereditos e achados na íntegra. -->

# Parecer de pré-publicação (conferência) — Gemini 4 Argon (gemini-4-argon-high)

## Conferência (resumo fiel)
- Resolvidas: AST-P01, AST-P02, AST-P03, AST-P04, AST-N02 a AST-N08, GRO-P01, GRO-P02, GRO-N01, GRO-N03 a GRO-N06, ARG-P01, ARG-P02, ARG-P03, ARG-N01, ARG-N03, ARG-N04 (texto/autor/ODIHR), ARG-N05.
- Resolvidas em parte: AST-N01 (p. 102 trocou para "seção 3.4" em vez de "3.3"; restam p. 76 "seção 3.9" e p. 93 "seção 2.5"); GRO-P03 (falta commitar a árvore limpa antes da rc1); GRO-N02 (pp. 76, 93 e 102); ARG-N02 (M1: busca simétrica aponta seção 3.6 em vez de 3.7; pp. 76, 93 e 102).
- Não procedência aceita: ARG-P01 (parte: QUADRO-E2 é a fonte da Tabela 2), ARG-P04, ARG-N04 (Tabela 3 e Lei 15.380: erros de OCR), ARG-N05 (ADENDO-2: bloco deflate não descomprimido).
- Nota: o conteúdo interno dos arquivos comprimidos do .zip ficou "não verificado diretamente" (deflate).

## Vereditos
| Pergunta | Veredito | Por quê (1 linha) |
|---|---|---|
| 1. PDF pronto | pronto com ressalvas | Zero bloqueantes: todas as falhas graves da pub1 foram sanadas e as referências APA 7 fecham com o texto, restando três pequenos deslizes de remissão interna nos apêndices (pp. 76/93, 102 e 165). |
| 2. Repositório atualizado | com ressalvas | A árvore do .zip contém todos os arquivos da v0.5 e o novo run 20261031T233520Z, mas o conteúdo comprimido fica não verificado e resta virar access_right: open em árvore limpa no commit da rc1. |
| 3. DOI | pode cunhar | Não há bloqueantes científicos, editoriais ou de integridade no PDF; cumprido o passo operacional de abrir access_right e selar o commit limpo da v1.0.0-rc1, o DOI pode ser cunhado. |

## Bloqueantes
Nenhum bloqueante identificado nesta rodada.

## Não bloqueantes
- ARG-N01 — p. 102 (Apêndice E): "controle positivo do argumento da seção 3.4 do artigo" deveria ser seção 3.3 (Mortes no Brasil, pp. 26–27).
- ARG-N02 — p. 93 (Apêndice D): "R = I × p (seção 2.5)" deveria ser seção 2.3; p. 76 (Tabela B4): "ressalvas do informe registradas na seção 3.9" deveria ser Apêndice I; p. 72 (Tabela B2): coluna "Seção" e Nota com as seções 3.1 a 3.13 da v0.4.4 sem aviso.
- ARG-N03 — p. 165 (Tabela M1): "Busca simétrica de atos de governo | seção 3.6" deveria ser seção 3.7 (abre a seção 3.7, p. 37).

## O que está bom
- Referências em APA 7 fecham com o texto, com desambiguação dos Clark, nomes corporativos por extenso e as fontes novas (Banco Central do Brasil, Gambling Commission, Ministério da Cidadania, "Big Data, 331 Deaths").
- Apêndice H conciliado com honestidade metodológica.
- Acabamento editorial limpo no corpo e no Apêndice C.
- Coerência numérica entre Resumo, Abstract, corpo, tabelas e figuras nas 166 páginas.
- Tabela M1 com rastreabilidade de cada seção, figura e tabela aos arquivos do repositório.
