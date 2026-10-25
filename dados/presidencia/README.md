# C09: a troca de presidente e a taxa de homicídio registrado (v0.3, 2026-10-24)

Pergunta: a troca de presidente (2016, 2019, 2023) coincide com mudança na taxa nacional de homicídio registrado, e o alinhamento entre
governador e presidente muda a taxa dos estados? Resposta curta em [`RELATORIO-C09.md`](RELATORIO-C09.md): nenhuma das 21 estimativas do
painel é distinguível de zero, e a queda nacional de 2019 não é atribuível à troca, porque o placebo de 2018 cai com o mesmo sinal.
Nada aqui é sobre violência contra pessoas LGBT: o Sistema de Informações sobre Mortalidade (SIM) não registra orientação sexual,
identidade de gênero nem motivação.

| Arquivo | O que é |
| --- | --- |
| `PREREGISTRO-C09.md`, `PREREGISTRO-C09.sha256` | pré-registro; a 1ª linha do `.sha256` é o hash do corpo, gravado em 2026-10-24T20:06:38Z antes de qualquer script que lesse desfecho |
| `c09_estrutura.py` -> `c09_estrutura.md` | estrutura do desenho (só exposições: presidente por ano, variação disponível, efeito mínimo do D1) |
| `c09_d2_painel.py` -> `c09_d2_resultados.{csv,md}` | D2, primária: painel UF x ano, interação governador x presidente, efeitos fixos de UF e de ano |
| `c09_d1_its.py` -> `c09_d1_resultados.{csv,md}`, `c09_resultados.md` | D1, descritivo: série nacional 2010-2024 com quebras em 2016, 2019 e 2023 e placebo um ano antes |
| `presidentes_2007_2024.csv` | presidentes, partido de eleição e datas de exercício (entrada) |
| `RELATORIO-C09.md` | relatório: desenho, resultado com intervalo, o que o intervalo exclui, o que não se pode dizer |
| [`../../tests/test_c09_presidencia.py`](../../tests/test_c09_presidencia.py) | testes que travam os números (hash do pré-registro, estrutura, primária, D1) |

Rodar (da raiz do repositório): `python3 -I dados/presidencia/c09_estrutura.py`, depois `c09_d2_painel.py` e `c09_d1_its.py` (nessa ordem;
`c09_d1_its.py` lê a saída do D2). O recálculo e a comparação byte a byte entram em `scripts/reproduzir.py` (Trilha 1).
Entradas: só derivados distribuídos (`dados/painel/`, `dados/ideologia/`, `dados/sim/`, `dados/atlas_uf_series.csv`) e as cópias abertas de
`fontes/` (SIDRA/IBGE; Power & Zucco, CC0).

**Pasta de trabalho de origem.** A análise foi feita na pasta `research-2026-10-24-presidencia/` do projeto privado e realocada aqui. Os scripts
e o relatório trazem o caminho novo (registro em `manifest/MODIFICACOES.tsv`); o pré-registro fica byte a byte, porque o hash foi gravado
antes, e por isso ainda cita a pasta de origem (linha 3) e o arquivo `ASTRA-B-lacunas.md` (revisão externa por modelo de linguagem, não
distribuída; ver o glossário em [`../../docs/INDEX.md`](../../docs/INDEX.md)). O briefing de método da frente não é distribuído.
