# PRÉ-REGISTRO D100 — o que o Disque 100 (denúncias ao MDHC) permite dizer sobre violência contra pessoas LGBT, 2011-2026

Gravado em 2026-10-24 (hora UTC exata e sha256 no arquivo irmão `PREREGISTRO-D100.sha256`, gerado logo após esta gravação e ANTES de qualquer script que conte linhas por categoria LGBT). O selo cobre o corpo deste arquivo (até a linha `**ADENDOS**`) e `scripts/d100_comum.py` (as regras de classificação); `scripts/d100_tabular.py` e `scripts/d100_series.py` têm o hash anotado como informação (correção de código depois do selo vira adendo). Erro, desvio ou regra nova entra só na seção final **ADENDOS** (datada), nunca por edição do corpo. Pasta: `/Users/ulissesflores/m4/pesquisas/lgbt-indicador-violencia/research-2026-10-24-disque100/`. Python: `/opt/homebrew/bin/python3.14 -I`. Pedido: `research-2026-10-24-v03/V03-BRIEFING.md`, FRENTE D. Modelo de forma: `research-2026-10-24-presidencia/PREREGISTRO-C09.md`.

Natureza do estudo: DESCRITIVO. Nenhuma hipótese causal, nenhum teste de efeito. O que se mede é o que o canal registrou, não a violência que aconteceu.

## 0. O que já tinha visto ANTES de gravar (honestidade do "declarado antes")

- Relatório da frente L (`research-2026-10-24-v03/L-RELATORIO.md`, item L3): acesso sem cadastro; 3 formatos; 2011 com 99.949 linhas; em amostras de cerca de 3 mil linhas de 2023-2026 o `hash` se repete até 33 vezes; pessoas trans aparecem na coluna de orientação em C; a coluna de identidade de A mistura orientação.
- Balanço oficial LGBT 2011-2019 (`research-2026-10-24-v03/L-fontes/disque100/balanco-lgbt-perfil-das-vitimas-uf.csv`): vi a estrutura (tabelas "Perfil das Vítimas" por ano x UF, coluna `NA`, linha `Total`) e, no despejo da estrutura, os totais de 2011 (1.206 vítimas) e parte de 2012. Unidade declarada: vítima. Não calculei nada com ele.
- Estrutura dos microdados (`scripts/d100_estrutura.py`, saídas em `saidas/estrutura/*.json`): para cada arquivo, RÓTULOS distintos (sem frequência) das colunas categóricas, linhas lidas, intervalo de datas e o diagnóstico de unidade. Nenhuma contagem por categoria (LGBT ou outra) foi produzida ou vista. Linhas lidas (todas as categorias juntas, sem recorte): 2011 99.949; 2012 399.383; 2013 425.993; 2014 311.538; 2015 285.660; 2016 266.415; 2017 307.521; 2018 293.878; 2019 325.540; 2020S1 137.681; 2020S2 270.245; 2021S1 450.418; 2021S2 482.197; 2022S1 733.051; 2022S2 938.168; 2023S1 1.372.510; 2023S2 1.483.990. Hashes distintos em C: 106.875 (2020S2) a 227.288 (2023S2); 2,5 a 6,7 linhas por hash. Rótulos de todos os 17 arquivos completos vistos e classificados em `saidas/dicionario_rotulos.csv` antes do selo (ex.: em C, de 2020S2 a 2022S1 a orientação só traz ASSEXUAL/BISSEXUAL/HOMOSSEXUAL/PANSEXUAL/OUTRO/N/D, sem rótulo trans nem hétero; desde 2022S2 aparecem HOMOSSEXUAL.GAY/LÉSBICA, PESSOA TRANS.*, NÃO, NÃO INFORMADO; o grupo varia dentro do hash em 0-0,1% das chaves repetidas até 2022S1 e em 14-18% a partir de 2022S2; em 2022S2 há rótulo de `Motivação` com várias motivações unidas por vírgula).
- Diagnóstico de unidade já visto: A (2011-2016) sem chave; o substituto `data_atendimento` (carimbo de data-hora) agrupa 2,2-2,5 linhas por carimbo, e dentro do carimbo repetido o perfil da vítima varia em 49-56% e o do suspeito em ~70%: a linha de A parece ser vítima x suspeito de um atendimento, mas o carimbo NÃO é chave pública. B (2020S1): `hash_par_vitima_suspeito` com 1,006 linha por chave (0,57% das chaves repetem). C (amostras de 2 MiB de 2023S2, 2024S1, 2026T3): `hash` com 4,9-6,9 linhas por chave; dentro do hash a violação varia em 99% das chaves repetidas, o perfil da vítima em <1%, e o grupo vulnerável em 13-23%; `sl_quantidade_vitimas` constante dentro do hash; perfis de vítima distintos <= quantidade declarada em 99,6%.
- Nada da comparação com Sinan e Anuário foi calculado com dados do Disque 100. Os números de Sinan e Anuário do projeto (`dados/sinan/serie_campo55_uf_ano.csv`, `dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv`) e a concordância Sinan x Anuário (`dados/concordancia/concordancia_v2.md`) já eram conhecidos.

