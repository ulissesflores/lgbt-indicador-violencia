# PRE-REGISTRO — frente "mortalidade" (discurso, rodada 3)

Pergunta: o que a literatura científica Q1 (texto integral lido) mostra sobre se pessoas gays/LGB/trans morrem mais que heterossexuais/cisgênero, por causa de morte, e o que isso implica para julgar a afirmação "gays morrem mais que héteros".
Escrito ANTES de qualquer busca ou leitura de estudo desta frente (única coisa lida antes: BRIEFINGs, tabelas de quartil e a lista de arquivos de `fontes/q1-textointegral/`; as citações a Dinno 2017, Herek 2009, Stotzer 2009 e Flores 2022 já constam no dossiê de 2026-10-12, portanto são conhecidas de antemão). Qualquer coisa acrescentada depois vai em "ADENDO pós-busca" no fim, sem reescrever este texto.

## A. Famílias de afirmação a julgar (F-M)
- F-M1 "Gays/LGB morrem mais que héteros" (mortalidade por todas as causas)
- F-M2 "Gays/LGB morrem mais por suicídio" (separar ideação, tentativa e óbito)
- F-M3 "Gays/LGB/trans são mais assassinados" (homicídio; denominador compatível)
- F-M4 "Gays morrem mais de HIV/aids" (causa específica; era pré-HAART x pós)
- F-M5 "Pessoas trans morrem mais" (todas as causas, suicídio, homicídio)
- F-M6 "No Brasil, gays/LGBT morrem mais" (qualquer causa com denominador)
Por causa: todas as causas; suicídio; homicídio/violência; HIV/aids; outras (câncer, cardiovascular, uso de substância). Por população: gays/homens que fazem sexo com homens; lésbicas/mulheres que fazem sexo com mulheres; bissexuais; trans/gênero diverso. Mundo e Brasil.

## B. Estratégia de busca (bases, termos exatos, idiomas)
Bases: B1 PubMed (E-utilities, sem cadastro); B2 OpenAlex (API pública); B3 Europe PMC (texto integral OA); B4 Crossref (metadados/DOI); B5 SciELO/BVS-LILACS (PT/ES, via WebSearch/WebFetch); B6 busca web geral (WebSearch) para localizar a versão OA; B7 pasta local `fontes/q1-textointegral/` (varrida ANTES de baixar).
Consultas (EN; PubMed, campos título/resumo):
- Q1 ("sexual orientation" OR "same-sex") AND mortality AND (cohort OR "national death index" OR register*)
- Q2 ("same-sex marriage" OR "registered partnership" OR "same-sex partner*") AND (mortality OR "cause of death" OR "life expectancy")
- Q3 (gay OR bisexual OR lesbian OR "sexual minority") AND suicide AND ("systematic review" OR meta-analysis)
- Q4 (suicide OR "suicide attempt") AND ("sexual orientation") AND (death OR mortality OR register* OR "death certificate")
- Q5 homicide AND ("sexual orientation" OR "sexual minority" OR LGBT) AND (NVDRS OR "violent death" OR NCVS OR victimization)
- Q6 (transgender OR "gender dysphoria" OR "gender identity") AND (mortality OR "cause of death" OR "suicide death" OR homicide) AND (cohort OR register*)
- Q7 HIV AND "gay and bisexual men" AND (mortality OR "life expectancy") AND (HAART OR antiretroviral)
- Q8 "sexual orientation" AND "death records" AND (collection OR "sexual orientation and gender identity" OR "SOGI") AND (suicide OR violent death)
- Q9 "sexual orientation" AND mortality AND "structural stigma" 
Consultas PT/ES (SciELO, BVS, WebSearch): "orientação sexual" mortalidade coorte Brasil; "orientação sexual" suicídio óbito Brasil; "homens que fazem sexo com homens" mortalidade Brasil; "minorias sexuais" suicídio tentativa Brasil; "pessoas trans" mortalidade Brasil; "mortalidad" "orientación sexual" cohorte; "suicidio" "minorías sexuales" meta-análisis.
Rastreio adicional: referências (backward) dos estudos incluídos e das revisões Q1 (Plöderl 2013/2015, King 2008, Haas 2011, Hottes 2016, Marshall 2016, Miranda-Mendizábal 2017); registro de cada achado como "via referência".
Janela: sem limite inferior; superior = 2026-10-22. Registrar n de resultados por consulta no ADENDO (não é pré-fixável).

