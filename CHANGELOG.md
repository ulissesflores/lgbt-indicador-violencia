# Changelog

Formato: Keep a Changelog; versionamento semântico. Versão `0.x` até o commit que prepara o DOI, que leva a `1.0.0`: nenhum release do GitHub antes do aval do autor.

## [1.0.0] - não lançada (artigo v0.5; 2026-10-30 a 2026-11-01)

### Acrescentado (2026-11-01, decisão do autor: análises que os revisores pediram e o texto declarava como não feitas)

- Razões ajustadas sem os 9 adultos de cor ou raça ignorada (8 heterossexuais e 1 LGB+), que no ajuste do artigo ficam
  na referência com os não negros: mudam no máximo 0,02 (Tabela C12; seção 8 de `dados/pns/agressor_risco_pns2019.md`).
- Razão por tipo de agressor também com o cônjuge no domicílio no ajuste (coluna nova da Tabela C10): familiar 4,31
  (2,33 a 7,99); como com o estado civil, só amigo, colega ou vizinho deixa de ser firme.
- Tabela 6 com a fração LGB+ de cada modo de preenchimento, sobre todos os adultos do modo (1,35% com entrevistador e
  3,26% com autopreenchimento): o módulo na PNAD Contínua detectaria 37,9% ou 23,8% (Tabela K2;
  `research-2026-10-21-rodada3/F2-custos/opcoes_por_modo.csv`).
- Terceira leitura, cega, dos 6 desacordos da conferência do GGB de 2019 por um modelo de outra família (GPT-6 Astra,
  `research-2026-10-21-rodada3/F3-ggb/scripts/s15_terceiro_codificador.py`), por maioria de dois de três, conferida
  pelo autor (`research-2026-10-21-rodada3/F3-ggb/dados/adjudicacao.json`): só um caso muda as contagens (morte indeterminada vira homicídio); mortes
  violentas confirmadas passam de 73 para 74 (84,1% de 88) e o motivo desconhecido, de 35 para 36; os 50 de 160
  verificáveis não mudam, e o kappa continua sendo o dos dois primeiros codificadores. Figura F1 refeita.
- `docs/processo-e-custo.md`: quem fez cada parte, rodadas de verificação, uso de cada modelo (tokens novos separados dos
  lidos do cache), tempo, custo e fontes consultadas.
- Pareceres da pré-publicação pub2 em `paper/v05/revisao/pub2/`.
- A subdeclaração de orientação LGB+ segue declarada como limite, sem estimativa (decisão do autor).

### Corrigido (diagramação do PDF, `paper/tools/export_v04.py`)

- Carimbos de data e hora da Tabela B3 sem quebra no meio; intervalos numéricos das tabelas sem quebra entre linhas;
  parágrafo com impressão digital longa alinhado à esquerda (no justificado, a linha anterior esticava); a nota da
  Tabela I1 desce com as últimas linhas da tabela.

### Corrigido (pré-publicação: GPT-6 Astra, Grok 4.7 e Gemini 4 Argon leram o PDF pronto e este repositório; respostas em `paper/v05/revisao/pub1/MATRIZ.md`)

- Metadados na versão 1.0.0, com data de 31/10/2026 e descrição da v0.5 (`CITATION.cff`, `codemeta.json`, `.zenodo.json`,
  `pyproject.toml`); o verificador de publicação aceita a versão de release com acesso fechado até o aval do autor.
- README, `REPRODUCIBILITY.md`, `ROADMAP.md` e a Tabela M1 do Apêndice M apontam o artigo v0.5 (`docs/paper/`, `paper/v05/`);
  caminho da LiHS corrigido; números do Sinan iguais aos do PDF (42,5% a 44,5%; 0,4% a 0,5%).
- Apêndice H: a Portaria nº 1.576/2019 foi lida no Diário Oficial depois da busca, e o texto diz isso, com a referência;
  sem as autorremissões. Remissões herdadas com o número da v0.4.4 apontam as seções e os apêndices atuais.
- Artigo: "Essas coortes são descritas no Apêndice E" (o apêndice não traz os números delas); "nesse material" e "no mesmo
  material" corrigidos; fontes do custo do painel citadas (contrato da Gambling Commission e câmbio do Banco Central);
  iniciais nos dois Clark; autores institucionais por extenso na primeira citação; p < 0,001 no lugar de 0,000 (Tabela G7);
  regra estrita do Disque 100 (39 denúncias) também no Apêndice D; acabamento da saída de script no Apêndice C.
  Referências: 105 (+ Portaria, Gambling Commission, Banco Central do Brasil e a reportagem que reproduz os limites
  declarados pela Transgender Europe).