- **Escopo deste selo (PARCIAL, por ordem do coordenador em 2026-10-24: entrega em até 60 min):** só os 17 arquivos completos no momento do selo, 2011 a 2023S2. Faltam 2024S1, 2024S2, 2025S1, 2025S2, 2026S1 e 2026T3 (download em curso, ~1,2 MB/s). Eles entram depois, por ADENDO datado, com as MESMAS regras deste corpo (nada é reespecificado). Até lá: 2023 é o último ano completo da série, 2024-2026 são AUSENTES (não zero), e a comparação com o Anuário (2022-2025) só tem 2022 e 2023.

## 1. Perguntas (descritivas)

- **P1 (catálogo):** quais arquivos existem, com URL, tamanho, data de acesso e sha256.
- **P2 (dicionário):** como cada formato registra grupo, sexo/gênero, orientação, identidade, motivação, violação e UF; o que é comparável entre formatos e o que não é.
- **P3 (unidade):** o que é uma linha em cada formato; quando dá para contar denúncias; se dá para contar vítimas únicas.
- **P4 (série):** quanto o canal registrou no grupo LGBT, com SOGI LGBT declarada da vítima e com motivação por orientação/identidade, por período, com as quebras marcadas.
- **P5 (composição):** dentro do grupo LGBT, distribuição por UF, sexo/gênero da vítima e do suspeito, SOGI da vítima e tipo (macro) de violação.
- **P6 (comparação):** como a distribuição por UF do Disque 100 se relaciona com Sinan (notificações de saúde com motivação LGBTfobia) e Anuário (BO de racismo por homofobia/transfobia), sem somar e sem taxa.

## 2. Dados (todos públicos, sem cadastro, sem aceite de termos, sem cookie persistido)

- 23 arquivos CSV de microdados listados em `scripts/urls.tsv` (URL, tamanho anunciado e Last-Modified medidos em 2026-10-24 por requisição Range, sem login), baixados por `scripts/baixar.py` para `raw/` (ignorado pelo git). sha256 de cada arquivo inteiro em `saidas/catalogo.tsv` (`scripts/d100_catalogo.py`). Arquivo que não completar o download sai da tabulação e aparece como "parcial, sem sha"; o período fica AUSENTE na série (nunca zero).
- Formatos (detectados pelo cabeçalho): **A** 2011-2019 (35 colunas, sem chave); **B** 1º semestre de 2020 (34 colunas, chave `hash_par_vitima_suspeito`); **C** 2º semestre de 2020 a 3º trimestre de 2026 (62 colunas, chave `hash`, 5 grafias de cabeçalho com o mesmo conteúdo por posição; nome canônico = cabeçalho de 2022S2).
- Porta de entrada para A: balanço LGBT 2011-2019 (acima).
- Comparação: `dados/sinan/serie_campo55_uf_ano.csv` (coluna `m_lgbtfobia`, 2015-2025); `dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv` (2022-2025, edição mais recente por ano, mesma regra `EDICAO_NOVA` de `dados/concordancia/concordancia_v2.py`; `...` e `-` = NA); população: Censo 2022 (`fontes/p2-f8-dados-uf/tabnet/raw/sidra_9514.json`).

## 3. Unidades de contagem (fixas)

| formato | unidade principal | outras unidades reportadas | vítima única? |
|---|---|---|---|
| A | **linha** (registro; parece vítima x suspeito de um atendimento, sem chave pública) | itens de violação (a coluna `violacoes` é multivalorada, `;` dentro do campo) | NÃO calculável |
| B | **par vítima-suspeito** (`hash_par_vitima_suspeito` distinto) | linhas; itens de violação | NÃO calculável |
| C | **denúncia** (`hash` distinto no arquivo) | linhas (violação x vítima x suspeito, uma violação por linha); vítimas DECLARADAS = soma, sobre as denúncias, do máximo de `sl_quantidade_vitimas` no hash (não é pessoa única: a mesma pessoa pode estar em várias denúncias) | NÃO calculável |

