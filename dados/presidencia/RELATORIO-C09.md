# C09 — A troca de presidente incide sobre a violência letal? (relatório, 2026-10-24)

Pasta de todos os arquivos citados: `dados/presidencia/`.

> [!IMPORTANT]
> **Resposta:** não se detecta incidência. Nenhuma das 21 estimativas do painel (alinhamento governador-presidente) fica distinguível de zero, e a queda nacional de 2019 não é atribuível à troca: o placebo de 2018 dispara com o mesmo sinal. Pela regra pré-registrada, 1 das 36 células do D1 coincide com a troca: mulheres negras em 2019, −19,7%. Ela some quando se soma a causa indeterminada. Nulo aqui é um intervalo, não "zero": o desenho só exclui efeitos grandes, de cerca de 18% para menos e 10% para mais no contraste principal. Nada disto é sobre violência contra pessoas LGBT: o SIM não registra orientação sexual, identidade de gênero nem motivação.

## Pergunta e desenho
- Pergunta do autor: "mudança de presidência incide? assim como governador?" (o briefing interno de método não é distribuído).
- Pré-registro: `PREREGISTRO-C09.md`, sha256 do corpo `f48b1ee4...a41a`, gravado em 2026-10-24T20:06:38Z ANTES de qualquer script que lesse desfecho (`PREREGISTRO-C09.sha256`). Um adendo só de forma (nomes de arquivo, arredondamento do CSV).
- **D2 (primária, painel de 351 UF-anos, 2012-2024):** ln(taxa total) = b1·governador + **b2·(governador × presidente)** + efeitos fixos de UF e de ano. O efeito de ano absorve o presidente; só a interação (alinhamento) é identificada. EP agrupado por UF + bootstrap wild-cluster (B = 4999, semente 20261024). Ideologia BRC por período, partido de eleição (Dilma/Lula PT, Temer PMDB, Bolsonaro PSL); 2016 ponderado por dias (0,361 Dilma, 0,639 Temer).
- Secundárias: distância |gov − pres|, 5 grupos, agressão + indeterminada, razão de indeterminadas (falsificação), escore único 2018, sem 2016, escala BLS9 (escore do próprio presidente), copartidarismo (D3).
- **D1 (descritivo):** série nacional padronizada por idade 2010-2024, quebras de nível e inclinação em 2016, 2019 e 2023, placebo 1 ano antes (2015, 2018, 2022).
- Portas de reprodução que passaram: b/EP dos 6 desfechos do painel de governadores e p wild 0,943; SIM agressão = Atlas por UF-ano; `asr_brasil.csv` recalculado (5 grupos, 2 desfechos); arma de fogo nacional = soma das UFs do Atlas.

## Resultado (todos os números vêm de `c09_d2_resultados.csv` e `c09_d1_resultados.csv`)
- **Primária:** b2 = −0,00214, IC95% [−0,00786; +0,00357], p wild 0,459. Contraste lido = governador 5 pontos mais à direita, presidente PT -> PSL: efeito na taxa entre **−18,3% e +9,6%**. Efeito mínimo detectável com 80% de poder: −18,9% / +23,3%. Veredito pré-registrado: **não distinguível de zero**.
- Distância (5 pontos): entre −5,4% e +11,1% (p 0,526). Copartidarismo (UF do partido do presidente): entre −9,8% e +12,5% (p 0,895).
- Mesmo sinal no escore único 2018 (b2 = −0,00288, p 0,396; ambos não distinguíveis de zero); sem 2016, entre −18,2% e +10,0%; BLS9, entre −20,5% e +10,7%.
- Grupos (Holm = 1,000 em todos): o intervalo mais largo é o de não negros, entre −29,7% e +10,6%.
- **Falsificação:** razão indeterminada/(agressão + indeterminada) no total, p 0,182, entre −1,1 e +5,6 p.p. no contraste. Agressão + indeterminada no total: entre −14,9% e +11,8%. O óbito registrado não parece reclassificado pelo alinhamento, mas o teste é fraco.
- **D1 nacional:** 2019 tem queda de nível de −17,0% [−29,5; −2,4], mas o placebo de 2018 dá −21,8% [−37,4; −2,4]. Pela regra, a queda **não é atribuível à troca**: ela começou em 2018, com Temer. Em 2016, +2,6% [−9,1; +15,9]; em 2023, −3,9% [−17,1; +11,3]. Os efeitos mínimos detectáveis ficam entre ±15% e ±25%.
- Uma única célula das 36 do D1 "coincide com a troca": mulheres negras em 2019, −19,7% [−30,2; −7,6], placebo de 2018 [−33,4; +4,3]. Ela some com agressão + indeterminada (−6,1% [−15,3; +4,1]). No mesmo período, a razão nacional de indeterminadas sobe de 13,3% (2017) para 18,0% (2018), 27,4% (2019) e 30,1% (2024). Com 36 testes esperam-se cerca de 1,8 falsos positivos. Rótulo pré-registrado: "coincide com a troca (descritivo; não causal)". Interpretação PÓS-HOC, fora da regra: reclassificação ou acaso, e não efeito do presidente. A falsificação pré-registrada (razão nacional, +6,5 p.p. [−0,6; +13,7]) não disparou formalmente.

