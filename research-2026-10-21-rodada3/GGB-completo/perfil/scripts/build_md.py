"""Gera GGB-O-QUE-E.md: narrativa (aqui) + tabela afirmacao->fonte->trecho->pagina->sha256 (de evidencias.csv)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, os, re
OUT = (REPO_ROOT + '/research-2026-10-21-rodada3/GGB-completo/perfil/')
ev = {r['id']: r for r in csv.DictReader(open(OUT + 'evidencias.csv', encoding='utf8'))}
SEL = ['ID01','ID02','ID03','ID04','ID06','ID09','SG01','SG04','SG06','SG07','SG10','FIN01','FIN02','FIN04',
       'MT01','MT02','MT05','MT07','MT14','MT20','MT21','MT24','MT25','MT26','MT27','MT29','MT31','MT34','MT37',
       'LIM04','LIM06','LIM07','USO01','USO02','USO03','USO06','USO08','USO09','USO12','CR01','CR02','CR04','CR05','OB01','OB03','OB04']
def short(t, n=88):
    t = re.sub(r'\s+', ' ', t).replace('|', '/')
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + ' …'
def row(i):
    r = ev[i]; f = os.path.basename(r['arquivo'])
    pg = r['pagina_pdf'] if r['pagina_pdf'].isdigit() else ('⚠️ p. 1-4 (leitura visual)' if i == 'ID09' else '⚠️ web, sem paginação (snapshot/URL em evidencias.csv)')
    return f"| {i} | {short(r['afirmacao'], 70)} | `{f}` | «{short(r['trecho_verbatim'])}» | {pg} | {r['sha256']} |"
table = '\n'.join(row(i) for i in SEL)

MD = f"""# O que é o Grupo Gay da Bahia (GGB) e o que a sua contagem mede

Data: 2026-10-22. Só documentos públicos, sem contato com ninguém (regra do autor, 2026-10-22). Site oficial: `grupogaydabahia.com.br` (o endereço `grupogaygbahia` do pedido não existe). Páginas PDF = índice do PDF. Nomes de vítimas ficam fora (`_raw`, fora do git).
Pasta de saída: `{OUT}`. Evidência completa ({len(ev)} trechos, trecho integral, caminho absoluto, sha256, URL): `evidencias.csv`; por ano: `metodologia_por_ano.csv`; ledger: `sources.jsonl` (41, via `emit_sources.py`).

## 0. Resposta e o que contradiz ou corrige o dossiê (primeiro)

> [!IMPORTANT]
> O GGB é uma associação privada de ativismo (CNPJ de 1983), com coleta voluntária de notícias, **sem verificação sistemática em inquérito, IML ou justiça por falta de recursos** (autodeclarado em 2019 e na página institucional; em 2021 diz ter checado por telefone com delegados, LIM07). A contagem mede **mortes violentas noticiadas de pessoas lidas como LGBT+, com critério de inclusão largo**. Não mede crime de ódio comprovado, taxa nem tendência.

