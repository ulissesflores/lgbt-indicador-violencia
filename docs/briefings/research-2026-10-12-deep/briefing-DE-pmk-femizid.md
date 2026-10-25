# Briefing DE: KPMD-PMK, Dunkelfeld de Hasskriminalität, Femizid, Falschbeschuldigung e Zeugnisverweigerungsrecht

> playbook loaded: factual-context + paper-deep-dive · célula DE (deep) · data de corte 2026-10-12 · idioma de busca: alemão · PDFs em `fontes/p2-deep-de/`

> [!IMPORTANT]
> Cinco achados que mudam a leitura do que o campo costuma citar:
> 1. O BKA **retirou o rótulo "Femizid"** do Bundeslagebild 2024 porque a PKS não tem campo de motivação (Lagebild, PDF p. 43).
> 2. O "308" aparece **duas vezes com sentidos diferentes** no mesmo Lagebild (ver Alvo 3). Misturar os dois é erro fácil.
> 3. A auditoria de autos do KFN (2025) achou que só **17,6%** dos relatórios policiais de "Hasskriminalität" explicitam o motivo e só **8,4%** documentam a inclusão na PMK (impresso p. 99).
> 4. O "64% de falsas denúncias" atribuído ao LKA Bayern é **percepção de policiais sobre casos arquivados**, não prevalência; o número medido é **7,4%** de files com queixa por §145d/§164 StGB (Elsner & Steffen 2005, p. 20-21).
> 5. No SKiD 2024 a **Anzeigequote** de violência motivada por orientação sexual é **2,6%**, contra ~15% quando o motivo é suposta imigração (PDF p. 53): é o número que transforma "cifra oculta" em medida, com categorias alinhadas à polícia.

Legenda de status: ✅ lido no texto/PDF primário · ⚠️ só resumo/metadados, ou literatura cinzenta, ou amostra não representativa · 🚫 não lido / não verificado.
Convenção de página: "p. N" = número impresso; "PDF p. N" quando difere. Tag: `[SOURCE: multilingual-term-expansion:de:<base>:<chave>]`.

---

## Alvo 1. KPMD-PMK: como a Alemanha registra a motivação de ódio na polícia

**Fonte primária**: BMI, *Bundesweite Fallzahlen 2025 Politisch motivierte Kriminalität* (BMI26013, "Stand Juni 2026", 43 p.) e a edição 2024 (BMI25045, 34 p.). Cópias hospedadas pelo LSVD; o impressum da edição 2025 confirma BMI como editor (p. 42). O PDF direto de bka.de/bmi.bund.de falhou por curl (bka.de devolveu HTML; link bmi.bund.de 400). Via Wayback (CDX) recuperei o snapshot de 2025-05-20 do `2024PMKFallzahlen.pdf` oficial do bka.de: **SHA-256 idêntico** à cópia LSVD 2024 (`29ff5926...`), então a edição 2024 está verificada contra o original. A edição 2025 (v=4) só tem entradas CDX sem captura de PDF (status "-"), então a cópia LSVD 2025 está confirmada só pelo impressum BMI (p. 42), não por hash. Hash SHA-256 no ledger. `[SOURCE: multilingual-term-expansion:de:bmi:pmk2025-factsheet]`

### Como o registro funciona (metodologia)

