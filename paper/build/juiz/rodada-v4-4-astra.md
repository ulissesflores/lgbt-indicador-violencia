# Rodada v4-4 — astra (tentativa 1)

Procedimento: codex exec -m gpt-6-astra (assinatura ChatGPT; CODEX_HOME temporário), model_reasoning_effort=high, sandbox read-only, web_search=disabled, --ephemeral, cwd vazio, --output-schema; prompt por stdin.
Prompt: sha256 e2d718cc604bfc6e2b43b25a66f30c4f452694dff19e44477718608612cfee84 (254108 B) = rodada-v4-4.prompt.txt (sha256 8fbdca822ef448f096aaa0ab2b2f7a22b130120054b79c6b726ad0da405d6091) + regra (8).
paper.md sha256 antes = depois = 3469a16764dc4f5382634a39c6d627b8065a6cbb51666402b64a460d6e01e23b ; sha256_conferido = 3469a16764dc4f5382634a39c6d627b8065a6cbb51666402b64a460d6e01e23b.
Classificação: válida (todos os critérios pré-registrados) (A=True B=True C=True D=True E=True).
Soma das dimensões: 885; total informado pelo modelo: 885.
Tokens de entrada: 91799; segundos: 238.0.

| Dimensão | Pontos | Máximo | Descontos |
|---|---|---|---|
| estrutura_formal | 150 | 150 | 0 |
| densidade_tecnica | 150 | 250 | 2 |
| fundamentacao_teorica | 150 | 150 | 0 |
| originalidade_tese | 200 | 200 | 0 |
| consistencia_interna | 90 | 100 | 2 |
| correcao_factual | 145 | 150 | 1 |
| **soma das dimensões** | **885** | 1000 | |
| total informado pelo modelo | 885 | 1000 | |

## Prova de leitura integral

- última frase do Apêndice D: "Fonte: Flores (2026)." -> True
- frase anterior: "Caminhos relativos à raiz do repositório https://github.com/ulissesflores/lgbt-indicador-violencia." -> True
- frase da §3.9: "O nível mede o tipo de documento que registra o ato, e não a certeza do fato nem a originalidade da investigação." -> True (paper.md:[484], 1 ocorrência(s) no paper)

## Descontos (verbatim)

- **densidade_tecnica**: -80 pontos — TDI. §1: "Cada termo técnico é definido no primeiro uso". A presença e a definição dos termos não satisfazem o limiar quantitativo: a ferramenta fornecida mede TDI de 1,94, abaixo de 3. Desconto integral deste subcritério, fundamentado na medição global fornecida; o trecho localiza a apresentação do vocabulário, não substitui a medição.
- **densidade_tecnica**: -20 pontos — Métricas quantitativas por subseção. §4.2: "O mecanismo não foi testado." A subseção apresenta interpretação e analogias, mas nenhuma métrica quantitativa substantiva; anos bibliográficos e remissões a seções não são métricas. Portanto, não cumpre a exigência de pelo menos uma métrica em cada subseção.
- **consistencia_interna**: -6 pontos — Sem contradição entre seções e componentes. §4.1: "A terceira hipótese não é sustentada em nenhuma das duas formas." Na Tabela 11, entretanto, aparece "contrariada como invenção, isto é, como fabricação de casos". O vocabulário definido em §2.2 distingue não sustentação de evidência contrária; prosa e tabela atribuem vereditos diferentes à mesma hipótese.
- **consistencia_interna**: -4 pontos — Vocabulário consistente. §2.6: "nenhum modelo foi usado para gerar dado". A mesma seção informa que modelos "codificaram itens de discurso". Esses rótulos constituem dados derivados utilizados nas análises. A declaração precisa distinguir geração de dados brutos ou sintéticos de produção de dados por codificação; sua formulação absoluta torna ambíguo o papel dos modelos.
- **correcao_factual**: -5 pontos — Suposições marcadas como tal. Apêndice A, Tabela A17: "| F2 | Parlamento | 56 | 56 (censo) | 49 | 49 [43-53] |". Para o universo recuperado integralmente e classificado, 49 é uma contagem censitária. O intervalo requer uma população inferencial adicional ou um modelo de erro de classificação; nenhum deles é declarado para essa célula. A incerteza não pode ser apresentada como se decorresse de amostragem desse universo.

## Achados críticos (verbatim)

- Estrutura formal, subcritérios: tese inicial 30/30; numeração 20/20; subtítulo 15/15; resumo bilíngue 25/25; palavras-chave 10/10; tabela 20/20; recuo das referências 10/10; figuras 20/20. A Tabela 5 satisfaz o formato compacto solicitado. O recuo deslocado foi aceito conforme a comprovação fornecida do DOCX.
- Densidade técnica, subcritérios: TDI 0/80; filler 60/60; info density 50/50; vocabulário específico 30/30; latim com propósito 10/10; métricas por subseção 0/20. Foram utilizados os valores fornecidos: 1,94; 0,0004; 51,27. Os usos de a priori, ceteris paribus e post hoc têm função explicativa.
- Fundamentação teórica, subcritérios: quantidade de referências 30/30; tipos 30/30; E-E-A-T 40/40; citação inicial 15/15; recência 20/20; ausência de referências banidas 15/15. São 97 referências, cinco tipos equivalentes aplicáveis, média 80,1 e recência de 50,5%, conforme as ferramentas. A Wikipédia aparece como objeto de análise, não como referência probatória.
- Originalidade/tese, subcritérios: tese argumentável 60/60; trade-off nomeado 50/50; insight 40/40; solução central 30/30; direções futuras 20/20. A tensão entre ampliar registro e preservar comparabilidade é explicitamente vinculada a Campbell; a não identificação recebe demonstração algébrica; a restrição externa é operacionalizada e dimensionada; §4.5 apresenta cinco direções numeradas. Esses créditos não certificam prioridade histórica das contribuições.
- Consistência interna, subcritérios: ausência de contradições 34/40; alinhamento com o resumo 20/20; correspondência entre citações e referências 20/20; vocabulário 16/20. As principais estimativas e ressalvas do resumo reaparecem no corpo e nos apêndices.
- Correção factual, subcritérios: claims com citação 60/60; ausência de invenção demonstrável 40/40; suposições explicitadas 20/25; URLs 15/15; DOIs 10/10. A avaliação aceita a verificação bibliográfica fornecida e não presume acesso ao conteúdo externo das fontes.
- A transparência sobre escolhas posteriores aos resultados, ausência de carimbo temporal externo, limitações dos modelos e reprodução parcial não elimina essas limitações. Contudo, elas estão declaradas e não justificam descontos adicionais por suposições ocultas.
- A cap dura não é acionada: densidade técnica de 150 pontos, acima de 100. Os descontos totalizam 115 pontos; a soma das seis dimensões é 885.

Veredito: Bom — 885/1000. Atende à faixa de 850–919, mas não ao alvo de 950. Corrigir a divergência do veredito sobre fabricação, esclarecer a produção de dados pelos modelos e justificar o intervalo censitário. O TDI medido permanece abaixo do limiar.

Registro e leitura dos descontos: paper/AUDIT.md (rodada final da v0.4.2; nenhuma edição depois dela).
