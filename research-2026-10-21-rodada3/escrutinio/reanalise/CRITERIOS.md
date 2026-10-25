# CRITERIOS de decisão das 4 reanálises (C02, C03, C05, C08), escritos ANTES de rodar

Projeto: `/Users/ulissesflores/m4/pesquisas/lgbt-indicador-violencia/`. Origem: `research-2026-10-21-rodada3/escrutinio/TRIAGEM.md` (seção 4) e `TRIAGEM.csv` (coluna cálculo_especificado). Python: `/opt/homebrew/bin/python3.14 -I`. Hash e hora de congelamento deste arquivo: `CRITERIOS.sha256` (mesma pasta), gerado com `shasum -a 256` e `date -u` ANTES de qualquer script novo rodar. Nenhuma linha deste arquivo muda depois do congelamento; erro ou desvio vira seção "DESVIOS" em RESULTADOS.md, nunca edição aqui.

Regra geral: resultado que CONTRARIE o dossiê entra como achado nº 1 de RESULTADOS.md. Nenhuma análise abaixo é causal; todas herdam os limites do painel (SIM sem motivação; 27 clusters) e do survey (uma onda, autorrelato). "Distinguível de zero" = IC95% exclui zero E p do bootstrap wild-cluster < 0,05 (C02) ou IC95% de cluster com t(G-1) exclui zero (C03). Não distinguível NÃO é equivalência: toda conclusão "fica" vem com o IC, nunca com "sem efeito" solto.

## 0. Reprodução obrigatória (porta de entrada de cada script; falhar aqui aborta o script)

| análise | número publicado a reproduzir | fonte | tolerância |
|---|---|---|---|
| C02, C03 | b e EP do TWFE por desfecho (6 linhas) e IC95%; BLS9 (6 linhas); p wild-cluster (0,943 0,970 0,951 0,661 0,911 0,970) | `dados/painel/resultados_tse_brc.md`, `dados/painel/diagnosticos.md` (1º bloco) | b e EP em 4 casas; p em ±0,000 (mesma semente 20261021 e mesma ordem de sorteio) |
| C02 | taxas registradas por UF-ano e grupo = `painel_uf_ano_tse_brc.csv`; contagens SIM agressão X85-Y09 por UF-ano e grupo = Atlas (`atlas_uf_series.csv`) | idem | 1e-9 nas taxas; igualdade exata nas contagens (se não bater, o desfecho "agressão+indet" usa só o que bate e a diferença é declarada) |
| C03 | 67 trocas reais + 27 de onda = 94 mudanças de escore no painel BRC; 68 mudanças (37 direita, 31 esquerda) no painel `tse` de escore único | `painel_uf_ano_tse_brc.csv`, `painel_uf_ano_tse.csv` | contagem exata |
| C05 | prevalências do artigo (14,70 / 3,82 / 41,63 / 17,61 / 4,86 / 0,68), RP 3,84 [2,92; 5,06], 442 mil vítimas LGB+; MC pontual 6,90% (cenário B) e 7,13% (cenário A) recalculados dos insumos publicados | `dados/pns/seguro_pns2019.md`, `dados/sinan/triangulacao_pns_sinan.md` | 0,05 p.p. nas prevalências; 0,01 p.p. nos MC |
| C08 | `cobertura_implicita.csv` (agressão e agressão+indet; 2023-24; todas as linhas de RR=1) | `dados/ggb/cobertura_implicita.csv` | esperado ±0,1 morte; cobertura ±0,001 |

## C02 — Painel F8 com desfechos que incluem causa indeterminada