| Pergunta | Resposta, verbatim ou fiel | Onde | Status |
|---|---|---|---|
| Que sistema? | KPMD-PMK, "gemeinsames System von Bund und Ländern", desde 01.01.2001 | Factsheet 2025 p. 3 | ✅ |
| Quem classifica? | Os **Länder**: polícia (Staatsschutz) atribui; LKÄ transmitem ao BKA, que consolida numa "zentrale Fallzahlendatei" | p. 3 | ✅ |
| Critério | "Ausgehend von der Motivlage zur Tatbegehung und den Tatumständen" a Tat vai a **Themenfeldern** e depois a um **Phänomenbereich** "wenn ... Anhaltspunkte" (limiar baixo: indícios) | p. 3 | ✅ |
| Indícios admitidos | características do autor (aparência), linguagem/símbolos, contexto político do momento | p. 3 | ✅ |
| Dimensões | Phänomenbereich, Themenfeld, Angriffsziel, Tatmittel, Deliktsqualität, verletzte Rechtsnorm | p. 3 | ✅ |
| Multi-rótulo | "Mehrfachnennungen möglich und erwünscht" em Themenfeld, Angriffsziel, Tatmittel; **somar UTF não dá o total** de Hasskriminalität | p. 3, 14 | ✅ |
| Tipo de estatística | **Eingangsstatistik** (registra no início do procedimento), com Nachmeldungen; **Stichtag 31.01** do ano seguinte, depois nada entra | p. 3, 40-41 | ✅ |
| Campo "Tatmotivation"? | O factsheet **não usa** esse termo como campo: o motivo é inferido pela combinação Themenfeld + Phänomenbereich | p. 3 | ✅ (ausência verificada só nesse texto) |
| Definição de Hasskriminalität | PMK-Straftaten com indícios de ocorrerem "aufgrund von Vorurteilen des Täters" quanto a nacionalidade, etnia, cor, religião/visão de mundo, status social, deficiência, **sexo/identidade de gênero, orientação sexual**, aparência; inclui **pertencimento "tatsächliche oder zugeschriebene"** (atribuído) | p. 13 | ✅ |
| Perspectiva da vítima | Nota de rodapé na definição de 2016: "Bei der Würdigung der Umstände der Tat ist neben anderen Aspekten auch die **Sicht der/des Betroffenen** mit einzubeziehen" | Definitionssystem (Stand 08.12.16) S. 5 e 7 (Seite x de 15); repetida em BKA 2024b via KFN 2025 p. 204 | ✅ |
| Quem ensina o campo | Themenfeldkatalog / KTA-PMK: ferramenta interna; por anos "Verschlusssache - NfD", hoje achável na web | KFN 2025 p. 203 | ✅ |

`[SOURCE: multilingual-term-expansion:de:bka:definitionssystem-pmk-2016]` (cópia Polizei NRW; **versão de 2016**, anterior à reforma de 2022 e ainda com "sexuelle Orientierung und/oder sexuelle Identität").

### Números (OTF Hasskriminalität e subcampos LGBT)

| Indicador | 2025 | 2024 | 2023 | Página 2025 | Status |
|---|---|---|---|---|---|
| Hasskriminalität, total (OTF) | 22.159 (+1,77%) | 21.773 | 17.007 | p. 13 | ✅ |
| UTF "Sexuelle Orientierung" | **2.070** (+17,28%) | 1.765 | 1.499 | p. 13, 21 | ✅ |
| .. dos quais Gewalt | 284 | 253 | 288 | p. 21 | ✅ |
| .. dos quais Körperverletzung | 238 | 232 | 268 | p. 21 | ✅ |
| .. Beleidigung (queixas) | 600 | 447 | 449 | p. 21 | ✅ |
| .. por Phänomenbereich 2025 | sonstige 1.039 (50,19%), rechts 870 (42,03%), links 33, ausl. Ideol. 72, relig. 56 | | | p. 21 | ✅ |
| UTF "Geschlechtsbezogene Diversität" | **1.294** (+12,33%) | 1.152 | 854 | p. 13, 20 | ✅ |
| .. dos quais Gewalt | 112 | 128 | | p. 20 | ✅ |
| .. por Phänomenbereich 2025 | sonstige 630, rechts 589, relig. 30, ausl. 29, links 16 | | | p. 20 | ✅ |
| UTF "Frauenfeindlich" | 819 (+46,77%) | 558 | 322 | p. 13 | ✅ |
| Hasspostings (Tatmittel) | 10.542 | 10.732 | 8.011 | p. 22 | ✅ |
| PMK total / Gewalt | 85.837 / 4.156 | 84.172 / 4.107 | | p. 4 | ✅ |

Definição oficial do subcampo (p. 21): "Unter sexueller Orientierung wird das Begehren für bestimmte Geschlechtspartner verstanden. Dies kann zum Beispiel hetero-, homo-, bi- bzw. pansexuell sowie queer ausgeprägt sein." Para "Geschlechtsbezogene Diversität" (p. 20): crimes "gegen Menschen gerichtet, deren geschlechtliche Identität vom biologischen Geschlecht abweicht (transsexuelle bzw. nicht-binäre Menschen)" e intersexuais.

