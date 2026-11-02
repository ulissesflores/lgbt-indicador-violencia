# 1. Verificação item a item do manual

> Cópia distribuída no repositório (2026-10-25, frente E5): caminhos absolutos da máquina do autor trocados por caminhos relativos à raiz do repositório ou por "pasta de trabalho do autor" (arquivos que não são distribuídos); nenhum outro texto mudou. Original: `S2-ASTRA-A2.md`, SHA-256 `ff69363639768333e6a9c9296d4da12526747ee0d3fb81d55254067d5d7f92df`.

**Referência das linhas:** todas as indicações “L.” remetem ao [paper-snapshot-v04.md](pasta de trabalho do autor/research-2026-10-24-v03/S2-astra/paper-snapshot-v04.md), SHA-256 `f283475e8853e8cec20278a46503bd756f0f68bc288249e8cc367e9980c7f69f`. Conferi sua igualdade com o `paper.md` local. README e REPRODUCIBILITY congelados também coincidem com os arquivos locais examinados.

“Atendido” significa atendimento ao item nas verificações indicadas; não certifica toda a análise correspondente. “Parcial” inclui correção no corpo que não chegou ao resumo, legenda, apêndice ou README — propagação expressamente exigida pelo manual.

| Código | Estado | Evidência | O que falta |
|---|---|---|---|
| N01 | atendido | L. 534: “1.554 LGB+ entrevistados”; “60,7%”. Recalculei o MDE: 60,7034%. | Nada quanto à troca da amostra esperada pela observada. |
| N02 | atendido | L. 534: “305.955 adultos triados”; “arredondamento único no fim”. CSVs de capacidade concordam. | Disponibilizar insumos com precisão suficiente para reproduzir a última unidade; ver seção 3. |
| N03 | atendido | [test_correcoes_v03.py](tests/test_correcoes_v03.py): `soma_das_27_ufs_igual_a_linha_br`; teste executado. | Nada: 2023–2025 resultam em 2.173, 2.264 e 2.410, sem duplicar BR. |
| N04 | atendido | L. 182: “59 variáveis em 9 blocos”; distingue formulário de cabeçalho dos microdados. | A contagem dos cabeçalhos brutos do SIM não foi reexecutada nesta revisão. |
| N05 | atendido | L. 319: “0,53 a 0,74”; “22 a 23 estados”. CSV principal: 0,527–0,740; 22/23/23/22. | Nada quanto à especificação principal. |
| N06 | atendido | L. 512 e 520: “1 de 49” principal; “0 de 49” sensibilidade. Fisher recontado. | A validade do conceito de “fonte primária” permanece uma questão separada. |
| N07 | atendido | [INVENTARIO-PUBLICO.md](manifest/INVENTARIO-PUBLICO.md): “906”, “905”, “19”, “11”, “166”; distingue painel histórico. | Nada na reconciliação atual; volume de fontes continua sem medir qualidade. |
| N08 | parcial | [README.md](README.md:60): “929 pares”; “464 com o SHA-256”. L. 653 ainda generaliza que os textos têm hash. | Harmonizar a alegação geral com hashes ausentes e distinguir documento de metadado. |
| N09 | parcial | L. 649: selo `5cf914…7066`, 721 arquivos, conferido. [REPRODUCIBILITY.md](REPRODUCIBILITY.md:166): execução identificada como v0.3. | Relatório final de execução vinculado à distribuição pública da v0.4. |
| R01 | parcial | L. 182 reconhece Luis/Rafael, mas abre com “a pergunta não é testável com dado público”; L. 18 e 575 repetem o absoluto. | Restringir à estimativa nacional comparável não obtida nas fontes examinadas. |
| R02 | parcial | L. 633 distingue prevalência; L. 34 e 1417 continuam chamando N1 de “incidência”. | Corrigir a taxonomia e seus consumidores. |
| R03 | parcial | L. 299: “uma não valida nem invalida a outra”; L. 307: “estimativa da mesma grandeza”; L. 956: “comparável ao Sinan”. | Retirar a equivalência da legenda, apêndice, dados rotulados e README. |
| R04 | parcial | L. 295 admite pessoas trans no denominador; L. 277 apresenta cenário, não limite. [README.md](README.md:172) ainda diz “numeradores comparáveis”. | Propagar a correção ao README e a todos os rótulos. |
| R05 | parcial | L. 277: “não estimam cobertura real”; apresenta `RR* = N/E₀`. README conserva linguagem de cobertura e compatibilidade. | Identificar sempre razão condicional e especificação; não máximo real de cobertura. |
| R06 | atendido | L. 32 separa “motivação documentada”, “viés percebido” e “efeito causal da discriminação”. | Nada na distinção conceitual solicitada. |
| R07 | atendido | L. 359: “nenhum dos seus desfechos identifica pessoas LGBT+”; L. 431 distingue Presidência e interação. | Não transportar esses resultados para violência LGBT+ em futuras sínteses. |
| R08 | atendido | L. 144: “diagnóstico descritivo”; reconhece que Goodman-Bacon não se aplica literalmente. | A ameaça de heterogeneidade continua sem solução empírica, agora declarada. |
| R09 | parcial | L. 144 e 359 distinguem normal, wild invertido e t; L. 359 e 578 confundem intervalos com detectabilidade. | Retirar limites causais e linguagem determinística de poder. |
| R10 | atendido | L. 329–345 apresentam trajetórias alternativas; o produto de crescimento e registro é preservado e há restrição de probabilidade. | Nada quanto à direção da compensação algébrica. |
| R11 | parcial | L. 319: associação “diminui”; [README.md](README.md:256): “o tamanho do estado explica”. | Trocar explicação causal por atenuação após ajuste em todas as superfícies. |
| R12 | parcial | L. 259: “intervalo que inclui 1”; na mesma linha, a correlação “desaparece”. | Manter “imprecisa após ajuste”; não converter não significância em desaparecimento. |
| R13 | atendido | L. 384 apresenta falsificação como não detecção e condiciona a faixa à fórmula adotada. | Nada na correção de modalidade; não é certificado contra todo viés. |
| R14 | parcial | L. 220 declara que a sensibilidade dos denominadores não foi testada; L. 374 reconhece a faixa feminina mais estreita. | Executar a sensibilidade demográfica ou manter a ordenação estritamente condicional. |
| R15 | atendido | L. 30: Campbell “orienta a leitura” e “não é testada”. | Nada. |
| R16 | parcial | L. 534 distingue mortalidade; L. 18 exige orientação “registrada no óbito”; L. 617 admite vinculação. | Sincronizar resumo e conclusão; não apresentar um único desenho como necessidade universal. |
| R17 | parcial | L. 431 diz que a queda “não pode ser atribuída”; L. 439 a chama de “não distinguível de zero”; L. 1423 afirma que a troca “não a explica”. | Distinguir falta de identificação causal, contribuição possível e significância da quebra. |
| R18 | parcial | L. 431 e 443 usam “interação”; [README.md](README.md:224) ainda afirma que “só o alinhamento” é identificável. | Corrigir o README e manter produto, distância e copartidarismo separados. |
| L01 | parcial | L. 184 identifica população, período, padronização e taxa não anual da ONS. | Incluir seleção, perdas de vinculação e reponderação da ONS. |
| L02 | atendido | L. 210: McKetta como “fator de aceleração”; Erlangsen com identificação administrativa e seleção. | Reestimação dos estudos originais não conferida. |
| L03 | atendido | L. 182: “563 (42,5% dos óbitos pareados, e não das notificações)”; distingue causas e acesso restrito. | Nada na correção pedida; não há reprodução independente do linkage. |
| L04 | parcial | L. 210–214 reequilibram Zachry e distinguem Halliwell/Dinno. | A coorte clínica brasileira indicada no manual não foi integrada à síntese. |
| L05 | atendido | L. 212 identifica McLellan, ausência de estudo elegível sobre homicídio e errata de abril de 2026. | Nada quanto à integração solicitada. |
| L06 | não atendido | L. 394 e 431 não apresentam a matriz de exposições e desenhos exigida; buscas pelos autores indicados não os localizaram no artigo. | Integrar a literatura presidencial/retórica/políticas com exposição, desenho, ameaça e acesso. |
| L07 | parcial | L. 257 cita Lum e explicita dependência; há arquivo de sensibilidades no repositório. | Mostrar no artigo o efeito do pareamento: aproximadamente 186 versus 221, entre outros cenários. |
| L08 | parcial | L. 247 admite coexistência de motivos; L. 615 incorpora OSCE. | Integrar a literatura de seleção midiática indicada, com estado real de acesso. |
| L09 | não atendido | L. 144 mantém a discussão centrada em Goodman-Bacon; De Chaisemartin/D’Haultfœuille não aparecem. | Justificar o tratamento contínuo e reversível com literatura apropriada e suporte observado. |
| L10 | parcial | L. 97 declara adendo posterior; L. 216 mostra dois vereditos. L. 210 ainda exclui estudos porque o quartil não foi conferido. | Fazer desenho e risco de viés governarem a síntese substantiva, não o quartil. |
| L11 | atendido | L. 210 incorpora Austrália, Taiwan e Suécia, declarando leitura em HTML; L. 184 integra expectativa de vida da ONS. | A leitura integral das três coortes não foi reconferida nesta rodada. |
| L12 | parcial | L. 544 discute PNDS 2023; [pns_2024_status.md](dados/pns_2024_status.md) existe, mas o artigo omite a PNS 2026 em realização. | Atualizar o estado oficial e condicionar uso à divulgação de microdados e documentação. |
| D01 | atendido | L. 64, 142, 158 e 633; [pns_c05_razao_direta.py](dados/pns/pns_c05_razao_direta.py): `Y008 em {2,3,4}`. | Nada documental; microdados não foram retabulados nesta revisão. |
| D02 | atendido | L. 309: Sinan permite descrever “notificações e suas mudanças”. | A contradição da Figura 11 está registrada em R03. |
| D03 | parcial | L. 247 mostra 160→106→88→73, 50/160, 3/73 e 35 desconhecidos, sem interpretar complementos como falsidade. | Declarar que 88 e 50 incluem correspondências parciais; mostrar análise restrita. |
| D04 | parcial | L. 257 condiciona Chapman e reconhece dependência. | Integrar sensibilidades e esclarecer o universo estimado, além do noticiário observado. |
| D05 | atendido | L. 431: 15 pontos, autocorrelação não tratada, poucos eventos e confundimento; L. 645 explicita limites. | Nada na declaração; esses limites continuam restringindo a inferência. |
| D06 | parcial | L. 431 declara 36 células e interpretação posterior; Tabela A13 mostra os resultados. | Corrigir “1,8 resultados assim” e explicitar correção/família da regra composta. |
| D07 | parcial | L. 463 declara cobertura desigual; L. 645 diz que dez consultas não garantem igual recuperação. | Restringir a ausência a consultas sobre mandatos; não a todo ato de agentes estatais. |
| D08 | atendido | L. 526 separa falsidade, não substanciação e retratação; nega transporte para LGBTfobia brasileira. | Nada na delimitação solicitada. |
| D09 | atendido | L. 645: “dados publicados e acessíveis sem solicitação”. | Nada. |
| T01 | não atendido | [README.md](README.md:59): “Cada número publicado é uma asserção de teste”; `manifest/CLAIMS.csv` ausente. | Criar índice de afirmações efetivamente cobertas e retirar a garantia universal. |
| T02 | atendido | [inventario_publico.py](scripts/inventario_publico.py): `--check`; executado com resultado conforme. | Nada no inventário público atual. |
| T03 | atendido | L. 121 e 645 distinguem correspondência de conteúdo de anterioridade declarada. | Anterioridade histórica externa permanece não conferida; não é provada pelo hash. |
| T04 | atendido | L. 247: “a ligação entre caso e fonte não é reproduzível com o repositório”. | Nada na declaração; validação nominal continua não conferida. |
| T05 | parcial | L. 512 separa fonte nomeada e capacidade probatória, mas define primária por documento oficial/estudo; protocolo classifica ONGs por origem. | Índice de uso/leitura/correções e classificação por proximidade da evidência, não por instituição. |
| T06 | parcial | L. 347 documenta quebras do Disque 100; `dados/INVENTARIO-SERIES.csv` ausente. | Consolidar universo, unidade, datas, faltantes, dependências e revisões de todas as séries. |
| T07 | atendido | [dados/presidencia/README.md](dados/presidencia/README.md) e scripts integrados; cinco testes C09 executados, aprovados. | Recálculo integral em clone separado não conferido nesta revisão somente leitura. |
| T08 | parcial | L. 651 declara SIM/Sinan não reexecutados; REPRODUCIBILITY contém matriz. | Corrigir “todos os números” da trilha leve e validar as etapas alteradas na versão final. |
| T09 | parcial | Sete testes de correções e controles negativos das figuras passaram. | Cobrir estimandos, escala e legendas atuais; testes numéricos aprovados deixam contradições passar. |
| T10 | parcial | [PAPER-SHA256.txt](paper/PAPER-SHA256.txt) corresponde a MD/DOCX/PDF; exportação não reproduzível declarada. | Validar texto/legendas da versão atual; inspeção visual integral das 126 páginas não conferida. |