- "Pessoa única" não é dita em nenhum formato: não há chave pública de pessoa.
- C, denúncia do recorte R: hash com **pelo menos uma** linha em R (primária); sensibilidade para o grupo LGBT: hash com **todas** as linhas no grupo LGBT (`denuncias_todas_as_linhas`).
- UF da denúncia em C: valor de `UF` na primeira linha do hash (canal) ou na primeira linha do hash que está no grupo LGBT (recorte grupo LGBT); denúncias com `UF` variando dentro do hash são contadas e reportadas em `saidas/d100_qualidade.csv`.

## 4. Recortes LGBT (três dimensões, nunca fundidas; regras exatas em `scripts/d100_comum.py`)

- **I1 grupo/módulo LGBT** (o único quase comparável 2011-2026): A `grupo_violacao` contém "LGBT"; B e C `Grupo_vulnerável` contém "LGBT". É a classificação da denúncia pelo atendimento, não a identidade declarada da vítima.
- **I2 SOGI LGBT declarada da vítima** (`sogi_vitima`; classes por formato, NÃO harmonizadas): A = orientação `Homossexual`/`Bissexual` ou identidade `Gay`/`Lésbica`/`Bissexual` (lgb) ou `Travesti`/`Transexual` (trans); B = coluna `orientacao_sexual` (sujeito não documentado; não tem valor "heterossexual": `NULL` funde hétero e não informado) com GAY/LÉSBICA/HOMOSSEXUAL/BISSEXUAL (lgb) ou TRANSEXUAL/TRAVESTI (trans), ou `Gênero_da_vítima` = `LGBTQIA+` (lgbt_genero); C = `Orientação_sexual_da_vítima` com HOMOSSEXUAL.*/BISSEXUAL/PANSEXUAL/ASSEXUAL (lgb), PESSOA TRANS.* / TRAVESTI / NÃO BINÁRI* (trans, também se vier em `Gênero_da_vítima`), INTERSEXO (intersexo). Classes não LGBT: `nao_lgbt` (hétero declarado), `nao_rotulo_nao` (C: rótulo literal "NÃO", sentido não documentado: NÃO é lido como hétero), `cis_ou_indef` (A: identidade Feminina/Masculina), e as faltantes. "LGBT declarado" = trans, lgb, intersexo ou lgbt_genero.
- **I3a motivação por orientação/identidade**: B (item de `motivacoes`) e C (`Motivação`) cujo rótulo casa `ORIENTAÇÃO SEXUAL | IDENTIDADE DE GÊNERO | IDEOLOGIA DE GÊNERO | LGBT | HOMOFOB | TRANSFOB | LESBOFOB | BIFOB`. A não tem motivação: I3a = n/d em A.
- **I3b violação que nomeia SOGI**: rótulo de violação que casa a mesma expressão (ex.: A "DISCRIMINAÇÃO.POR ORIENTAÇÃO SEXUAL", "VIOLÊNCIA INSTITUCIONAL.HOMOFOBIA INSTITUCIONAL"). Não é o mesmo conceito de I3a; reportado só como composição.
- Interseções reportadas em tabela: por linha, (I1, classe I2, I3a); por denúncia em C, (I1, I2 LGBT, I3a).

## 5. Períodos, quebras e parciais

- Período = rótulo do arquivo publicado (ano em A; semestre em B/C; 3º trimestre de 2026). Datas fora do intervalo do rótulo são contadas (`linhas_data_fora_do_periodo`) e NÃO realocadas.
- Ano = soma dos períodos do ano. 2020 = B (S1) + C (S2): marcado `quebra_de_formato_no_ano`, unidade "misto" na série por UF. 2026 = S1 + T3 (janeiro a setembro): marcado `parcial_jan_set`; nunca comparado com ano cheio sem a marca.
- Quebras de série marcadas: A->B (2020S1), B->C (2020S2); dentro de C, qualquer período em que um rótulo de grupo, orientação ou motivação aparece ou some é listado no dicionário (`saidas/dicionario_rotulos.csv`, coluna `periodos`) e citado como possível quebra. O formato do `hash` muda (32 hex em 2020S2-2022S1, 64 hex depois): hashes não ligam denúncias entre formatos.
- Denúncias em C somadas entre semestres podem contar o mesmo hash duas vezes; a sobreposição entre arquivos C consecutivos é contada (`saidas/d100_sobreposicao_hash.csv`) e reportada, não descontada.

