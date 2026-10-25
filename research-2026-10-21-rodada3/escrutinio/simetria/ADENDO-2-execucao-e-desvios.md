# ADENDO-2: o que mudou ou falhou durante a execução (CRITERIOS.md intacto; ADENDO-0 e ADENDO-1 aplicados)

Escrito depois de rodar tudo. Hora UTC em `ADENDO-2.hora.txt`.

## C18
- 60 consultas rodadas como no gabarito, com a ferramenta WebSearch (modo standard), 1 chamada cada; as 60 estão em `consultas_C18.tsv`. Desvio: NÃO registrei por consulta o n de URLs devolvidas (a ferramenta devolveu 9 a 10 por consulta); o registro por consulta é o texto exato. As 60 consultas saíram em 6 lotes de 10 na mesma tarde (data 2026-10-23, entre 16h e 18h, horário de Brasília).
- Regra de leitura do ADENDO-1 aplicada igual: 55 URLs selecionados (G1 8, G2 8, G3 10, G4 9, G5 10, G6 10; as vagas sem URL elegível não foram repostas). Baixados 54; úteis 51 (ilegíveis: G1_Q6, G2_Q8; texto de 67 caracteres: G4_Q9; 404: G1_Q3). Lista em `picks_C18.tsv`, `downloads_C18.tsv`.
- Na leitura, achado vale por evento; o mesmo evento visto em mais de uma página conta uma vez (E09 = E08). Eventos podem vir de páginas lidas para OUTRO governante (coluna `achado_na_leitura_de`): mantive por data de mandato.
- 4 consultas extras da fala de 25/04/2019 (as 4 permitidas) e 5 páginas baixadas em `fontes/.../fala-2019-04-25/`.
- Leitura posterior FORA do orçamento simétrico (item visto no resumo de busca, aberto depois): artigo de Junge (Rev. Antropologia USP 2008) sobre a piada de Pelotas de Lula, e Pereira (Sociologias 2020) sobre Dilma e "propaganda de opção sexual". Não entram na tabela; entram no texto como "secundário". Só vi no resumo o que a ferramenta devolveu; aberto depois: 2 itens, um por flanco, escolhidos por mim (viés de seleção declarado).
- Pelotas: o artigo lido data a piada de Lula na campanha municipal de 2000 (antes do mandato), contra "2006" em outro resumo; vale a data do artigo.

## C16
- Consultas executadas: as 10 do CRITERIOS (resultados lidos nos resumos da ferramenta). A rota que decidiu não estava nas consultas: índice de relatórios por país da CIDH (`pais.esp.htm` via Wayback), seguido da leitura integral, por varredura de texto "homosexual|UMAP", de 39 arquivos dos informes CIDH sobre Cuba de 1967, 1970, 1976, 1979 e 1983 (lista e sha256 em `SHA256SUMS-cuba.txt`). Os informes de 1962-63 não foram abertos.
- Vaga de leitura: usei La Jornada (Wayback), Tahbaz (udel), Ladrón de Guevara et al. (SciELO/UERJ, CC BY). Lumsden não é de acesso aberto: não gastou vaga.

## C27
- Modelo: `grok-4.7-build` (Grok pela assinatura, `grok -p --output-format json --json-schema ... --tools "" --disable-web-search --max-turns 1`), 30 lotes (24 + 6), nenhuma repetição, `total_cost_usd` de lista somado US$ 4,12 (preço de lista que o CLI imprime; assinatura, nada cobrado).
- Desvios: (1) a família entra no prompt (CRITERIOS §3); (2) o prompt congelado já tinha o campo `forma` omitido na linha de base, via `FORMAS["BASE"]`; (3) lote-teste de 1 lote (F1_00) rodado antes do lançamento completo e sobrescrito pelo lançamento; (4) lotes de 10 itens, não 1 item por chamada, por custo de contexto do CLI (34 mil tokens de entrada por chamada).
- Cego: o script do codificador nunca leu rótulo; o cruzamento só em `analise_C27.py`. Não vi nada item a item antes do cruzamento; vi só agregados (CRITERIOS §0).
- Linha de base: 219.562 discursos da Câmara (dedup), 4.905 excluídos pelo GATE, 68.052 elegíveis com estatística, 60 sorteados.

## Acréscimos após revisão do advisor (antes da entrega)
- Regra "primeiro URL ainda não selecionado" aplicada POR governante, não global: a mesma página entrou para mais de um governante (Aos Fatos/Temer em G3-Q6, G4-Q5 e G6-Q6; Christian Post 2008 em G1, G2 e G6; PrideSource 2010 em G1 e G6). Isso explica em parte G6 ter só 3 de 10 páginas publicadas no mandato. Leitura válida do CRITERIOS, declarada aqui.
- E24 (Gazeta do Povo, programa de campanha 2026) reclassificado de T3 para NA: programa de campanha não é suspensão, corte, extinção nem silêncio documentado. E23 permanece T3 fraco (opinião). Corrigidos `eventos_C18.csv`, `TABELA_C18.md`, `SIMETRIA.md`.
- Carta Capital sobre o orçamento LGBT de 2024 (record) apareceu no resumo da consulta G6-Q6 e NÃO foi lida (regra mecânica): visto, não lido, não soma.
- Portal da Transparência: tentado agora com curl (GET): HTTP 405, página "Human Verification" (AWS WAF); não abre sem navegador. Vai para `fila-chrome.jsonl`.
- Correio Braziliense/Estado de Minas (`fala-2019-04-25/em.txt`) não cita a Crusoé: usa Agência Estado e traz contexto maior da fala; os dois relatos são de jornalistas presentes ao mesmo café, não independentes.
