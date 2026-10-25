# TRIAGEM dos 4 revisores hostis - dossiê LGBT-INDICADOR (2026-10-23)

> [!NOTE]
> Entrada: 48 ataques (codex 12, grok 12 = 6 direita + 6 esquerda, agy 12, opus 12) sobre o extrato `PACOTE-ESCRUTINIO.md` (sha256 12b61462e48630e7). Saída: 33 clusters em `TRIAGEM.csv` (mesma pasta; 12 colunas: as 9 pedidas + simetria, subpontos_rejeitados, cálculo_especificado). Todo cluster foi conferido contra o dossiê COMPLETO (`DOSSIE-CONSOLIDADO-2026-10-12.md`), as pastas das frentes e `dados/`; os 48 ids estão cobertos (conferido por script). Nada em dossiê ou dado foi editado.

Abreviações: DC = `DOSSIE-CONSOLIDADO-2026-10-12.md`; R3 = `.../research-2026-10-21-rodada3`. Os textos de correção do CSV são literais e prontos para colar; nenhum cria fonte ou número novo (todo número vem de arquivo local citado na coluna de evidência, exceto aritmética simples marcada "derivado" ou "do triagista": razões do Sinan/PNS, conversão exp(5b), teto p = 1, 160 milhões de adultos, 77 de 253).

## 1. Placar

| decisão | P1 | P2 | P3 | total |
|---|---|---|---|---|
| ACEITO-CORRIGIR | 9 | 6 | 0 | 15 |
| PARCIAL | 0 | 6 | 3 | 9 |
| VERIFICAR-ANALISE | 0 | 6 | 1 | 7 |
| ACEITO-LIMITAÇÃO | 0 | 0 | 1 | 1 |
| REJEITADO | 0 | 0 | 1 | 1 |
| FORA-DE-ESCOPO | 0 | 0 | 0 | 0 |
| total | 9 | 18 | 6 | 33 |

Por flanco (1º rótulo do cluster): AMBAS 10, METODOLÓGICO 10, DIREITA 7, ESQUERDA 6. Nenhum ataque factualmente errado no todo; 1 cluster rejeitado (artefato do extrato) e 13 subpontos rejeitados dentro de clusters aceitos (11 linhas da seção 5). Padrão dominante: o corpo do dossiê quase sempre já traz a ressalva; o que cai é a SÍNTESE e os VEREDITOS, que ficaram mais fortes que o corpo.

## 2. Os 10 clusters mais perigosos (ordem de risco)

| # | cluster | problema verificado | decisão |
|---|---|---|---|
| 1 | C16 | Cuba/UMAP entra como "sustentada" em §6.3 e §0.12 com UM artigo de quartil não verificado e rótulo L3, mas o pré-registro (l.41) exige órgão, tribunal ou relatório oficial lido para L3; a Alemanha nazista fica L4 provisório pela mesma falta de primária (correção: Cuba = "L3 PROVISÓRIO" no molde do adendo A6, veredito (b) mundo "provisória"); (a) testa "quer matar" e (b) testa "persegue"; "direita persegue" (Franco, Ley 20/2022; CNV) é sustentada com fonte mais forte e não sobe para a síntese | ACEITO-CORRIGIR P1 |
| 2 | C20 | F4 diz "'Não existe' é falso" (único "falso" do §1.6) saltando de N1/N2 para N4; F1 cita OR 2,52 sem desfecho; a disparidade de vitimização PNS (RP 3,84; ajustada 2,82 [2,16-3,68]; positiva em 18-29, 30-44 e 60+; em 45-59 o IC inclui 1) é o achado brasileiro mais forte e não tem item próprio na síntese | ACEITO-CORRIGIR P1 |
| 3 | C17 | F3 Brasil: "sustentada só em parte" para a direita (retórica + omissão), "não sustentada" para a esquerda embora T3 exista nos dois (Dilma 2011, Temer 2017); busca = 2 consultas para Lula; espaço (12 consultas + 13 normas) não cobre DOU, MPF, STF, polícia, Judiciário | ACEITO-CORRIGIR P1 |
| 4 | C06 | GGB: §1.3 "capta uma fração" x §4.1 "NÃO permitida: concluir que capta só uma fração" x "piso nominal" (§0.10, §2): "piso" é falso pelo próprio §4.1 (31,3% verificáveis; 4,1% LGBTfobia na fonte; critério largo) | ACEITO-CORRIGIR P1 |
| 5 | C01 | "Nenhum efeito do governador" (§0.6, §6.2) = coeficiente nulo lido como ausência de efeito; o próprio §6.2 lista os furos (TWFE contínuo, pesos não calculados, especificação pós-variantes, lead sem poder, 27 de 94 trocas são troca de onda do escore); §0.5 usa régua mais branda para o mesmo tipo de IC | ACEITO-CORRIGIR P1 |
| 6 | C14 | Síntese §0.11 "excesso real só em HIV antes de 1996" apaga SMR 1,33 (1,04-1,68) pós-1995, NHANES AHR 2,32 (1,25-4,30), lésbicas GSS 6,28 (1,45-27,22) e trans (Dhejne aHR 2,8) que o §1.5 mostra | ACEITO-CORRIGIR P1 |
| 7 | C04 | Triangulação PNS x Sinan: "independentes, pela primeira vez... e passa" convive com Sinan fora do IC (razão 0,58); "2x a 3,6x" mistura os dois canais (cenários do Sinan: ~1,7x a 2,7x; 3,65x é a PNS) | ACEITO-CORRIGIR P1 |
| 8 | C21 | F2 "sustentada só em parte": o membro "número absoluto" não tem nenhuma comparação entre países em DC, MIDIA.md ou analises.md | ACEITO-CORRIGIR P1 |
| 9 | C12 | §3 "exatamente o mesmo suporte" e §0.5 "assinatura do registro"; IC90 mal rotulado; teto p = 1 atingido antes de 2030 em S1 e S3; feminicídio tem quebra legal datada (restrição externa) | ACEITO-CORRIGIR P1 |
| 10 | C19 | "não existe / ninguém / nenhum / pela primeira vez" em §0.1, §0.7, §1.2, §1.4, §5.1, §6.2 quebram a regra do próprio cabeçalho (🚫 = busca enumerada); §1.5 perdeu "padronizado" de Zachry | PARCIAL P2 |