1. **Mendes & Silva 2020 não é Q1.** *Ciência & Saúde Coletiva* está como Q2 em `fontes/scimago/quartis-sjr-2026-10-10.md`. Além disso os dados foram "cedidos" pelo GGB e revisados com ajuda de técnico do GGB (CR05): não é validação independente. Serve só para o que declara.
2. **Três datas incompatíveis para a entrada dos suicídios** na contagem: 10 suicidas já em 2013 (MT14), "desde o relatório de 2016" (MT21), "desde a edição de 2010" (MT31). A manchete mistura suicídio sem tabela de reconciliação.
3. **A contagem acompanha o esforço de coleta, por declaração do próprio GGB**: a queda de 158 (2004) para 81 (2005) é atribuída à suspensão do clipping por falta de financiamento (MT05). Isso é incompatível com ler a série como tendência.
4. **Revisão retroativa não explicada:** 1980-1989 = 503 (relatório 2005, MT06b) e 369 (relatório 2021, MT07).
5. **Há listas por caso públicas antes de 2019**, que a F3 não usou (a F3 disse "só 2019" para 2017-2025, o que continua certo para esse intervalo): tabelas gerais (Wayback lista 2004, 2005, 2008-2010, 2012) e registros 2013, 2015, planilha 2016 e listagem 2017 no blog Homofobia Mata, hoje só via Wayback (seção 7). **Os relatórios 2012 e 2016 existem** (HM/Wayback) e faltam na página atual do GGB; o anual 2022 não foi localizado.
6. **Uso institucional sem auditoria e com distorção de categoria:** o voto do STF chama de "homicídios" os 445 de 2017 que o GGB descreve como 387 assassinatos mais 58 suicídios (USO01/USO02); o GGB era amicus curiae na ADO 26 (USO03). Um orador no Senado (2015) disse "temos criticado o GGB por não ser tão científico, talvez, mas em todas as falas oficiais, eles é que são citados" (USO08).
7. **Sobre a F3:** o Observatório (Acontece/ANTRA/ABGLT, 2026) não tem o GGB como signatário (OB04; a "notícia" de que o GGB o fundou segue não verificada). O Observatório classifica motivo (60% "precisamente motivados", 40% "dúbios", OB03); o GGB não.
8. **ONU:** não localizei citação direta do GGB em documento primário da ONU. O A/HRC/29/23 que li usa o relatório do governo (310 em 2012; USO12). Resultado: "não localizado", não "não existe" (espaço: 5 consultas web EN/PT, 2 cortadas; 1 documento ONU aberto).

## 1. Origem e identidade

| fato | fonte |
|---|---|
| Fundado em 1980 (estatuto: 29/02/1980), registro civil 1983, utilidade pública municipal 1987 (Lei 3.725/1987) | ID01, ID06, ID09 |
| Fundador e figura central: Luiz Mott (antropólogo); Marcelo Cerqueira, vice-presidente e coordenador político | ID02, ID02b, ID02c |
| CNPJ 13.220.876/0001-95, abertura 18/03/1983, natureza 399-9 associação privada, CNAE principal "cultura e arte" (não direitos humanos) | ID03-ID05 |
| Sede: site diz Rua Frei Vicente 24; CNPJ e estatuto dizem Ladeira de São Miguel 24 (mesmo número; não inferi nada) | ID07 |
| Estatuto reformado 06/07/2017 e registrado 12/07/2018: sem fins econômicos, sem cunho político ou partidário (leitura visual do scan, ⚠️ sem camada de texto) | ID09 |
| Financiamento declarado: 2000 = fundações estrangeiras, Banco Mundial/Bird, Ministério da Saúde, Unesco (FIN01); 2020 e 2026 = nenhum apoio financeiro governamental, trabalho voluntário (FIN02, FIN03); parceiros frequentes: Prefeitura de Salvador e Governo da Bahia (ID08). Demonstrações financeiras: **não vi nenhuma** no que li (mídia do site 2024-2026; não busquei em portais de transparência), embora o estatuto (art. 30, leitura visual) mande publicá-las | ID08, FIN01-03 |

**Quem assina, por ano:** 2011-2015 autor Eduardo Michels (hemeroteca "Homofobia Mata"), coordenador Mott, "em parceria com o GGB" (SG01, SG02); 2016-2017 Mott, Michels, Paulinho (SG03, SG04); 2018 ainda "Site Homofobia Mata", Michels autor (SG05); **2019 organizadores José Marcelo Domingos de Oliveira e Mott**, Acontece entre colaboradores (SG06); **2020 copyright conjunto Acontece + GGB** (SG07, SG08); 2021-2025 releases só com a marca GGB (SG09), em 2025 "voluntários Marcelo Oliveira e Luiz Mott" (MT41). Observatório com ANTRA e ABGLT (2026): produtor distinto, GGB fora da assinatura (SG10, OB04). Consequência: a "série GGB" mudou de autor em 2019 e de coprodutor em 2020; não é um instrumento único.

## 2. Metodologia declarada ano a ano (detalhe: `metodologia_por_ano.csv`)