## C. Critérios de inclusão (todos obrigatórios para entrar na tabela de evidência)
- I1 Desfecho: óbito (todas as causas ou por causa) OU, em bloco separado e rotulado, ideação/tentativa de suicídio. Ideação/tentativa NUNCA entra como "morrem mais".
- I2 Exposição: orientação sexual ou identidade de gênero medida (autodeclaração, parceria registrada/casamento entre pessoas do mesmo sexo, parceiro(a) do mesmo sexo declarado, diagnóstico de disforia/atendimento em serviço de gênero), com definição transcrita verbatim.
- I3 Denominador: a mesma população fornece numerador e denominador (coorte, registro ligado, amostra probabilística ligada a óbitos, ou levantamento com amostra de comparação) OU o estudo é meta-análise de tais estudos. Contagens de ONG/mídia sem denominador = "contagem declarada", fora da evidência.
- I4 Periódico Q1 no SJR (melhor quartil 2023-2025; tabelas em `fontes/scimago/`), senão `nao_verificado` e rebaixado a "apoio" (não decide veredito). Documento oficial primário (ex.: BJS, CDC) vale como fonte de dado, lido no original.
- I5 Texto integral (PDF/XML/HTML) LIDO por mim e salvo localmente com sha256; trecho verbatim + página/seção. Sem isso: "não lido", linha em `fila-chrome.jsonl`, e NÃO é evidência.
- I6 Fonte pública acessível sem pedir nada (sem e-mail, cadastro, termos, LAI, cópia a autor). Sem Sci-Hub/LibGen. Sem Playwright.
Exclusões: só abstract; preprint sem versão publicada usado como evidência decisiva (pode apoiar, marcado); estudos de prevalência de HIV sem mortalidade; estudos de bullying/violência autorrelatada citados como "homicídio".

## D. Dados extraídos por estudo (estudos.csv)
ref completa; DOI; periódico; quartil SJR; país/período; desenho; amostra (n, óbitos); definição de orientação (verbatim); desfecho; estimativa + IC95% (verbatim, razão de taxas/hazard/odds); trecho verbatim; página/seção; caminho do arquivo; sha256; limitações declaradas; população; causa; acesso/estado (lido/não lido).

## E. Regra de classificação do veredito (por causa x população x mundo/Brasil)
- sustentada: >= 2 estudos Q1 independentes (países/bases diferentes OU desenhos diferentes), com denominador compatível, estimativa na mesma direção e IC95% excluindo 1, no período atual (pós-HAART para causas gerais; qualquer período para HIV).
- parcial: apenas 1 estudo, OU apenas um subgrupo/sexo/período (declarar qual), OU IC95% cruza 1 em parte dos estudos, OU a evidência é de tentativa/ideação mas não de óbito.
- não sustentada: estudo(s) com denominador compatível e estimativa sem excesso (IC inclui 1 ou razão < 1) e sem estudo contrário de mesmo peso.
- não testável: não existe estudo com orientação/identidade registrada entre os óbitos E denominador do grupo (inclui Brasil, onde o SIM não registra orientação), ou só existem contagens sem denominador.
Magnitude: sempre a estimativa e o IC do próprio estudo; nunca reconstruída por mim; se reconstruída, marcada "calculada por mim".
Acerto/erro: a frase "gays morrem mais que héteros" é lida como razão de TAXAS DE MORTALIDADE (óbitos por pessoa-tempo) > 1 com IC excluindo 1; "mais risco de X" (prevalência/odds de tentativa) é outra afirmação e será julgada à parte. Confusão a registrar: idade, raça, classe, seleção (parceria registrada, amostra de conveniência), era do HIV.