## 3. Assimetrias de régua, tom ou ordem encontradas no dossiê (ambos os sentidos)

| # | assimetria | onde | quem é prejudicado |
|---|---|---|---|
| A1 | forma testada: direita "quer matar" (parcial) x esquerda "persegue" (sustentada) | §6.3 (a)/(b), §0.12 | esquerda na síntese; direita fora dela |
| A2 | Cuba L3 com artigo sem quartil x nazismo L4 provisório | §6.3, pré-registro l.41 e adendo A6 | esquerda |
| A3 | Brasil: rótulo "parcial" só para a direita; 2 consultas para Lula x 12 no total | §6.3, §1.6 F3 | direita |
| A4 | vocabulário "falso" só em F4 | §1.6 | direita |
| A5 | "piso nominal" do GGB (favorece a leitura "subconta") contra o resto do §4.1; incentivos do GGB listados, os da Gazeta do Povo só adjetivos | §0.10, §4.1 | direita (críticos do GGB) |
| A6 | IC com zero: "ausência de evidência" (§0.5) x "nenhum efeito" (§0.6) | §0 | esquerda |
| A7 | N3 com proxy para mulheres e 🚫 para LGBT+, mas o N3 não fatal LGB+ existe em `dados/pns/seguro_pns2019.md` §4 (n = 179) | §0 tabela, §1.2 | esquerda |
| A8 | 3 das 4 famílias de afirmação são típicas da esquerda; "F3 dos dois lados" é qualitativo | §1.6 | direita |
| A9 | disparidade de vitimização sem item próprio na síntese | §0 | esquerda e pares |

Leitura: as assimetrias não apontam para um único lado; a correção simétrica é aplicar a mesma célula (forma forte e fraca; mesma busca; mesmo vocabulário) aos dois flancos, como no CSV.

## 4. VERIFICAR-ANALISE (cálculo a rodar com dados locais; NÃO executado aqui)

