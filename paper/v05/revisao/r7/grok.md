Vou conferir a revisão contra o repositório: o que a matriz diz que mudou e se o texto revisado e os arquivos batem.Faltam três conferências no repositório antes de fechar o parecer: a figura regenerada, o intervalo com correção para população finita e o efeito de desenho.## Verificação

Conferi o corpo da r7 (`paper/v05/MANUSCRITO.md`), o Material Complementar publicado (`paper/v05/MATERIAL-COMPLEMENTAR.md`) e os arquivos citados. Dezenove críticas fecham; cinco ficam em parte. Nenhuma refutação foi rejeitada.

| ID | Status | Por quê |
|---|---|---|
| AST-01 | resolvida | A seção 2.6 diz "23 casos... com 21 pares válidos"; a Tabela MC5.C0 dá κ = 0,91 (condição LGBT+) e κ = 0,46 (morte violenta) nesses 21 pares. |
| AST-02 | resolvida | A seção 3.2 e a nota da Figura 6 dizem "fichas... não marcadas como violência autoprovocada". |
| AST-03 | resolvida | `paper/figures/make_figures.py` (`figura3`) e `paper/figures/fig3_governos_painel_eventos.svg` trazem "deslocamento para a direita" e "(b) Deslocamento do escore". O PNG não foi aberto. |
| AST-06 / GRO-01 | resolvida | Resumo, Abstract e a linha 7 da Tabela 2 limitam os 80% de poder ao aumento relativo de 60,7%; a seção 3.1 declara que o limiar de queda não foi calculado. |
| AST-07 | resolvida | Filho(a)/enteado(a) e viúvos LGB+ estão como "nenhum caso (intervalo não estimável)" (`MATERIAL-COMPLEMENTAR.md`, linhas 219 e 307), com a exceção na nota da tabela. |
| AST-08 | resolvida | O MC11 descreve a pesquisa da FRA como amostra não probabilística pela internet, com 100.577 respondentes (linha 1212). |
| AST-10 | resolvida | A nota da Tabela 6 e o MC10 (linha 1194) dizem "R$ de 2026" e câmbio de 20/10/2026 para o contrato estrangeiro. |
| AST-13 | resolvida | Não há "Tabela MC1.2 de Vasconcelos"; a Tabela MC1.2 é a de hipóteses, e Vasconcelos et al. (2023) entra como reanálise da Tabela 2 deles. |
| GRO-02 | resolvida em parte | Resumo, Abstract, Introdução e a linha 2 da Tabela 2 incluem "ou de outra orientação não heterossexual", e a seção 3.1 diz que o 2,68 não corrige quem deixou de se declarar. O cenário extremo de realocação pedido na r5 não foi feito. |
| GRO-04 | resolvida | A nota da Tabela 3 e a seção 5 trocam "firme" por intervalo nominal que exclui o zero, com 5 vítimas LGB+ e sem correção para comparações; "empregado, patrão ou chefe" e "outro" têm 5 vítimas cada. O "firme" que resta é o de intervalos que incluem o zero. |
| AST-R2-01 | resolvida em parte | O corpo descreve o −21,8% como teste de sensibilidade com a série inteira e as quebras deslocadas, e apoia o início da queda em 31,47 (2017) para 27,61 (2018) (`dados/sim/asr_brasil.csv`). O MC (linhas 87, 770, 774 e 778), a nota da Figura MC6.20 e a Tabela MC6.A13 (linhas 982 a 1012) ainda chamam esse coeficiente de placebo um ano antes da posse. |
| AST-R2-02 | resolvida em parte | A nota da Tabela MC2.A2 declara que a cor ignorada (C009 = 9) entra na referência junto com os não negros (`seguro_pns2019.py`, linha 40). O recálculo sem esses casos não foi feito; o efeito sobre o 2,82 é não verificado. |
| AST-R2-03 | resolvida | A seção 3.6 diz "Entre as mortes por agressão e as de intenção indeterminada, a fatia das indeterminadas". A conta 12.310/(55.914 + 12.310) = 18,04% fecha com os 18,0% de 2018. |
| AST-R2-04 | resolvida | O MC5 (linha 687) trata os antecedentes da LiHS como possível viés intelectual, sem vínculo documentado com a produção da lista, e reserva o vínculo operacional a Mendes e Silva (2020). |
| AST-R2-05 | resolvida | A linha 25 da Tabela 2 diz "Não foi localizado cálculo de expectativa de vida...". |
| AST-R2-06 | resolvida | A linha 2 da Tabela 2 diz que a razão global não identifica o tipo de agressor nem o motivo e que o agressor apontado é analisado à parte. |
| GRO-R2-01 | resolvida | A Introdução e a seção 6 dizem "quatro conclusões", e a seção 6 as numera. |
| ARG-01 | resolvida em parte | A nota da Tabela 6 diz que o efeito de desenho é por desfecho e que os 5.212 e 2.161 adultos LGB+ supõem 1,89% e exigiriam autopreenchimento (3,51% contra 1,38%). `deff_pns2019.csv` tem 5,11 na violência física LGB+ e 3,47 em qualquer violência. O MC10 não foi recalculado com a fração por modo. |
| ARG-02 | resolvida em parte | A seção 3.1 declara o agressor único do episódio mais grave e que o ajuste por cônjuge no domicílio só entrou na violência física geral. O ajuste por coabitação dentro de cada tipo de agressor não foi rodado. |
| ARG-03 | resolvida | Os seis pontos de conteúdo estão no MC publicado (35 anos no MC9; Hatzenbuehler 2020 com o subgrupo; "os 2 desacordos"; 1,35% contra 1,38% na linha 573; Disque 100 em três formatos, linha até 2019 e par vítima-suspeito; "seção 6 do artigo; MC10"; 44,5%). A refutação dos caminhos `../../../../Developer/...` procede: o MC publicado usa `../figures/`, que resolve para `paper/figures/`, onde as figuras do MC estão. |
| ARG-04 | resolvida | É o mesmo acerto de GRO-R2-01. |
| ARG-05 | resolvida | A nota da Tabela MC5.C0 (linha 660) registra a ausência de correção para população finita e o intervalo 26,3% a 36,6%. Wilson com z = 1,96 × √((329−160)/(329−1)) recai em cerca de 26,35% a 36,61%. A raça ignorada está declarada no MC2. |
| ARG-06 | resolvida | Corpo, nota da Tabela 3 e seção 5 falam em "diferença na fatia" de policial; a seção 3.5 e o MC5 dizem que só 3 casos da LiHS tiveram dois revisores e 14 não têm revisor. |
| ARG-07 | resolvida | (i) o denominador está na seção 3.6; (ii) a seção 3.7 e a linha 1131 do MC dão 1 de 50 contra 2 de 38, p = 0,58; (iii) não há citação do Atlas da Violência 2026 em `paper/v05/`, e Kitagawa (1955) está no MC (linhas 89, 459 e 1277) e em `paper/v05/referencias-mc.md`. A seção 2.5 do corpo ainda escreve "Kitagawa" sem ano. |