- `ruff check` e `ruff format --check` limpos em `make_provenance.py` e `scripts/registra_run.py`.
- Não procederam (conferidos no arquivo): "(Apêndice )" sem letra, "2,58 8,90" na Tabela 3, URL da Lei 15.380 e
  `ADENDO-2.hora.txt` truncado.

### Alterado (texto em `paper/v05/`; a v0.4.4 em `paper/paper.md` segue como estava)
- Estrutura em dois eixos: o que os dados permitem afirmar sobre a mortalidade e a violência, e o que cada fonte deixa de medir.
- Governos: as séries LGBT+ (lista do GGB, Disque 100, fichas do SUS, boletins do Anuário) são REGISTRO, e nenhuma separa violência de registro;
  a resposta à pergunta "a violência subiu ou caiu no governo X" passa a ser "não dá para saber". A Figura 8 (nova) mostra o que cada série
  mostra por período de governo, ao lado do homicídio geral com e sem a causa indeterminada; a variação por governo é descrição, nunca causa.
- Atos de governo (proteção, retórica hostil, ato administrativo hostil) saem do corpo do texto e vão para o Material Complementar MC7.
- Seção 3.5: parágrafo de simetria com a checagem da LiHS sobre a lista do GGB de 2016 (31 "sim", 127 "não", 159 "inconclusivo", 23 "não
  localizado", 6 "exterior", 1 duplicado, em 347); a contra-base é a única auditável, com os limites declarados, e "falta ciência do outro lado"
  fica como hipótese não medida (`research-2026-10-30-contraponto/`).
- 8 figuras em fundo branco (cinco `fig_v05_*`, novas ou redesenhadas, e três já presentes em `paper/figures/`); título, nota e fonte ficam no documento.
- Glossário como Apêndice A.

### Alterado (PDF no padrão Codex Hash e APA 7; reprovação do autor em 2026-10-31)

- Formato pela norma da casa (`CODEX-HASH-STYLE.md`, contrato `codex-hash-canon.json`): capa com o logo do Codex Hash
  Research Laboratory, corpo justificado sem recuo, títulos à esquerda, quebra de página só em Resumo, Abstract,
  1. Introdução, Referências e em cada apêndice. Validador da casa: 54/54 requisitos (1 N/A por desenho). O PDF segue
  gerado pelo Word, e as referências em APA 7.
- APA 7: uma só lista de referências (as 18 obras citadas só no material complementar entram na lista do artigo, que
  passa a 101 entradas); MC1 a MC12 viram Apêndices B a M, com tabelas e figuras numeradas pela letra (Tabela C1);
  mapa dos rótulos antigos em `paper/v05/` (a revisão r5–r8 usou os rótulos MC). Subtítulos herdados perdem o número
  da v0.4.4; a Tabela B1 liga o número antigo ao título.
- Repositório: `docs/paper/paper-final.{pdf,docx}`; `runs/<UTC>/manifest.json` com o pip freeze de cada execução
  selada (`scripts/registra_run.py`); `codemeta.json` com a afiliação; `.zenodo.json` com as licenças; `docs/paper/` e
  `runs/` fora do selo. Nos vereditos do juiz v4 publicados, o nome da instituição de ensino citada pela rubrica foi
  omitido (nota em `paper/AUDIT.md`).

### Adicionado (PDF em APA 7, pré-DOI)

- Primeiro PDF da v0.5 (rascunho de trabalho de 169 páginas, com o Material Complementar MC1 a MC12; não distribuído):
  substituído no mesmo dia pelo PDF no padrão Codex Hash, em `docs/paper/paper-final.pdf` (ver acima). Fonte única
  montada por `paper/tools/monta_fonte_v05.py`.
- `paper/tools/export_v04.py` e `crivo_docx.py` aceitam rótulos do MC (Tabela MC2.A1); marcador de lista sem tabulação
  em Arial; tabela de até 10 linhas fica inteira numa página.

### Corrigido (leitura do PDF)

- MC: os "Apêndices" herdados da v0.4.4 viram seções MC1.B, MC2.A e MC12.D (não colidem com o Apêndice A do artigo);
  6 tabelas sem rótulo viram Tabelas MC2.B1 a MC2.B6, com título e Nota; títulos sem marca de versão, parecer ou
  caminho de script; "release" -> "divulgação"; seta da Tabela MC4.A16.
- Referência de Campbell (1979): faixa de páginas 3–43 com traço curto.
- Figura MC4.5 (`fig25`): fundo branco no lugar das faixas cinza entre as linhas; valores desenhados iguais.

### Corrigido (rodada r8: verificação dos três revisores; Argon recomenda aceitar sem novas exigências; respostas em
`paper/v05/revisao/r8/MATRIZ.md`; texto corrigido = revisão r9)
- `paper/figures/make_figures.py` (Figura MC6.20): "quebra um ano antes" no lugar de "placebo"/"troca de controle", na imagem e nos
  textos fora dela (`textos_fora_da_imagem.json`); só a figura 20 foi regenerada.
