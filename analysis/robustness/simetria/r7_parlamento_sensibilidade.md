# R7 — Parlamento (F2): fonte nomeada, fonte primária e fonte capaz de sustentar a afirmação (v0.3, 2026-10-24)

Gerado por `scripts/r7_parlamento_sensibilidade.py` a partir de contagens já gravadas (nenhuma recodificação). Denominador: falas F2 do Parlamento que afirmam ou atribuem o número (AFIRMA + ATRIBUI). Linha de base: 38 falas da Câmara com estatística fora dos 4 temas, codificadas pelo segundo codificador.

| variável | F2 | a/n | linha de base | b/n | mesmo codificador | p (Fisher exato, bicaudal) |
|---|---|---|---|---|---|---|
| fonte primária | original, regra aplicada (relatório tratado como ONG) | 0/49 | base (Grok) | 2/38 | não | 0.1879 |
| fonte primária | original, regra literal do codebook (nome + ano) | 1/49 | base (Grok) | 2/38 | não | 0.5784 |
| fonte primária | segundo codificador (Grok) | 1/50 | base (Grok) | 2/38 | sim | 0.5758 |
| fonte nomeada (qualquer fonte) | original | 8/49 | base (Grok) | 3/38 | não | 0.3350 |
| fonte nomeada (qualquer fonte) | segundo codificador (Grok) | 5/50 | base (Grok) | 3/38 | sim | 1.0000 |

- **Fonte nomeada** (qualquer fonte mencionada): 8/49 no original (7 de ONG, 1 oficial sem referência localizável).
- **Fonte primária** (nome + ano localizáveis): 0/49 pela regra aplicada pelo codificador original; 1/49 pela letra do codebook (um relatório com título e ano, cuja autoria não foi conferida); 1/50 pelo segundo codificador. As duas codificações do original ficam como sensibilidade; nenhuma é "a verdadeira".
- **Fonte capaz de sustentar a afirmação** (a fonte mede o que a fala afirma, por exemplo uma comparação internacional de incidência): **não codificada** como variável. Medi-la exigiria recodificar as 49 falas; fica declarada como não medida.
- Nenhum p acima de 0,05 é prova de equivalência com a linha de base; n pequeno. Só as linhas "mesmo codificador = sim" comparam o mesmo codificador.