## O que o intervalo exclui
- Com 95% de confiança e as premissas do modelo, ficam excluídos três tipos de efeito. Primeiro, um alinhamento que reduza a taxa em mais de cerca de 18% ou a aumente em mais de cerca de 10% (contraste PT -> PSL com governador 5 pontos à direita). Segundo, efeitos de distância fora de −5% a +11%. Terceiro, efeitos de copartidarismo fora de −10% a +13%. É a mesma ordem dos limites do painel de governadores (±10% a ±20%).

## O que NÃO dá para concluir
- Que a presidência "não importa": o efeito principal do presidente não é identificável. No painel ele vira efeito de ano. Na série nacional, as 3 trocas ficam confundidas com a queda iniciada em 2018, a COVID, a política de armas, as facções e a piora do SIM.
- Nada sobre violência anti-LGBT. Alinhamento ideológico não é coalizão, repasse nem cooperação policial (não há dado de coalizão em disco). O escore BRC é do partido, não da pessoa.

## Caveats
- 27 clusters; 3 trocas presidenciais no painel (2016 parcial, 2019, 2023) mais a troca de onda do PSL em 2021. Bolsonaro tem só 3 UFs copartidárias.
- D1: 15 pontos e 7 graus de liberdade; o EP clássico ignora a autocorrelação; 2023-24 tem 2 pontos e denominador extrapolado.
- Indeterminadas crescem desde 2018. Por isso as séries de agressão + indeterminada e de razão foram rodadas, e elas atenuam as quedas de 2019 (Brasil: −9,6% contra −17,0%).

## Para o paper e o dashboard
- **Paper:** um parágrafo e uma tabela. Testamos a troca federal de dois jeitos: pelo alinhamento no painel e pela série nacional com placebo. Nenhum dos dois atribui efeito ao presidente; dar o intervalo (−18,3% a +9,6%) e a queda que começa em 2018. Citar o pré-registro e o hash.
- **Dashboard:** a série nacional pode marcar os mandatos como contexto, sempre com a faixa de agressão + indeterminada e a nota "sem atribuição causal; queda iniciada em 2018".
- **Para ganhar poder:** estender o SIM para antes de 2010 (público no DATASUS, ainda não baixado) acrescenta a troca de 2003 (FHC -> Lula; a série em CID-10 começa em 1996). Uma medida de coalizão exigiria dado que não está em disco.

Arquivos: `c09_estrutura.py/.md`, `c09_d2_painel.py`, `c09_d1_its.py`, `c09_resultados.md`, `c09_d2_resultados.csv/.md`, `c09_d1_resultados.csv/.md`, `presidentes_2007_2024.csv`, `tests/test_c09_presidencia.py`, na raiz do repositório (5 testes passam; rodar da raiz com `python3 -m pytest -q tests/test_c09_presidencia.py`).
