# Cobertura implícita da contagem do GGB (gerado por cobertura_implicita.py)


**Exercício de escala, não estimativa de mortes nem taxa.** Leia o cabeçalho do script. E = mortes por agressão ESPERADAS entre adultos LGB+ se tivessem o risco dos pares (mesmo sexo, raça, faixa etária).

Prevalência LGB+ entre respondentes com orientação válida: 1.96% (a composição por célula vem daí); o resultado principal escala para 1,89% (publicado por Vasconcelos et al., não resposta contada como não LGB+); 1,96% e cenários maiores entram na sensibilidade.
Composição LGB+ vs adultos em geral (PNS): 18-29 anos 57% vs 22%; 30-44 27% vs 30%; 45+ 16% vs 48%; negros 56% vs 55%; homens 48% vs 47%.

## Resultado principal (desfecho agressão X85-Y09; prevalência 1,89%; GGB = todas as mortes da contagem)

| ano | pop. LGB+ adulta | GGB | esperado RR=1 (mesmo risco dos pares) | cobertura implícita | esperado RR=2,82 | cobertura | esperado RR=3,84 | cobertura |
|---|---|---|---|---|---|---|---|---|
| 2023 | 3.025.764 | 257 | 1122 | 23% | 3165 | 8% | 4309 | 6% |
| 2024 | 3.027.156 | 291 | 1013 | 29% | 2856 | 10% | 3889 | 8% |

IC95% só pela prevalência (1,73-2,07% vs 1,89%): esperado e cobertura variam ~±9% (linear).

## Sensibilidade: prevalência maior que a autodeclarada (cenários, NÃO fatos) e desfecho 'agressão + intenção indeterminada'

| desfecho | ano | prevalência | RR | GGB (medida) | esperado | cobertura implícita |
|---|---|---|---|---|---|---|
| agressao | 2023 | 1,89% (PNS 2019, publicado; não resposta = não LGB+) | 1.0 | 257 (todas) | 1122 | 23% |
| agressao | 2023 | 1,89% (PNS 2019, publicado; não resposta = não LGB+) | 1.0 | 221 (homicidios_decl) | 1122 | 20% |
| agressao | 2023 | 1,96% (PNS, só respostas válidas) | 1.0 | 257 (todas) | 1162 | 22% |
| agressao | 2023 | 1,96% (PNS, só respostas válidas) | 1.0 | 221 (homicidios_decl) | 1162 | 19% |
| agressao | 2023 | 3% (cenário) | 1.0 | 257 (todas) | 1781 | 14% |
| agressao | 2023 | 3% (cenário) | 1.0 | 221 (homicidios_decl) | 1781 | 12% |
| agressao | 2023 | 5% (cenário) | 1.0 | 257 (todas) | 2969 | 9% |
| agressao | 2023 | 5% (cenário) | 1.0 | 221 (homicidios_decl) | 2969 | 7% |
| agressao | 2024 | 1,89% (PNS 2019, publicado; não resposta = não LGB+) | 1.0 | 291 (todas) | 1013 | 29% |
| agressao | 2024 | 1,89% (PNS 2019, publicado; não resposta = não LGB+) | 1.0 | 273 (homicidios_decl) | 1013 | 27% |
| agressao | 2024 | 1,96% (PNS, só respostas válidas) | 1.0 | 291 (todas) | 1048 | 28% |
| agressao | 2024 | 1,96% (PNS, só respostas válidas) | 1.0 | 273 (homicidios_decl) | 1048 | 26% |
| agressao | 2024 | 3% (cenário) | 1.0 | 291 (todas) | 1607 | 18% |
| agressao | 2024 | 3% (cenário) | 1.0 | 273 (homicidios_decl) | 1607 | 17% |
| agressao | 2024 | 5% (cenário) | 1.0 | 291 (todas) | 2679 | 11% |
| agressao | 2024 | 5% (cenário) | 1.0 | 273 (homicidios_decl) | 2679 | 10% |
| agressao+indet | 2023 | 1,89% (PNS 2019, publicado; não resposta = não LGB+) | 1.0 | 257 (todas) | 1298 | 20% |
| agressao+indet | 2023 | 1,89% (PNS 2019, publicado; não resposta = não LGB+) | 1.0 | 221 (homicidios_decl) | 1298 | 17% |
| agressao+indet | 2023 | 1,96% (PNS, só respostas válidas) | 1.0 | 257 (todas) | 1343 | 19% |
| agressao+indet | 2023 | 1,96% (PNS, só respostas válidas) | 1.0 | 221 (homicidios_decl) | 1343 | 16% |
| agressao+indet | 2023 | 3% (cenário) | 1.0 | 257 (todas) | 2060 | 12% |
| agressao+indet | 2023 | 3% (cenário) | 1.0 | 221 (homicidios_decl) | 2060 | 11% |
| agressao+indet | 2023 | 5% (cenário) | 1.0 | 257 (todas) | 3433 | 8% |
| agressao+indet | 2023 | 5% (cenário) | 1.0 | 221 (homicidios_decl) | 3433 | 6% |
| agressao+indet | 2024 | 1,89% (PNS 2019, publicado; não resposta = não LGB+) | 1.0 | 291 (todas) | 1245 | 23% |
| agressao+indet | 2024 | 1,89% (PNS 2019, publicado; não resposta = não LGB+) | 1.0 | 273 (homicidios_decl) | 1245 | 22% |
| agressao+indet | 2024 | 1,96% (PNS, só respostas válidas) | 1.0 | 291 (todas) | 1289 | 23% |
| agressao+indet | 2024 | 1,96% (PNS, só respostas válidas) | 1.0 | 273 (homicidios_decl) | 1289 | 21% |
| agressao+indet | 2024 | 3% (cenário) | 1.0 | 291 (todas) | 1976 | 15% |
| agressao+indet | 2024 | 3% (cenário) | 1.0 | 273 (homicidios_decl) | 1976 | 14% |
| agressao+indet | 2024 | 5% (cenário) | 1.0 | 291 (todas) | 3294 | 9% |
| agressao+indet | 2024 | 5% (cenário) | 1.0 | 273 (homicidios_decl) | 3294 | 8% |

## Como ler

- Se LGB+ tivessem o MESMO risco de morte por agressão dos pares, o esperado superaria em várias vezes a contagem do GGB: a cobertura implícita da contagem seria baixa. A contagem do GGB só 'fecha' com o esperado se LGB+ tivessem risco MUITO MENOR que os pares, o que contraria a PNS (risco de violência física 2,8x a 3,8x maior).
- Isso NÃO prova que o GGB capta só uma fração: o numerador do GGB inclui menores (fora do denominador adulto) e pessoas trans (a PNS 2019 não perguntou identidade de gênero: trans que declararam orientação LGB estão no denominador sem identificação, as demais não; correção v0.3, 2026-10-24), e a prevalência autodeclarada pode subestimar. Prova que numerador de mídia e denominador de survey não casam, e que a leitura 'GGB = todas as mortes LGB+' é inconsistente com qualquer cenário de risco igual ou maior que o dos pares.
- Limite do pareamento: só sexo x raça x idade; sem escolaridade, UF e urbano/rural (não medido o quanto isso reduziria o esperado).
- Não usar como taxa. Não usar para 'país que mais mata'. Serve para limitar o que a contagem do GGB pode significar.