Totais declarados: 2000-2005: 130, 132, 126, 125, 158, 81; 2007: 122; 2008: 190 (depois 189); 2009: 198; 2010: 260; 2011: 266; 2012: 338; 2013: 312; 2014: 326; 2015: 318; 2016: 343; 2017: 445; 2018: 420; 2019: 329; 2020: 237; 2021: 300; 2022: só balanço semestral (135); 2023: 257; 2024: 291; 2025: 257. Sem documento localizado: 2000-2003 (só totais), 2006, anual 2022 (achado, não lacuna).
- **Fonte constante:** notícias de jornal e internet (2007-2017), depois Google Alerts e palavras-chave (2019-2020), obituários e redes sociais (2018, 2021), correspondência (2023-2025). Em 2000 o manual manda usar "limbo" para casos sem identificação expressa e lista indícios de inferência (MT01, MT02).
- **Critério largo, declarado:** suicídio (2013 em diante), heterossexuais "confundidos" (2012, 2014, 2024), latrocínio e profissionais do sexo trans sempre incluídos como "crimes de ódio" (MT34, MT40), "homotransfobia estrutural" (MT29), mortos no exterior.
- **Filtros declarados:** 158 casos descartados e 58 retirados em 2019 (MT25, MT26); "limbo" de 20 (2023) e 32 (2024) fora da conta.
- **Quebras de série:** suicídios 26 (2016) → 58 (2017) → 100 (2018) → 32 → 13 → 24; coautoria Acontece (2020); "aprimoramento" de coleta em 2024 sem reconciliação (MT37); 2025 com planilha citada e não publicada. **Tendência 2017-2025 não é interpretável.**

## 3. O que o GGB diz sobre a própria precisão

"Ponta de um iceberg" desde 2005 (LIM01); "amostra assumidamente subnotificada" (2009); "somos os primeiros a reconhecer a subnotificação" (LIM02); dados "apenas" de imprensa, sem estatístico (LIM04); a variação anual "continua sendo uma incógnita sociológica" e o GGB é "refém de notícias" (MT33); autor 2014 e 2015 negam que a variação seja interpretável ou tendência (MT17, MT19); 2019 pergunta "como comprovar a relação direta entre o ódio ... e o ato violento?" (MT27). **Contrapeso:** o mesmo GGB presume motivação em 99% dos casos (MT12, MT24) e descreve a série como mortes "motivadas" pela LGBTfobia (LIM06). Subnotificação (para baixo) e critério largo (para cima) coexistem.

## 4. Uso institucional (citação não é validação)

STF (ADO 26, voto Celso de Mello, p. 37; Moraes, p. 13): cita os 445 de 2017 e a condição de amicus (USO01-USO04); a imprensa oficial do STF registra advogado do GGB na sessão (USO05). CIDH 2015 adota "pelo menos 312" (GGB 2013) sem auditoria própria (USO06). Senado, CDH, 24/06/2015, p. 2 e 18 (USO07, USO08). Câmara, CDHM, 2021: "única pesquisa nacional que inclui todos os segmentos", e trata os 329 (297 H + 32 S) como vítimas da LGBTfobia (USO09, USO10). MDH (ano-base 2016, publ. 2018): usa Disque 100, GGB e Rede Trans (USO11). ONU: não localizado (item 8). **Leitura:** é uso por falta de série oficial, não prova de exatidão; a citação propaga categorias (homicídio vs suicídio).

## 5. Crítica e avaliação externa

