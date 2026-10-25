# Concordância Sinan x Anuário (LGBTfobia por UF-ano, 2022-2025): CORRIGIDO em 2026-10-21

> [!IMPORTANT]
> A versão de 2026-10-12 (Spearman 0,49-0,74 sobre contagens) NÃO mede concordância: contagem de UF cresce com a população (rho Sinan x pop 0,77-0,89) e duas contagens quaisquer "concordam" por tamanho. A versão corrigida está em `concordancia_v2.md` (gerada por `concordancia_v2.py`).

Resultado corrigido (Censo 2022 como tamanho; IC95% por bootstrap de UFs):
- Correlação parcial de Spearman dado o tamanho: 0,14 (2022), 0,17 (2023), 0,15 (2024), 0,32 (2025); IC95% inclui zero em todos os anos; pooled 0,20 [-0,13; 0,50].
- Correlação de taxas por 100 mil: 0,01 / 0,08 / 0,12 / 0,36.
- O tamanho sozinho prevê 0,45-0,63 dos 0,53-0,74 observados em contagens. O controle de especificidade (Sinan RACISMO x BO LGBT) dá resíduo parecido (pooled 0,14), logo o pouco que sobra não é específico de LGBTfobia.
- Poder baixo (n=22-25; poder 0,69 para rho=0,5): é ausência de evidência de concordância líquida, não evidência de discordância.
- Inalterado: razão mediana BO/Sinan 0,78 (2022) -> 1,21 (2025); `-` no Anuário lido como zero revela candidatos a zero cerimonial (PA 2022-23, TO 2024-25), que a v1 escondia ao tratar `-` como NA.

A tabela original (v1, contagens) fica em `resumo_v1_contagens.md` se o script legado for rodado de novo.
