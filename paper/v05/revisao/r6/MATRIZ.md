# Matriz de respostas da rodada r6 (verificação de Astra e Grok sobre a r6; Argon r6 completo, no navegador)

Manuscrito verificado: `revisao/r6/MANUSCRITO.md` (sha256 `b7107535…`). Corrigido: `revisao/r7/MANUSCRITO.md` (sha256 `db18b029…`). Trava 0 falhas nos 6 blocos; quadro 0 divergências.

## Pendências "resolvida em parte" da r5

| ID | O que faltava | Resposta | Onde |
|---|---|---|---|
| AST-01 | κ em 21 pares, não 23 | "23 casos... com 21 pares válidos" | bloco-2 |
| AST-02 | filtro exclui só a marcação afirmativa | "fichas não marcadas como violência autoprovocada" | bloco-3a (texto e nota da Figura 6) |
| AST-03 | imagem da Figura MC6.18 dizia "Troca de lado" | rótulos "deslocamento para a direita/esquerda"; título "(b) Deslocamento do escore"; só a figura 3 regenerada (`make_figures.figura3`) e o SHA256SUMS da pasta atualizado | repo `paper/figures/` |
| AST-06 / GRO-01 | Tabela 2 linha 7, MC10 | "80% de poder só para aumento relativo"; MC10 texto, nota da Figura MC10.24 | QUADRO-E2 (A15), monta_mc.py |
| AST-07 | viúvos LGB+ 0,00 (0,00 a 0,00); nota "sem alteração" | "nenhum caso (intervalo não estimável)"; a nota da tabela diz a exceção | monta_mc.py |
| AST-08 | MC11 sem a qualificação | "amostra não probabilística pela internet... respondentes" | monta_mc.py |
| AST-10 | MC10.10 "R$ de setembro" | "R$ de 2026; painel = contrato estrangeiro pelo câmbio de 20/10/2026" | monta_mc.py |
| AST-13 | "Tabela MC1.2 de Vasconcelos" | a remissão não se aplica a tabela de outro autor ("Tabela N de Autor") | monta_mc.py (regex) |
| GRO-02 | Resumo, Abstract, Introdução e Tabela 2 só com "lésbicas, gays e bissexuais" | "ou de outra orientação não heterossexual" nos quatro lugares; cenário de subdeclaração segue não feito | bloco-1, QUADRO-E2 (A1) |
| GRO-04 | "firme" na nota da Tabela 3 e na seção 5; n de empregado/patrão | nota e seção 5 dizem intervalo nominal com 5 vítimas, sem correção para comparações; "empregado, patrão ou chefe" e "outro" com 5 vítimas cada | monta_bloco3.py, bloco-4 |

## Críticas novas

| ID | Crítica | Conferência | Resposta | Onde |
|---|---|---|---|---|
| AST-R2-01 | Placebo de 2018 não é estimativa feita antes da posse | `c09_d1_its.py` ajusta à série inteira e desloca as três quebras; `asr_brasil.csv`: 31,47 (2017) -> 27,61 (2018) | Aceita. O início da queda vem dos valores observados; o −21,8% passa a teste de sensibilidade à data | bloco-3c |
| AST-R2-02 | Raça ignorada vira referência na regressão | `seguro_pns2019.py:40` (`negro` = C009 ∈ {2, 4}) | Aceita em parte: declarado no MC2; recálculo sem os ignorados NÃO feito (efeito não verificado) | monta_mc.py |
| AST-R2-03 | "Mortes violentas" no denominador | 12.310/(55.914 + 12.310) = 18,04% | Aceita. "Entre as mortes por agressão e as de intenção indeterminada" | bloco-3c |
| AST-R2-04 | Antecedentes não provam falta de independência | a crítica a Mendes e Silva tem vínculo operacional; a LiHS, não | Aceita. MC5 trata os antecedentes como possível viés intelectual, sem vínculo documentado | mc5-contraponto.md |
| AST-R2-05 | "Ninguém calculou" é negativa universal | regra de ausência do MC1 | Aceita. "Não foi localizado cálculo..." | QUADRO-E2 (A17) |
| AST-R2-06 | "Não mede quem agrediu" contradiz a Tabela 3 | a PNS pergunta quem agrediu (V018) | Aceita. "a razão global não identifica o tipo de agressor nem o motivo; o agressor apontado é analisado à parte" | QUADRO-E2 (A1) |
| GRO-R2-01 | "três conclusões" × quatro | seção 6 numera quatro | Aceita | bloco-1 |

## Mudança na trava

- `reescreve_bloco.py`: CSV de script entra no dicionário de números com as colunas separadas antes da troca do ponto decimal (antes, "2017,31.47" não virava "31,47"); `asr_brasil.csv` entra como fonte do bloco 3c.

## Argon (revisão completa da r6, pelo navegador; parecer em `revisao/r6/argon.md`)

| ID | Crítica | Conferência | Resposta | Onde |
|---|---|---|---|---|
| ARG-01 | Tabela 6: efeito de desenho por desfecho e identificação LGB+ dependente do modo | `deff_pns2019.csv`: física LGB+ 5,11; qualquer 3,47; `agressor_risco_pns2019.md` §5: 3,51% × 1,38% | Aceita. Nota da Tabela 6 diz que o efeito de desenho é por desfecho e que o número de LGB+ supõe 1,89% e exigiria autopreenchimento privado. MC10 não recalculado com a fração por modo | bloco-4 |
| ARG-02 | V018 = um agressor (episódio mais grave); razão por familiar sem coabitação | `seguro_pns2019.md` §4 "episódio mais grave"; ajuste por C01001 só na física geral | Aceita em parte: as duas limitações declaradas na seção 3.1; ajuste por coabitação por tipo de agressor NÃO rodado | bloco-3a |
| ARG-03 | MC contradiz o corpo em 6 pontos | conferidos no MC | Aceita: 35 anos (MC9), Hatzenbuehler 2020 com o subgrupo (MC4), "os 2 desacordos" na Tabela MC5.C0, 1,35% × 1,38% explicado (MC5), Disque 100 (três formatos; linha até 2019; par vítima-suspeito), "(seção 4.4)" → "seção 6 do artigo; MC10", 44,5%. "Tabela MC1.2 de Vasconcelos" já corrigida na r7. Caminhos `../../../../Developer/...`: refutação — vale só para a cópia de trabalho; a cópia publicada em `paper/v05/` usa `../figures/` (o pacote do revisor trazia a cópia de trabalho) | monta_mc.py |
| ARG-04 | "três conclusões" | já corrigido (GRO-R2-01) | Aceita | bloco-1 |
| ARG-05 | Wilson sem correção para população finita; raça ignorada na regressão | recalculado: com FPC, 26,3% a 36,6% | Aceita: nota da Tabela MC5.C0; raça ignorada declarada no MC2 (AST-R2-02) | mc5-contraponto.md, monta_mc.py |
| ARG-06 | "fatia" × "diferença na fatia" de policial; "cada caso um revisor" | `agressor_risco_pns2019.md` §1; planilha LiHS: 3 com dois revisores, 14 em branco | Aceita (corpo, nota da Tabela 3, seção 5, MC5) | bloco-3a, bloco-3b, bloco-4, monta_bloco3.py |
| ARG-07 | denominador da causa indeterminada; segundo codificador nos dois grupos; Atlas 2026 órfão; Kitagawa sem ano | MC9.A18: 1/50 × 2/38, p = 0,58 | Aceita: (i) já na r7; (ii) frase na seção 3.7; (iii) Atlas 2026 sai de referencias-mc.md; "Kitagawa (1955)" no MC | bloco-3c, monta_mc.py |