Desenho fixo: variante `tse brc`, 351 UF-anos, ln(taxa) = b x ideologia(0-10) + EF(UF) + EF(ano), EP agrupado por UF (CR1, G = 27), IC95% = b ± 1,96 EP (igual ao publicado) e p wild-cluster-t (Rademacher, H0 imposta, B = 4999; semente 20261021 para a reprodução dos 6 registrados e 20261023 para os desfechos novos). Grupos: total, homens, mulheres, negros, não negros, arma de fogo. Denominadores: os do `painel_f8.py` (SIDRA 6407/6403). Numeradores novos: agressão (X85-Y09) + indeterminada (Y10-Y34) de `dados/sim/sim_agressoes_agregado.csv`, mesma agregação do `agrega_sim.py` (negros = preta+parda; não negros = branca+amarela+indígena; homens = total - mulheres; ignorados fora, como no Atlas).
Desfechos: (i) ln taxa(agressão+indet); (ii) razão indet/(agressão+indet) em PONTOS PERCENTUAIS por UF-ano (modelo linear, mesmos EF) como desfecho de FALSIFICAÇÃO. Tabela: 6 grupos x [b registrado | b agressão+indet | b razão indet], cada um com IC95% e p wild.
Limite já sabido: o agregado só marca `arma` dentro de X85-Y09 (Y22-Y24, disparo com intenção indeterminada, não está marcado), portanto a linha "arma de fogo" fica **n/d** nas colunas (i) e (ii); não se imputa. Estimado do Atlas: não rodado (série pública de estimado por UF-ano não está em disco; fora de escopo declarado). Restam 5 grupos avaliáveis (total, homens, mulheres, negros, não negros).

Regras de decisão (unidade de leitura = a frase do dossiê "o painel não encontra efeito do governador sobre a taxa de nenhum grupo", §0.6 e §6.2):

| leitura | a conclusão FICA | a conclusão CAI ou é REBAIXADA |
|---|---|---|
| (ii) razão, grupo **total** (teste primário de falsificação, alfa = 0,05) | IC95% inclui zero E p wild >= 0,05: a ressalva "homicídio oculto" muda para "teste de falsificação rodado, razão não varia com a ideologia (b, IC)", acompanhado do **viés máximo implícito** em b registrado = -(limites do IC da razão)/(1 - razão média), em % | p wild < 0,05: o painel de óbito registrado **não é válido** para sustentar "sem efeito"; a frase passa a "indeterminado: a classificação da causa varia com a ideologia do governador" (achado nº 1) |
| (ii) razão, demais 4 grupos (secundário; correção de Holm sobre esses 4) | nenhum com p ajustado < 0,05 | algum com p ajustado < 0,05: ressalva específica daquele grupo (não derruba o total) |
| (i) ln taxa(agressão+indet), cada um dos 5 grupos | IC95% inclui zero E p wild >= 0,05 nos 5: "sem efeito" **robusto à inclusão de causa indeterminada** | algum grupo com IC95% excluindo zero E p wild < 0,05: "sem efeito" cai **para aquele grupo** (achado nº 1; reportar também o p de Holm sobre os 5 e dizer que com 5 testes são esperados 0,25 falsos positivos) |
| largura | reportar, por grupo, o limite exato 100[exp(5b)-1] do IC (C03-1) também para (i); não afirmar equivalência | |

Observação de leitura: raça/cor é muito mais ignorada nas indeterminadas que nas agressões; para negros e não negros a coluna (i) e a razão (ii) têm viés de completude (declarar; D4 do diagnóstico já mostra o efeito da completude sobre agressão).

## C03 — Painel: conversão exata, event study empilhado e pesos do TWFE

**(1) Conversão exata.** Para cada um dos 6 desfechos (escore atual/BRC, por ponto) e para BLS9 (por unidade), converter os dois limites do IC95% (b ± 1,96 EP, EP publicado) em 100[exp(k b)-1], com k = 5 pontos (PT 2,97 -> DEM/PL ~8) e, para BLS9, k = distância BLS9 2021 PT -> DEM e PT -> PL lida de `fontes/p2-f8-governos/zucco-power-dataverse/bls9_estimates_partiespresidents_long.tab`. Regra: se algum limite exato diferir do linear (100 k b) em >= 1,0 p.p. no desfecho citado pelo dossiê (total ~±12%, mulheres ~±10%, arma ~±18%), a frase do dossiê **muda obrigatoriamente** para o intervalo exato assimétrico; senão, apenas acrescenta-se "(exato: ...)".

