# Rodada v4-3 — astra (tentativa 1)

Procedimento: codex exec -m gpt-6-astra (assinatura ChatGPT; CODEX_HOME temporário), model_reasoning_effort=high, sandbox read-only, web_search=disabled, --ephemeral, cwd vazio, --output-schema; prompt por stdin.
Prompt: sha256 9e219cafee23d3888703cd568d28d368576bde380e1770e8e5d4e838a27073c8 (252930 B) = rodada-v4-2.prompt.txt (sha256 f450110b42eb6d2a1289ee3e2b844bb901e3ca9a09b083e040f2db02175f3540) + regra (8).
paper.md sha256 antes = depois = 4a775cccceb6d7b5eb112b98320d938a7358a16c62c78093b60a25f05127bc02 ; sha256_conferido = 4a775cccceb6d7b5eb112b98320d938a7358a16c62c78093b60a25f05127bc02.
Classificação: válida (todos os critérios pré-registrados) (A=True B=True C=True D=True E=True).
Soma das dimensões: 868; total informado pelo modelo: 868.
Tokens de entrada: 91451; segundos: 178.6.

| Dimensão | Pontos | Máximo | Descontos |
|---|---|---|---|
| estrutura_formal | 140 | 150 | 1 |
| densidade_tecnica | 160 | 250 | 2 |
| fundamentacao_teorica | 150 | 150 | 0 |
| originalidade_tese | 200 | 200 | 0 |
| consistencia_interna | 74 | 100 | 5 |
| correcao_factual | 144 | 150 | 1 |
| **soma das dimensões** | **868** | 1000 | |
| total informado pelo modelo | 868 | 1000 | |

## Prova de leitura integral

- última frase do Apêndice D: "Fonte: Flores (2026)." -> True
- frase anterior: "Caminhos relativos à raiz do repositório https://github.com/ulissesflores/lgbt-indicador-violencia." -> True
- frase da §3.9: "O nível mede o tipo de documento que registra o ato, e não a certeza do fato nem a originalidade da investigação." -> True (paper.md:[484], 1 ocorrência(s) no paper)

## Descontos (verbatim)

- **estrutura_formal**: -10 pontos — Palavras-chave presentes (0/10). Resumo: "violência; LGBT+; mortalidade; subnotificação; identificabilidade; pré-registro; reprodutibilidade". Há sete palavras-chave, acima do máximo de seis. O problema se repete no Abstract.
- **densidade_tecnica**: -80 pontos — TDI (0/80). §1: "Cada termo técnico é definido no primeiro uso". A definição dos termos não satisfaz o limiar quantitativo: a ferramenta fornecida mede TDI de 1,94, inferior a 3. Aplicado o limiar como requisito, sem pontuação proporcional não prevista.
- **densidade_tecnica**: -10 pontos — Latim usado com propósito (0/10). §5.4: "há risco de leitura post hoc, isto é, posterior aos dados". Esse emprego é pertinente, mas não cumpre as duas a quatro ocorrências exigidas. Abreviações bibliográficas convencionais não constituem usos argumentativos adicionais.
- **consistencia_interna**: -8 pontos — Sem contradição entre seções. §4.3, objeção 7: "contou episódios de hostilidade e de proteção nos dois lados". A Tabela 8 registra proteção somente nos governos Lula e Dilma; Temer e Bolsonaro têm zero nessa categoria. A resposta à objeção atribui à tabela uma simetria de resultados que ela não apresenta.
- **consistencia_interna**: -6 pontos — Sem contradição entre seções. §4.4: "Com ele, a série policial, o campo de motivação do Sinan e as contagens da sociedade civil passariam a ser calibráveis." O levantamento proposto mede vitimização não letal; as contagens da sociedade civil examinadas medem mortes. A calibração destas não decorre daquele levantamento, conforme a própria separação entre desenhos estabelecida em §3.13.
- **consistencia_interna**: -6 pontos — Sem contradição entre seções. §3.7: "nas 67 trocas de partido do governador entre 2013 e 2024" e "entre os três anos anteriores e os três posteriores". O SIM utilizado termina em 2024. Janelas posteriores completas para trocas recentes ultrapassam esse limite; falta explicar quais eventos tiveram janelas truncadas, como foram calculadas e como permanecem comparáveis.
- **consistencia_interna**: -3 pontos — Vocabulário consistente. Apêndice A, Tabela A16: "negros / não negros: limite inferior (raça ignorada descartada)". O valor denominado limite inferior é 2,56, mas a própria tabela apresenta 2,42 como cenário extremo admissível. Descartar raça ignorada é um cenário, não o limite inferior indicado.
- **consistencia_interna**: -3 pontos — Vocabulário consistente. Apêndice C, definição do numerador B: "contagem do GGB menos todas as pessoas trans da tabela de identidade". Em §3.4 e nas Tabelas A6–A7, B subtrai pessoas trans do numerador A, restrito a homicídios e latrocínios, não da contagem total. O glossário omite a restrição que define a operação.
- **correcao_factual**: -6 pontos — Suposições marcadas como tal (19/25). §5.2: "tem ruído que atenua o coeficiente". A direção do viés é apresentada como consequência necessária do ruído. A atenuação exige condições sobre o erro de mensuração que não são declaradas nem demonstradas para esse painel; deveria aparecer como possibilidade condicionada, não como fato estabelecido.