- Texto: seção 2.2 com as comparações de mortes noticiadas de pessoas trans; exceção de amigo, colega ou vizinho nas seções 4.3 e 6;
  seção 2.6 diz que o efeito dos desacordos do GGB não foi estimado.
- Material Complementar: coluna da Tabela MC6.A13; extremos estaduais do Sinan no mesmo universo do parágrafo (11,0% em Roraima a
  54,2% em Mato Grosso do Sul, em 2023).

### Corrigido (rodada r7: verificação dos três revisores; respostas em `paper/v05/revisao/r7/MATRIZ.md`; texto corrigido = revisão r8)
- Texto: comparações entre países existem só para mortes noticiadas de pessoas trans, sem cobertura comum; o número de adultos LGB+ da
  Tabela 6 é hipótese de planejamento, e o modo de preenchimento é escolha a testar em piloto; o excesso por parceiro, familiar ou
  desconhecido persiste também com o estado civil; Kitagawa (1955) entra nas referências do artigo.
- `paper/figures/make_figures.py`: Figura MC6.18 diz "mudança anterior não detectada" (não significância não prova ausência);
  Figura MC10.24 diz "80% de poder para aumento"; só as figuras 3 e 17 foram regeneradas.
- Material Complementar: o teste de 2018 do MC6 é sensibilidade à data, com a série inteira; denominador da parcela de indeterminadas;
  10 estados distintos de controle no estudo de eventos; filtro de violência não autoprovocada e 53,4% no MC3; nota de intervalo nominal
  na tabela de fatias do MC2; universos de 347 e de 258 casos separados na checagem da LiHS; "(MC12)" no lugar de "(Apêndice D)".

### Corrigido (rodada r6: verificação de Astra e Grok e revisão completa do Gemini 4 Argon, pelo navegador, com o repositório anexo;
respostas em `paper/v05/revisao/r6/MATRIZ.md`; texto corrigido = revisão r7)
- Texto: placebo de 2018 vira teste de sensibilidade à data, e o início da queda vem dos valores (31,47 em 2017, 27,61 em 2018);
  denominador da causa indeterminada = agressões mais indeterminadas; "não localizado" no lugar de "ninguém calculou"; a razão global
  não identifica o agressor, que é analisado à parte; quatro conclusões; diferença (e não fatia) de policial, com 5 vítimas, sem
  correção para comparações; um agressor por vítima (episódio mais grave) e razão por familiar sem ajuste por coabitação, declarados;
  efeito de desenho por desfecho e identificação LGB+ dependente do modo, na nota da Tabela 6; LGB+ com "outra orientação" no Resumo,
  Abstract e Tabela 2; revisores da checagem da LiHS (3 com dois, 14 em branco); comparação com o mesmo segundo codificador (p = 0,58).
- `paper/figures/make_figures.py` (Figura MC6.18): "deslocamento para a direita/esquerda" no lugar de "troca de lado"; só essa figura
  foi regenerada.
- Material Complementar: 35 anos (MC9) e Hatzenbuehler et al. (2020) alinhados ao corpo; Disque 100 com três formatos e a unidade de
  cada um; "os 2 desacordos" e correção para população finita na Tabela MC5.C0; raça ignorada na referência das regressões, declarada;
  células sem caso como "nenhum caso"; FRA não probabilística; moeda da Tabela MC10.10; Kitagawa (1955); Atlas da Violência 2026,
  não citado, sai das referências.

### Corrigido (rodada r5 dos revisores GPT-6 Astra e Grok 4.7, que leram o texto e este repositório; resposta crítica a crítica em
`paper/v05/revisao/r5/MATRIZ.md`; texto corrigido = revisão r6)
- Texto: κ da conferência do GGB declarado (0,91 condição LGBT+; 0,46 morte violenta; Tabela MC5.C0); fichas do Sinan = violência não
  autoprovocada, e a falta de motivo soma ignorado, branco e "não se aplica"; efeito mínimo detectável = 80% de poder só para aumento
  relativo; ajustes da PNS listados em separado; LGB+ inclui "outra" orientação; regra complementar de elegibilidade dita não prospectiva
  no corpo; ressalvas de Valodzin (cerca de metade com estupro ou menores) e dos 15 diplomatas (7 por homossexualidade); FRA como amostra
  não probabilística; janela do ONS; cobertura do corpus do Parlamento e intervalo do κ de fonte; custo do painel pela internet como
  contrato estrangeiro convertido pelo câmbio de 20/10/2026; SIDRA 9606 na referência do IBGE.