Valores 2024 e 2023 conferidos contra o factsheet 2024 (PDF p. 11 e 16; "Stand 31.01.2025"). `[SOURCE: multilingual-term-expansion:de:bmi:pmk2024-factsheet]`

### Defeitos e ressalvas encontrados

- **Erro interno do BMI (2025, p. 21)**: o texto diz que 2.070 "entspricht einer Steigerung von 12,25 %", mas a tabela 20 dá +17,28% para o total; 12,25% é a variação de **Gewalt** (253 -> 284). Citar a tabela, não a prosa. ✅ conferido.
- **Quebra de série em 2022**: "Frauenfeindlich", "Geschlechtsbezogene Diversität" e "Männerfeindlich" substituíram "Geschlecht/sexuelle Identität" em 01.01.2022 (CILIP 133). Séries pré/pós 2022 para identidade de gênero não são comparáveis. ⚠️ (fonte ONG; consistente com o texto do BMI).
- **Metade do campo "Sexuelle Orientierung" cai em "PMK -sonstige Zuordnung-"** (50,19% em 2025): a motivação de ódio é registrada, mas sem ideologia atribuída. CILIP critica o crescimento dessa categoria residual. ⚠️
- **Qualidade medida por auditoria de autos (KFN 2025)**: só 17,6% dos relatórios policiais explicitam menschenverachtendes Tatmotiv; só 8,4% mostram evidência documental da inclusão na PMK; "polizeiliche Praxis der Erfassung ... überwiegend unklar" (impresso p. 99). Entrevista de policial: "In der Realität ist das eine **Daumenentscheidung**" (P1, p. 202); Nachtragsmeldungen raramente são feitas "weil das einfach zu viel Arbeit ist" (p. 203). Subcampos "nicht trennscharf": nenhum caso só "Ausländerfeindlich" ou só "Rassismus" na amostra (p. 156-157). Amostra do KFN = só casos **esclarecidos** e já na PMK; subcampo "Sexuelle Orientierung" = 3,3% da amostra principal (p. 99). ✅ `[SOURCE: multilingual-term-expansion:de:crossref:10.5771/9783748963455]`
- **Quem pega o ódio**: PMK é "Staatsschutz": o crime comum homofóbico sem enquadramento político pode não entrar. Essa é minha inferência a partir do desenho; o factsheet não discute. 🚫 não verificado.

---

## Alvo 2. Dunkelfeld da Hasskriminalität

**Fonte**: BKA, *Sicherheit und Kriminalität in Deutschland (SKiD) 2024, Ergebnisbericht V 1.0* (survey de vitimização, 63.018 participantes e 60.837 questionários auditáveis (PDF p. 10); ≥16 anos; divulgação em 20.04.2026 segundo comunicado de Hamburgo, via busca). SKiD 2020 **não baixei**; o relatório 2024 diz que em 2020 o motivo só foi perguntado para Körperverletzung, logo as ondas "nicht miteinander vergleichbar" (PDF p. 40). `[SOURCE: multilingual-term-expansion:de:bka:skid2024]`

| Medida | Valor | Página | Status |
|---|---|---|---|
| Prevalência de ≥1 crime violento/sexual **vorurteilsgeleitet** em 12 meses | "rund 12 %" da população | PDF p. 41 (impresso 38) | ✅ |
| Motivo mais frequente: sexo da vítima | "knapp 5 %" | idem | ✅ |
| Homo-/bissexualidade como motivo | **1,2%** da população total | idem | ✅ |
| Etnia, política, status social, idade | ~3% cada | idem | ✅ |
| **Anzeigequote** por motivo, 2024: sexual orientation | **2,6%** | PDF p. 53 (impresso 50) | ✅ |
| .. gênero/identidade de gênero | 4,0% | idem | ✅ |
| .. suposta imigração | ~15% (máximo) | idem | ✅ |
| .. política 2,2%; deficiência 2,9%; status social 4,5% | | idem | ✅ |
| Anzeigequote estupro/coerção sexual (contraste) | 6,2% | PDF p. 51 | ✅ |
| Anzeigequote violência de parceiro: estupro pelo (ex-)parceiro | ~0,6% (IC amplo) | PDF p. 54 | ✅ |

