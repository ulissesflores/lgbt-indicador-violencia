# C10 — Exposição por governo: o que aconteceu com a taxa de homicídio quando o governo mudou (2026-10-24)

Pasta: `dados/exposicao/`. Números de `c10_e1_federal.csv`, `c10_e2_resumo.csv` e `c10_e2_trocas_longo.csv` (gerados por `c10_exposicao.py`; travados em `tests/test_c10_exposicao.py`, na raiz do repositório).

> [!IMPORTANT]
> **Isto é exposição, não atribuição.** Mostramos o que a taxa fez quando o governo mudou. Não dizemos que foi por causa do governo: com este desenho, isso é impossível. Nada aqui é sobre violência contra pessoas LGBT: o SIM (Sistema de Informações sobre Mortalidade) não registra orientação sexual, identidade de gênero nem motivação.

## Como foi feito
- Pré-registro `PREREGISTRO-C10.md`: o sha256 do corpo (`83c4ef0f...496f14`) foi gravado em 2026-10-24T20:43:46Z, ANTES de qualquer script que lesse desfecho (`PREREGISTRO-C10.sha256`). Antes disso só rodou `c10_estrutura.py`, que lê exposições. Há 1 adendo, de forma e com uma observação pós-hoc rotulada.
- **Federal (E1):** taxa nacional padronizada por idade, por 100 mil. Compara o último ano inteiro antes do governo com o último ano inteiro dentro dele. A tendência dos 3 anos antes da posse entra como contexto, nunca como contrafactual. O intervalo mede só a incerteza de contagem (Poisson): não mede tendência nem causa.
- **Estadual (E2):** 67 trocas reais de governador (o partido muda). A conta é o excesso relativo ao Brasil, r, entre a média dos 3 anos antes e a dos 3 anos depois (do ano e ao e+2, cortado em 2012-2024). A referência de acaso são as UFs sem troca no mesmo ano, por reamostragem pareada por ano (B = 9999, semente 20261024).

## Federal: taxa nacional de homicídio registrado (agressão), ano-base -> ano-fim
| governo | anos | taxa | variação [IC de contagem] | + causa indeterminada | 3 anos antes da posse |
|---|---|---|---|---|---|
| Lula 2007-10 | 2006 -> 2010 | n/d | n/d (o SIM em disco começa em 2010) | n/d | n/d |
| Dilma | 2010 -> 2015 | 25,93 -> 28,81 | +11,1% [+9,8; +12,5] | +7,9% | n/d |
| Temer | 2015 -> 2018 (inclui 2016, ano dividido: Dilma até 11/05) | 28,81 -> 27,61 | −4,2% [−5,3; −3,0] | −0,4% [−1,4; +0,7] | 2012->2015: +3,4% |
| Bolsonaro | 2018 -> 2022 | 27,61 -> 21,81 | −21,0% [−22,0; −20,0] | −13,7% | 2015->2018: −4,2% |
| Lula (em curso, 2 de 4 anos) | 2022 -> 2024 | 21,81 -> 19,50 | −10,6% [−11,8; −9,4] | −6,1% | 2019->2022: +0,2% |
- A fração de óbitos com causa indeterminada sobe de 14,4% (2015) para 18,0% (2018), 25,9% (2022) e 30,1% (2024). Por isso a queda medida com agressão + indeterminada é sempre menor.
- Os grupos estão no CSV. Exemplo do governo Bolsonaro: mulheres negras −22,4% em agressão, mas −6,1% com indeterminada; arma de fogo −22,8%. Com Dilma: homens negros +11,4%, mulheres não negras −2,9% [−9,3; +3,9].
- Como contexto: a queda nacional começou em 2018, ainda com Temer (C09: o placebo de 2018 dispara). Os denominadores de 2023-24 são extrapolados.