- `dados/sim/padroniza_idade.py`: nos extremos de raça ignorada, os ignorados entravam de novo sobre a base já redistribuída; agora entram
  uma vez sobre a raça conhecida (saídas publicadas iguais a duas casas: 2,60 e 2,42).
- `dados/exposicao/fig_caminho_v05.py` (Figura 1): a linha da lista passa a "GGB" (os números são só do GGB) e o Sinan, a "sem motivo útil".
- Material Complementar: estudo de eventos chamado de "deslocamento" do escore (não troca de bloco); intervalo degenerado [0,00; 0,00]
  vira "nenhum caso"; remissões a tabelas e figuras apontam o MC onde cada uma mora; Tabela MC0.1 mapeia as seções da v0.4.4; o selo
  citado é o da v0.4.4, e o atual fica em `output/hash-chain.md`.

### Corrigido (lista com o texto anterior ao lado em `docs/historico-de-correcoes.md`, seção 12)
- Os "35 anos": a v0.4.4 dizia que o número remontava a "uma única autora". O dossiê da ANTRA de 2019 o atribui a Antunes (2013, p. 32) e a uma
  reportagem da Agência Brasil (Martins, 2018, p. 77), e calcula a idade média das vítimas, 29,7 anos (p. 30), que não é expectativa de vida.
- "familiar em 31,2% (19,3%" -> 19,2%, valor bruto 19,2466% (o 19,3 vinha de arredondar duas vezes).
- "Reino Unido" -> Inglaterra e País de Gales onde a fonte é a ONS ou o Home Office.
- "42% a 44%" -> "42,5% a 44,5%" (campo de motivo do Sinan sem informação útil, 2023-2025).

### Adicionado
- Material complementar (até a r8, MC1 a MC12; no PDF, Apêndices B a M), quadro de afirmações (`QUADRO-E2.md`) e referências em `paper/v05/`, com
  `README.md`, `SHA256SUMS.txt` e 9 figuras. Os `.md` e `SHA256SUMS.txt` ficam fora do selo (como `paper/paper.md`); figuras e README entram.
- `research-2026-10-30-contraponto/`: briefing, três frentes (Brasil, exterior, academia), `sources.jsonl` (131 registros; o inventário passa a 20
  ledgers e 1025 identificadores) e conferência de identificadores. A planilha da LiHS NÃO é distribuída (nomes de vítimas e de acusados):
  `research-2026-10-30-contraponto/dados/lihs-checagem-ggb2016.META.md` guarda a URL, o SHA-256 e a tabulação.
- Scripts e saídas novos: `dados/pns/agressor_risco_pns2019.{py,csv,md}` (quem agrediu e o risco por tipo de agressor; moram com cônjuge 29,49% dos
  LGB+ e 62,39% dos heterossexuais) e os geradores de figura `dados/pns/fig_pns_v05.py`, `dados/pns/fig_agressor_pns2019.py`,
  `dados/exposicao/fig_caminho_v05.py`, `dados/exposicao/fig_series_por_governo.py` e `dados/disque100/fig_disque_v05.py`.
- `tests/test_numeros_v05.py`: trava a tabulação da LiHS, as variações de homicídio por governo (a de Bolsonaro com agressão e causa indeterminada,
  -13,7%, sai da série de precisão cheia: nas 2 casas de `asr_brasil.csv` dá -13,6%), a fatia de causa indeterminada (18,0% em 2018 e 30,1% em
  2024) e a coabitação na PNS.
- `make_provenance.py`: os `.md` e `SHA256SUMS.txt` de `paper/v05/` entram na lista de exclusão do selo.

## [Não lançado] - artigo v0.4.4 (2026-10-26), segundo commit

### Corrigido (achados da rodada v4-5 do juiz sobre a v0.4.3, com o texto inteiro entregue e prova de leitura: `paper/AUDIT.md`; lista com o texto anterior ao lado em `docs/historico-de-correcoes.md`, seção 11; mudanças de precisão sem número novo, versão não julgada de novo)
- Tabela A2: a Nota diz a regra de cor ou raça (negros = pretos e pardos; não negros = brancos, amarelos e indígenas) e que 1 adulto
  LGB+ tem cor ou raça ignorada e fica fora das duas linhas (916 + 637 = 1.553 dos 1.554); as células não mudam.