## 6. Composição (SÓ estas, sempre dentro do recorte I1 grupo LGBT, por período)

UF (27 + não informado/ausente), sexo/gênero da vítima, sexo/gênero do suspeito (feminino, masculino, lgbt_ou_outro, faltantes), classe I2 da vítima (unidade linha) e tipo macro de violação (unidade item de violação: A/B itens, C linhas), com a tabela de mapeamento rótulo -> macro publicada no dicionário. Macro (primeira regra que casa vence): vida, sexual (exceto "ORIENTAÇÃO SEXUAL"), discriminação, institucional, negligência, psicológica, física, patrimonial, liberdade/trabalho, direitos sociais/civis, outros. Percentuais dentro do recorte e do período, sem teste.

## 7. Faltantes, zero e não se aplica (separados sempre)

`ausente` = `NULL` ou vazio; `nao_informado` = `N/D`, `NA`, `NI`, "Não informado", "Não sabe/soube informar", "Atendimento interrompido"; `nao_se_aplica` = "Não se aplica ..."; zero = a categoria existe no formato e a contagem é 0 (escrito 0); categoria que não existe no formato = linha ausente no CSV e "n/d (não existe no formato)" no texto. Em A, se orientação ou identidade forem `nao_informado`, a vítima é `nao_informado` (o campo foi perguntado).

## 8. Duplicatas e qualidade

Por arquivo: linhas malformadas (número de campos errado), linhas idênticas repetidas (conteúdo inteiro igual a uma linha anterior do mesmo arquivo; contadas, NÃO descartadas), linhas sem data reconhecida, linhas com data fora do período, denúncias com UF variando (C). Nenhuma linha é removida.

## 9. Porta de entrada de A (balanço oficial)

Para 2011-2019, comparar linhas de A no grupo LGBT (total do ano e por UF, coluna `NA` do balanço x UF não informada/ausente) com a linha `Total` da tabela "Perfil das Vítimas - Sexo" do balanço. Regra fixa: se a diferença for 0 em todos os anos, "a linha de A no grupo LGBT corresponde à vítima como o balanço oficial conta" e a série A pode ser lida como "vítimas registradas pelo canal" (ainda não pessoas únicas). Se houver diferença em qualquer ano, a unidade de A permanece "linha" (o rótulo "vítima" NÃO é usado) e a diferença por ano é reportada. A porta não aborta nada: só decide o nome da unidade.

## 10. Comparação com Sinan e Anuário (descritiva; unidades distintas)

- Nacional, por ano: tabela lado a lado (Disque 100 grupo LGBT na unidade do formato do ano; Sinan `m_lgbtfobia` BR; Anuário BR da edição mais recente). Proibido: somar fontes, razão entre fontes, taxa de vitimização.
- Por UF, por ano (2015-2019 com A em linhas; 2021-2025 com C em denúncias; 2020 e 2026 fora por quebra e parcialidade): Spearman das contagens, o rho esperado só por tamanho (rho(D, pop) x rho(ref, pop), população do Censo 2022), e **correlação parcial de Spearman dado o posto da população** (estimando de leitura, mesma lógica de `dados/concordancia/concordancia_v2.py`), com IC95% por bootstrap de UFs (B = 5000, semente 20261024, ordem: anos crescentes, Sinan antes de Anuário). UF sem valor na referência sai (NA nunca vira zero). Leitura: "a ordem dos estados no Disque 100, líquida de tamanho, se parece / não se distingue de zero" com o IC; nunca "as fontes medem a mesma coisa".

## 11. O que NÃO se poderá concluir, qualquer que seja o resultado

1. Aumento (ou queda) de denúncias NÃO é aumento (ou queda) de violência: o volume depende de divulgação, canais novos (WhatsApp, webchat, Telegram), mudanças de formulário e de classificação, e confiança no canal.
2. Nenhuma taxa de vitimização: não há denominador de pessoas LGBT por UF-ano, e a unidade não é pessoa.
3. Nenhum total de vítimas únicas: não há chave pública de pessoa em nenhum formato.
4. Nada sobre homicídio de pessoas LGBT como fenômeno populacional: o Disque 100 recebe denúncias, não registra óbitos de forma sistemática.
5. As três dimensões (grupo, SOGI declarada, motivação) não são intercambiáveis; a série de SOGI declarada não é harmonizável entre A, B e C.
6. Comparação entre fontes por UF não valida nenhuma delas: correlação líquida de tamanho próxima de zero ou positiva não diz qual fonte está certa.

