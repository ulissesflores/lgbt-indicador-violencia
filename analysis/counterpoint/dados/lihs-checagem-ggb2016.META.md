# Checagem da Liga Humanista Secular do Brasil (LiHS) sobre a lista do GGB de 2016: metadados e tabulação

Este arquivo existe no lugar da planilha. A planilha da LiHS (Vieira et al., 1 de maio de 2019) é pública e de terceiros, e **não é distribuída
aqui**: ela traz o nome de cada vítima (`NOME`), os nomes de acusados (`NOME_ASSASSINO`, `NomeAss2`, `NomeAss3`) e os links de imprensa de cada caso,
e este repositório não distribui dado nominal (`manifest/MANIFESTO-FONTES.csv`, linha "DADOS NOMINAIS"; `.gitignore`). O que fica é o que
permite conferir a leitura sem a planilha.

| Campo | Valor |
|---|---|
| Fonte | Liga Humanista Secular do Brasil (LiHS), "Principais estatísticas brasileiras de morte por homofobia são falsas, conclui checagem independente", 1 de maio de 2019 (https://lihs.org.br/sociedade/homofobia/) |
| URL da planilha | https://docs.google.com/spreadsheets/d/1QdVdDhPLsFomf9edOscMz-hZhIitqwkSuSi3I7XV3Po/ |
| Arquivo lido | CSV exportado da planilha, 349 linhas: 1ª linha de título, 2ª linha de cabeçalho (39 colunas), 347 casos |
| SHA-256 do CSV lido | `0dc25783bfc422ec635826009fbdfbda4efc41ecd7dca0fa05fc469a9179d5ad` |
| Data da leitura | 2026-10-30 (registro no ledger: 2026-10-30T05:20:57Z) |
| Coluna tabulada | `Motivacao_Homof` |

## Tabulação da coluna Motivacao_Homof

Contagem feita sobre o CSV lido (cabeçalho na 2ª linha); `tests/test_numeros_v05.py` trava estes números. Sob o critério dos autores, "sim" é
o piso comprovado, e não uma estimativa da fração verdadeira; "inconclusivo" não é ausência de motivo.

| Motivacao_Homof | Casos | % de 347 |
|---|---|---|
| Sim | 31 | 8,9% |
| Não | 127 | 36,6% |
| Inconclusivo | 159 | 45,8% |
| Não localizado | 23 | 6,6% |
| Exterior | 6 | 1,7% |
| Duplicado | 1 | 0,3% |
| Total | 347 | 100,0% |

Quem tiver a planilha confere o SHA-256 acima e refaz a contagem; se o CSV for posto em `analysis/counterpoint/dados/`, o teste
`tests/test_numeros_v05.py` conta a coluna nele em vez de ler esta tabela. Ressalvas de leitura (um revisor por caso,
critério de "indício", coautores com crítica prévia ao GGB): `analysis/counterpoint/frente-A-brasil.md`, item 1.