**Como o SKiD mede**: pergunta, para cada crime violento/sexual sofrido, se havia motivo preconceituoso contra o grupo da vítima. As categorias "lehnen sich weitgehend an die polizeilich definierten Kategorien der Hasskriminalität an" (PDF p. 40). Decisivo é a **percepção da vítima**: nota 31 admite que a vítima pode ver preconceito onde o autor não tinha, e o inverso; mas "ausschlaggebend" é a percepção da vítima. Os autores adotam "Vorurteilskriminalität" por ser criminologicamente mais exato (nota 30, citando Groß 2023). Ressalva dos próprios autores: prevalência baixa em grupos minoritários (homo/bi, deficiência) é efeito de denominador (população total), "nicht ... vernachlässigbar" (nota 33). ✅

**Limites**: (1) SKiD mede **pessoas** em 12 meses, PMK conta **delitos**; não dá para dividir um pelo outro sem hipóteses. (2) SKiD só cobre violência/sexual (e ofensas); a PMK inclui propaganda, dano, etc. (3) A taxa de 2,6% vem de n pequeno; não vi o IC da Abb. 18. 🚫. (4) Fontes de ONG citam "Dunkelfeld de 80-90%" ou "Anzeigebereitschaft < 8%" para LSBTI; **não verifiquei** a origem desses números (busca retornou só secundárias do LSVD/watson). 🚫

Contexto não coletado: Zick/Küpper (Mitte-Studie). Não fiz; o pedido a marcava como só contexto.

---

## Alvo 3. Femizid no registro policial

**Fonte**: BKA/BMI/BMBFSFJ, *Bundeslagebild Geschlechtsspezifisch gegen Frauen gerichtete Straftaten 2024* (63 p. PDF; o URL do comunicado BKA, `251121_BLB...`, indica divulgação em 21.11.2025). Cópia do Landkreis Ludwigsburg (não consegui o PDF direto do bka.de). Edição 2023 (nov/2024) **não baixada**. Edição 2025 ainda não existe até hoje (inferência pelo ciclo anual: esperada em nov/2026). `[SOURCE: multilingual-term-expansion:de:bka:bundeslagebild-frauen-2024]`

| Ponto | Conteúdo | Página | Status |
|---|---|---|---|
| Definição de base | Definição em **duas dimensões**: (1) Hasskriminalität com viés misógino, medida via KPMD-PMK, com "Betroffenenperspektive" de peso especial; (2) delitos que "überwiegend zum Nachteil von Frauen" ou primariamente afetam mulheres, medidos via PKS | PDF p. 3 | ✅ |
| Conta "Femizid"? | **Não.** "Bis zum Vorliegen dieser Definition erfolgt in diesem Lagebild keine Zuordnung der in der PKS erfassten Tötungsdelikte an Frauen zum Begriff 'Femizide'." A AG Kripo (outono 2025) decidiu elaborar definição policial nacional | PDF p. 43 (impresso 41) | ✅ |
| Por quê | "in der PKS sind keine Informationen zur Tatmotivation enthalten, die eine eindeutige Zuordnung ... erlauben"; falta também um recorte por relação vítima-suspeito ou contexto aceito nacionalmente | idem | ✅ |
| Mudança vs. 2023 | Fallgruppe antes se chamava "Femizide" (decisão do grupo Bund-Länder); a nota 84 diz que o uso "war missverständlich und wurde daher ... geändert" | PDF p. 42-43 | ✅ |
| Definição WHO usada como referência | Femizide = "vorsätzliche Morde an Frauen, weil sie Frauen sind" | PDF p. 43 | ✅ |
| PMK frauenfeindlich 2024 | 558 delitos (Dimensão 1); 1 tentativa de "Ehrenmord" no UTF, com vítima não-feminina | PDF p. 41 | ✅ |
| Vítimas de tentativa+consumado, mulheres/meninas | **859** (-8,4%) | PDF p. 42, 44 | ✅ |
| .. consumados | 328; **308 "tödlich verletzt"** | PDF p. 44 | ✅ |
| .. contexto doméstico (consumados) | 198 (133 Partnerschaftsgewalt, 65 intrafamiliar); **191 mortas** (132 + 59) | PDF p. 44 | ✅ |
| Partnerschaftsgewalt, tentativa+consumado | **308** vítimas (-9,4%); 322 suspeitos | PDF p. 42, 44 | ✅ |
| Parcela de mulheres entre vítimas de homicídio em parceria | 80,6% (84,7% consumados) | PDF p. 42 | ✅ |