**(2) Event study empilhado (stacked DD).** Evento = troca real de governante: UF-ano em que o PARTIDO do governador (coluna `partido`, partido de eleição TSE) muda E a ideologia muda (Δ != 0). As 27 mudanças de escore por troca de onda no MESMO partido (todas em 2021 na especificação BRC) NÃO são eventos e NÃO contam como contaminação (são medida, não governo). Direção pelo sinal de Δ ideologia (maior = mais à direita): esquerda->direita (Δ > 0) e direita->esquerda (Δ < 0), estimadas SEPARADAS. Painel principal = `painel_uf_ano_tse_brc.csv` (o do dossiê); como o "68 trocas" do dossiê vem do painel `tse` de escore único (68 mudanças, sem trocas de onda), o mesmo exercício roda também nele como conferência (não entra no veredito).
Desenho (estrito, principal): janela -3..+3 completa (evento entre 2015 e 2021); tratado limpo = nenhuma outra troca real da mesma UF em (e-3, e+3]; controles limpos = UFs sem troca real em (e-3, e+3]; desfecho ln(taxa) de total, mulheres, negros, arma; efeitos fixos de UF x pilha e de ano x pilha; coeficientes beta_tau para tau em {-3,-2,0,+1,+2,+3} com tau = -1 como referência; EP agrupado por UF (CR1) e IC95% com t(G-1). Saída: coeficiente por t, IC95%, n de eventos e de controles por direção.
Desenho de sensibilidade (pré-fixado porque o estrito deve ficar com poucos eventos): janela truncada na faixa de ideologia constante, isto é, tau de max(-3, ano da troca anterior - e, 2012 - e) até min(+3, ano da próxima troca - e - 1, 2024 - e), exigindo tau_min <= -2; controles = UFs sem troca em toda a janela usada. Mesmo modelo.
Contagens verificadas em disco ANTES de redigir estas regras (só estrutura do painel, nenhum desfecho olhado): painel BRC = 94 mudanças de escore = 67 trocas de partido com Δ != 0 + 27 trocas de onda no mesmo partido (todas em 2021); painel `tse` de escore único = 68 mudanças (37 direita, 31 esquerda), logo o "68" do dossiê e o "27 de 94" vêm de especificações diferentes; no desenho estrito havia ~19 eventos limpos (cerca de 9 para a direita e 10 para a esquerda) com 6-7 controles limpos, contagem feita com a janela fechada nas duas pontas (a definição final, (e-3, e+3], pode dar um pouco mais). O limiar "n < 10" foi escrito sabendo que cada direção pode ficar perto dele; é por isso que o desenho truncado de sensibilidade está pré-fixado. Leitura PRIMÁRIA = desfecho total, desenho estrito; o teste conjunto (F com G-1 gl, CR1) é anticonservador com poucos clusters, então os IC individuais por tau são sempre reportados ao lado.

Regras de decisão (por direção; leitura primária = desfecho **total**; os outros 3 são descritivos, com Holm de 3 se algum disparar):

| situação | veredito |
|---|---|
| n de eventos < 10 na direção | "inconclusivo: n insuficiente"; o event study não confirma nem refuta; só o IC é reportado |
| teste conjunto das antecipações tau = -3,-2 (Wald agrupado, F(2, G-1)) com p < 0,05, OU qualquer antecipação com IC95% excluindo zero | **a leitura causal do pós é invalidada** (tendência/seleção); o dossiê não pode usar o event study como corroboração |
| antecipações limpas E teste conjunto dos pós tau = 0..+3 (F(4, G-1)) com p >= 0,05 | event study **não contradiz** "sem efeito"; frase = IC do coeficiente médio de pós mais o n de eventos; o limite excluído é o do IC, não "zero" |
| antecipações limpas E teste conjunto dos pós com p < 0,05 | "sem efeito do governador" **cai** para aquela direção (achado nº 1); descrever sinal e magnitude |
| sentidos opostos entre as duas direções, cada um não significativo | lembrar que o coeficiente linear do TWFE mistura as duas trocas |