- Seção 3.5 e Nota da Tabela A5: 7,1% é a parcela ponderada pelo desenho amostral; 179 de 3.291 são contagens da amostra não ponderada.
- Tabela 1 e Referências: o enquadramento dos boletins de "racismo por homofobia ou transfobia" cita o acórdão da ADO 26 do Supremo
  Tribunal Federal (2019), fonte primária já no registro de fontes; `paper/tools/eeat_referencias.py` classifica a referência nova.
- Seção 2.6 e Tabela D1: o quarto exame (rodada v4-5) é apontado.
- `docs/revisao/S2-TRIAGEM.md` (cópia), esta lista (v0.4.2) e `docs/historico-de-correcoes.md`, seções 9 e 10: "corte de cerca de 94 KB"
  -> corte do programa do juiz em prompts de 100.000 bytes ou mais (94 KB é o começo entregue, e não o limiar; medido em 2026-10-26).

### Adicionado
- Veredito da rodada v4-5 (`paper/build/juiz/rodada-v4-5.json`), fora do selo.

## [Não lançado] - artigo v0.4.3 (2026-10-25), base da v0.4.4

### Corrigido (descontos da rodada final v4-4 sobre a v0.4.2: `paper/AUDIT.md`; lista com o texto anterior ao lado em `docs/historico-de-correcoes.md`, seção 10; mudanças de texto sem número novo, versão não julgada de novo)
- Seção 4.1: a terceira hipótese usa o mesmo veredito da Tabela 11 (não sustentada como taxa ou total; contrariada como invenção).
- Seção 2.6: modelos de linguagem codificaram itens de discurso (dupla codificação e teste exato de Fisher já descritos); nenhum
  número de resultado foi gerado por modelo; o juiz do segundo exame leu só parte do texto; o terceiro exame é apontado na seção 2.6
  e na Tabela D1.
- `docs/laudos/MIDIA.md` e Tabela A17: a célula de censo F2 × Parlamento perde o intervalo [43-53] (49 é contagem do universo
  inteiro, como nas outras linhas de censo); a soma segue 871.
- Glossário: verbete do numerador B encurtado (o Apêndice C volta a caber em duas páginas).

## [Não lançado] - artigo v0.4.2 (2026-10-25), base da v0.4.3

### Corrigido (terceiro exame da v0.4.1, com leitura integral comprovada: `paper/AUDIT.md`; lista com o texto anterior ao lado em `docs/historico-de-correcoes.md`, seção 9)
- Objeção 7 da seção 4.3: a busca de atos de governo é simétrica no procedimento, e o resultado não (proteção só nos mandatos do PT; retórica
  hostil e ato administrativo hostil só em 2019; omissão nos dois lados), conforme a Tabela 8.
- Seção 4.4: o levantamento de vitimização calibraria os registros de ocorrência e de notificação, e não as contagens de mortes da sociedade
  civil, que dependem do registro no óbito (coerente com a seção 3.13).
- Seção 3.7: a janela de três anos é cortada em 2012-2024 (47 das 67 trocas com janela completa); entra, ao lado do principal, o recorte de
  janela completa já calculado em `dados/exposicao/c10_resultados.md` (20 subiram, 27 caíram; mediana -0,8%; p = 0,008).
- `docs/laudos/MIDIA.md` e Tabela A17: entra a linha F3 na Wikipédia (60 itens), que faltava; a tabela passa a somar os 871 itens da amostra.
- `dados/sim/padroniza_idade.py` e `asr_brasil.md` (Tabela A16): "limite inferior (raça ignorada descartada)" -> "cenário"; nenhum número mudou.
- Seis palavras-chave (sai "reprodutibilidade"); três expressões latinas explicadas na frase; glossário do numerador B; atenuação do
  coeficiente condicionada ao erro de medida clássico.
- `docs/revisao/S2-TRIAGEM.md` (cópia) e `docs/historico-de-correcoes.md`, seção 8: a rodada v4-1 do juiz recebeu o artigo inteiro, mas
  leu só parte dele (corte do programa do juiz em prompts de 100.000 bytes ou mais (descarga do programa grok 1.0.62, corrigida com --verbatim; correção de 2026-10-26)); correção datada, original intacto.

### Adicionado
- Vereditos do terceiro exame (`paper/build/juiz/rodada-v4-3-astra.{json,md}`, `rodada-v4-3-gemini.{json,md}`) e da rodada final
  (`rodada-v4-4-astra.{json,md}`), fora do selo; `.gitignore` deixa entrar os `rodada-v4-*.md`.

