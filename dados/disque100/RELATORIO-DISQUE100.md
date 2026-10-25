# Disque 100 (v0.3): o que o canal permite dizer, 2011-2026

> [!NOTE]
> Versão COMPLETA (23/23 arquivos). A entrega parcial (17 arquivos, selo `PREREGISTRO-D100.sha256` em 2026-10-24T22:52:55Z) foi estendida pelo ADENDO 2 com as mesmas regras seladas; os números de 2011-2023 não mudaram. 2026 = janeiro a setembro (parcial).

**Acesso:** 23 CSV em `dadosabertos.mdh.gov.br`, sem cadastro, aceite ou login; catálogo com URL, tamanho, Last-Modified, data de acesso e sha256 de todos (`saidas/catalogo.tsv`; 2011 e 2020S1 batem com a leitura prévia dos cabeçalhos).

**Formatos e unidade:** três formatos, nenhum com chave de pessoa.

| formato | períodos | o que é uma linha | unidade usada | vítimas únicas |
|---|---|---|---|---|
| A | 2011-2019 | vítima x suspeito de um atendimento, sem chave | linha | não calculável |
| B | 2020S1 | par vítima-suspeito (`hash_par`) | par | não calculável |
| C | 2020S2-2026T3 | violação x vítima x suspeito dentro da denúncia (`hash`, 2,5-6,7 linhas por denúncia) | denúncia | não calculável |

Porta de entrada: as linhas de A no grupo LGBT superam as vítimas do balanço oficial em todos os anos (2011: 1.592 x 1.206; 2019: 1.331 x 926), então a unidade de A é "linha", não "vítima". **O total de vítimas únicas não é calculável em nenhum período.**

**Três recortes LGBT, nunca somados:** I1 grupo/módulo LGBT da denúncia; I2 orientação/identidade LGBT declarada da vítima (não harmonizável entre formatos); I3 motivação por orientação/identidade (não existe em A e some do formulário a partir de 2024).

**Série do grupo LGBT (I1), `saidas/d100_serie_anual.csv`:**

| ano | n | unidade | % do canal | nota |
|---|---|---|---|---|
| 2011-2019 | 1.331 a 4.787 (2011 1.592; 2019 1.331) | linhas | 0,41-1,59 | A |
| 2020 | 3.412 linhas | misto | — | quebra B->C no ano |
| 2021 / 2022 / 2023 | 1.367 / 4.163 / 6.173 | denúncias | 0,62 / 1,38 / 1,43 | C |
| 2024 / 2025 | 8.176 / 9.346 | denúncias | 1,48 / 1,47 | C; canal: 551.693 / 637.890 denúncias |
| 2026 (jan-set) | 10.461 | denúncias | 1,90 | parcial |

- A regra de contagem pesa muito: denúncia "com ao menos uma linha LGBT" x "com todas as linhas LGBT" = 6.173 x 1.827 (2023), 9.346 x 39 (2025), porque o grupo passou a variar dentro da mesma denúncia desde 2022S2.
- O canal inteiro cresceu muito mais (linhas: 0,93 milhão em 2021, 4,59 milhões em 2025); a fatia LGBT ficou entre 1,4% e 1,9% desde 2022.
- Motivação por orientação/identidade (I3): 1.718 / 2.148 / 1.872 denúncias em 2021-2023; zero em 2024-2026 porque a categoria deixou de existir no campo (não é ausência de motivação).
- Composição (dentro de I1, `saidas/d100_composicao.csv`): violação psicológica é a maior em todos os 23 períodos (44-70% dos itens); física 9,5% (2019), 19,3% (2023S2), 19,2% (2026T3); suspeito masculino 39-58%; na vítima, `trans` 12-24% desde 2022S2; em 2020S2-2022S1 trans = 0 porque o formulário não tinha o rótulo.
- Qualidade (`saidas/d100_qualidade.csv`): 0 linhas malformadas; A tem 3.648-14.870 linhas idênticas repetidas por ano (contadas, não removidas); nenhum hash se repete entre semestres; `sl_quantidade_vitimas` vale 10-100 em 2020S2-2022S1, então "vítimas declaradas" não é interpretável nesses períodos.

**Comparação com Sinan e Anuário** (`saidas/d100_comparacao_uf.csv`; nada somado, nenhuma taxa): as contagens por UF se correlacionam (Spearman 0,57-0,91), mas o tamanho da UF explica a maior parte (0,51-0,80). Descontada a população, a correlação parcial com o Sinan vai de -0,17 (2015) a 0,55 (2019 e 2025); o IC95% exclui zero em 2019, 2023, 2024 e 2025. Com o Anuário: 0,11 (2022), 0,28 (2023), 0,54 (2024, IC 0,07 a 0,81), 0,51 (2025, IC inclui zero).

## Frase que se PODE dizer
"Os microdados públicos do Disque 100 registram, no módulo LGBT, de 1,3 mil a 4,8 mil linhas por ano em 2011-2019 e de 1,4 mil (2021) a 9,3 mil (2025) denúncias com ao menos uma linha no módulo, 1,4% a 1,5% das denúncias do canal desde 2022; são contagens de registros de um canal que mudou de formato três vezes, não de pessoas nem de violência ocorrida."

## Frases que NÃO se pode dizer
- "A violência contra pessoas LGBT aumentou": aumento de denúncias não é aumento de violência (de 2021 a 2025 as denúncias do canal quase triplicaram, de 222 mil para 638 mil, e as linhas quase quintuplicaram; houve canais novos, divulgação e formulário novo em 2022S2).
- "X vítimas LGBT únicas" ou qualquer taxa de vitimização: não há chave de pessoa nem denominador.
- "A série 2011-2026 é contínua": quebras em 2020S1, 2020S2, 2022S2 e (motivação) 2024S1.
- "A motivação LGBTfóbica sumiu em 2024": sumiu a categoria do formulário.
- "Disque 100, Sinan e Anuário confirmam um ao outro": a concordância bruta é sobretudo tamanho da UF.
- Comparar 2026 com ano cheio sem a marca de parcial.

Arquivos: `PREREGISTRO-D100.md` (+ `.sha256`, ADENDOS 1-2), `DICIONARIO-D100.md`, `saidas/` (CSV longos), `scripts/` (python3.14 -I), `tests/` (63 testes, `python3.14 -m pytest -q tests`).