# 2. Ataques à v0.4, em ordem de severidade

Os vereditos abaixo qualificam **o ataque**, não a afirmação do artigo.

**Severidade alta**

**A2-01 — O resumo continua deduzindo impossibilidade científica da ausência de um campo.**

- **Onde:** L. 18 e 24: “a mortalidade de pessoas LGBT+ no Brasil não é estimável com dado público”; L. 182 e 575: “não testável”; L. 18 exige orientação “registrada no óbito”.
- **Problema:** a conclusão excede a ausência de uma estimativa nacional comparável e contradiz as alternativas de vinculação reconhecidas pelo próprio artigo.
- **Verificação — procede:** L. 182 descreve evidência brasileira parcial; L. 617 admite vinculação a outra fonte. Conferi o estudo de [Luis et al.](https://www.scielo.br/j/ress/a/QhSQqkLFnk9xGscGywBpDYG/?ilang=en&lang=en): ele não resolve o risco populacional nacional, mas impede transformar ausência de campo em impossibilidade geral de estudar mortalidade.
- **Correção mínima:** “Nas fontes examinadas, não obtivemos estimativa nacional comparável; existem resultados parciais por vinculação e populações específicas.”
- **Flanco:** ambos/método.

**A2-02 — A Figura 11 restaura exatamente a equivalência PNS–Sinan que o corpo retirou.**

- **Onde:** L. 307: “Cada linha é uma estimativa da mesma grandeza” e “As fontes concordam no sentido”; L. 956–961: “comparável ao Sinan”.
- **Problema:** pessoas vitimadas e notificações com elegibilidade diferencial continuam sendo apresentadas como estimativas do mesmo objeto.
- **Verificação — procede:** L. 299 explica corretamente a seleção institucional e a exceção de notificação para população LGBT; o CSV C05 conserva o rótulo de comparabilidade. O último período da legenda reconhece universos diferentes, mas não cancela os dois primeiros.
- **Correção mínima:** apresentar as parcelas lado a lado como descrições de universos distintos, sem concordância, validação ou comparação inferencial.
- **Flanco:** método.

**A2-03 — A Figura 20 contradiz seus próprios intervalos.**

- **Onde:** L. 439: “o resultado é ‘não distinguível de zero, com poder baixo’”.
- **Problema:** a quebra nacional de 2019 e o placebo de 2018 têm intervalos publicados que excluem zero.
- **Verificação — procede:** recalculei a leitura de [c09_d1_resultados.csv](dados/presidencia/c09_d1_resultados.csv): 2019, −17,046%, IC [−29,490%; −2,406%]; placebo, −21,821%, IC [−37,410%; −2,350%]. L. 431 e Tabela A13 concordam com esses números. A contradição aparece também no PDF, página 55.
- **Correção mínima:** “Há quebras estatisticamente detectáveis nessa especificação, inclusive antes da posse; o desenho não identifica efeito presidencial.”
- **Flanco:** ambos/método.

**A2-04 — A busca por mandatos presidenciais não cobre “agentes do Estado” em geral.**

- **Onde:** L. 18: “não localizou perseguição por agentes do Estado entre 2003 e 2026”; L. 461–463 e Tabela 8.
- **Problema:** a unidade de busca é o mandato presidencial, enquanto a conclusão abrange polícia, autoridades estaduais e outras ações estatais.
- **Verificação — procede quanto ao alcance:** conferi o protocolo, as 60 consultas e a cobertura declarada. A [CIDH](https://www.oas.org/en/iachr/multimedia/2015/lgbti-violence/forms-lgbti-violence.html) registra informação recebida sobre alegada execução por agente estatal em Patu, em 2013. Isso é **alegação reportada**, não prova de perseguição presidencial nem confirmação judicial; demonstra por que a busca proposta não sustenta uma conclusão ampla sobre agentes estatais.
- **Correção mínima:** limitar a frase aos episódios recuperados pelas consultas sobre os seis mandatos e declarar que violência estatal local não foi inventariada sistematicamente.
- **Flanco:** esquerda/método.

**A2-05 — Intervalo de confiança e poder continuam sendo confundidos.**

- **Onde:** L. 359 e 578: “efeitos menores que essas faixas não são detectáveis”; L. 447: “efeitos menores não seriam detectados”; L. 1405: “passariam despercebidos”.
- **Problema:** um intervalo observado não é MDE, e poder abaixo de 80% não significa probabilidade zero de detecção.
- **Verificação — procede:** os arquivos distinguem IC normal, t, wild invertido e MDE; as frases voltam a fundi-los. A definição de 80% na L. 431 contradiz a conclusão determinística da L. 447.
- **Correção mínima:** separar “valores compatíveis sob o modelo” de “efeitos para os quais o poder previsto é inferior a 80%”.
- **Flanco:** método.

**Severidade média**

**A2-06 — O README ainda apresenta cenários do GGB como numeradores comparáveis.**

- **Onde:** [README.md, L. 27 e 172](README.md:172): “numeradores comparáveis”; contraste com L. 277 e 295 do artigo.
- **Problema:** a correção substantiva de N2 não foi propagada ao documento de entrada do repositório.
- **Verificação — procede:** a recontagem confirma N2=94/167, mas também as marginais 100–118 e 164–168; nenhum desses cenários resolve simultaneamente orientação, identidade, idade e causa. O próprio artigo o admite.
- **Correção mínima:** substituir por “cenários aritméticos não harmonizados” e retirar a interpretação de cobertura real.
- **Flanco:** ambos/método.

**A2-07 — “50 casos verificáveis” inclui dez correspondências apenas parciais.**

- **Onde:** L. 247: “88 tinham a matéria do próprio caso”; L. 255: “50 casos [...] verificáveis”.
- **Problema:** a formulação apaga um grau de incerteza do pareamento que altera materialmente a fração final.
- **Verificação — procede como omissão, não como erro de soma:** em [codificacao_A.csv](research-2026-10-21-rodada3/F3-ggb/dados/codificacao_A.csv), os 88 são 73 correspondências `S` e 15 `P`; os 50 finais são 40 `S` e dez `P`. O [CODEBOOK.md](research-2026-10-21-rodada3/F3-ggb/scripts/CODEBOOK.md) define `P` como correspondência parcial por cidade, data e perfil.
- **Correção mínima:** publicar 50/160 sob a regra inclusiva e 40/160 sob correspondência estrita, sem chamar o complemento de falso.
- **Flanco:** ambos/método.

**A2-08 — A sensibilidade de captura-recaptura existe, mas não acompanha o resultado principal.**

- **Onde:** L. 257: “186 (175 a 198)” e “63% (60% a 68%)”.
- **Problema:** a ressalva verbal não mostra que uma mudança já calculada no pareamento supera amplamente o intervalo estatístico destacado.
- **Verificação — procede:** em [captura_recaptura_sensibilidade.json](research-2026-10-21-rodada3/F3-ggb/dados/captura_recaptura_sensibilidade.json), mantendo 118 e 139 casos, reduzir a sobreposição de 88 para 74 muda Chapman de 186,19 para 221,13 e a razão de 63,38% para 53,36%.
- **Correção mínima:** mostrar essa sensibilidade ao lado do IC e identificar população-alvo, regra de pareamento e incerteza não amostral.
- **Flanco:** método.

**A2-09 — “Fonte primária” continua dependendo da instituição que publica.**

- **Onde:** L. 512: “documento oficial ou estudo”; [CRITERIOS.md](research-2026-10-21-rodada3/escrutinio/simetria/CRITERIOS.md:52): “GGB, ANTRA, TGEU = secundaria_ONG por definição”.
- **Problema:** a classificação confunde origem institucional com proximidade da evidência e pode predeterminar a baixa frequência de fontes primárias.
- **Verificação — procede:** o Fisher está correto para os rótulos existentes, mas não valida o construto. A capacidade de sustentar a afirmação permanece “não [...] codificada”, segundo a própria L. 512.
- **Correção mínima:** renomear o indicador como presença da categoria documental operacional adotada ou recodificar primariedade independentemente de ser Estado, universidade ou ONG.
- **Flanco:** ambos/método.

**A2-10 — O filtro Q1 ainda decide a síntese, apesar da declaração contrária.**

- **Onde:** L. 97: “a avaliação substantiva [...] considera desenho”; L. 210: “os periódicos não tiveram o quartil conferido, e as três ficam fora do veredito”.
- **Problema:** estudos lidos são excluídos da decisão por metadado bibliométrico não conferido, não por avaliação metodológica.
- **Verificação — procede:** a contradição é textual. Além disso, a síntese da ONS omite seleção e perdas: a [documentação oficial](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthinequalities/bulletins/allcauseandcausespecificmortalitybysexualorientationenglandandwales/march2021tonovember2024) informa vinculação de 94,6% do Censo ao PDS, 90,2% dos óbitos ao PDS e reponderação; o conjunto final corresponde a 59,0% da população censitária adulta considerada.
- **Correção mínima:** manter o veredito histórico do protocolo como sensibilidade e produzir síntese principal por desenho, seleção e risco de viés.
- **Flanco:** método.

**A2-11 — A fundamentação metodológica dos modelos políticos ficou incompleta.**

- **Onde:** L. 144: regressor “contínuo e reversível”; L. 394 e 431; L. 220: sensibilidade demográfica não testada.
- **Problema:** o artigo declara limites, mas não entrega duas verificações exigidas pelo manual: adequação à exposição contínua/reversível e robustez aos denominadores extrapolados.
- **Verificação — procede:** não localizei os trabalhos metodológicos de L09 nem a matriz de L06 no artigo; a ausência da sensibilidade demográfica é expressamente declarada. Não identifiquei, por isso, uma ordenação alternativa demonstradamente invertida.
- **Correção mínima:** justificar o estimando associativo com suporte observado e acrescentar a sensibilidade demográfica, ou retirar qualquer pretensão de estabilidade demonstrada.
- **Flanco:** método.

**A2-12 — A Tabela 9 universaliza uma limitação específica da HRW.**

- **Onde:** L. 502: “mortes relatadas, não verificadas de forma independente”; L. 485 mantém a atribuição à HRW.
- **Problema:** a tabela transforma o limite de uma investigação em estado geral da evidência.
- **Verificação — procede:** o [relatório da HRW, p. 15](https://backend.hrw.org/sites/default/files/report_pdf/chechnya0517_web.pdf), diz que a própria organização não conseguiu confirmar independentemente as mortes. O [ASTRA-B2.md](dados/regimes/ASTRA-B2.md) já exigia preservar essa atribuição.
- **Correção mínima:** “mortes relatadas, não verificadas independentemente pela HRW nessa investigação de 2017”.
- **Flanco:** ambos/método.

**A2-13 — A “mesma régua” de regimes privilegia o selo institucional sobre a natureza da investigação.**

- **Onde:** L. 483: nível 3 exige “órgão internacional, tribunal ou relatório oficial”; L. 485 admite que o informe da CIDH é secundário.
- **Problema:** uma compilação oficial secundária pode superar uma investigação original de ONG apenas por categoria institucional.
- **Verificação — procede:** o protocolo distingue `L3` de `L3_declarado` por essa regra. O [relatório da HRW](https://backend.hrw.org/sites/default/files/report_pdf/chechnya0517_web.pdf) descreve entrevistas próprias; o artigo reconhece a cadeia secundária da CIDH sobre Cuba. Isso não invalida a ocorrência histórica, mas invalida chamar a hierarquia de primariedade metodológica.
- **Correção mínima:** separar tipo de instituição, evidência original/compilada, corroboração e certeza do fato, aplicando os mesmos critérios a todos os casos.
- **Flanco:** ambos/método.

**A2-14 — A passagem sobre o Brasil precisa preservar o universo e a conclusão da CNV.**

- **Onde:** L. 483: “de 300 a 500 pessoas [...] por dia”; “não houve uma política de Estado formalizada”.
- **Problema:** a condensação permite ler uma contagem ampla de operações policiais como contagem LGBT e uma qualificação sobre extermínio como ausência de política estatal persecutória.
- **Verificação — parcial:** o número e o trecho existem na [CNV, volume II, pp. 301 e 307](https://www.gov.br/memoriasreveladas/pt-br/assuntos/comissoes-da-verdade/volume_2_digital.pdf/@@display-file/file). O número é relato atribuído ao delegado à imprensa, não censo de vítimas LGBT distintas. A CNV também descreve uma visão homofóbica de Estado que legitimava violência e restrições. A v0.4 não nega toda perseguição, mas comprime qualificações essenciais.
- **Correção mínima:** explicitar origem e universo dos 300–500 e conservar a distinção entre ausência de política formal coerente de extermínio e presença de perseguição estatal.
- **Flanco:** esquerda/método.

**A2-15 — A promessa de testes para cada número não corresponde ao que foi testado.**

- **Onde:** [README.md, L. 59](README.md:59): “Cada número publicado é uma asserção de teste”; L. 649–651.
- **Problema:** os testes conferem números selecionados e artefatos, mas não certificam todas as afirmações nem a versão textual atual.
- **Verificação — procede:** executei 44 testes pertinentes, todos aprovados. Entretanto, [test_figuras.py](paper/tests/test_figuras.py:264) lê `paper_v0.1.md` em cinco pontos, inclusive procura `p = 0,19`; a Figura 20 contraditória passa. `manifest/CLAIMS.csv` não existe.
- **Correção mínima:** inventariar a cobertura real, testar o texto corrente e substituir a garantia universal por uma descrição verificável.
- **Flanco:** método.

**A2-16 — O selo confere, mas a descrição de seu alcance e da versão pública não.**

- **Onde:** L. 649: “SHA-256 de cada arquivo do repositório”, “muda se qualquer arquivo mudar” e selo de 721 arquivos.
- **Problema:** existem exclusões além do PDF, e o commit público informado não contém o conjunto local de 721 arquivos.
- **Verificação — procede quanto à redação e prontidão; não procede como acusação de selo quebrado:** `make_provenance.py --verify` aprovou o selo local `5cf914…7066`. Consultei o [commit público 0601c65](https://github.com/ulissesflores/lgbt-indicador-violencia/blob/0601c65/output/hash-chain.md): selo `6bf05c…a6a6a`, 716 arquivos. A diferença é compatível com o segundo commit ainda pendente. MD, PDF e outros componentes estão excluídos por regra.
- **Correção mínima:** dizer “arquivos enumerados no manifesto” e publicar referência imutável que associe commit, selo e hashes do artigo.
- **Flanco:** método.

**A2-17 — “Todos os números” da trilha leve é uma afirmação excessiva.**

- **Onde:** L. 651: “todos os números que dependem só dos derivados distribuídos”.
- **Problema:** o conjunto de passos executados não coincide com esse universo.
- **Verificação — procede:** contei 29 entradas em `PASSOS` de [reproduzir.py](scripts/reproduzir.py). O dimensionamento/custo de F2, por exemplo, não é um desses passos. A matriz de REPRODUCIBILITY distingue corretamente recálculo, conferência e não reprodução, distinção apagada nessa frase.
- **Correção mínima:** vincular a promessa às etapas enumeradas na matriz e informar cobertura por resultado.
- **Flanco:** método.

**A2-18 — A explicação do dimensionamento amostral contém uma causa errada e duas garantias sem demonstração.**

- **Onde:** L. 542: “as respostas no mesmo domicílio se correlacionam”; L. 544: usar DEFF da PNS “superestima” o necessário para painel; L. 534: sobreamostra “não reduz esse número”.
- **Problema:** o DEFF observado é explicado por múltiplas respostas individuais no domicílio, e propriedades de desenhos alternativos são afirmadas sem suas hipóteses.
- **Verificação — procede:** a PNS seleciona um morador para o questionário individual, conforme a [descrição do IBGE para 2019](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/25261-ibge-da-inicio-a-pesquisa-nacional-de-saude-pns-2019). O código estima variância por UPA e pesos. A L. 641 reconhece limitações de transporte do DEFF. Sobreamostragem e triagem dependem do cadastro e da estratégia de recrutamento.
- **Correção mínima:** explicar DEFF por desenho e pesos; tratar eficiência do painel e custo de triagem como hipóteses condicionais.
- **Flanco:** método.

**A2-19 — Multiplicidade e ausência de diferença ainda recebem interpretações fortes demais.**

- **Onde:** L. 431: “1,8 resultados assim”; L. 522: “a linha de base mostra que a falta de fonte não é traço do tema”.
- **Problema:** a expectativa de rejeições simples é aplicada a uma regra composta, e um teste pouco informativo é usado para concluir ausência de especificidade temática.
- **Verificação — procede:** `36 × 0,05 = 1,8` vale para rejeições individuais sob nulas verdadeiras e testes calibrados; a regra descrita incorpora troca, placebo e sinal. O Fisher de 1/49 versus 2/38 é 0,5784, mas não demonstra equivalência.
- **Correção mínima:** referir 1,8 apenas a testes individuais e dizer que a amostra não distinguiu as frequências entre temas.
- **Flanco:** método.

**A2-20 — Há três divergências numéricas/editoriais adicionais.**

- **Onde:** L. 317: “a maior parte das fichas não informa o motivo”; L. 347: “1,4% a 1,5% [...] desde 2022”; L. 277: faixa “8,2% [...] a 28,7%”, remetida à Tabela A6.
- **Problema:** os qualificadores não correspondem aos períodos e cenários efetivamente mostrados.
- **Verificação — procede:** em 2025, faltante efetivo do Sinan é 44,473%, não maioria; Disque 100 em 2026 é `10.461/550.546 = 1,900%`; a Tabela A6 inclui 7,0% no cenário agressão+indeterminada, prevalência 1,96%, 2023.
- **Correção mínima:** substituir “maior parte” por percentual; limitar a faixa do Disque 100 a 2022–2025; especificar o subconjunto usado na faixa C08.
- **Flanco:** método.

**Severidade baixa**

**A2-21 — O inventário distingue hashes disponíveis, mas o texto volta a universalizá-los.**

- **Onde:** L. 653: textos “dos quais o repositório guarda endereço, data de acesso e SHA-256”; [README.md, L. 285](README.md:285): “Toda fonte consultada”.
- **Problema:** a linguagem não preserva as ausências documentadas no manifesto.
- **Verificação — procede:** 464 das 929 entradas `A-ledger` possuem SHA-256; entre 91 brutos, 90. Ter URL e data não equivale a ter hash de documento lido.
- **Correção mínima:** acrescentar “quando disponível” e publicar ausências por categoria e objeto efetivamente hasheado.
- **Flanco:** método.

**A2-22 — A taxonomia N1 ainda chama prevalência de incidência.**

- **Onde:** L. 34 e 1417: “N1, incidência”; contraste com L. 633.
- **Problema:** uma taxonomia central mistura prevalência de pessoas vitimadas, episódios e mortalidade.
- **Verificação — procede:** a PNS utilizada mede autorrelato de vitimização em 12 meses; o corpo reconhece essa distinção.
- **Correção mínima:** renomear N1 como frequência/ocorrência e declarar o estimando específico em cada resultado.
- **Flanco:** método.

**A2-23 — A atualização da agenda de denominadores ficou incompleta.**

- **Onde:** L. 544 e seção 4.5; ausência de referência à edição em curso da PNS.
- **Problema:** a agenda discute pesquisas futuras sem atualizar uma pesquisa nacional já em realização.
- **Verificação — procede:** a [página oficial do Ministério da Saúde](https://www.gov.br/saude/pt-br/composicao/svsa/inqueritos-de-saude/pns/perguntas-frequentes) informa a terceira edição, PNS 2026, em coleta. Isso não significa que já existam microdados adequados ou denominador trans utilizável.
- **Correção mínima:** registrar a situação e condicionar qualquer incorporação à divulgação efetiva de variáveis, pesos e documentação.
- **Flanco:** método.

**A2-24 — O título principal pode permanecer; o subtítulo e dois títulos internos precisam de precisão.**

- **Onde:** L. 2–3: título novo e “2010–2026”; L. 188 e 204: “fora do Brasil”, embora incluam Luis et al.; L. 198 e 208.
- **Problema:** o intervalo do subtítulo não caracteriza todo o material histórico/bibliográfico, e os títulos internos contradizem a presença de estudo brasileiro.
- **Verificação — parcial:** **não procede** repetir o ataque ao antigo “ninguém sabe”: ele saiu. O título novo não afirma igualdade de risco nem inexistência de violência. Procedem a contradição “fora do Brasil” e a necessidade de identificar 2010–2026 como recorte das séries brasileiras, com 2026 parcial.
- **Correção mínima:** manter o título principal; precisar o recorte temporal e trocar os títulos internos por “evidência brasileira e internacional”.
- **Flanco:** ambos/método.

Na seção 3.9, **não reapresento como erros** a atribuição de 35 mil homossexuais às UMAP, a apresentação de 64 mil condenações alemãs como contagem administrativa exata, a omissão das outras acusações no agregado do Estado Islâmico ou a mistura explícita de unidades para ordenar regimes: a v0.4 corrigiu esses pontos. A nota da L. 504 impede usar a tabela como ranking. A existência de casos em regimes diferentes sustenta uma proposição existencial; não estima frequência, intensidade ou efeito da ideologia.

# 3. Recontagem independente

Os cálculos abaixo foram feitos em memória, lendo os arquivos distribuídos. **Recontar derivados não equivale a refazer a extração dos microdados nem a validar classificações nominais.**

| Número/objeto | Arquivo e cálculo independente | Resultado e comparação |
|---|---|---|
| 1. Amostra LGB+ e MDE | [deff_pns2019.csv](research-2026-10-21-rodada3/F2-custos/deff_pns2019.csv): domínio LGB+, física; fórmula de duas proporções, α=5%, poder=80%, DEFF=5,10688, bisseção. | **n=1.554; MDE=60,7034%**. Concorda com L. 534 e Figura 24. |
| 2. Dimensionamento para +30% | Mesmo arquivo: cálculo contínuo de duas proporções × DEFF. [n_necessario.csv](research-2026-10-21-rodada3/F2-custos/n_necessario.csv). | **5.786,288 LGB+**, arredondados a **5.787**. Os derivados publicam **305.955** adultos. Há ressalva de precisão abaixo. |
| 3. RP física bruta | [seguro_pns2019.csv](dados/pns/seguro_pns2019.csv): `0,1469592557313 / 0,03824548307977`. | **3,842526**. Concorda com **3,84**, L. 158. Não reestimei a regressão ajustada. |
| 4. Parcela LGB+ entre vítimas | [c05_razao_direta.csv](dados/pns/c05_razao_direta.csv): razão ponderada e `R ± 1,96×EP`. | **7,1231%; IC 5,1124–9,1337%**. Já `179/3.291=5,4391%` é a fração não ponderada: não constitui erro, mas deve ser distinguida. |
| 5. Sinan nacional | [serie_campo55_uf_ano.csv](dados/sinan/serie_campo55_uf_ano.csv): soma de 27 UFs comparada com a linha BR, sem somá-la novamente. | **2.173 / 2.264 / 2.410**, 2023/2024/2025. A duplicação anterior não voltou. |
| 6. Faltante efetivo do motivo | Mesmo CSV: `(ignorado+branco+não se aplica)/notificações interpessoais`, linha BR. | **53,3701% em 2015; 44,1503% em 2023; 42,4622% em 2024; 44,4730% em 2025**. L. 309 confere; “maior parte”, L. 317, não. |
| 7. Correlação principal entre fontes | [concordancia_v2.csv](dados/concordancia/concordancia_v2.csv): filtro `S0 principal`. | Brutas **0,527/0,575/0,590/0,740**; UFs **22/23/23/22**; parciais **0,142/0,166/0,152/0,324**. Concorda com L. 319. |
| 8. Funil GGB | [codificacao_A.csv](research-2026-10-21-rodada3/F3-ggb/dados/codificacao_A.csv): recuperação; correspondência S/P; morte S; identificação LGBT S. | **160→106→88→73→50**. `50/160=31,25%`, arredondamento adotado **31,3%**. A soma confere; a correspondência parcial fica oculta no texto. |
| 9. Sensibilidade de correspondência GGB | Mesmo CSV: repetir o filtro admitindo apenas `corresp=S`. | **73 correspondências estritas; 61 mortes violentas; 40 casos finais**, ou **25,0% de 160**. Dez dos 50 principais dependem de `P`. |
| 10. Motivo no GGB | Mesmo CSV, entre as 73 mortes da regra S/P. | **3/73=4,1096%** com atribuição LGBTfóbica; **35/73=47,9452%** desconhecidos. Concorda com L. 247. |
| 11. Chapman principal | [captura_recaptura_sensibilidade.json](research-2026-10-21-rodada3/F3-ggb/dados/captura_recaptura_sensibilidade.json): `(118+1)(139+1)/(88+1)−1`. | **186,1910**; `118/N=63,3758%`. Concorda com L. 257, sob as hipóteses. |
| 12. Chapman com pareamento estrito | Mesmo arquivo: substituir sobreposição 88 por 74. | **221,1333**; `118/N=53,3615%`. Sensibilidade existente, não incorporada ao destaque do artigo. |
| 13. Razões C08, cenário principal | [c08_numeradores.csv](dados/ggb/c08_numeradores.csv): `N/E₀`, agressão, prevalência 1,89%. | 2023: N0 **22,9013%**, N1 **19,6933%**, N2 **8,3763%**. 2024: **28,7361%**, **26,5636%**, **16,4912%**. Conferem com os números principais. |
| 14. Limites por marginais | [c08_cenarios_marginais.csv](dados/ggb/c08_cenarios_marginais.csv): confrontar os cenários e `269−(96+6−3)−6`. | Faixas **100–118** e **164–168**; contraexemplo **164<167**. Confirma que N2 não é limite inferior harmonizado. |
| 15. Taxas por sexo e raça | [asr_brasil.csv](dados/sim/asr_brasil.csv): média aritmética de 2022–2024 por grupo. | Mulheres não negras **2,6033**; mulheres negras **4,3300**; homens não negros **19,9900**; homens negros **51,7267**. Razão extremos **19,87**, arredondada **19,9**, L. 241. |
| 16. Variações federais | Mesmo arquivo e [c10_e1_federal.csv](dados/exposicao/c10_e1_federal.csv): `100×(taxa final/taxa anterior−1)`. | **+11,1068%; −4,1652%; −21,0069%; −10,5915%**. Concorda com Tabela 7. São variações descritivas. |
| 17. Trocas estaduais | [c10_e2_trocas_longo.csv](dados/exposicao/c10_e2_trocas_longo.csv): filtro total, contar sinais e calcular mediana. | **67 trocas; 31 altas/36 quedas; mediana −0,6859%**. Com indeterminadas: **34/33; +0,4739%**. Concorda com L. 449. |
| 18. Contraste C09 | [c09_d2_resultados.csv](dados/presidencia/c09_d2_resultados.csv): `100×expm1(25,681×limite)`. | IC normal **−18,2752% a +9,6121%**; t **−18,8578% a +10,3992%**. Concorda com L. 431. |
| 19. Quebra nacional e placebo | [c09_d1_resultados.csv](dados/presidencia/c09_d1_resultados.csv): selecionar total, 2019 e placebo anterior. | **−17,0463%** e **−21,8214%**, ambos com IC abaixo de zero. Divergência interpretativa da Figura 20. |
| 20. Fisher parlamentar | [r7_parlamento_sensibilidade.csv](research-2026-10-21-rodada3/escrutinio/simetria/r7_parlamento_sensibilidade.csv): soma bilateral de probabilidades hipergeométricas. | `1/49 vs 2/38`: **0,5783952**; `0/49 vs 2/38`: **0,1879177**; `1/50 vs 2/38`: **0,5758001**. Conferem. |
| 21. Disque 100 | [d100_serie_anual.csv](dados/disque100/saidas/d100_serie_anual.csv): grupo LGBT dividido pelo canal, mesma unidade/período. | 2021: **1.367/222.010=0,6157%**; 2025: **9.346/637.890=1,4651%**; 2026 parcial: **10.461/550.546=1,9001%**. A faixa “desde 2022” precisa de término. |
| 22. Inventário de fontes | Ledgers enumerados em [INVENTARIO-PUBLICO.json](manifest/INVENTARIO-PUBLICO.json): recontagem e normalização conforme regra documentada. | **19 ledgers; 1.652 registros; 906 identificadores; 905 obras; 11 idiomas; 166 arquivos Python**. Concorda com inventário e README atuais. |
| 23. Cobertura de hashes | [MANIFESTO-FONTES.csv](manifest/MANIFESTO-FONTES.csv): contar por `parte` e preenchimento de `sha256`. | **929 entradas A-ledger, 464 com hash; 91 brutos, 90 com hash**. Não significa hash documental de toda fonte. |
| 24. Regimes | [sources.jsonl](dados/regimes/sources.jsonl): contar linhas JSON não vazias. | **53 registros**, como L. 1461. Não equivale a 53 documentos integralmente lidos. |

**Precisão de N02.** Com os insumos arredondados publicados no CSV, obtenho `ceil(5.786,288…/0,0189122)=305.956`, uma unidade acima de 305.955. O gerador calcula com precisão anterior à exportação; portanto, isso é uma **lacuna de precisão para reprodução**, não prova de que 305.955 esteja errado. Já a expressão impressa `5.786,3/1,89%` resulta em aproximadamente 306.153,4: os números exibidos são arredondados e não reproduzem literalmente o inteiro. A antiga divergência de 305.993 foi corrigida.

**Integridade e execução conferidas:**

| Objeto | Resultado |
|---|---|
| Selo local | **721 arquivos**, `5cf914b02715db7a0f009185bac1540ae53d26875f7be5985bcf7b022b827066`; verificação aprovada. |
| Selo do commit público informado | **716 arquivos**, `6bf05c72fde4a9310356867afc03c8c80545ecce2187bb970d9e65f7ae6b9a6a`; corresponde a outra versão. |
| Markdown | `f283475e8853e8cec20278a46503bd756f0f68bc288249e8cc367e9980c7f69f`; confere. |
| PDF | `53c74d093e0f1348ad2ee25d982972eefdb05ccbbc0e563b33727987b1eef1a9`; **126 páginas, 2.529.521 bytes**; confere. |
| DOCX | `898af2f0455581938c867a408be6c0f07e1ee66d4abe8a0db0286a5a99687dba`; confere. |
| Testes executados | **7** de correções, **32** de figuras e **5** de C09: **44 aprovados**. |
| Testes não executados | Três comparações opcionais com árvores externas; suíte completa e trilhas que escrevem réplicas não executadas. |

As divergências encontradas entre superfícies são: mortalidade absoluta no Resumo versus vinculação no corpo; equivalência PNS–Sinan na legenda/apêndice/README versus distinção no corpo; significância na Figura 20 versus CSV/corpo/Tabela A13; “numeradores comparáveis” no README versus cenários no artigo; pareamentos parciais omitidos no funil; sensibilidade de Chapman omitida no destaque; IC confundido com MDE; maioria de faltantes versus 44,5%; Disque 100 “desde 2022” versus 1,9% em 2026; faixa C08 versus cenários adicionais da Tabela A6; população brasileira em títulos “fora do Brasil”; atribuição retirada na linha da Chechênia; cobertura universal de testes/hashes versus cobertura efetiva; e pacote público anterior versus selo local novo. A diferença de 28 passos no relato histórico da v0.3 e 29 na configuração atual está datada e **não deve ser tratada como falsificação do resultado histórico**.

Na conferência externa da Tabela 9:

- [USHMM](https://encyclopedia.ushmm.org/content/en/article/gay-men-under-the-nazi-regime): os números nazistas citados encontram apoio.
- [Bundestag, p. 12](https://dserver.bundestag.de/btd/18/120/1812038.pdf): cerca de 64 mil é estimativa adotada no documento, não a série judicial de 54.023; a v0.4 preserva essa distinção.
- [BOE](https://www.boe.es/buscar/doc.php?id=BOE-A-1979-700): publicação em janeiro de 1979 confere.
- [Tahbaz](https://www1.udel.edu/LAS/Vol14-2Tahbaz.html): 35 mil refere-se ao total estimado de internados; não fornece proporção global confiável de homossexuais.
- CNV e HRW: conferidas nos limites descritos nos ataques.
- **Não conferido integralmente nesta rodada:** original completo de Valodzin, total polonês de 11 mil, cópia arquivada da CIDH de 1983, cada episódio/contagem ONU–OutRight e cada referência das coortes recentes. Não os certifico apenas porque constam do ledger.

Também ficaram **não conferidos** a retabulação dos microdados brutos, a ligação nominal caso–fonte do GGB, a anterioridade independente dos protocolos e a equivalência visual de todas as 126 páginas. A inspeção visual do PDF foi amostral; seus hashes e número de páginas foram conferidos.

# 4. Veredito

**Não está pronta para publicar como preprint nesta forma.** O impedimento principal são contradições verificáveis entre conclusões, legendas e dados, não os erros aritméticos antigos já corrigidos.

Condições mínimas:

1. Corrigir mortalidade no Resumo/Abstract, equivalência PNS–Sinan, Figura 20, interpretação de poder e alcance da busca de atos estatais.
2. Sincronizar README, apêndices, rótulos dos derivados e textos das figuras; mostrar as sensibilidades de pareamento GGB e captura-recaptura.
3. Corrigir a classificação de evidência por origem institucional e preservar as qualificações da Tabela 9.
4. Substituir garantias universais de testes, hashes e recálculo por cobertura enumerada; testar o texto atual.
5. Publicar o conjunto final em referência imutável, associando commit, selo e hashes do artigo, com relatório de validação dessa mesma versão.

O título principal novo pode permanecer. Ele não resolve, por si, os absolutos que sobreviveram no resumo e nos vereditos.