## [Não lançado] - artigo v0.4.1 (2026-10-25), base da v0.4.2

### Corrigido (segundo exame da v0.4: `docs/revisao/`; lista completa com o texto anterior ao lado em `docs/historico-de-correcoes.md`, seção 8)
- Resumo e Abstract: as duas regras de elegibilidade da mortalidade fora do Brasil ("sustentada" só pela complementar, "parcial" pela
  pré-registrada); a fração verificável do GGB como fração, não prova (50 de 160; 40 com correspondência estrita); o alcance da busca de atos de
  governo (seis governos federais; agentes estaduais e locais não inventariados) e os episódios de 2019; a linha de base do Parlamento (2 de 38).
- Nota da Figura 20 (a queda de 2019 é distinguível de zero, mas não atribuível, porque o placebo de 2018 também cai); intervalo de confiança
  separado de efeito mínimo detectável (seção 3.6, Tabelas 11, Figuras 16 e 21, glossário); Nota da Figura 11 sem "mesma grandeza".
- Figura 25 (`fig7`): coluna de motivação em cinza, "não testável" (nenhuma fração nacional estimada), e não "não sustentada"; linha
  "LGBT+ morrem mais que as demais pessoas?"; N1 = "ocorrência". Figuras 18 e 19 (`fig3`, `fig22`): letra interna de 9,5 pt (cerca de 7,4 pt
  impressa a 14 cm). Figura 1 (`fig24`): sem a sigla BRC; faltante do Sinan arredondado como no texto.
- Anotações dentro das imagens que liam o intervalo como limite de detecção (Figuras 16, 18 e 21) reescritas; sai a seta "para o Sinan
  igualar a PNS" da Figura 11 (universos diferentes).
- Faltante efetivo do campo de motivo do Sinan: 42% a 44% (2023-2025), e não 45%: arredondamento meio para cima sobre as contagens.
- Comissão Nacional da Verdade: sai a citação "de 300 a 500 por dia", sem âncora no registro de fontes; entra o trecho ancorado da p. 301.
- `paper/tools/eeat_referencias.py` lê as 97 referências do próprio `paper.md` (a lista fixa de 78 entradas era da v0.3): E-E-A-T 80,1 e 50,5%
  de referências de 2023 em diante (49 de 97); `paper/tools/juiz_rubrica.py` julga a v0.4 sem rodar o pipeline da v0.3 (`tools/build.sh`,
  marcado como legado).
- README: abertura sem o "Não:" do título antigo; "numeradores comparáveis" -> cenários não harmonizados; alcance da busca; "Como citar" com o
  título novo e o artigo.

### Adicionado
- `docs/revisao/`: triagem do segundo exame, relatório do revisor de outra família e revisão hostil de um terceiro modelo (caminhos locais trocados).
- O artigo entra no git: `paper/paper.md`, `paper/build/v04/paper-v04.pdf`, `paper/AUDIT.md`, `paper/PAPER-SHA256.txt`, `paper/tools/`,
  `paper/tests/test_anexo.py` e os vereditos `paper/build/juiz/rodada-v4-*.json`, todos fora do selo; DOCX, logs e páginas renderizadas ficam fora
  do git (`.gitignore`).

## [Não lançado] - artigo v0.4 (2026-10-25), base da v0.4.1

### Alterado
- Título e subtítulo (decisão do autor): "Mortalidade e violência contra pessoas LGBT+ no Brasil: o que os dados públicos permitem afirmar" —
  "uma auditoria de fontes e indicadores, 2010–2026", em README, `CITATION.cff`, `codemeta.json` (`name`; `identifier` = nome do repositório) e `.zenodo.json`.
- Figuras (`paper/figures/make_figures.py`): regra APA do artigo, título, legenda, nota e fonte ficam no documento e nunca duplicados na imagem.
  `moldura()` não desenha mais título-conclusão, subtítulo, cartão "Como ler", termos nem rodapé; esses textos, gerados do dado, vão a
  `paper/figures/textos_fora_da_imagem.json`. Sem eles, a maior razão altura/largura cai de 1,63 para 1,08 e todas as figuras cabem a 14 cm.
  Também: rótulos da busca no Parlamento sem linguagem de processo ("dicionário pré-registrado" / "dicionário revisto"), eixos com vírgula
  decimal, Figura de mortalidade internacional redesenhada (razão 0,95) e ajustes de rótulo que se sobrepunham ou eram cortados. Nenhum valor
  desenhado mudou (`valores_plotados.json` conferido por `paper/tests/test_figuras.py`, controle negativo incluído).