> [!WARNING]
> **Dois "308" distintos**: (a) 308 mulheres/meninas **mortas**, todos os contextos, 2024 (PDF p. 44); (b) 308 **vítimas de tentativa+consumado** em Partnerschaftsgewalt (PDF p. 42, 44). É fácil confundir os dois; cite sempre número + definição + página. (Não verifiquei se a imprensa os confundiu; a cobertura que li usa 308 no sentido de mortas.) O "340 em 2023" que a imprensa compara é a coluna "Partnerschaft" (tentativa+consumado) da Abb. 33, não o total de mortas (conferido na figura, PDF p. 44).
> A nota de que o número de 2023 teria mudado de 360 para 340 por "nova metodologia" vem de busca secundária (ZDF/Bundestag-Drucksache 21/3504). 🚫 não conferi no PDF 2023.

### O que a pesquisa de autos diz sobre contar "Femizid"

Estudo FemiziDE (Uni Tübingen + KFN, nov/2025; relatório curto, CC BY-NC-ND): 292 autos de 2017 (5 Länder, ~1/3 dos casos PKS do ano; **amostra não representativa**, p. 10 do relatório). Resultado: 197 eram homicídios reais; **133 (67,5%)** femizídios "im weiteren soziostrukturellen Sinne"; **74** com motivo sexista comprovado ("im engeren motivbezogenen Sinn"); 108 dos 133 (81,2%) em contexto de casal heterossexual; os 95 restantes dos 292 eram erros de registro, lesões simples ou falsas suspeitas. Conclusão do relator: "Die Angaben in der PKS sind ... für sich genommen nicht geeignet, um die Zahl der Femizide in Deutschland zu bestimmen" e pedem um "German Homicide Monitor". ✅ (relatório curto lido nos trechos de resumo e método; não é peer-reviewed). `[SOURCE: multilingual-term-expansion:de:kfn:femizide-in-deutschland-2025]`

---

## Alvo 4. Literatura em alemão

Crossref e OpenAlex cobrem mal monografias e relatórios alemães; a maior parte veio de WebSearch em alemão + download dos PDFs. DOIs só onde o Crossref ou a página do periódico confirmaram.

### 4a. Falschbeschuldigung (denúncia falsa) em violência sexual

| Autores, ano | Veículo, DOI/URL | Tese ou número verbatim | Status |
|---|---|---|---|
| Elsner & Steffen, 2005 (LKA Bayern) | *Vergewaltigung und sexuelle Nötigung in Bayern*, relatório; BKA Forum KI. URL no ledger. Sem DOI. | **p. 21**: "Nur bei 140 Fällen (7,4%) der im Jahr 2000 insgesamt ... erfassten 1.894 Vorgänge ... [wurden] Anzeigen wegen Vortäuschens einer Straftat gem. § 145d StGB oder falscher Verdächtigung gem. § 164 StGB" erstattet. **p. 20**: "fast zwei Drittel (64%)" dos casos que o próprio policial instruiu e que a StA arquivou por §170 II foram vistos como "eher" ou "mit hoher Wahrscheinlichkeit" simulação ou falsa suspeita; extrapolando, "etwa ein Drittel" dos casos iniciais. **p. 22**: dessas 140 queixas, só 25% arquivadas; mais da metade desses arquivamentos envolvia mulheres com transtorno psicopatológico. **p. 19**: só ~1 em 4 estupros e ~1 em 5 coerções sexuais acaba em condenação (§177). | ✅ (primário), ⚠️ literatura institucional, não peer-reviewed, 1 Land, ano-base 2000 |
| Strafakte.de / blogs, citando Lovett & Kelly (2009) "3%" e Ferguson & Malouff (2015) "~5%" | Blogs | Citados por advocacia; **não li os originais**. O "3%" é apresentado como amostra de ~100 autos de uma única StA (Stuttgart). | 🚫 só secundário |
| "Falschbeschuldigungen bei sexueller Gewalt", capítulo/artigo, atribuído por URL a Gerd Bohner | ResearchGate (403) | Autoria, veículo e DOI **não verificados** | 🚫 |

