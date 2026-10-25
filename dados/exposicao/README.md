# C10: exposição por governo, sem atribuição de causa (v0.3, 2026-10-24)

O que aconteceu com a taxa de homicídio registrado quando o governo mudou, no nível federal (mandatos presidenciais) e estadual (67 trocas
reais de partido no governo do estado). É **exposição, não atribuição**: o desenho não separa o governo de tudo o que mudou junto, e nenhuma
frase daqui diz que a taxa subiu ou caiu "por causa" de um governo. Resumo e frases que se pode e que não se pode dizer:
[`RELATORIO-EXPOSICAO.md`](RELATORIO-EXPOSICAO.md). Nada aqui é sobre violência contra pessoas LGBT (o SIM não registra orientação sexual,
identidade de gênero nem motivação).

| Arquivo | O que é |
| --- | --- |
| `PREREGISTRO-C10.md`, `PREREGISTRO-C10.sha256` | pré-registro; hash do corpo gravado em 2026-10-24T20:43:46Z antes de qualquer script que lesse desfecho; 1 adendo datado |
| `c10_estrutura.py` -> `c10_estrutura.md`, `c10_trocas.csv` | estrutura (só exposições): as 67 trocas e a direção (esquerda/direita/centro) |
| `c10_exposicao.py` -> `c10_e1_federal.csv`, `c10_e1_serie_longo.csv` | federal: taxa padronizada por idade antes e no fim de cada mandato, por grupo, com e sem causa indeterminada |
| `c10_exposicao.py` -> `c10_e2_trocas_longo.csv`, `c10_e2_resumo.csv`, `c10_resultados.md` | estadual: taxa do estado relativa ao Brasil, 3 anos antes x 3 depois, contra UFs sem troca no mesmo ano (reamostragem) |
| `RELATORIO-EXPOSICAO.md` | relatório |
| [`../../tests/test_c10_exposicao.py`](../../tests/test_c10_exposicao.py) | testes que travam os números |

Rodar (da raiz): `python3 -I dados/exposicao/c10_estrutura.py` e depois `python3 -I dados/exposicao/c10_exposicao.py` (lê
`dados/presidencia/presidentes_2007_2024.csv` e `dados/presidencia/c09_d1_resultados.md`). Recálculo e comparação: `scripts/reproduzir.py`.
Os CSV de formato longo são as entradas das figuras 22 e 23 do artigo.

**Pasta de trabalho de origem:** `research-2026-10-24-exposicao/` do projeto privado. O pré-registro fica byte a byte (hash gravado) e por isso
cita a pasta de origem (linha 3) e caminhos `research-2026-10-24-presidencia/...`, que aqui são `dados/presidencia/...`.