## Estadual: 67 trocas de governador, taxa do estado relativa ao Brasil
- **Todas as 67, total:** 31 subiram e 36 caíram. Mediana −0,7%, quartis [−9,4%; +12,1%], extremos −25,0% (DF 2015) e +35,4% (TO 2015). Nas UFs sem troca no mesmo ano, a mediana de referência ficou em [+0,8%; +7,8%] (95%), p = 0,016; com Holm nos 6 grupos, 0,073. A fração que subiu foi 0,46, contra [0,51; 0,75] na referência.
- **Com agressão + indeterminada, a diferença some:** 34 subiram e 33 caíram, mediana +0,5%, p = 0,54.
- **Por direção (total, 67):** esquerda->direita 12 trocas, 8 subiram e 4 caíram, mediana +9,5%, p = 0,36. Direita->esquerda 8 trocas, 5 subiram e 3 caíram, mediana +3,5%, p = 0,74. Envolve centro 8 trocas, 2 subiram e 6 caíram, −5,4%. Mesmo bloco 39 trocas, 16 subiram e 23 caíram, −2,8%. Pelo sinal do escore: para a direita 38 trocas, −0,4%; para a esquerda 29 trocas, −0,8%. As direções não têm sinais opostos (nenhum teste entre direções foi pré-registrado).
- **Sensibilidades pré-declaradas (total):** janela completa (47), 20 subiram e 27 caíram, mediana −0,8%. Completa e sem outra troca próxima (21), 8 subiram e 13 caíram, −10,2% [−11,9; +7,0]. Só posse eleitoral (45), 21 subiram e 24 caíram, −0,8%.
- **Pós-hoc (adendo 1):** a referência é pequena e não é neutra. São 3 a 15 UFs por ano e 21 UFs distintas no total. Em 2018-2019 são 9 UFs, 7 delas do Nordeste. A mediana de referência de 2019 foi +8,4% (Piauí +37%, Amapá +27%, Bahia +24%). O p só mede o sorteio dentro desse grupo fixo e é anticonservador. A "diferença" pode ser região, não troca.

## A frase que se PODE dizer
- "Entre 2018 e 2022 (governo Bolsonaro), a taxa nacional padronizada de homicídio registrado caiu 21,0%. Somando as mortes de causa indeterminada, caiu 13,7%. A queda começou em 2018, ainda com Temer. Isso não é prova de causa."
- "Entre 2010 e 2015 (governo Dilma), a taxa subiu 11,1% (7,9% com indeterminada). Isso não é prova de causa."
- "Nas 67 trocas de governador de 2013 a 2024, a taxa do estado, relativa ao Brasil, subiu em 31 e caiu em 36 (mediana −0,7%). Quando a troca foi da esquerda para a direita, subiu em 8 de 12. Quando foi da direita para a esquerda, subiu em 5 de 8. Nessas duas direções, o resultado não se distingue do que acontece nas UFs que não trocaram de governo no mesmo ano. Isso não é prova de causa."

## A frase que NÃO se pode dizer
- "Bolsonaro/Temer/Dilma/Lula aumentou ou reduziu os homicídios." "Governador de direita (ou de esquerda) reduz a violência." "Trocar de governo reduz homicídio." "Não tem efeito": nulo descritivo não é ausência de efeito. Qualquer frase sobre violência contra pessoas LGBT.
- Por quê: as trocas coincidem com COVID, mudanças na política de armas, facções, demografia, a piora do registro (indeterminadas) e o ciclo eleitoral. A referência não é contrafactual. Trocas sobrepostas da mesma UF (2018 e 2019) não são independentes.

## Arquivos e reprodução
- `c10_estrutura.py/.md`, `c10_trocas.csv` (só exposições); `c10_exposicao.py`; `c10_e1_federal.csv` (governo x série); `c10_e1_serie_longo.csv` (ano x série, com a fração do ano de cada presidente, pronto para figura); `c10_e2_trocas_longo.csv` (troca x grupo, com o r de cada referência); `c10_e2_resumo.csv` (189 células: recorte x direção x grupo, Holm em `p_*_holm6`); `c10_resultados.md` (tabelas completas).
- Portas que passaram: taxas recalculadas = `asr_brasil.csv` (0,005); arma = série do C09; taxas por UF-ano = painel (diferença 0); agressão SIM = Atlas nos 351 UF-anos; Brasil = soma das 27 UFs (teste independente). Duas execuções geram saídas byte a byte iguais.
- Rodar: `/opt/homebrew/bin/python3.14 -I c10_exposicao.py`; testes: da raiz do repositório, `python3 -m pytest -q tests/test_c10_exposicao.py` (5 passam).

Becos: Lula 2007-10 não computável (o SIM em disco começa em 2010; baixar 1996-2009 do DATASUS daria Lula 1 e 2 e a tendência pré de Dilma). Não há sexo x raça por UF no painel, então o E2 usa 6 grupos. Arma + indeterminada fica n/d, porque o agregado não marca arma em Y22-Y24. 2017 tem 3 UFs de referência. A reamostragem não reproduz a dependência entre trocas da mesma UF.