- `paper/tests/test_figuras.py`: os testes de texto das Figuras 26 e 28 leem `textos_fora_da_imagem.json`; teste novo trava que nenhuma imagem
  traz título, "Como ler", "Fonte:" ou texto de processo.

### Adicionado
- `dados/regimes/`: relatório sobre violência de Estado contra homossexuais por tipo de regime (`H-RELATORIO.md`), ledger de 53 fontes
  (`sources.jsonl`, sem cópias de terceiros) e o escrutínio externo do relatório (`ASTRA-B2.md`); manifesto de fontes e inventário público refeitos
  (19 ledgers, 906 identificadores).
- `docs/historico-de-correcoes.md` listado em `docs/INDEX.md`.

## [Não lançado] - v0.3 (2026-10-24) e commit inicial público (2026-10-25)

### Alterado (commit inicial público, frente R0)
- O repositório vem primeiro e o artigo deriva dele: o selo (`make_provenance.py`) deixa de cobrir `paper/paper.md`, `paper/AUDIT.md`, `paper/build/`,
  `paper/tools/`, `paper/tests/test_anexo.py` e `paper/PAPER-SHA256.txt` (regra única `make_provenance.excluido()`, usada também pelo inventário,
  pelos testes de privacidade e pelo auditor). O primeiro commit público não contém o artigo; ele entra depois, citando a URL e o `chain_hash`, com o
  sha256 do PDF final em `paper/PAPER-SHA256.txt`. As figuras e os testes de figura ficam no selo.
- `scripts/auditar_publicacao.py --check literatura`: a conferência artigo x ledger sai "NÃO EXERCIDA" enquanto o artigo não está no repositório.
- `tests/test_integridade.py`: percorre o mesmo conjunto do selo; o teste do interior do DOCX do artigo saiu (volta com o artigo).
- README, `REPRODUCIBILITY.md`, `CITATION.cff`, `codemeta.json` e `.zenodo.json` não descrevem mais o artigo como parte do conjunto; o artigo e o hash do PDF
  não aparecem como entrega deste commit.
- Selo regravado uma vez com a nova regra; histórico do git passa a ser o registro de mudanças (`manifest/MODIFICACOES.tsv` fica só com a sincronização inicial; as 12 linhas de arquivos do artigo saem junto com ele e voltam no commit do artigo).

### Adicionado
- `dados/presidencia/` (C09, troca de presidente) e `dados/exposicao/` (C10, exposição por governo sem atribuição de causa): pré-registros com
  hash do corpo, scripts, saídas, relatórios; testes em `tests/test_c09_presidencia.py` e `tests/test_c10_exposicao.py`; os 5 scripts entram
  no recálculo de `scripts/reproduzir.py` (28 passos).
- Ledgers `research-2026-10-21-rodada3/A-textointegral/sources.jsonl` (antes só na árvore privada) e `research-2026-10-24-v03/L-ledger/sources.jsonl`
  (literatura de mortalidade da v0.3); `A-textointegral/verificacao-metadados.csv` (139 conferências de texto integral: periódico, quartil,
  texto lido, veredito; sem trecho de terceiros).
- `scripts/inventario_publico.py` -> `manifest/INVENTARIO-PUBLICO.{md,json}`: fontes, idiomas, tipos e scripts contados só com os arquivos
  distribuídos; com os 17 ledgers do painel reproduz 829 / 10 / tipos.
- `scripts/auditar_publicacao.py` (`--check literatura|inventario|privacidade|release`; 0 ok, 1 falhou, 2 não exercido) e
  `tests/test_auditar_publicacao.py` (com controles negativos).
- `REPRODUCIBILITY.md`: matriz de reprodução (recalcula, só confere, não se refaz) e o que o hash prova e não prova.

### Adicionado (frente P3, 2026-10-24)
- `dados/disque100/`: Disque 100 (23 arquivos públicos, 2011 a setembro de 2026): catálogo com sha256, pré-registro com hash gravado antes das contagens
  (2 adendos), dicionário, séries e comparações (CSV), scripts e 63 testes em arquivos sintéticos; **sem os microdados** (14 GB; `raw/` ignorado pelo git).
  `scripts/reproduzir.py` ganhou o passo `d100_series.py` (29 passos); `pyproject.toml` inclui `dados/disque100/tests` no pytest (173 testes; `run_all.py`: 110).
  Nenhuma conclusão depende dele: não há chave de pessoa, o total de vítimas únicas não é calculável, a série tem quatro quebras.
