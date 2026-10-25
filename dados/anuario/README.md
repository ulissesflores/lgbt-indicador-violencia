# Racismo por homofobia ou transfobia - registros por UF e ano (Anuário Brasileiro de Segurança Pública, FBSP)

Extração determinística do texto `pdftotext` das três edições. Números absolutos. Gerado sem interpretação: cada valor é a célula da coluna "Racismo por homofobia ou transfobia" (Ns. Absolutos) lida na linha indicada.

## Arquivos

- `anuario_lgbtfobia_uf_ano.csv`: 168 linhas = 3 edições x 2 anos x (27 UFs + BR). Colunas: `edicao, ano_dado, uf, registros, nota, linha_txt`. `uf = BR` é a linha Brasil (incluída para conferência). `registros` vazio = `...` (informação não disponível) ou `-` (fenômeno inexistente): a regra pedida manda deixar vazio nos dois casos; a distinção fica implícita aqui e pode ser reconstituída pelo `.txt`.
- Parser (versionado desde 2026-10-21, substitui o rascunho de scratchpad que se perdeu): `extrai_anuario_lgbtfobia.py` nesta pasta. Reproduz as 168 linhas deste CSV sem divergência (colunas `registros` e `linha_txt`) e grava `anuario_lgbtfobia_uf_ano_v2.csv` com a coluna `marca` (`valor` | `nd` = '...' | `inexistente` = '-'), que este CSV legado perdeu. A coluna `nota` deste arquivo é curadoria manual e não é gerada.

## Onde está a tabela em cada edição

| Edição | Arquivo `fontes/` | Tabela / página impressa | Cabeçalho (linha) | Linhas de UF | Notas (linhas) | Anos |
|---|---|---|---|---|---|---|
| 2024 | `t2-anuario-2024-dados2023/anuario.txt` | Tabela 18, continuação na p. 108 (p. 107 traz só injúria e racismo) | 5541 | 5545-5583 (BR = 5547) | 5574-5583 | 2022 (2), 2023 |
| 2025 | `t2-anuario-2025-dados2024/anuario.txt` | Tabela 18 (NT), p. 116 (bloco anterior na p. 115) | 5998 | 6005-6046 (BR = 6005) | 6004-6062 | 2023 (2), 2024 |
| 2026 | `t2-anuario-2026-dados2025/anuario.txt` | **Tabela 19** (LGBTQIAPN+), p. 135. A Tabela 18 (p. 134) NÃO tem essa coluna | 6761 | 6768-6795 (BR = 6768) | 6799-6803 | 2024 (3), 2025 |

Ponto de atenção: na edição 2026 a coluna "Racismo por homofobia ou transfobia" está na Tabela 19 (crimes contra população LGBTQIAPN+), primeira coluna do bloco, com "Variação (%)" logo depois. A Tabela 18 de 2026 traz só Injúria Racial e Racismo, com as proporções. Tratei a coluna como equivalente; a leitura é não ambígua porque o bloco tem exatamente três colunas numéricas antes de "Lesão Corporal Dolosa".

## Notas de rodapé transcritas (verbatim; quebras de linha do PDF removidas)

### Edição 2024, p. 107-108

- (1) Por 100 mil habitantes.
- (2) Atualização das informações publicadas no Anuário Brasileiro de Segurança Pública, ano 17, 2023.
- (3) Em relação ao registros de racismo, o quantitativo refere-se ao total de ocorrências com base na Lei 7.716/1989, independente da natureza específica dentro da Lei. A estatística informada também independe se o crime foi tentado ou consumado.
- (4) Os dados de Racismo por homofobia ou transfobia incluem ocorrências de injúria racial por homofobia ou transfobia.

Marcas nas linhas do bloco homofobia: Amapá (3) (linha 5551) e Minas Gerais (4) (linha 5561).

### Edição 2025, p. 115-116

- (1) Taxa por 100 mil habitantes.
- (2) Atualização das informações publicadas no Anuário Brasileiro de Segurança Pública, ano 18, 2024.
- (3) No Espírito Santo, os dados informados de racismo por homofobia/transfobia consideram às ocorrências marcadas com a motivação "homofobia / transfobia".
- (4) Em Minas Gerais, os dados informados de racismo por homofobia/transfobia consideram às ocorrências marcadas com a motivação "homofobia / transfobia / lesbofobia".
- (5) No Estado de São Paulo, os dados de racismo (total) incluem tanto os registros de injúria racial quanto os de racismo por homofobia ou transfobia. Estes últimos correspondem a boletins de ocorrência registrados com base na Lei do Racismo, nos quais a forma de intolerância foi especificada como homofobia ou transfobia.
- Legenda: "(...) Informação não disponível." / "(-) Fenômeno inexistente."
- Nota Técnica (NT), trecho que atinge o bloco de racismo: "Esse aspecto é importante de ser ressaltado na medida em que nem todas as UFs contabilizaram os registos do crime de injúria racial dentro da categoria racismo, ainda havendo, portanto, uma adaptação dos sistemas de informação e da própria forma de classificar os crimes." O texto da NT ocupa as linhas 6004-6045 do `.txt`; transcrevi só o trecho que atinge a coluna.

Marcas nas linhas: Espírito Santo (3), Minas Gerais (4), São Paulo (5).

### Edição 2026, p. 134-135 (Tabela 19)