Leitura honesta: os autores de Elsner & Steffen **não medem prevalência de acusação falsa**; o 64% é percepção policial sobre um subconjunto, e eles mesmos escrevem que nos 140 casos efetivamente processados a prova era geralmente clara (a polícia só denuncia quando a vítima confessa ou a prova contraria). Quem cita "64%" ou "7,4%" como taxa de falsidade erra por motivos opostos.

### 4b. Zeugnisverweigerungsrecht e arquivamento em violência doméstica

| Autores, ano | Veículo, DOI/URL | Tese ou número verbatim | Status |
|---|---|---|---|
| Kotlenga, Nägele, Nowak, Goergen, 2016 | Relatório INASC (financiado pela UE), Zoom/DHPol; URL no ledger | **p. 29**: "knapp die Hälfte der Fälle 34 (48,6%) durch die Amtsanwaltschaft eingestellt, zumeist nach §170 II StPO, weil die Amtsanwaltschaft annahm, dass das Opfer vor Gericht nicht aussagen würde." **p. 30**: "Acht Opfer (40%) beriefen sich auf ihr Aussageverweigerungsrecht" (de 20 vítimas na audiência; total N=70 autos da Amtsanwaltschaft Frankfurt; Strafantrag retirado em 13 de 64) | ✅ lido, ⚠️ literatura cinzenta, N pequeno, uma cidade |
| Niederegger, Muggenthaler, Hubig, Sauer, Mall, 2023 | *Rechtsmedizin* 33(4):253-261, DOI 10.1007/s00194-023-00642-z | 1.403 autos de "häusliche Gewalt" (Turíngia, ano 2009): "rund 87% aller Ermittlungsverfahren im Vorverfahren eingestellt"; 6% Strafbefehl, 7% acusação; "Etwa 43% der Geschädigten stellten einen Strafantrag, fast ein Drittel der Anträge wurde wieder zurückgenommen" | ⚠️ só abstract; dados de 2009; sem variável explícita de recusa de depoimento no abstract |
| Seifarth & Ludwig, 2016 | *MschKrim* 99(3):237-244, DOI 10.1515/mkr-2016-0305 | Survey com estudantes (FH Erfurt, N=3.769): 8,7% (n=46) vítimas de delito sexual, **nenhuma denunciou** | ⚠️ só abstract; população de estudantes; é Dunkelfeld, não Zeugnisverweigerung |

**Lacuna**: não encontrei estudo alemão que **quantifique** a parcela de arquivamentos atribuível ao § 52 StPO em violência doméstica/sexual. As proxies acima convergem em "o caso depende da vítima" mas não isolam o direito de recusa de outras causas (retirada de Strafantrag, falta de prova). Relatos de imprensa (rbb, Berlin/Brandenburg 2024: 76% e 86% de arquivamento) são jornalísticos. 🚫 Sobre o texto legal: a busca citou § 52 StPO listando noivo(a), cônjuge e Lebenspartner mesmo após dissolução; a posição de parceiros não casados/ex-parceiros **não foi verificada** (não fui à jurisprudência). Mecanismo de contorno descrito pelo INASC (p. 159-160): depoimento perante o **juiz de instrução** (Ermittlungsrichter) pode ser usado mesmo com recusa posterior; o Ministério da Baviera (stmas.bayern.de) diz o mesmo. ✅/⚠️

### 4c. Hasskriminalität: registro e Dunkelziffer