- Figura do Disque 100 (`paper/figures/fig28_disque100_serie.*`, teste com controle negativo): módulo LGBT por ano com a unidade e as quebras, e canal inteiro.
  A figura de revisores hostis passa a ser a de número 28 na numeração dos arquivos.

### Alterado
- Correções do escrutínio externo (frente R, registradas como `v0.3-R` em `manifest/MODIFICACOES.tsv`): 1.554 LGB+ observados, 305.955
  adultos, série do Sinan sem duplicação do total, 59 variáveis do formulário x 87 campos do arquivo do SIM, PNS sem pergunta de identidade
  de gênero (N2 = cenário), intervalo por inversão do wild-cluster (R6), Parlamento 0/49 e 1/49 (R7).
- `manifest/MANIFESTO-FONTES.csv` cobre os 18 ledgers (antes só o consolidado e a rodada 3).
- `pyproject.toml`: lint em dois níveis (estrito no código de infraestrutura, informativo nos scripts de pesquisa copiados); CI com matriz
  3.12/3.13, lint estrito bloqueante e auditoria; o passo de diagnóstico com `|| true` saiu (o `run_all.py` já lista as divergências).
- `run_all.py --selar` regrava também o inventário público.
- `make_provenance.py`: o selo usa o mesmo conjunto do `.gitignore` (fora: cópias de figura que o build regrava em `paper/build/fig-embed/`,
  `.DS_Store` em qualquer pasta e o envelope cru da rodada v2-1 do juiz); antes o `--verify` falharia num clone limpo.
- README: seção da v0.3, fontes em linguagem comum, índice do que está exibido.
## [0.1.0] - 2026-10-23

### Adicionado
- Dados derivados, scripts e saídas de `dados/`, `simulacao/` e `research-2026-10-21-rodada3/` (frentes F2, F3, F5, F6, F8, GGB-completo, ideologia, discurso).
- Ledgers de fontes (`research-consolidado/sources.jsonl`, 571 registros) e `manifest/MANIFESTO-FONTES.csv` (URL, data de acesso, SHA-256).
- `run_all.py` (integridade -> réplica -> testes -> selo), `make_provenance.py`, `scripts/reproduzir.py`, `scripts/acquire_{sim,sinan,pns2019,tse}.py`.
- `tests/`: números publicados, integridade/privacidade e verificação independente.
- Pré-registros com hash em `docs/PRE-REGISTROS/`; dossiês e laudos em `docs/`.
- CITATION.cff, codemeta.json, .zenodo.json (`access_right: closed`, sem DOI).
- `paper/`: figuras com testes de figura (o artigo, o PDF, o DOCX e as ferramentas de export entram depois, fora do selo).
- Reanálises pré-registradas C02, C03, C05 e C08 (`dados/painel/`, `dados/pns/`, `dados/ggb/`) e `tests/test_reanalises_publicadas.py`;
  C02 e C03 entram no recálculo de `scripts/reproduzir.py`.
- `research-2026-10-21-rodada3/escrutinio/`: pacote enviado, as quatro revisões hostis, triagem, critérios e resultados das reanálises, busca simétrica.
- `dashboard/`: números do painel de contagens (extrato público) e o script de contagem (ferramenta do autor).
- Dossiês atualizados (consolidado e parte 2 com a simetria e as reanálises integradas).

### Alterado
- `scripts/reproduzir.py`: número impresso em precisão total (>= 15 algarismos) aceita diferença relativa <= 1e-10 (soma em BLAS multithread varia entre execuções).
- Linguagem interna de operação (nomes de agentes e ferramentas, números de pedido, papéis) trocada por termos neutros em 50 arquivos, sem alterar números;
  cada arquivo em `manifest/MODIFICACOES.tsv` com sha256 antes e depois. Exceção: pré-registros com hash gravado ficam intactos (ver `docs/INDEX.md`).
- `tests/`: `pytest` e `run_all.py` rodam também `paper/tests/` (testes de figura).
- `CITATION.cff`: tipo das referências de dados corrigido para o esquema 1.2.0 (`data`).

### Removido da publicação (presente no projeto privado)
- Nomes de vítimas e qualquer dado nominal; PDFs/HTML de terceiros; microdados brutos; texto integral de notícias; instruções internas de agente.
- Do escrutínio: itens com texto de notícia/resumo enviados ao segundo codificador, respostas cruas do modelo, filas de navegador e logs.
- Lista de PDFs pendentes do projeto (lista de tarefas datada; o status "não lido" já está nos ledgers e no manifesto).