## 12. Saídas, ordem de execução e testes

Ordem: `baixar.py` -> `d100_catalogo.py` -> `d100_estrutura.py <todos>` (rótulos, sem contagem) -> `d100_dicionario.py` -> [SELO] -> `d100_tabular.py` (exige o selo) -> `d100_series.py` (exige o selo). Saídas em `saidas/`: `catalogo.tsv`, `estrutura/*.json`, `dicionario_rotulos.csv`, `d100_por_periodo.csv` (longo: periodo, formato, recorte, dimensao, unidade, categoria, n), `d100_qualidade.csv`, `d100_sobreposicao_hash.csv`, `d100_serie_anual.csv`, `d100_composicao.csv`, `d100_uf_ano.csv`, `d100_porta_balanco.csv`, `d100_comparacao_nacional.csv`, `d100_comparacao_uf.csv`; relatório `RELATORIO-DISQUE100.md` (<= 60 linhas). Testes (`/opt/homebrew/bin/python3.14 -m pytest -q tests`, sem `-I`): regras em arquivos sintéticos (`tests/test_d100_regras.py`), re-hash do selo, e números travados lidos dos CSV de `saidas/` (rodam sem `raw/`). Se a passada estrutural dos períodos que faltavam acontecer antes do selo, os números de linhas lidas desses períodos ficam no `saidas/estrutura/` e são citados no relatório como vistos antes do selo.

---

**ADENDOS** (datados; vazio na gravação)

**ADENDO 1 — 2026-10-24T23:10Z, depois de rodar (leitura e escopo; nenhuma regra mudou).**
- Rodada com os 17 arquivos do selo (2011-2023S2). 2024S1 completou o download DEPOIS do selo (sha256 no `catalogo.tsv`) e NÃO entrou; 2024S2-2026T3 seguem baixando. Entram em adendo posterior, com as mesmas regras, rodando `d100_tabular.py` e `d100_series.py` de novo.
- Porta da seção 9: linhas de A no grupo LGBT superam as vítimas do balanço em todos os anos (2011: 1.592 x 1.206; 2019: 1.331 x 926). Pela regra, a unidade de A fica "linha"; a palavra "vítima" não é usada para A.
- `sl_quantidade_vitimas` em 2020S2-2022S1 assume valores 10, 20, ..., 100 (desde 2022S2 só 1 a 7): a soma "vítimas declaradas" desses períodos não é interpretável como número de vítimas; fica no CSV, marcada no relatório, e não é usada em nenhuma frase.
- Taxonomia de orientação em C de 2020S2 a 2022S1 não tem rótulo trans nem hétero: a classe `trans` = 0 nesses períodos é ausência de categoria no formulário, não ausência de pessoas trans.
- Reprodução exata desta rodada: `scripts/d100_tabular.py --so 2011,2012,2013,2014,2015,2016,2017,2018,2019,2020S1,2020S2,2021S1,2021S2,2022S1,2022S2,2023S1,2023S2`; ampliar para 2024S1+ só por ADENDO 2.

**ADENDO 2 — 2026-10-25T00:29Z, ANTES de tabular os 6 arquivos novos (escopo; nenhuma regra mudou).**
- O download terminou (23/23, 0 pedaços com erro). A passada estrutural de 2024S1-2026T3 (só rótulos) foi feita antes desta rodada. Entram agora, com as MESMAS regras seladas (o selo confere `d100_comum.py` sem alteração), 2024S1, 2024S2, 2025S1, 2025S2, 2026S1, 2026T3. Os números dos 17 períodos do selo não mudam (a tabulação é por arquivo).
- Visto na estrutura e declarado antes de contar: desde 2024S1 o campo `Motivação` tem só 23 rótulos e nenhum de orientação/identidade (some também "EM RAZÃO DE SER MULHER"): I3a = 0 a partir de 2024 é ausência da categoria no formulário, não ausência de motivação; I3a não é série em 2024-2026. Em 2025S1 aparece o rótulo `nulo` em orientação, que a regra selada classifica como `outro` (não como `ausente`); a contagem é reportada como está.
- Comparação por UF (seção 10) passa a incluir 2024 e 2025 (Sinan e Anuário); 2026 segue fora (parcial, janeiro a setembro).
