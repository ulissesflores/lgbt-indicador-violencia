# C08 — cobertura implícita do GGB com numeradores comparáveis (gerado por ggb_c08_numeradores.py)

> [!NOTE]
> **Exercício de escala, não estimativa de mortes nem taxa.** Cabeçalho do script traz os numeradores, as fontes e todos os LIMITES. Critérios pré-escritos em `research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md`. N2 é um cenário de subtração (todas as pessoas trans da tabela de identidade), não limite inferior nem superior demonstrado (correção v0.3; seção 5).

## 0. Reprodução: 96 linhas de `dados/ggb/cobertura_implicita.csv` reproduzidas (esperado ±0,1; cobertura ±0,001); senão o script aborta.

## 1. Numeradores (de onde vem cada número)

| ano | N0 total | N1 homicídio + latrocínio | trans na tabela de identidade | N2 = N1 - trans | observação |
|---|---|---|---|---|---|
| 2023 | 257 | 204 + 17 = 221 | 127 ("Travestis e Transgêneros") | 94 | script antigo: 221 = mesmo N1 |
| 2024 | 291 | 239 + 30 = 269 | 96 + 6 homens trans = 102 | 167 | script antigo usa 273 (inclui 4 "outras"): definição diferente da de 2023 |
| 2025 | 257 | 204 + 17 = 221 | 46 + 18 + 3 = 67 | 154 | tabela de causa IDÊNTICA à de 2023; sem SIM 2025: sem veredito |

## 2. Resultado principal: desfecho agressão X85-Y09, prevalência 1,89%, cobertura = n / E

| ano | numerador | n | E (RR=1) | cobertura RR=1 | cobertura RR=2,82 | cobertura RR=3,84 |
|---|---|---|---|---|---|---|
| 2023 | N0 | 257 | 1122 | 22.9% | 8.1% | 6.0% |
| 2023 | N1 | 221 | 1122 | 19.7% | 7.0% | 5.1% |
| 2023 | N2 | 94 | 1122 | 8.4% | 3.0% | 2.2% |
| 2024 | N0 | 291 | 1013 | 28.7% | 10.2% | 7.5% |
| 2024 | N1 | 269 | 1013 | 26.6% | 9.4% | 6.9% |
| 2024 | N2 | 167 | 1013 | 16.5% | 5.8% | 4.3% |
| 2025 (PROXY: taxas SIM 2024) | N0 | 257 | 1015 | 25.3% | 9.0% | 6.6% |
| 2025 (PROXY: taxas SIM 2024) | N1 | 221 | 1015 | 21.8% | 7.7% | 5.7% |
| 2025 (PROXY: taxas SIM 2024) | N2 | 154 | 1015 | 15.2% | 5.4% | 4.0% |

## 3. Prevalência 1,96% (só respostas válidas) e desfecho agressão + indeterminada (sensibilidade)

| desfecho | ano | prevalência | numerador | n | E (RR=1) | cobertura RR=1 | cobertura RR=2,82 | cobertura RR=3,84 |
|---|---|---|---|---|---|---|---|---|
| agressao | 2023 | 1,96% | N0 | 257 | 1162 | 22.1% | 7.8% | 5.8% |
| agressao | 2023 | 1,96% | N1 | 221 | 1162 | 19.0% | 6.7% | 5.0% |
| agressao | 2023 | 1,96% | N2 | 94 | 1162 | 8.1% | 2.9% | 2.1% |
| agressao | 2024 | 1,96% | N0 | 291 | 1048 | 27.8% | 9.8% | 7.2% |
| agressao | 2024 | 1,96% | N1 | 269 | 1048 | 25.7% | 9.1% | 6.7% |
| agressao | 2024 | 1,96% | N2 | 167 | 1048 | 15.9% | 5.6% | 4.1% |
| agressao | 2025 PROXY | 1,96% | N0 | 257 | 1051 | 24.5% | 8.7% | 6.4% |
| agressao | 2025 PROXY | 1,96% | N1 | 221 | 1051 | 21.0% | 7.5% | 5.5% |
| agressao | 2025 PROXY | 1,96% | N2 | 154 | 1051 | 14.7% | 5.2% | 3.8% |
| agressao+indet | 2023 | 1,89% | N0 | 257 | 1298 | 19.8% | 7.0% | 5.2% |
| agressao+indet | 2023 | 1,89% | N1 | 221 | 1298 | 17.0% | 6.0% | 4.4% |
| agressao+indet | 2023 | 1,89% | N2 | 94 | 1298 | 7.2% | 2.6% | 1.9% |
| agressao+indet | 2023 | 1,96% | N0 | 257 | 1343 | 19.1% | 6.8% | 5.0% |
| agressao+indet | 2023 | 1,96% | N1 | 221 | 1343 | 16.5% | 5.8% | 4.3% |
| agressao+indet | 2023 | 1,96% | N2 | 94 | 1343 | 7.0% | 2.5% | 1.8% |
| agressao+indet | 2024 | 1,89% | N0 | 291 | 1245 | 23.4% | 8.3% | 6.1% |
| agressao+indet | 2024 | 1,89% | N1 | 269 | 1245 | 21.6% | 7.7% | 5.6% |
| agressao+indet | 2024 | 1,89% | N2 | 167 | 1245 | 13.4% | 4.8% | 3.5% |
| agressao+indet | 2024 | 1,96% | N0 | 291 | 1289 | 22.6% | 8.0% | 5.9% |
| agressao+indet | 2024 | 1,96% | N1 | 269 | 1289 | 20.9% | 7.4% | 5.4% |
| agressao+indet | 2024 | 1,96% | N2 | 167 | 1289 | 13.0% | 4.6% | 3.4% |
| agressao+indet | 2025 PROXY | 1,89% | N0 | 257 | 1249 | 20.6% | 7.3% | 5.4% |
| agressao+indet | 2025 PROXY | 1,89% | N1 | 221 | 1249 | 17.7% | 6.3% | 4.6% |
| agressao+indet | 2025 PROXY | 1,89% | N2 | 154 | 1249 | 12.3% | 4.4% | 3.2% |
| agressao+indet | 2025 PROXY | 1,96% | N0 | 257 | 1293 | 19.9% | 7.1% | 5.2% |
| agressao+indet | 2025 PROXY | 1,96% | N1 | 221 | 1293 | 17.1% | 6.1% | 4.5% |
| agressao+indet | 2025 PROXY | 1,96% | N2 | 154 | 1293 | 11.9% | 4.2% | 3.1% |