| cluster | cálculo exato | tabela de saída | critério declarado antes |
|---|---|---|---|
| C02 (P2) | `dados/painel/painel_f8.py` (tse brc, 351 UF-anos) com 3 desfechos novos: log taxa de (agressão X85-Y09 + indeterminada Y10-Y34) por grupo, vinda de `dados/sim/sim_agressoes_agregado.csv`; razão indet/(agressão+indet) como desfecho de falsificação; estimado do Atlas só se houver fonte pública | 6 grupos x [b registrado, b agressão+indet, b razão indet] com IC95% e p wild | se o IC da razão indet for distinguível de zero, o painel registrado não sustenta "sem efeito" |
| C03 (P2) | (1) conversão exata 100[exp(5b)-1] dos limites (aritmética do triagista: -9,5%/+10,5% e -16,5%/+19,7%); (2) event study empilhado nas 68 trocas, sem as 27 trocas de onda, janela -3..+3, controles limpos, direita->esquerda e inverso; (3) pesos do TWFE contínuo (resíduo da ideologia sobre os 2 EF) com % de peso negativo | coeficiente por t com IC95% e n de eventos; % de pesos negativos | lead distinguível de zero invalida a leitura causal |
| C05 (P2) | em `dados/pns/seguro_pns2019.py`: razão de totais ponderados P(LGB+ \| violência física 12 m, 18+) com Taylor (estrato V0024, UPA, peso V00291) + jackknife de UPA; bases (a) todos e (b) só hetero/LGB+; cortes total, 18-29, 30-44, 45+, sexo | estimativa, EP, IC de desenho vs 6,9% (5,3-9,0), 7,1% (5,4-9,3) e Sinan 4,12/4,08 | se o IC direto contiver 4,1%, "discordam na magnitude" cai |
| C08 (P2) | estender `dados/ggb/cobertura_implicita.py` com N0 total, N1 homicídios+latrocínios, N2 = N1 menos todas as pessoas trans (127 em 2023, 67 em 2025; 2024 pelo release); E sob RR 1, 2,82, 3,84; também prevalência 1,96% | ano x numerador x [n, E, cobertura RR=1/2,82/3,84] | cobertura(RR=1) de N2 abaixo de ~15% reforça "GGB = todas as mortes LGB+" inconsistente; N2 é limite, não estimativa |
| C18 (P2) | coleta pública simétrica: mesmo n de consultas web PT/EN por governante, mesmos descritores; transcrição primária da fala de 25/4/2019; Portal da Transparência (Chrome real) | governante x [consultas, T1, T3, T4, T5/T6] | com esforço igual, o veredito F3 passa a ter lista nos dois lados |
| C27 (P2) | recodificar às cegas F2 Parlamento (56), F3 Parlamento (60) e 100 itens sorteados (semente 20261023) por codificador de outra família (assinatura própria do fornecedor); mais linha de base: 60 falas com estatística fora dos 4 temas | kappa de Cohen (IC bootstrap) por campo, matriz de confusão, tabela §1.6 sob cada codificador | kappa < 0,6 em postura ou fonte rebaixa os percentuais a "indicativos" |
| C22 (P3, opcional) | se a API pública do TMM cobre todos os países: total por país 2019-2025, por 100 mil, fração com mesmo coletor | país x ano com posição do Brasil | sempre "ranking de contagens declaradas", nunca de incidência |

## 5. REJEITADOS e subpontos rejeitados (motivo e evidência)

| item | motivo |
|---|---|
| C29 (agy-A4) inteiro: "números órfãos" | artefato do extrato; Sinan 36% x 9% = soma CONJ+EXCON+NAMO da Parte C (35,6% x 8,9%); Baviera 7,4% em Parte B; Espanha 0,007% e UK 54,7% em §5.2; DE 17,6%/BKA em Parte B §3; validação GGB 2019 em §4; Greiner & Rubin 2011 em §1.1. Residual P3: remissões de seção na síntese |
| C01 multiplicidade de 72 coeficientes (codex-A1) | multiplicidade infla falsos positivos; os 72 cruzam zero; vale só a nota de dependência |
| C04 "tabela de cenários ausente" e "régua muda com o sinal" (grok-A1) | a tabela está na Parte C; o §1.3 trava "morrem menos" e "taxa/país que mais mata" com o mesmo argumento |
| C13 "nenhuma taxa é padronizada" (codex-A6, grok-A10) | `dados/sim/asr_brasil.md` existe e confirma a ordem (H/M 10,8; negro/não negro 2,56); o dossiê é que está desatualizado |
| C14 "Q1 nulos contam como nulo" (opus-A6) | o §1.5 já os chama "nulos e sem poder" (n = 85; HR 0,40, IC 0,05-3,05) |
| C15 "quartil não é validade" (codex-A2, opus-A6) | quartil é regra do autor (BRIEFING regra 1), critério de elegibilidade; vira frase de limitação |
| C16 transplantar a regra Q1 do §1.5 para o §6.3 (agy-A1, opus-A1) | são pré-registros distintos; a falha real é interna ao §6.3 (letra de L3) |
| C23 "Espanha 0,007% fora do §5.1" e "Baviera ensina viés" (grok-A6) | está em §5.2 com página; Baviera é auditoria de autos x percepção, com n |
| C25 Wilson sem fração amostral (codex-A10) | é conservador (IC mais largo); o defeito real é IC em linha censitária |
| C12 "identificabilidade não é impossibilidade" (codex-A8) | só redação: o §3 já limita a "sem restrição externa sobre p_t" |
| C20 "três ORs da PNS = mesmo carimbo" (grok-A3) | a matriz §2 já separa ORaj 3,00, RP 3,84, RP aj. 2,82 e ORaj 2,52; só o §1.6 omite o desfecho |
| C32 "triagem de porta impossível" (agy-A11) | não verificado em fonte; fica como aviso |