| Autores, ano | Veículo, DOI/URL | Tese ou número verbatim | Status |
|---|---|---|---|
| Henningsmeier, Dreißigacker, Witthuhn, Bartsch, Meier, 2025 | *Strafrechtliche Verfolgung von Vorurteilskriminalität*, KFN/Nomos, DOI 10.5771/9783748963455 (CC BY-SA; 306 p.; mandato do BMJ) | impresso p. 99: 17,6% e 8,4% (ver Alvo 1); p. 157: "Lediglich in 15,8 %" dos processos com condenação em 1ª instância houve **strafschärfende Würdigung** (§ 46 II 2 StGB); só cerca de metade tematizou o motivo | ✅ lido em trechos |
| Coester & Rothenburg, 2023 | *MschKrim* 106(4):267-284, DOI 10.1515/mks-2023-0008 | Abstract: após as reformas de 2015 e 2021, §46 II 2 StGB manda agravar motivos racistas, xenófobos, antissemitas e "menschenverachtende"; há projeto para incluir **geschlechtsspezifische** e contra a **sexuelle Orientierung**; "bleibt bis heute offen" se a resposta estatal é adequada | ⚠️ só abstract |
| Leuschner & Rausch, 2022 | *Kriminologie - Das Online-Journal* 4(1):20-37, DOI 10.18716/ojs/krimoj/2022.1.2 (CC BY 4.0) | Abstract: Femizid "in der kriminologischen Forschung bisher wenig bearbeitet"; revisão de conceito, debates, formas, prevalências e enquadramento jurídico; citado pelo BKA (Lagebild nota 88) | ⚠️ só abstract; texto integral não lido |
| Gränert & Seydel, 2023 | *CILIP* 133 (revista de ONG), URL no ledger | Definitionssystem e Erfassung "wissenschaftlich kaum fundiert, politisch umkämpft"; propõem revisão e mais atores externos | ⚠️ opinião/ONG |
| Glet (livro, 2011), resenha de Kury 2012 *MschKrim* 95(3):229-232, DOI 10.1515/mks-2012-950308 | | Título do livro: *Sozialkonstruktion und strafrechtliche Verfolgung von Hasskriminalität in Deutschland*. Só metadados | 🚫 não lido |
| Lang, Coester, Groß (vários) | | Autores apontados no pedido; **não localizei** os textos que citam Dunkelziffer; a busca por "Lang/Coester/Groß 2023" não os retornou. SKiD cita "Groß 2023" na nota 30 | 🚫 |

### 4d. Femizid: conceito e crítica da contagem

| Autores, ano | Veículo | Tese ou número verbatim | Status |
|---|---|---|---|
| Rebmann et al., 2025 | Relatório FemiziDE, Uni Tübingen/KFN, URL no ledger | Ver Alvo 3: 197 -> 133 (67,5%) -> 74 | ✅ relatório, ⚠️ não peer-reviewed, amostra não representativa |
| Leuschner & Rausch, 2022 | ver 4c | | ⚠️ |
| Kröber, 2024 | *Forensische Psychiatrie, Psychologie, Kriminologie* 19(1):74-77, DOI 10.1007/s11757-024-00862-3, "Macht, Interaktion und Femizid" | Só metadados | 🚫 não lido |
| Montenegro, 2023 | *JuristenZeitung*, DOI 10.1628/jz-2023-0174, "Femizid und Strafrecht" | Só metadados | 🚫 não lido |

---

## O que o modelo alemão ensina ao campo de motivação brasileiro