## 4. Vereditos pelas convenções pré-escritas (agressão; 1,89%; RR=1; anos com SIM)

- 2023: cobertura N0 22.9%, N1 19.7%, N2 8.4%. N0 e N1 < 100%: sim. N2 < 15%: sim. Entre os cenários N2 e N1: [8.4%; 19.7%] (cenários, não intervalo demonstrado; v0.3, seção 5).
- 2024: cobertura N0 28.7%, N1 26.6%, N2 16.5%. N0 e N1 < 100%: sim. N2 < 15%: NÃO. Entre os cenários N2 e N1: [16.5%; 26.6%] (cenários, não intervalo demonstrado; v0.3, seção 5).

## 5. Correção v0.3 (2026-10-24, post hoc): N2 é cenário, não limite (faixas pelas marginais publicadas do GGB)

> [!WARNING]
> A versão anterior chamava N2 de "limite inferior do numerador cis LGB" e lia a cobertura cis LGB "entre N2 e N1". Isso não está demonstrado: o GGB inclui heterossexuais (6 em 2024), não publica causa x identidade x idade e o numerador tem menores. Os números acima ficam; a leitura muda. Além disso, a PNS 2019 não perguntou identidade de gênero: pessoas trans que declararam orientação LGB estão no denominador, sem identificação.

Faixas abaixo: só tabelas de identidade, causa e idade e a frase sobre suicídios por identidade de cada release; agressão X85-Y09, prevalência 1,89%, RR = 1. Em 2023, os 2 suicidas não binários foram contados ora entre trans, ora entre cis (a faixa é a união). 2025 fica de fora: a tabela de identidade soma 255, não 257, e o release não separa os 20 suicídios entre gays e trans.

| ano | cenário | n | E (RR=1) | cobertura RR=1 |
|---|---|---|---|---|
| 2023 | N1 homicídio + latrocínio (inclui trans e heterossexuais) | 221 | 1122 | 19.7% |
| 2023 | N2 cenário: N1 menos TODAS as trans da tabela (publicado) | 94 | 1122 | 8.4% |
| 2023 | cis LGB dentro de N1: mínimo compatível com as marginais | 100 | 1122 | 8.9% |
| 2023 | cis LGB dentro de N1: máximo compatível com as marginais | 118 | 1122 | 10.5% |
| 2023 | mínimo compatível menos toda a faixa etária até 18 anos do release (cenário de idade; idade não informada fica) | 92 | 1122 | 8.2% |
| 2024 | N1 homicídio + latrocínio (inclui trans e heterossexuais) | 269 | 1013 | 26.6% |
| 2024 | N2 cenário: N1 menos TODAS as trans da tabela (publicado) | 167 | 1013 | 16.5% |
| 2024 | contraexemplo do Astra: 269 - 99 trans (102 - 3 suicidas) - 6 heterossexuais | 164 | 1013 | 16.2% |
| 2024 | cis LGB dentro de N1: mínimo compatível com as marginais | 164 | 1013 | 16.2% |
| 2024 | cis LGB dentro de N1: máximo compatível com as marginais | 168 | 1013 | 16.6% |
| 2024 | mínimo compatível menos toda a faixa etária até 18 anos do release (cenário de idade; idade não informada fica) | 148 | 1013 | 14.6% |
- 2023: N2 = 94 está abaixo do mínimo compatível [100; 118] de cis LGB dentro de N1.
- 2024: N2 = 167 está dentro da faixa [164; 168] de cis LGB dentro de N1.
- Conclusão: N2 não é limite em nenhuma direção (abaixo da faixa em 2023, dentro dela em 2024). Nenhum cenário muda a leitura de escala: em todos, a contagem fica muito abaixo das mortes esperadas sob risco igual. O numerador comparável ao denominador da PNS (adultos que se declarariam LGB, inclusive pessoas trans) não é obtenível sem cruzamento público de causa x orientação x identidade x idade.