**(3) Pesos do TWFE contínuo.** Resíduo da ideologia sobre EF de UF e de ano (balanceado: eps = D - D_i - D_t + D_bar). Reportar: % de observações com eps < 0 (mecanicamente ~50% num painel balanceado; não é, sozinho, defeito); massa de peso negativo sob w = eps x (D - D_i) (desvio dentro da UF) e sob w = eps x (D - D_bar); e as inclinações b+ = soma(eps+ y~)/soma(eps+ eps) e b- (análogo com eps < 0), com EP por UF, em que y~ é o desfecho residualizado nos mesmos EF. Se o efeito de D fosse linear e constante, b+ = b- = b_TWFE.
Regra: se b+ e b- têm sinais opostos e AMBOS têm IC95% (t(26)) excluindo zero, o TWFE mistura efeitos de sinais opostos e "sem efeito" fica **indeterminado**; se um ou ambos cruzam zero, nada muda além de a frase "pesos do TWFE não foram calculados" ser substituída pelos números. Razão b_TWFE/b+ só é reportada se |b_TWFE| > 2 EP (senão é razão de ruído e a saída diz isso).

## C05 — PNS 2019: razão de totais P(LGB+ | violência física em 12 meses, 18+)

Estimador: R = soma(w x LGB+ x física) / soma(w x física) com w = V00291, estrato V0024, UPA = V0024 + UPA_PNS, linearização de Taylor de último conglomerado (função `var_from_u` do `seguro_pns2019.py`) e jackknife JKn por UPA dentro do estrato (estratos com 1 UPA saltados, como no Taylor), IC95% de desenho = R ± 1,96 EP (gl da PNS = UPA - estratos ≈ 7.453; z e t são indistinguíveis). Bases: (a) todos os adultos vítimas (denominador inclui quem respondeu "não sabe/recusou" em Y008 e quem não respondeu); (b) só quem declarou hetero ou LGB+ (comparável ao Sinan, cuja parcela é entre orientação válida). Cortes: total, 18-29, 30-44, 45+, homens, mulheres; n bruto de LGB+ vítimas por corte sempre ao lado.
Comparadores: 6,9% (5,3-9,0) e 7,1% (5,4-9,3) do Monte Carlo; Sinan 4,12% (2023) e 4,08% (2024). Decisão (somente base (b), total, que é o teste primário; os cortes são descritivos):

| resultado | veredito |
|---|---|
| IC95% de desenho de (b) total contém 4,12% E 4,08% | "PNS e Sinan discordam na magnitude" **cai**; a frase vira "as estimativas pontuais diferem (PNS x%, Sinan 4,1%), mas o IC de desenho da PNS contém a do Sinan; sem poder para afirmar discordância" |
| IC contém um dos dois e não o outro | frase com os dois números e a leitura de fronteira |
| IC não contém nenhum dos dois | "discordam na magnitude" **permanece**, agora com IC de desenho |
| largura do IC direto de (b) total > 1,25 x a do Monte Carlo (5,43-9,32) | o Monte Carlo **subestimou** a incerteza; o IC de desenho substitui o do Monte Carlo no §1.4/§0.4 |
| Taylor e jackknife com EP que diferem em mais de 20% | reportar ambos e usar o maior |

Mesmo que o IC contenha 4,1%, a comparação continua limitada: o Sinan é registro de quem buscou serviço de saúde (não amostra), com 24% sem orientação preenchida (limites 3,1% a 27,4%).

## C08 — Cobertura implícita do GGB com numeradores comparáveis