Agência Pública/Truco, 29/08/2018: "principal referência nacional ... estatísticas, no entanto, não são precisas"; ranking mundial "impossível de provar" (CR01). Gazeta do Povo, 01/03/2019 (linha editorial própria; checagem amadora e parcial, 6% comprovados e 42% "de forma alguma", dados 2017, **não verificada por mim**): "somam os casos noticiados ... sem passar por qualquer revisão independente" (CR02, CR03). Mendes & Silva 2020 (Q2): "necessariamente não ocorreram por motivações homofóbicas" (CR04). Galbieri 2023 (*Simbiótica*, quartil não verificado): lê os relatórios como "estatativismo", não audita exatidão (CR06). **Resposta do GGB:** 2020 admite críticas "da ala conservadora ... e de membros do segmento LGBTI+" e responde com a tese de homotransfobia estrutural (LIM03, MT29); 2021 afirma ter "revisto e checado" os 300 casos, inclusive por telefone a delegados (LIM07; autodeclaração, não reproduzível por mim). **Lacuna:** nenhuma validação empírica independente peer-reviewed Q1 do GGB encontrada; a única validação por amostra é a da F3 (2019: 31,3% verificáveis hoje; 4,1% com LGBTfobia atribuída na fonte).

## 6. Distinção de objeto e incentivos

**É:** contagem declarada de mortes violentas noticiadas (homicídio, latrocínio, suicídio, atropelamento etc.), de pessoas identificadas como LGBT+ por imprensa, redes ou terceiros, com inclusão ampla. **Não é:** crime de ódio comprovado (4,1% na amostra F3), taxa de incidência (denominador próprio de 10% a 16,5% (MT24b; "mais de 10%" em 2024)), série comparável no tempo, nem ranking mundial (CR01).
**Incentivos e conflitos documentados (fatos, sem imputar má-fé):** objetivo declarado de "comover a sociedade e pressionar os poderes públicos" (MT04); uso da contagem para ameaçar denúncia à CIDH/ONU (OB01); posicionamento político explícito no mesmo comunicado (OB02); amicus curiae no julgamento que criminalizou a LGBTfobia (USO03); página institucional que liga o Observatório à captação de recursos (FIN04); histórico de apoio de fundações (FIN01). **Não se infere:** manipulação, inflação deliberada ou fraude (F3: duplicata 0,3%, sem sinal de inflação por internet); o amicus (2019) é posterior à série (1980); falta de recursos produz **subcontagem** (MT05).

## 7. Pode e não pode ser afirmado

**Pode:** (a) o GGB é associação privada fundada em 1980, CNPJ de 1983, voluntária, com contagem declarada baseada em mídia; (b) o próprio GGB declara subnotificação, ausência de verificação oficial, critério largo e quebras de método; (c) o GGB é citado por STF, Senado, Câmara, CIDH e MDH, com categorias às vezes alteradas; (d) 2023-2025 não têm lista por caso pública.
**Não pode:** "mortes por LGBTfobia" ou "crimes de ódio" (GGB presume, não prova); taxa ou "país que mais mata" (CR01); tendência 2016-2025 (suicídios, coautoria, esforço de coleta); "Q1" para Mendes & Silva; "validado por órgão oficial" (citação não é validação); "o GGB infla" ou "o GGB é confiável como taxa". **Não verificado / não publicado:** financeiro (sem balanços), planilhas 2020-2025, anuais 2022, ONU, vínculo Observatório×GGB.
Listas por caso hoje só via Wayback (blog `homofobiamata.wordpress.com`; arquivos em `_raw/pdf-hm-listas/`): tabela geral 2010 e 2012; registros 2013 (com links), 2015; planilha 2016; listagem 2017. Não auditadas (próximo passo possível, sem pedir nada a ninguém).

## 8. Tabela afirmação, fonte, trecho, página, sha256 ({len(SEL)} de {len(ev)}; o restante em `evidencias.csv`)

| id | afirmação | arquivo | trecho verbatim (encurtado) | pág. | sha256 |
|---|---|---|---|---|---|
{table}

Becos: ONU (busca devolveu pouco; fonte primária não localizada); Wayback intermitente; WebSearch cortou 2 consultas; estatuto é scan (⚠️ ID09 só visual); relatórios 2000-2003 e 2006 não localizados; 2012/2016 só via HM/Wayback (condição de volta: o GGB republicar ou outra cópia pública).
"""
open(OUT + 'GGB-O-QUE-E.md', 'w', encoding='utf8').write(MD)
print(MD.count('\n') + 1, 'linhas')