# Parecer — Grok 4.7 (grok-4.7)

## Avaliação geral

Auditoria de fontes públicas com a pergunta certa: o que cada série mede e o que ela não mede. Os números centrais da PNS, do GGB e do SIM batem com os arquivos do repositório e com a conferência automática do quadro (DIVERGÊNCIAS: 0). A r7 corrige no corpo o que mudava a leitura: denominador da causa indeterminada, teste de 2018, LGB+ com "outra orientação", poder só para aumento, quatro conclusões, agressor único e intervalos nominais. Cinco itens ficam em parte. O Material Complementar ainda apresenta −21,8% como placebo anterior à posse. Não há cenário de subdeclaração. O efeito da raça ignorada não foi recalculado. A Tabela 6 não foi refeita com a fração por modo. O ajuste por coabitação não foi rodado por tipo de agressor. Recomendação: revisão menor. O que resta é alinhar o MC ao corpo e completar análises já declaradas como não feitas.

## Críticas

Nenhuma crítica nova. O ID GRO-R2-01 da matriz é a linha já resolvida das quatro conclusões; não há GRO-R2 desta rodada. O placebo que permanece no Material Complementar é resíduo de AST-R2-01, não regressão.

## Pontos fortes

- A razão 2,82 é razão de prevalência da reanálise, separada das razões de chance de Vasconcelos et al. (2023), e o desenho complexo está declarado.
- A Equação 1 e as três trajetórias dos boletins (783 a 3.481) mostram identificabilidade sem escolher uma história.
- A auditoria do GGB separa caso confirmado (50 de 160), caso não verificável e caso inventado, com Wilson e κ.
- O controle positivo por sexo e raça (51,7 contra 2,6 por 100 mil) delimita o que o SIM mede quando o campo existe.
- Análises feitas depois de ver os resultados, n pequeno e ausência de correção para comparações estão ditos no lugar do número.