Numeradores por ano (releases em `fontes/p3-ggb/_raw/txt/ggb20NN.txt` e `research-2026-10-21-rodada3/GGB-completo/perfil/GGB-O-QUE-E.md`): N0 = total declarado (257, 291, 257). N1 = homicídios + latrocínios declarados, sem suicídios e sem "outras causas": 2023 = 204 + 17 = 221; 2024 = 239 + 30 = 269 (tabela de causa mortis do release; o "273 homicídios" do texto de abertura inclui 4 "outras causas"); 2025 = 204 + 17 = 221 (tabela do release). N2 = N1 menos todas as pessoas trans da tabela de identidade: 2023 = 221 - 127; 2024 = 269 - (96 travestis/trans + 6 homens trans); 2025 = 221 - (46 + 18 + 3). N2 é **limite inferior** do numerador cis LGB (subtrai trans que podem estar fora de N1, como os suicidas, e não subtrai os heterossexuais e os não informados que estão no GGB). Esperado E: o método do `cobertura_implicita.py` (SIM pareado por sexo x raça x faixa, PNS 2019), RR = 1, 2,82, 3,84; prevalência 1,89% e 1,96%. **SIM só existe até 2024**: 2023 e 2024 entram nos vereditos; 2025 recebe só os numeradores e uma linha PROXY (taxas SIM 2024, população extrapolada) marcada como não verificável e fora de qualquer veredito.

Regras (somente RR = 1, prevalência 1,89%, desfecho agressão X85-Y09, por ano com SIM; a faixa real de cobertura do numerador cis LGB está entre cobertura(N2) e cobertura(N1)):

| resultado | veredito |
|---|---|
| cobertura(RR=1) de N0 < 100% e de N1 < 100% | "GGB = todas as mortes LGB+" segue **inconsistente** com risco igual ou maior (o enunciado do §4.1 fica) |
| cobertura(RR=1) de N2 < 15% no ano | reforça a inconsistência: mesmo o limite inferior cis cobre menos de 15% do esperado |
| cobertura(RR=1) de N2 >= 15% em algum ano | a frase "abaixo de ~15% mesmo sem trans" **não pode** ser usada para esse ano; o dossiê cita a faixa [cobertura N2; cobertura N1] do ano |
| N1 de 2024 = 269 em vez de 273 (o `homicidios_decl` 2024 do script antigo) | corrige a coluna "homicídios declarados" (o script antigo usa 221 em 2023 = homicídio + latrocínio, mas 273 em 2024 = homicídio + latrocínio + outras: definições diferentes) |

As regras do C08 são convenção de leitura sobre aritmética determinística (contagens do release / esperado do SIM e da PNS), não teste estatístico; sem IC amostral além do da prevalência (±9%, linear). Contagens das tabelas de causa mortis de 2023 e 2025 (204/20/17/16) conferidas em disco antes de escrever estas regras: são idênticas, e o destaque de 2025 diz "237 homicídios" (= 204+17+16); isso é declarado em RESULTADOS.md como suspeita de reaproveitamento de texto, sem efeito nos vereditos (2025 não tem SIM).

N2 nunca é estimativa de mortes de LGB+; a cobertura é exercício de escala (limites do cabeçalho do script antigo valem integralmente: pareamento só por sexo, raça e idade; menores no numerador; autorrelato; denominador 2023-24 extrapolado).

## Seeds, saídas e rastreio

Sementes: 20261021 (reprodução), 20261023 (desfechos novos). Cada script grava .md e .csv ao lado e uma linha por arquivo em `SHA256SUMS-reanalise.txt` na sua pasta (`dados/painel/`, `dados/pns/`, `dados/ggb/`). Scripts novos (cópias, sem tocar nos existentes): `dados/painel/painel_c02_indet.py`, `dados/painel/painel_c03_event_pesos.py`, `dados/pns/pns_c05_razao_direta.py`, `dados/ggb/ggb_c08_numeradores.py`.