## 6. Limitações aceitas (frases prontas no CSV) e filtro da REGRA DO AUTOR

- C06/C10: "GGB 2020-2025 não publica lista nominal; ANTRA não publica; contagem inauditável (achado, não pendência)". C15: "o corte Q1 é critério de elegibilidade, não prova de validade". C24: "Spohn 2014, Thoennes & Tjaden 1990 e Baía 2021 só abstract; não decidem conclusão". C26: "um codificador (modelo), mesma sessão; sem linha de base". C28: "famílias vieram da pergunta de pesquisa do projeto; 3 de 4 típicas da esquerda".
- Evidências pedidas pelos revisores e descartadas pela regra (viram "não publicado = inauditável"): lista nominal do GGB 2023-25 (grok-A4, agy-A6), lista da ANTRA (codex-A5), qualquer cópia de autor ou planilha. As coletas propostas em §5.3 e §9 do dossiê ficam marcadas "agenda para quem tiver mandato", sem contato (C32).
- Permitido pela regra e mantido como pendência pública: quartil SJR de Historia Crítica e dos 22 periódicos (Chrome real); varredura SciELO/BVS/CAPES; leitura de Macpherson 1999 em fonte aberta; Spohn só se houver versão aberta.

## 7. O que o dossiê acerta (steel-man consolidado, citado por 2 ou mais revisores)

1. Identificabilidade (§3): com incidência e registro exponenciais, g e h compensam-se exatamente; a série de BO não sustenta nenhuma das duas manchetes (4 de 4 revisores).
2. Escada N1-N4: separa quem morre, disparidade residual, contexto e motivação; tira o chão das duas bancadas (codex, grok, agy, opus).
3. Não independência GGB/ANTRA/TDoR/TMM antes de 2019, com percentuais (72%-94%; 52%-100%) e a ressalva de 2019 (independentes na citação, ambas de mídia) (grok, agy, opus, codex).
4. Autocorreções contra a conclusão anterior: Spearman 0,49-0,74 era tamanho da UF (parcial 0,14-0,32, IC com zero); deff 5,1 (n do survey 5,1x maior); desvio v1/v2 do dicionário declarado (grok, agy, codex).
5. §1.3 publica o número desfavorável (8,8 e 10,0 contra 26,4 e 24,2), declara numerador de mídia e recusa "morrem menos" e "taxa" (grok, codex).
6. Pré-registro com hash, desvios declarados, contagens tratadas como pisos de falas recuperadas (opus, codex).
7. Derruba mitos dos dois lados: Dinno 2017 (8 de 12 RR < 1), Hatzenbuehler 2014 retratado, "2x" é taxa bruta de veteranos, "35 anos" sem fonte primária, 14,70% x 3,82% (agy, opus, grok).
8. Taxonomia falsa provada / não substanciada / retratação ("não provado não é falso") e SIM sem campo de orientação (87 campos) como achado primário (opus, grok, codex).

## 8. Achados da triagem que os revisores não viram

- O consolidado ficou atrás do registro de andamento do projeto em 4 pontos já resolvidos em disco: taxas padronizadas por idade (C13), N3 não fatal LGB+ (C33), RP por faixa etária e ajustada (C20) e a ressalva do Monte Carlo (C05). Corrigir o texto não exige análise nova.
- O PACOTE omitiu §4, §5.2 e a Parte B; dois revisores (agy-A4, opus) atacaram como ausente o que existe. Regerar o extrato antes de nova rodada. O revisor opus declarou não ter aberto GOVERNOS.md, MIDIA.md nem MORTALIDADE.md; a verificação deste arquivo cobriu os três.
- Tarefa de redação consolidada: aplicar os textos do CSV em ordem P1 (C16, C20, C17, C06, C01, C14, C04, C21, C12), depois P2/P3; rodar `dados/verificacao_independente.py` depois das edições e registrar em `LOG-APLICACAO-4.md`.

Becos: (1) `fontes/scimago/sjr2025.csv` é página do Cloudflare, não tabela; o quartil de Historia Crítica continua não verificado, volta se o Chrome real abrir o Scimago. (2) Não li `GGB-completo/vies/` nem as planilhas por UF do Anuário; nada aqui depende delas. (3) Não rodei nenhum dos 7 cálculos (por instrução); o único número novo é a conversão exp(5b), marcada "a conferir no script".
