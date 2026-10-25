# C10 — estrutura do desenho (gerado por c10_estrutura.py; NÃO lê desfecho)

Trocas reais de governador (partido muda E ideologia BRC muda): 67; trocas de onda (mesmo partido, só o escore muda): 27.

| ano da troca | trocas | com janela completa (3+3) | contaminadas (outra troca da UF em e-2..e+2) | UFs de referência sem troca em e-2..e+2 |
|---|---|---|---|---|
| 2013 | 1 | 0 | 1 | 10 |
| 2014 | 6 | 0 | 6 | 10 |
| 2015 | 16 | 16 | 5 | 10 |
| 2017 | 1 | 1 | 1 | 3 |
| 2018 | 8 | 8 | 8 | 9 |
| 2019 | 18 | 18 | 8 | 9 |
| 2022 | 4 | 4 | 4 | 15 |
| 2023 | 12 | 0 | 5 | 15 |
| 2024 | 1 | 0 | 1 | 15 |

Direção por bloco (todas): {'direita->esquerda': 8, 'envolve centro': 8, 'esquerda->direita': 12, 'mesmo bloco': 39}; com janela completa: {'direita->esquerda': 7, 'envolve centro': 7, 'esquerda->direita': 8, 'mesmo bloco': 25}.
Sentido do escore (todas): {'direita': 38, 'esquerda': 29}; com janela completa: {'direita': 25, 'esquerda': 22}.
Janela completa e não contaminada: 21.

Janelas federais (ano-base = último ano completo antes do mandato; ano-fim = último ano completo dentro dele):

| presidente | partido | início | fim | ano-base | ano-fim | tendência pré desde | em curso |
|---|---|---|---|---|---|---|---|
| Luiz Inácio Lula da Silva (2º mandato) | PT | 2007-01-01 | 2010-12-31 | 2006 | 2010 | 2003 | não |
| Dilma Rousseff | PT | 2011-01-01 | 2016-05-11 | 2010 | 2015 | 2007 | não |
| Michel Temer | PMDB | 2016-05-12 | 2018-12-31 | 2015 | 2018 | 2012 | não |
| Jair Bolsonaro | PSL | 2019-01-01 | 2022-12-31 | 2018 | 2022 | 2015 | não |
| Luiz Inácio Lula da Silva | PT | 2023-01-01 | 2024-12-31 | 2022 | 2024 | 2019 | sim |