## Achados críticos (verbatim)

- Estrutura formal, subcritério por subcritério: tese no primeiro parágrafo 30/30; numeração 20/20; subtítulo 15/15; resumo bilíngue 25/25; palavras-chave 0/10; tabela 20/20; recuo das referências 10/10; figuras 20/20. O recuo foi aceito conforme o export informado; a Tabela 5 cumpre o formato dimensional exigido.
- Densidade técnica, subcritério por subcritério: TDI 0/80; filler 60/60; info density 50/50; vocabulário específico 30/30; latim 0/10; métricas quantitativas 20/20. Foram utilizados os resultados fornecidos: 1,94; 0,0004; 51,28. Densidade de 160 pontos: a cap dura não se aplica.
- Fundamentação teórica, subcritério por subcritério: quantidade de referências 30/30; tipos de fonte 30/30; E-E-A-T 40/40; citação no primeiro parágrafo da Introdução 15/15; recência 20/20; ausência de referências banidas 15/15. Aceitos os resultados fornecidos: 97 referências, cinco tipos equivalentes aplicáveis, média 80,1 e recência de 50,5%. A Wikipédia aparece como objeto de análise, não como fundamento bibliográfico.
- Originalidade/tese, subcritério por subcritério: tese argumentável 60/60; trade-off nomeado 50/50; insight 40/40; solução central 30/30; direções futuras numeradas 20/20. Campbell fundamenta a tensão entre ampliar o registro e preservar comparabilidade; a não identificação e os cenários fornecem o insight; o levantamento repetido responde à tendência não letal; §4.5 enumera cinco direções.
- Consistência interna, subcritério por subcritério: ausência de contradições 20/40; alinhamento com o resumo 20/20; correspondência entre citações e referências 20/20; vocabulário consistente 14/20. A ferramenta informa zero citações órfãs.
- Correção factual, subcritério por subcritério: claims com citação 60/60; ausência de invenção demonstrada 40/40; suposições marcadas 19/25; URLs 15/15; DOIs 10/10. Aplicados os resultados de verificação fornecidos e a restrição de não consultar fontes externas; pertencimento ao ledger não foi reinterpretado como uma nova checagem de acessibilidade.
- A contradição mais direta está na alegação de proteção nos dois lados políticos: ela não corresponde à Tabela 8.
- As janelas das trocas estaduais precisam de documentação explícita diante do término da série em 2024. Declarar limitações gerais não resolve essa incompatibilidade temporal específica.
- A proposta de vigilância extrapola seu alcance ao prometer calibrar contagens de mortes com levantamento de violência não letal.
- Os desvios pós-resultados e a ausência de carimbo temporal externo estão declarados. Transparência permite avaliar essas limitações, mas não transforma os componentes retrospectivos em confirmação prospectiva.
- O hash foi transcrito conforme solicitado; nenhuma ferramenta, arquivo externo ou consulta à web foi utilizada.

Veredito: 868/1000 — Bom, pela escala da rubrica; abaixo do alvo padrão de 950. Requer corrigir as contradições identificadas, esclarecer as janelas estaduais e restringir a promessa de calibração ao desfecho efetivamente medido.

Triagem de cada desconto: docs de trabalho do autor, S3-TRIAGEM.md (resumo em paper/AUDIT.md).