## F. Produtos
PRE-REGISTRO.md (este), estudos.csv, MORTALIDADE.md (<= 180 linhas), sources.jsonl (só via emit_sources.py), fila-chrome.jsonl (PDFs não obtidos). PDFs/XML em `fontes/q1-textointegral/discurso/mortalidade/` (pasta fora do git), salvos com nome DOI.

---
## ADENDO pós-busca (2026-10-22, escrito DEPOIS de rodar as consultas e ler os textos; não faz parte do pré-registro acima)
Hash e hora do pré-registro original: ver PRE-REGISTRO.sha256.txt (sha256 calculado sobre o arquivo ANTES deste adendo) e PRE-REGISTRO.hora.txt (2026-10-22T21:19:32Z). O arquivo atual difere do hash porque o adendo foi acrescentado; a cópia PRE-REGISTRO.original.md (texto anterior ao adendo) reproduz exatamente o sha256 a17cf2f7...0065f3.
**A. Contagens por consulta (PubMed E-utilities, 2026-10-22; lista bruta em busca-pubmed-2026-10-22.json; retmax=60):** Q1=104, Q2=16, Q3=44, Q4=88, Q5=1, Q6=66, Q7=3, Q8=0, Q9=4.
**B. Consultas e regras acrescentadas depois (não estavam no pré-registro):** (i) Brasil em inglês no PubMed: `Brazil AND (orientation|minority|MSM|LGBT) AND (mortality|death|suicide)` = 22; `Brazil AND (orientation|minority) AND (suicide attempt|ideation|behavior)` = 5; `Brazil AND "National Health Survey" AND "sexual orientation"` = 5; `Brazil AND (homicide|violent death) AND (LGBT|minority|transgender|travesti)` = 2; `Rio de Janeiro AND SINAN AND orientation AND mortality` = 0. (ii) três consultas amplas com países (Países Baixos, Inglaterra, Noruega, Finlândia, Canadá, Austrália, Taiwan, Israel) = 24; título com orientação+mortalidade = 56; suicide-mortality+orientação = 16. (iii) buscas por autor/título para estudos nomeados na tarefa (Cochran & Mays 2011/2016, Haas 2011, Plöderl 2013, Hogg 1997, Friedman 2011, Marshall 2016, Wood 2000, Koblin, Pompili). (iv) WebSearch em PT: 1 consulta respondeu (sem resultado primário útil), 2 falharam por corte; não entram como evidência. (v) varredura da pasta `fontes/q1-textointegral/` ANTES de baixar (Dinno, Flores 2022, Herek 2009, Stotzer 2009 já estavam lidos).
**C. Desvios do pré-registro:** (1) I4 estrito deixa quase todas as coortes de registro (JAMA, Lancet, JECH, Eur J Epidemiol...) como "apoio" só porque as duas tabelas SJR não as cobrem; por isso o veredito sai em DUAS colunas (sob I4 estrito / se os nao_verificado forem Q1, pendente de conferência no Chrome real, ver fila-chrome.jsonl). (2) "Texto integral" inclui HTML/XML de PMC/Europe PMC e manuscritos aceitos (marcados em estudos.csv, coluna estado); PDF escaneado de Stotzer foi lido por OCR (pasta entregues-pelo-ulisses/_ocr). (3) Hatzenbuehler 2014 foi lido, mas está RETRATADO (Crossref update-to=retraction): registrado e excluído da evidência. (4) A escada `acquire_fulltext.py` abortou com ForbiddenHost (hdl.handle.net) ao rodar em lote; rodei registro a registro (pasta acq/, removida ao final) e usei só os arquivos que de fato traziam texto integral. (5) Nenhum e-mail, cadastro, termo aceito, LAI ou pedido a autor.
**D. Contagem final:** 48 estudos lidos em texto integral ou manuscrito aceito (1 deles retratado e 1 sem comparador heterossexual) + 2 fontes oficiais (BJS e cabeçalho do SIM) = 50 linhas em estudos.csv; 28 DOIs não lidos (fila-chrome.jsonl), nenhum usado como evidência.