- (1) LGBTQIAPN+ é o acrônimo para lésbicas, gays, bissexuais, transgêneros, travestis, queer, intersexuais, assexuais, pansexuais, não-binários e outros.
- (2) Os dados de estupro incluem os crimes de estupro (art. 213, CP) e estupro de vulnerável (art. 217-A, CP), ambos na modalidade consumada.
- (3) Atualização das informações publicadas no Anuário Brasileiro de Segurança Pública, ano 19, 2025. (aplica-se à coluna "2024 (3)")
- Legenda: "(...) Informação não disponível." / "(-) Fenômeno inexistente."
- NT da Tabela 18 (p. 134), linhas 6734-6742, com a lista das UFs que não somaram injúria no racismo: "...nem todas as UFs contabilizaram os registos do crime de injúria racial dentro da categoria racismo (DF, MA, PE, RS, RO, SC), ainda havendo, portanto, uma adaptação dos sistemas de informação e da própria forma de classificar os crimes."

## Conferência: soma das UFs x linha Brasil

Soma apenas das UFs com valor numérico (`...` e `-` contam como vazio, `-` como ausência). Diferença = soma - Brasil.

| Edição | Ano | UFs lidas | Brasil (linha) | Soma UFs | Diferença | UFs vazias |
|---|---|---|---|---|---|---|
| 2024 | 2022 | 27 | 783 | 783 | 0 | 5 |
| 2024 | 2023 | 27 | 2090 | 2090 | 0 | 3 |
| 2025 | 2023 | 27 | 1633 | 1633 | 0 | 4 |
| 2025 | 2024 | 27 | 2480 | 2480 | 0 | 4 |
| 2026 | 2024 | 27 | 2567 | 2567 | 0 | 4 |
| 2026 | 2025 | 27 | 3481 | 3481 | 0 | 5 |

Todas as diferenças são zero: a soma por UF fecha com o Brasil em todas as edições e anos.

## Divergências entre edições para o mesmo ano

### 2023: edição 2024 x edição 2025 (16 linhas divergentes de 28)

| UF | ed. 2024 | ed. 2025 | Δ (2025 - 2024) |
|---|---|---|---|
| AL | 12 | 11 | -1 |
| AM | 22 | vazio | n/a |
| AP | 6 | 9 | 3 |
| BR | 2090 | 1633 | -457 |
| DF | 84 | 92 | 8 |
| GO | 115 | 123 | 8 |
| MA | 14 | 13 | -1 |
| MG | 17 | 11 | -6 |
| PB | 3 | 8 | 5 |
| PE | 80 | 81 | 1 |
| PI | 18 | 23 | 5 |
| RN | 39 | 35 | -4 |
| RS | 325 | 292 | -33 |
| SC | 6 | 1 | -5 |
| SE | 8 | 19 | 11 |
| SP | 809 | 383 | -426 |

Não divergem: AC (1), CE (341), ES (39), MS (14), MT (7), PR (115), RO (12), RR (2), TO (1). Vazias nas duas: BA, PA, RJ.

### 2024: edição 2025 x edição 2026 (17 linhas divergentes de 28)

| UF | ed. 2025 | ed. 2026 | Δ (2026 - 2025) |
|---|---|---|---|
| AM | vazio | 5 | n/a |
| AP | 9 | 15 | 6 |
| BR | 2480 | 2567 | 87 |
| DF | 136 | 139 | 3 |
| ES | 59 | 62 | 3 |
| GO | 124 | 133 | 9 |
| MS | 7 | 16 | 9 |
| PA | vazio | 38 | n/a |
| PB | 14 | 20 | 6 |
| PE | 94 | 96 | 2 |
| PI | 56 | 57 | 1 |
| PR | 137 | 145 | 8 |
| RN | 43 | 38 | -5 |
| RS | 377 | 400 | 23 |
| SC | 1 | vazio | n/a |
| SP | 973 | 955 | -18 |
| TO | 2 | vazio | n/a |

Não divergem: AC (9), AL (8), CE (352), MA (15), MG (15), MT (14), RO (8), RR (7), SE (20). Vazias nas duas: BA, RJ.

Leitura para o uso: a diferença de Brasil em 2023 (2.090 na ed. 2024 x 1.633 na ed. 2025, -21,9%) vem sobretudo de SP (809 x 383); as demais diferenças são de valor, não de presença de dado. A ed. 2025 marca o ano 2023 com a nota (2) de atualização. Em 2024, 2.480 (ed. 2025) x 2.567 (ed. 2026), +3,5%. Na ed. 2026, PA aparece com 38 em 2024, enquanto a ed. 2025 registrava "-" (fenômeno inexistente); não verifiquei se é reclassificação ou dado novo, e a extração não resolve isso.

## Ambiguidades

- Nenhuma linha ficou marcada como ambígua: o parser (regra: nome da UF seguido de pelo menos dois valores numéricos ou `...`/`-`) pegou as 27 UFs e o Brasil nas três edições, sem colunas deslocadas.
- Marca de nota no nome (`(3)`, `(4)`, `(5)`) é removida antes de casar a UF. A coluna `nota` recebe o texto curto da nota da UF (AP/MG em 2024; ES/MG/SP em 2025) e da nota de ano (`(2)` em 2024 e 2025, `(3)` em 2026). Nota de SP (5) e de AP (3) de 2024 falam do total de racismo, não só da coluna homofobia; está registrado assim na coluna.
- Diferença de série entre edições: a coluna de 2026 vem da Tabela 19. Se o FBSP pretender que a Tabela 18 de 2026 contenha esse dado, ele não está lá; não inferi.
