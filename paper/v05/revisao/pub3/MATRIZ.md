# Matriz da rodada de pré-publicação pub3 (2026-11-01)

PDF auditado: `docs/paper/paper-final.pdf` (sha256 `62150314…`, 169 páginas), depois das quatro análises que o autor decidiu fazer
antes do DOI (entrada da rodada: `revisao/pub2-para-pub3.md`). Pareceres: `astra.md` (GPT-6 Astra, 349 s), `grok.md` (Grok 4.7,
635 s), `argon.md` (4 Argon pelo app, https://gemini.google.com/app/a9e25290fc4b9400). Vereditos na pergunta 3: os três, "DOI
depois de corrigir os bloqueantes". Pergunta 1: Astra e Argon "pronto com ressalvas", Grok "não pronto", os três pelo mesmo motivo.

## Conferência das análises (os três revisores)

| ID | Astra | Grok | Argon |
|---|---|---|---|
| AST-R2-02 (cor ou raça ignorada) | resolvida | resolvida | resolvida |
| ARG-02 (cônjuge por tipo de agressor) | resolvida | resolvida | resolvida |
| ARG-01 (Tabela 6 por modo) | resolvida | resolvida | resolvida |
| AST-01 (desacordos do GGB) | resolvida em parte (frase da seção 2.6) | resolvida em parte (idem) | resolvida em parte (idem) |
| GRO-02 (subdeclaração) | limite declarado, aceito | limite declarado, aceito | não procedência aceita |

## Procedentes (aplicados)

| IDs | Achado | Conferência | Correção |
|---|---|---|---|
| ARG-P01, AST-N01, GRO-P01 | seção 2.6 ainda dizia "O efeito dos desacordos sobre as contagens não foi estimado" | lido em `docs/blocos/bloco-2.md` (eu tinha procurado "desacordo" e deixei passar) | frase trocada pelo resultado (um caso; 73 -> 74; 50 de 160 iguais); teste de prosa novo em `tests/test_numeros_v05.py` |
| ARG-N01 | texto da Tabela C10 numerava as colunas errado e sugeria n menor no ajuste com cônjuge | n igual nas três colunas (assert novo no script) | "Colunas ajustadas: a primeira… a segunda… a terceira… O n é o mesmo nas três." |
| ARG-N02 | Apêndice F chamava 1,35% de "conta da versão 0.4.4" | o artigo agora usa 1,35% (Tabela 6, K2) | "a fração LGB+ entre todos os adultos entrevistados por outra pessoa (Tabelas 6 e K2; 1,38% entre quem declarou orientação…)" |
| ARG-N03 e leitura visual | intervalos partidos em tabelas com sinal, %, p.p. e colchete | 4 leitores (`LEITURA-VISUAL.md`) | regra do exportador ampliada; parágrafo com caminho longo à esquerda |
| AST-N02 | nota da K2 não explicava a linha do painel com entrevistador do CSV | conferido | nota explica o cenário de referência e a linha hipotética não usada |
| AST-N03 | metadados e `docs/processo-e-custo.md` prometiam SHA-256 de toda fonte | 554 de 1.139 têm hash | "data de acesso de cada fonte e, quando houve arquivo salvo, o SHA-256" (CITATION, codemeta, .zenodo, processo) |
| AST-N04 | REPRODUCIBILITY com data e número de passos antigos e sem as análises novas | 29 passos; run de 01/11 | data, 29 passos e parágrafo sobre como as análises novas são conferidas |
| GRO-N01 | laudo `docs/laudos/F3-ggb-README.md` com o funil antigo | lido | nota datada no topo com os números vigentes; laudo mantido como escrito |
| GRO-N02 | CHANGELOG com caminho curto do adjudicacao.json | conferido | caminho completo |
| GRO-N03 (parte) | URL Wayback da CNV sem carimbo de 14 dígitos (`2016id_`) | a API do Wayback redireciona a 20181011151123; o arquivo baixado tem o mesmo SHA-256 do manifesto (`3d0527a3…`) | carimbo completo na referência |
| GRO-N04 | capa com 31/10; resultados de 01/11 | conferido | capa, CITATION e codemeta em 2026-11-01 |

## Não procedentes

| ID | Alegação | Por que não procede |
|---|---|---|
| GRO-N03 (parte) | `%5EM%5EJ` no nome do release do GGB seria CR/LF | `%5E` é "^": o nome do arquivo no servidor tem "^M^J" literal; a URL baixou o arquivo (manifesto: SHA-256 `6e22ad45…`) |

## Fica para o fluxo de publicação (OK do autor)

| ID | Achado | Encaminhamento |
|---|---|---|
| AST-P01 | o selo atual é de árvore suja sobre o commit `0601c65`; falta o commit completo que receberá a rc1 | commit e push com OK do autor; depois `--verify` e `registra_run` no commit; `access_right: open` no commit da rc1 |