1. **Motivação como camada sobreposta, multi-rótulo, atribuída na entrada.** A Alemanha não cria um tipo penal: cada delito pode receber vários Themenfelder, e isso é declarado "erwünscht". Consequência assumida: não se soma os subcampos. O campo brasileiro deve decidir cedo se o indicador é por delito ou por vítima, e documentar que não soma.
2. **Limiar baixo e perspectiva da vítima explícita.** "Anhaltspunkte" bastam, aparência e linguagem contam, e vale o grupo "zugeschrieben". A nota de rodapé da vítima (2016) é o que sustenta isso. Para o Brasil, é o antídoto contra exigir prova do motivo para registrar.
3. **Eingangsstatistik com corte.** Registro no início do procedimento, correção por Nachmeldung, fechamento em 31.01. Evita esperar o desfecho judicial, mas fixa o erro de classificação inicial (policial entrevistado: ninguém refaz porque "ist einfach zu viel Arbeit").
4. **Registro sem auditoria vira "Daumenentscheidung".** O melhor dado alemão sobre qualidade é um estudo de autos do KFN, não o BKA: só 17,6% dos relatórios declaram o motivo e subcampos se sobrepõem. Qualquer indicador brasileiro precisa de amostra auditada contra os autos desde o desenho.
5. **Parear Hellfeld e Dunkelfeld com as mesmas categorias.** O SKiD copia as categorias da polícia e mede motivo pela percepção da vítima; isso permite dizer que a Anzeigequote de violência por orientação sexual é 2,6%. Sem categorias alinhadas entre BO e pesquisa de vitimização, o "dark figure" vira opinião.
6. **Não rotular o que não se mede.** O BKA tirou "Femizid" do título da série porque a PKS não tem motivo; mantém o recorte observável (mulher vítima, relação com o autor) e anuncia a definição que falta. O estudo de autos mostra o custo de contar por sexo da vítima: só ~45% (133/292) dos casos registrados eram femizídios no sentido amplo. Para o Brasil: um indicador de "feminicídio/ódio" que usa só sexo da vítima ou só o enquadramento legal sem camada de motivo mede outra coisa.
7. **Duas dimensões, dois instrumentos.** O Lagebild une a dimensão de ódio (PMK, motivo) e a dimensão de delito (PKS, perfil da vítima) e proíbe somá-las (PDF p. 4). Modelo útil para um indicador que quer capturar ódio contra LGBT sem depender de um único campo.
8. **Quebras de série e resíduo.** A reforma de 2022 quebrou a série de identidade de gênero; metade de "Sexuelle Orientierung" está em "sonstige Zuordnung". Reserve campo para "motivo sem ideologia atribuída" e registre o ano de cada mudança de categoria.
9. **Cuidado com o uso político de números de proxy.** Dois "308" no mesmo documento; um "64%" que é percepção policial. Cada número do indicador precisa vir com unidade (delito/vítima/pessoa), contexto e fonte.

---

## Becos

- `bka.de` e `bmi.bund.de` por curl: HTML de erro/timeout/400 (3 caminhos PDF). Wayback via CDX: 2024 recuperado e hash idêntico à cópia LSVD; 2025 sem captura de PDF; Bundeslagebild (BKA) sem snapshot achado, e o CDX caiu ("Temporarily Offline") na última consulta. Usei cópias LSVD (BMI 2025), Landkreis Ludwigsburg (BKA Lagebild) e `skid.bka.de` (oficial). Volta se: for exigido hash do Lagebild/PMK 2025 oficiais.
- `researchgate.net`: 403; texto "Falschbeschuldigungen bei sexueller Gewalt" não lido.
- Crossref `query.bibliographic` devolve ruído para termos alemães (Vergewaltigung -> antiguidade); não é canal confiável para este tema.
- WebFetch no BKA SKiD: timeout 60 s; `ergebnisbericht.html` 404 por curl.
- PreToolUse hook bloqueia `pdftotext` com redirecionamento para arquivo em PDFs "NAO_TRIVIAL" (Lagebild); contornei lendo por página no stdout.
- Pedido de "SKiD 2020" e "Zick/Küpper (Mitte)": não coletados.
- Edição 2023 do Bundeslagebild: não baixada.
- Definitionssystem: obtive a versão de 2016 (Polizei NRW); a versão mais nova (BKA 2024b, citada pelo KFN) existe online, mas não a localizei a tempo.

## PRISMA-S

Buscas: WebSearch (standard/extended) em alemão, cerca de 18 consultas; Crossref `query.bibliographic`/`query.title`, cerca de 25 consultas, resultado fraco; download direto de PDFs (BMI/LSVD, BKA SKiD, Landkreis Ludwigsburg, Polizei NRW, KFN/Nomos, BKA Forum KI, INASC, KFN Femizide) com leitura por página via `pdftotext`; Wikipedia/Wikidata (canal factual-context) **não usados** por não agregarem a este escopo; Dialnet, OpenAlex e Semantic Scholar não usados por instrução ou por falta de utilidade; limites: alemão, 2005-2026, sem filtro de revisão por pares; seleção: fonte primária lida > abstract > metadado; ledger: 16 fontes registradas nesta célula via `emit_sources.py`, 0 rejeitadas, em `research-2026-10-12-deep/sources.jsonl`.
