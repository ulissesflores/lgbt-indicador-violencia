# AUDIT — `paper.md` · rubrica `rubrica-academica` (0-1000) · 2026-10-23

> Fases 4 a 7 da skill `codex-hash-research`. Gate: **total >= 920 E densidade técnica >= 100**
> (abaixo de 100 a nota fica capada em 600). Régua da casa: quem escreveu não pontua; com mais de
> uma rodada válida sobre o mesmo arquivo, **vale a menor**.

> [!IMPORTANT]
> **Versão vigente: v0.4.4** (`sha256 fdd8e9d48b32a8bef3d0d7f226c95f665677185781f168e69562cf4b7aea0ced`; PDF único de 129 páginas,
> `sha256 7a63b6fb4042ac29827ee56f68508bf580f56c828abe3a768d81502288159445`, em `paper/PAPER-SHA256.txt`; selo do repositório
> `d1d2e4d77e2be87486b635c230d2e88025b6ac87888682e89f4dcf87942b215b`, 724 arquivos).
>
> **v0.4.4: mudanças de precisão sem número novo, listadas abaixo (seção final "Rodada v4-5 e v0.4.4"); não re-julgada.** A versão
> anterior, 0.4.3 (`b21b2dd4…`), recebeu a rodada v4-5 (Grok com `--verbatim`, 928, leitura integral comprovada). As notas da tabela
> abaixo são das versões indicadas na coluna "Texto julgado".
>
> **Leitura do juiz em TODAS as rodadas (corrigido em 2026-10-26, frente G).** Medição controlada (prompts sintéticos com sentinelas e o
> registro de sessão gravado pelo próprio programa do juiz): o `grok -p` (CLI 1.0.62) entrega o prompt inteiro só até **99.974 B**; com
> **100.000 B ou mais** manda ao modelo o começo (cerca de 94,3 KB) e o fim (3.988 B) e omite o meio. Os "~94 KB" citados até aqui eram o
> tamanho do começo entregue, não o limiar. Consequências: **as 11 notas do Grok da v0.2 à v0.4.1 (prompts de 134.455 a 251.724 B) foram
> dadas sobre 33% a 70% do artigo: leitura parcial, sem validade como medida do texto inteiro**; as 9 notas da v0.1 (prompts de 86.009 a
> 95.764 B, abaixo do limite) foram dadas com o prompt inteiro na mensagem, mas sem prova de leitura: **leitura não comprovada**; e o
> `--tools ""` usado pelo juiz até a v0.4.1 **não removia as ferramentas do programa** (nenhuma rodada pontuada as usou). **Notas com leitura
> integral comprovada: só Astra 868 (v0.4.1), Gemini 941 pela soma / 881 com a regra (2) (v0.4.1) e Astra 885 (v0.4.2); acréscimo de 2026-10-26 (frente E8): Grok 928 (v0.4.3, com `--verbatim`, rodada v4-5).** Tabela de todas as
> rodadas, com o tamanho de cada prompt e o que chegou ao modelo, na seção seguinte a esta caixa.
>
> **Rodadas do juiz de rubrica na v0.4** (mesma rubrica de 6 dimensões; detalhes nas seções "v0.4 e v0.4.1" e "rodadas v4-3" abaixo):
>
> | Rodada | Modelo | Texto julgado | Nota | Leitura do artigo |
> |---|---|---|---|---|
> | v4-1 | Grok | v0.4 | 811 | parcial: o programa do juiz entregou à mensagem só o começo e o fim do prompt ~~(corte de ~94 KB)~~ (corrigido em 2026-10-26: prompt de 241.763 B; chegaram ao modelo 35,1% do artigo) |
> | v4-2 | Grok | v0.4.1 | 890 | parcial, pelo mesmo corte (corrigido em 2026-10-26: prompt de 251.724 B; chegaram 33,0% do artigo) |
> | v4-3 | Astra (`gpt-6-astra`) | v0.4.1 | 868 | integral, com prova (últimas frases do Apêndice D e frase da seção 3.9) |
> | v4-3 | Gemini (`gemini-4-argon-high`) | v0.4.1 | 941 pela soma das dimensões; 881 com a regra (2) do prompt | integral, com prova; ressalva de procedimento |
> | v4-4 | Astra (`gpt-6-astra`) | v0.4.2 | 885 | integral, com prova |
> | v4-5 | Grok (`grok -p --verbatim`, ferramentas removidas) | v0.4.3 | **928** | integral, com prova (última frase e frase depois do marcador a 60,4%); entrega conferida no registro do programa |
>
> **Conclusão (2026-10-26, frente E8): gate atendido por uma rodada válida de uma família; o TDI segue como desconto declarado.** A rodada
> v4-5 (Grok, `grok -p --verbatim` com as 25 ferramentas do programa removidas; prompt de 254.558 B entregue inteiro: mensagem
> igual ao prompt, 106.952 tokens de entrada, nenhum aviso de corte, nenhuma ferramenta) deu **928/1000** à v0.4.3, com densidade
> técnica 221 (acima de 100; o teto de 600 não se aplica), hash conferido (`b21b2dd4…` antes = depois = devolvido pelo
> modelo) e prova de leitura verdadeira nas duas frases. **Nota de aceite declarada: a MENOR das rodadas válidas com leitura integral
> comprovada sobre a versão final julgada (regra da casa, já usada na v0.1); sobre a v0.4.3 há uma só rodada: 928.** A v0.4.4 difere da
> v0.4.3 só em precisão, sem número novo (seção final), e não foi julgada. O TDI continua abaixo de 3 (1,93; −29 nesta rodada, por
> crédito proporcional; a regra (2) das rodadas Astra dava 0 de 80). **Variância entre famílias, todas com leitura integral comprovada,
> sobre textos que da v0.4.1 à v0.4.3 mudaram sem análise nova (a v0.4.2 trouxe ao texto números de arquivos já publicados; a v0.4.3,
> nenhum número novo):** Astra 868 (v0.4.1) e 885 (v0.4.2); Gemini 941 pela
> soma e 881 com a regra (2) (v0.4.1); Grok 928 (v0.4.3): 73 pontos entre a menor e a maior. A 928 não substitui as outras: é de outra
> versão e de outra família, e nenhuma segunda família julgou a v0.4.3; se a régua fosse a menor nota com leitura integral em qualquer
> versão desde a v0.4.1, seria 868.
>
> **Conclusão até a rodada v4-4 (histórica): nota ≥ 920 não demonstrada.** Impedimento declarado: a densidade técnica do corpo (TDI 1,94 na v0.4.2 e 1,93 na v0.4.3,
> abaixo de 3) vem da decisão
> de escrever para o leitor não especialista (termos por extenso, sem sigla solta), e a regra (2) do prompt do juiz não dá crédito parcial a
> critério não cumprido, de modo que o subcritério do TDI vale 0 de 80. **Critério de escrutínio do projeto atendido:** nenhum ataque de
> severidade alta ficou sem resposta; os 16 descontos das rodadas v4-3 foram triados (9 procederam ou procederam em parte, nenhum alto; 3
> limites já declarados; 2 não procederam) e os que procederam foram corrigidos na v0.4.2 (`docs/historico-de-correcoes.md`, seção 9).
> **Rodada final v4-4 (Astra, sobre a v0.4.2): 885/1000, leitura integral comprovada**; 3 descontos procedem (1 médio, 2 baixos) e foram
> aplicados na v0.4.3, sem nova rodada do juiz (seções finais).
>
> As seções abaixo da caixa são históricas (v0.1 a v0.4.1), salvo as seções finais "Rodada final v4-4" e "v0.4.3".
> (Acréscimo de 2026-10-26, frente E8: também a seção final "Rodada v4-5 e v0.4.4".)
> (Acréscimo de 2026-10-26: também a seção seguinte, "Todas as rodadas do juiz", e a final, "Frente G"; nas históricas, o que a medição
> desmentiu ficou no lugar, riscado ou seguido de nota "Corrigido em 2026-10-26".)

## Todas as rodadas do juiz e o que cada uma leu (2026-10-26, frente G)

**Como foi medido.** (1) Experimento controlado com o `grok -p` 1.0.62 (16 chamadas, 2026-10-26): prompts sintéticos só em ASCII, com
linhas numeradas e três sentinelas de código aleatório (no meio do arquivo, no centro da faixa que o corte omitiria e na última linha), em
pasta vazia, com as flags do juiz. 96.000, 98.000, 99.000, 99.973 e 99.974 B chegaram inteiros; 100.000, 130.000 e 200.000 B chegaram
cortados, com 94.313 B do começo e 3.988 B do fim, o meio trocado por "[middle omitted — see the offload note for how to read it]" e uma
nota pedindo ao modelo que leia as linhas omitidas de um arquivo com a ferramenta `read_file`. O corte é do programa (recurso interno
`prompt_offload`, presente no binário), não do modelo, e é contado em bytes. `--prompt-file`, `--prompt-json`, entrada padrão e `@arquivo`
não evitam o corte; **`--verbatim` evita** (130.000 e 260.000 B chegaram byte a byte e o modelo citou as três sentinelas). `--tools ""` deixa
as 25 ferramentas do programa (inclusive `read_file`, `grep` e `run_terminal_command`); `--disallowed-tools` com os 25 nomes as remove. (2)
Forense das 25 sessões históricas do juiz, gravadas pelo próprio programa na máquina do autor (mensagem efetivamente enviada ao modelo,
cópia integral do prompt quando houve corte e ferramentas oferecidas), casadas com `build/juiz/rodada-*.prompt.txt` pelo conteúdo e,
quando o prompt se repete (rodadas 6/7 e 8/9/10), pelo horário. Os registros de sessão e o relatório completo da medição
(`G-GROK-CORTE.md`, com comando, tamanho, resposta e hora de cada chamada) ficam na pasta de trabalho do autor: trazem caminhos locais e
identificadores de sessão.

"Leitura": **integral** = prova de leitura conferida (frases do fim e de um trecho que o corte omitiria, copiadas verbatim pelo modelo);
**parcial** = o programa entregou ao modelo só parte do artigo (a coluna "Entregue" dá a fração do bloco do artigo que chegou);
**não comprovada** = o prompt chegou inteiro à mensagem, mas a rodada não teve prova de leitura. Nota parcial não mede o texto inteiro e não
vale para o gate; nota não comprovada é registro, não demonstração.

| Versão do texto | Rodada | Juiz (programa) | Prompt (B) | Limite medido do programa | Entregue ao modelo | Leitura | Nota |
|---|---|---|---|---|---|---|---|
| v0.1 | 1 | Grok (`grok -p`) | 86.009 | 99.974 B | inteiro | não comprovada | 854 |
| v0.1 | 2 | Grok | 89.466 | 99.974 B | inteiro | não comprovada | 949 |
| v0.1 | 3 | Grok | 92.151 | 99.974 B | inteiro | não comprovada | 958 |
| v0.1 | 4 | Grok | 93.622 | 99.974 B | inteiro | não comprovada | 928 |
| v0.1 | 5 | Grok | 94.025 | 99.974 B | inteiro | não comprovada | 900 |
| v0.1 | 6 | Grok | 94.468 | 99.974 B | inteiro | não comprovada | 970 |
| v0.1 | 7 | Grok | 94.468 | 99.974 B | inteiro | não comprovada | 929 |
| v0.1 (final) | 8 | Grok | 95.764 | 99.974 B | inteiro | não comprovada | 970 |
| v0.1 (final) | 9 | Grok | 95.764 | 99.974 B | inteiro | — | inválida (sem saída estruturada; o modelo usou `grep` no repositório e achou um veredito anterior, `build/juiz/rodada-1.json`) |
| v0.1 (final) | 10 | Grok | 95.764 | 99.974 B | inteiro | não comprovada | 960 |
| v0.2 | v2-1 | Grok | 134.455 | 99.974 B | começo + fim: 69,8% | parcial | inválida (JSON de zeros; o modelo leu parte do arquivo do corte e do paper.md com ferramentas) |
| v0.2 | v2-2 | Grok | 134.455 | 99.974 B | 69,8% (omitido: das Referências ao Anexo C) | parcial | 875 |
| v0.2 | v2-3 | Grok | 135.270 | 99.974 B | 69,5% (idem) | parcial | 856 |
| v0.2 | v2-4 | Grok | 135.270 | 99.974 B | 69,5% (idem) | parcial | 862 |
| v0.2 | v2-5 | Grok | 144.381 | 99.974 B | 64,5% (omitido: da seção 7.1 ao Anexo C) | parcial | 862 |
| v0.2 | v2-6 | Grok | 144.381 | 99.974 B | 64,5% (idem) | parcial | 876 |
| v0.2 | v2-7 | Grok | 145.298 | 99.974 B | 63,9% (omitido: da seção 7 ao Anexo C) | parcial | 877 |
| v0.2 (final) | v2-8 | Grok | 145.769 | 99.974 B | 63,7% (omitido: da seção 6 ao Anexo C) | parcial | 876 |
| v0.3 | v3-1 | Grok | 189.901 | 99.974 B | 46,3% (omitido: da seção 3.6 ao Apêndice B) | parcial | inválida (max turns; o modelo leu parte do arquivo do corte com ferramentas) |
| v0.3 | v3-2 | Grok | 189.901 | 99.974 B | 46,3% (idem) | parcial | inválida (idem) |
| v0.3 | v3-3 | Grok | 189.901 | 99.974 B | 46,3% (idem) | parcial | 804 |
| v0.3 (final) | v3-4 | Grok | 190.680 | 99.974 B | 46,2% (omitido: da seção 3.5 ao Apêndice B) | parcial | 893 |
| v0.4 | v4-1 | Grok | 241.763 | 99.974 B | 35,1% (omitido: da seção 3.6 ao Apêndice C) | parcial | 811 |
| v0.4.1 | v4-2 | Grok | 251.724 | 99.974 B | 33,0% (omitido: da seção 3.5 ao Apêndice C) | parcial | 890 |
| v0.4.1 | v4-3 | Astra (`codex exec`, prompt pelo stdin) | 252.930 | nenhum corte observado (91.451 tokens de entrada) | inteiro | **integral** (3/3 frases) | **868** |
| v0.4.1 | v4-3, tentativa 1 | Gemini (`agy -p`) | 252.930 | o `agy -p` cortou em 191.581 B | 191.581 B | parcial | inválida (sem resposta) |
| v0.4.1 | v4-3, tentativa 2 | Gemini (`agy`, 2 mensagens por stream-json) | 252.930 (131.271 + 121.659) | cada mensagem abaixo de 191.581 B | inteiro | **integral** (3/3 frases) | **941** pela soma; **881** com a regra (2) |
| v0.4.2 | v4-4 | Astra (`codex exec`, stdin) | 254.108 | nenhum corte observado (91.799 tokens) | inteiro | **integral** (3/3 frases) | **885** |
| v0.4.3 | v4-5 (frente E8) | Grok (`grok -p --verbatim`, 25 ferramentas removidas) | 254.558 | sem corte com `--verbatim` (mensagem igual ao prompt; 106.952 tokens) | inteiro | **integral** (2/2 frases) | **928** |

Contagem: 9 notas do Grok da v0.1 = não comprovadas; **11 notas do Grok da v0.2 à v0.4.1 = parciais** (9 delas, da v0.2 e da v0.3, não
estavam marcadas como parciais até 2026-10-26; v4-1 e v4-2 já estavam); 5 rodadas inválidas também tiveram entrega parcial ou leitura
fora do prompt (rodada 9, v2-1, v3-1, v3-2 e a tentativa 1 do Gemini); 3 rodadas com leitura integral comprovada (Astra 868 e Gemini
941/881 sobre a v0.4.1; Astra 885 sobre a v0.4.2; acréscimo de 2026-10-26, frente E8: e Grok 928 sobre a v0.4.3, a 4ª). Nenhuma rodada
pontuada chamou ferramenta, mas o modelo as tinha à disposição em todas as rodadas do Grok (o `--tools ""` não as removia), e em 5 sessões
sem nota as usou: a rodada 9 da v0.1, a v2-1, a v3-1, a v3-2 e uma sonda manual da v0.2 (seção v0.2 abaixo).

## Veredito (v0.1)

| | |
|---|---|
| Artefato auditado | `paper/paper.md` (canônico); derivados `paper/build/paper.docx` e `paper/build/paper.pdf` |
| Versão congelada | `sha256 8f6cd9f100de042849a48995f0161895ce229943c33f9a29ffb8cbfeadccb2a6` (`build/juiz/hash-final.txt`) |
| Nota de aceite (menor das rodadas válidas sobre esta versão) | **960/1000** (rodada 10; rodada 8 = 970) |
| Densidade técnica | 250/250 nas duas rodadas finais (cap não acionado) |
| Resultado | ✅ APROVADO no gate de 920, com 1 juiz de 1 família (limite abaixo) |

> [!NOTE]
> **Corrigido em 2026-10-26 (frente G).** O prompt das rodadas 8 e 10 (95.764 B) ficou abaixo do limite medido do programa do juiz (99.974 B)
> e chegou inteiro ao modelo (registro de sessão do próprio programa). Mas nenhuma rodada da v0.1 teve prova de leitura, e o juiz tinha as
> ferramentas do programa à disposição (o `--tools ""` não as removia; nenhuma rodada pontuada as usou). A 960 fica como nota com
> **leitura não comprovada**, de um juiz de uma família, sobre uma versão superada; não é aprovação com leitura integral comprovada.

## Juiz e rodadas

Juiz externo: Grok (`grok-4.7-build`) pela assinatura do fornecedor, `grok -p` sem ferramentas e sem
web, uma volta, saída em JSON com esquema fixo (`tools/juiz_rubrica.py`). *(Corrigido em 2026-10-26: "sem ferramentas" não valia; o
`--tools ""` deixava as 25 ferramentas do programa, e na rodada 9 o modelo usou `grep` no repositório.)* O script congela o sha256
antes de montar o prompt e o confere depois; o prompt leva a rubrica verbatim, as saídas reais das
ferramentas determinísticas e o artigo inteiro. Codex está fora (suspenso desde 2026-10-13); nenhum
modelo pago por uso foi chamado. **Limite: um juiz de uma família só; a variância entre rodadas sobre
o mesmo arquivo foi de 41 pontos (rodadas 6 e 7: 970 e 929), então a nota tem incerteza dessa ordem.**

| Rodada | sha256 (12) | Estrutura | Densidade | Fundamentação | Tese | Consistência | Factual | Total | Hash ok | Observação |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 87a6cef32d82 | 122 | 240 | 128 | 178 | 74 | 112 | 854 | sim | teste de figura vermelho (painel de origem regenerado por outro processo); 10 blocos x 12; 8,4-28,7% sem origem |
| 2 | 6cc54537eb88 | 150 | 250 | 150 | 200 | 75 | 124 | 949 | sim | N1 homônimo; PNDS e minuta sem fonte; linha de base 60 x 38 |
| 3 | f3c20f5b47c3 | 150 | 250 | 150 | 190 | 86 | 132 | 958 | sim | "compensado exatamente" sem p < 1; HIV pré-1996 sem citação |
| 4 | d5d1a710789c | 145 | 250 | 145 | 178 | 86 | 124 | 928 | sim | T1/T4 sem fonte na frase |
| 5 | 44337c1ea4e3 | 143 | 240 | 135 | 188 | 82 | 112 | 900 | sim | CIDH 1967 sem referência; prioridade de Silva et al. (2026) |
| 6 | bc3ccb37e816 | 150 | 250 | 150 | 200 | 92 | 128 | 970 | sim | mesma versão da 7 |
| 7 | bc3ccb37e816 | 150 | 250 | 150 | 188 | 84 | 107 | 929 | sim | "sem sinal de fabricação" na conclusão; deff transportado sem marca |
| 8 | **8f6cd9f100de** | 150 | 250 | 150 | 196 | 87 | 137 | 970 | sim | versão final |
| 9 | 8f6cd9f100de | — | — | — | — | — | — | — | — | descartada: o juiz não devolveu saída estruturada (`max turns reached`) |
| **10** | **8f6cd9f100de** | **150** | **250** | **150** | **200** | **82** | **128** | **960** | sim | **versão final; menor nota válida = nota de aceite** |

Arquivos: `build/juiz/rodada-<n>.json` (veredito estruturado; todos os descontos, com seção e frase) e
`build/juiz/hash-final.txt`. Os prompts, as respostas cruas e a saída do CLI (`rodada-<n>.{prompt.txt,raw.txt,stdout.txt}`)
e os envelopes crus das rodadas 1 e 9 (`rodada-1.json`, `rodada-9.json`, com caminho local e identificador de sessão) ficam
fora do repositório público (`.gitignore`); a nota da rodada 1 (854) consta só nesta tabela.

## Gates determinísticos (saída real, versão final)

Densidade (`tools/densidade_paper.py`, adaptado do exemplar, lista de termos do domínio declarada no
arquivo, fronteira de palavra para não casar "SIM" dentro de "assim"; padrões de filler da skill
`density-checker` incluídos verbatim):

```text
palavras (corpo, sem apêndices): 10112
TDI          = 4.10   (alvo >= 3)      · 83 termos distintos
filler_ratio = 0.0012 (alvo < 0,12)   · 7 ocorrência(s)
info_density = 49.30  (alvo >= 0,15)   · 55 citações + 942 números + 0 âncoras
  filler encontrado: May; de forma
[PASS] as três métricas de densidade batem o alvo
```

"May" é falso positivo do padrão da skill dentro de "Mays" (Cochran & Mays). Latim com propósito:
a priori (§2.2), ceteris paribus (§5), de facto (§5), post hoc (§5).

E-E-A-T (`tools/eeat_referencias.py`, fórmula da skill `citation-eeat`, classificação conservadora
declarada linha a linha no arquivo; nenhum periódico recebeu autoridade 100; boost de URL não aplicado):

```text
referências: 56 · tipos distintos: 11 (auto-citação, dataset, dataset oficial, decisão judicial, lei, livro, padrão internacional, periódico, relatório oficial, sociedade civil, working paper)
menu de 6 tipos da rubrica, equivalência declarada: 5/5 aplicáveis cobertos -> paper; livro; norma oficial (RFC/NIST no gênero); framework / padrão; documentação oficial de dados (builder's library no gênero)
últimos 3 anos (>= 2023): 28/56 = 50.0%
média E-E-A-T = 81.5/100 (limiar 75) · abaixo de 75: 15
[PASS] média E-E-A-T >= 75
```

Referências e vocabulário (`tools/verifica_referencias.py`; controle negativo exercido: autoria
trocada, DOI inventado e "pela primeira vez" injetados reprovam com 6 falhas):

```text
  [exceção declarada] CIDH (1983) -> research-2026-10-21-rodada3/escrutinio/simetria/SHA256SUMS-cuba.txt (frente sem ledger jsonl)
  [info] auto-citação sem URL pública ainda: Flores, C. U. (2026)
1. pertencimento: 56/56 referências com DOI/URL em ledger (ou exceção declarada)
2. autoria e ano: 32 referências com DOI conferidas contra Crossref/DataCite
3. citação <-> lista: 56/56 citadas; 0 citação(ões) órfã(s)
4. vocabulário: 0 achado(s)
[PASS]
```

Figuras (`tests/test_figuras.py`; parser independente do script de figura; controle negativo exercido):
`7/7 passaram`. Figuras determinísticas (duas execuções, mesmos bytes; `figures/SHA256SUMS`).

Export: `tools/build.sh` (reference-doc v2 da casa + `fix_docx_tables.py` + LibreOffice);
`qpdf --check` sem erro; PDF 1.113.208 bytes (limite 4 MB); 51 páginas; 12.122 palavras no DOCX;
referências no estilo Bibliography com recuo deslocado de 720 twips e sem marcador; nenhuma string
proibida pelo canon (instituição acadêmica) no PDF; nenhum caminho de sistema no `document.xml`.

## Descontos residuais aceitos (não corrigidos depois do congelamento)

- Eventos de governo T1/T4 de 2019 citados pelo veículo, sem entrada na lista: as fichas (URL,
  trecho, sha256) estão na tabela de eventos da frente de simetria do projeto de origem, que não
  emite ledger e não está no repositório público.
- Dois tamanhos da população LGB+ adulta (3,01 milhões pelo peso calibrado da PNS; 2,92 milhões
  como 1,89% dos adultos do Censo 2022) não reconciliados no texto (são bases diferentes, não erro).
- N1 não letal definido "por 100 mil" e reportado como prevalência de 12 meses.
- 306 mil adultos (para +30%) e o módulo PNAD de 275.573 adultos (detecta 31,7%) aparecem lado a
  lado na conclusão sem dizer que o módulo de um ano fica ligeiramente abaixo de +30%.
- Sem referência bibliográfica para Kitagawa, para o bootstrap wild-cluster, para o acórdão da ADO 26
  e para a lista do TDoR (há caminho de script ou de dado; não há entrada na lista).
- `[REPO_URL]` e "DOI a ser atribuído" na auto-citação, por decisão de não publicar nada nesta tarefa.

## O que não foi feito (fases da skill)

- Fase 7 (release): nenhum commit, push, tag, release ou DOI.
- `validate_canon.py` não rodado: espera o layout `docs/paper/paper-final.*` da fábrica, e a tarefa
  fixou `paper/`.
- O selo `chain_hash 680fd2c9…84dd` do repositório é anterior a `paper/`; `make_provenance.py --verify`
  passa a apontar os arquivos de `paper/` como novos até a próxima regravação (não regravado aqui).

## Higiene pré-publicação (2026-10-23, depois do congelamento; paper.md intacto)

- `build/juiz/`: só os vereditos estruturados e o hash final entram no repositório; o resto fica fora (ver acima).
- `tools/` e `tests/`: caminhos absolutos trocados pela raiz do repositório (`ledger_lookup.py`, `verifica_referencias.py`,
  `tests/test_figuras.py`) ou por variável de ambiente (`build.sh`: `CODEX_HASH_REFERENCE_DOCX`, `CODEX_HASH_CANON`;
  `juiz_rubrica.py`: `GROK_BIN`, `RUBRICA_ACADEMICA_MD`). `build.sh` e `juiz_rubrica.py` ficam marcados como ferramentas do autor:
  dependem de material privado do laboratório ou de assinatura de modelo e não rodam só com o repositório.
- `tests/test_figuras.py` confere as cópias de `figures/fontes/` contra `dados/` do próprio repositório e o extrato do painel contra
  `dashboard/dashboard_dados.publico.json`; roda no clone limpo (`pytest -q` na raiz). `figures/fontes/dashboard_extrato.json` mudou só
  no campo `origem` (texto), com `SOURCES.tsv` e `figures/SHA256SUMS` atualizados; valores e figuras intactos.
- `verifica_referencias.py` no repositório: 56/56 referências em ledger (ou exceção declarada), 0 achado de vocabulário (canon da casa
  ausente: só a lista fixa).
- Selo: `run_all.py --selar` regravou o selo com `paper/` dentro; o novo `chain_hash` está em `../output/hash-chain.md`. O texto
  congelado do artigo continua citando o selo anterior (`680fd2c9…`), como registro do estado no congelamento.


## v0.2 (2026-10-24): título ditado, 19 figuras, anexos A-E — gate de 920 NÃO atingido

| Rodada | sha256 (12) | Estrutura | Densidade | Fundamentação | Tese | Consistência | Factual | Total | Hash ok | Observação |
|---|---|---|---|---|---|---|---|---|---|---|
| v2-2 | ba885b26… | — | — | — | — | — | — | 875 | sim | antes da rodada 2 de figuras |
| v2-3 / v2-4 | ef004728… | — | — | — | — | — | — | 856 / 862 | sim | idem |
| v2-5 | 8fb702a5116f | 138 | 238 | 132 | 168 | 74 | 112 | 862 | sim | 19 figuras; o juiz leu o artigo cortado na §7 (ver abaixo) |
| v2-6 | 8fb702a5116f | 130 | 230 | 135 | 175 | 78 | 128 | 876 | sim | mesma versão da v2-5 |
| v2-7 | 1e8354bf3619 | 132 | 240 | 135 | 178 | 74 | 118 | 877 | sim | prompt com aviso de leitura até "FIM DO ARTIGO" |
| **v2-8** | **6af3fe410989** | 132 | 240 | 140 | 178 | 74 | 112 | **876** | sim | **versão final**: 4 consertos de precisão + figuras reordenadas; o juiz citou os Anexos C e D (leu além da §7) |

> [!WARNING]
> **Corrigido em 2026-10-26 (frente G): todas as notas desta tabela são de leitura PARCIAL.** Os prompts tinham de 134.455 a 145.769 B,
> acima do limite medido do programa do juiz (99.974 B); chegaram ao modelo de 63,7% (v2-8) a 69,8% (v2-2) do artigo, com o meio omitido
> (das Referências ao Anexo C na v2-2 a v2-4; da seção 7.1, da 7 ou da 6 ao Anexo C na v2-5 a v2-8). "Leu além da §7" na v2-8 não procede: o
> fim entregue (3.988 B) é o final do último anexo, e o que estava entre a seção 6 e o Anexo C não chegou. Falta na tabela a rodada v2-1
> (134.455 B), inválida: JSON de zeros, depois de o modelo ler parte do arquivo do corte e do paper.md com ferramentas. Tabela completa na
> seção "Todas as rodadas do juiz".

- **Resultado: ❌ abaixo do gate de 920.** Versão final (`sha256 6af3fe410989f32f20b59744038f9291a56120fb621d39cc1c4064ad434a2e89`):
  876, uma rodada só (v2-8). Versões anteriores: 877 (v2-7) e 862/876 (v2-5/v2-6, variância de 14 pontos sobre o mesmo
  arquivo). Um juiz, uma família (Grok pela assinatura). Nenhuma referência foi inventada para subir a recência; o título é do autor.
- **A nota da v0.1 (960/970) também pode ter sido dada sobre prompt cortado:** os prompts das rodadas 8 e 10 tinham 95.764 bytes,
  logo acima do limiar de ~94 KB em que o Grok tira o resto do corpo da mensagem; o fim da lista de referências pode não ter sido lido.
  *(Corrigido em 2026-10-26: não procede. O limiar medido é 99.974 B; os 95.764 B chegaram inteiros ao modelo, pelo registro de sessão
  do programa. Os "~94 KB" eram o tamanho do começo entregue quando há corte. A nota da v0.1 fica como "leitura não comprovada".)*
- **Defeito de medição corrigido:** com o artigo de 130 KB, o Grok deixa fora do corpo da mensagem o que passa de ~94 KB do
  prompt e nem sempre lê esse resto (v2-4 e v2-5 descontaram uma §7 "cortada no meio da frase"). `tools/juiz_rubrica.py` agora
  manda ler todo o restante e marca o fim com `===== FIM DO ARTIGO =====`; uma sonda manual confirmou leitura até a última linha.
  *(Corrigido em 2026-10-26: o defeito NÃO foi corrigido. O programa omite o meio do prompt antes de o modelo recebê-lo, e o juiz rodava
  com `--max-turns` baixo e instrução de pontuar; mandar "ler todo o restante" não traz o texto de volta. A sonda manual (144.647 B)
  também foi cortada (64,4% do artigo entregue): a "última linha" que ela confirmou está no fim, que o corte sempre entrega. A v2-7 e a
  v2-8 continuaram parciais.)*
- **Corrigido depois da v2-7 (erros de precisão):** legenda da Figura 13 (estudo de eventos inconclusivo, sem atribuir a queda nem a
  ausência de efeito à ideologia); §4.2(2) com a faixa de cada desfecho; §4.3 sem "risco muito menor" (contagem e população não se
  combinam numa taxa); "1 em 7" declarado como arredondamento de 14,70%.
- **O que o juiz ainda desconta (v2-8):** Figura 17 lida como se "o quarto mais bem classificado" fosse o 4º lugar (é o quartil
  superior); Resumo com a compensação incidência x registro mais forte que o §3.5; teste de escala transporta razões não letais (2,82 e
  3,84) para morte por agressão sem marcar o transporte; Tabela 1 com 56 falas e a linha de governos sem T1/T4; §4.1 diz "em todos os
  anos de 2012 a 2024" com a Tabela 5 só na média 2022-2024 (a série anual está na Tabela 19 do Anexo A); recência 50,0%; 15 referências
  abaixo de 75 de E-E-A-T.
- **Descontos da v2-7 (antes dos consertos):** legenda da Figura 13 ("não indica efeito de ideologia") mais forte que o estudo de
  eventos inconclusivo com antecipações p = 0,009 e 0,028; §4.2(2) junta limites de desfechos diferentes; §4.3 tira "risco
  muito menor" da cobertura implícita sem lembrar a incompatibilidade de numerador; "1 em 7" para 14,70% sem dizer que é
  arredondamento; atos T1/T4 de 2019 e a auto-citação sem entrada ou URL pública; recência 28/56 = 50,0% no piso; 15
  referências abaixo de 75 de E-E-A-T; título jornalístico fora da tese; a solução (survey) não responde mortalidade.
- Gates determinísticos da versão final: TDI 3,07; filler 0,0001; info 48,22; E-E-A-T 81,5; verifica 56/56, 0 órfãs, 0 vocabulário;
  Anexo A idêntico ao gerado; `pytest` 23 passaram. PDF 3.838.614 bytes, 82 páginas (eram 87), cada página lida renderizada.
- Build: `tools/embed_figs.py` embute cópias de 1200 px em paleta de 256 cores (as figuras de referência de 300 dpi ficam
  intactas) e o LibreOffice exporta com JPEG qualidade 85; figura mais alta que 5,6 polegadas é limitada pela altura para não
  deixar a legenda sozinha na página.
- Layout: figuras reposicionadas um parágrafo adiante (ou antes) onde deixavam meia página em branco; tabelas dos anexos em 8 pt e
  podendo quebrar entre páginas (cabeçalho repetido); mapa de respostas (Figura 1) limitado a 5,0 polegadas.
- README atualizado (título, sha, BibTeX v0.2 com "Flores, Carlos Ulisses"); selo regravado (ver `../output/hash-chain.md`); sem commit.


## v0.3 (2026-10-24): artigo principal e anexos em dois PDFs — gate de 920 NÃO atingido

Texto julgado: só o **artigo principal** (`paper.md` até o marcador `<!-- parte:anexos -->`, o mesmo corte de `tools/make_export.py`),
com `tools/juiz_rubrica.py --parte=principal`: o prompt diz ao juiz que os Anexos A a F estão num PDF separado, fora do texto julgado, e
lista os anexos e as figuras impressas só no Anexo F (3, 6, 7, 8, 11, 16, 24, 25, 26, 27). O hash conferido é o do `paper.md` inteiro.
Juiz: Grok (`grok-4.7-build`, CLI 1.0.62) pela assinatura do fornecedor, sem ferramentas e sem web; um juiz, uma família.

| Rodada | sha256 (12) | Estrutura | Densidade | Fundamentação | Tese | Consistência | Factual | Total | Hash ok | Observação |
|---|---|---|---|---|---|---|---|---|---|---|
| v3-1 | 9b993d069076 | — | — | — | — | — | — | — | — | inválida: "max turns reached" (teto de 3 voltas), sem saída estruturada |
| v3-2 | 9b993d069076 | — | — | — | — | — | — | — | — | inválida: idem com teto de 6 voltas |
| v3-3 | 9b993d069076 | 128 | 180 | 142 | 168 | 74 | 112 | 804 | sim | teto de 14 voltas; terminou em 1 volta; leu até o Apêndice C |
| **v3-4** | **1f99edbddb3f** | 143 | 214 | 150 | 168 | 86 | 132 | **893** | sim | **versão final**, depois de 4 correções de precisão; 1 volta; segunda e última rodada |

> [!WARNING]
> **Corrigido em 2026-10-26 (frente G): 804 e 893 são notas de leitura PARCIAL.** Os prompts (189.901 e 190.680 B) passavam do limite medido
> do programa do juiz (99.974 B); chegaram ao modelo 46,3% e 46,2% do artigo principal, com o meio omitido (da seção 3.6, na v3-3, ou da
> 3.5, na v3-4, até o Apêndice B). "Leu até o Apêndice C" (v3-3) diz respeito ao fim entregue, não ao meio. "Sem ferramentas" (parágrafo
> acima) não valia: o `--tools ""` deixava as 25 ferramentas do programa. Nas inválidas v3-1 e v3-2, o modelo recebeu o aviso de corte, tentou
> ler as linhas omitidas do arquivo do programa com `read_file` e `grep` e esgotou as voltas devolvendo JSON provisório: é essa a causa que
> o parágrafo "Rodadas inválidas" abaixo dava como não isolada.

- **Resultado: ❌ abaixo do gate de 920.** Nota de aceite da versão final: **893** (única rodada válida sobre o sha final). A versão
  anterior às correções teve 804; a diferença de 89 pontos mistura correção de texto e variância do juiz. Variância sobre o MESMO
  arquivo não foi medida na v0.3 (uma rodada válida por sha); a histórica é de 41 pontos (v0.1) e 14 pontos (v0.2).
- **Rodadas inválidas:** v3-1 e v3-2 pararam por limite de voltas com o modelo devolvendo JSON provisório a cada volta; com teto de 14,
  v3-3 e v3-4 terminaram em uma volta. A causa não está isolada (pode ser estocástica): o teto maior coexistiu com o sucesso, não o
  prova. O prompt tinha 189.901 bytes (v2-8: 145.769). `juiz_rubrica.py` agora rejeita rodada sem saída estruturada sem gravar `.json`;
  os envelopes crus das rodadas inválidas ficam fora do repositório (`.gitignore` cobre `*.raw.txt`).
- **Corrigido entre v3-3 e v3-4 (precisão, sem número novo; cada número inserido já estava no artigo):** (1) Resumo e Abstract citam o
  1 de 49 com a regra aplicada (0 de 49) e os dois p de Fisher (0,58 e 0,19); (2) o "sim" para mortalidade geral fora do Brasil vem
  marcado como dependente do adendo posterior da seção 2.3 (pela regra original, "parcial") no Resumo, no Abstract, na Tabela 2, na seção
  3.3 e na seção 7; (3) Resumo e Abstract dizem que 50 de 160 é fração verificada, não piso nem teto; (4) o resumo para leigos diz que a
  queda nacional começou em 2018, ainda no governo Temer.
- **Não procede (com a linha que prova):** "numerador B 167 contra a conta 164" (a seção 3.4 diz que 164 < 167 é justamente o que mostra
  que B não é limite inferior); "latim: só *a priori*" (há *a priori* na seção 2.2, *ceteris paribus* e *post hoc* na seção 5); "a
  Figura 1 é o arquivo fig24" (a numeração é por ordem de menção; o nome do arquivo não é numeração); "só 41 de 78 DOIs" (as demais
  referências são lei, dado oficial e relatório, sem DOI).
- **O que impede 920 (não corrigido, por decisão ou fora da alçada desta etapa):** densidade técnica TDI 2,40 no texto julgado (corpo
  técnico sozinho 2,80; abertura para leigos 4,92; a abertura em linguagem comum foi pedida pelo autor e não foi cortada); título do
  autor ("Ninguém sabe") mais largo que o enunciado sustentado fora do Brasil (o título não muda por decisão do autor); tese enunciada
  na seção 1, não no 1º parágrafo do Resumo (Resumo em respostas curtas desde a v0.2); Tabelas 1 e 2 com 10 linhas; Lei de Campbell
  tratada como hipótese, não resultado (escolha de rigor); seção 7 sem lista numerada de trabalho futuro; veredito mundial
  "sustentada" dependente de adendo escrito depois de conhecer os estudos (declarado nos mesmos lugares); auto-citação e `[REPO_URL]`
  sem URL pública (nada foi publicado); exceções de URL declaradas (TSE, Câmara, Senado, CIDH); 31,2% no título da Figura 10 contra
  31,3% no texto (arredondamento do PNG da figura; a legenda declara); "T4" com dois sentidos nos dois documentos de governo
  (pré-registros intocáveis; o texto usa os nomes). Residual da v3-4 não corrigido para não mudar o texto julgado: o Resumo dá "p = 0,58
  e 0,19" na mesma ordem de "1 de 49 (0 de 49)", sem nomear qual p é de qual regra.
- *(Corrigido em 2026-10-26: o item a seguir não procede; os 95.764 B chegaram inteiros, abaixo do limite medido de 99.974 B; ver a seção
  "Todas as rodadas do juiz".)* ~~**A nota da v0.1 (960/970) foi dada com o prompt possivelmente cortado** (95.764 bytes, acima do limiar de ~94 KB em que o Grok tira o~~
  ~~resto do corpo da mensagem); não é comparável com a da v0.3.~~ (Segue não comparável, mas por outro motivo: a v0.1 teve o prompt
  inteiro e a v0.3, 46% do artigo.)
- Gates determinísticos da versão final: TDI 2,40 (texto julgado; FAIL declarado); filler 0,0001; info 48,53; E-E-A-T 83,7 (16 abaixo
  de 75; 47/78 = 60,3% de 2023 em diante); verifica_referencias 78/78, 0 órfãs, 0 vocabulário; `pytest -q tests paper/tests` 109 passaram.
- PDFs: `build/paper.pdf` (artigo principal) e `build/anexos.pdf` (Anexos A a F), gerados do mesmo `paper.md` por `tools/build.sh`;
  `qpdf --check` sem erro, abaixo de 4 MB, título e autor nos metadados. Layout: Resumo e Abstract sem espaço entre itens
  (`fix_docx_tables.py`; entrelinha do canon intacta) para as palavras-chave não caírem sozinhas na página seguinte.
- Vereditos estruturados: `build/juiz/rodada-v3-3.json` e `rodada-v3-4.json`; prompts, respostas cruas e saída do CLI fora do git.


## P3 — o texto mudou depois da última rodada do juiz (2026-10-24)

A rodada v3-4 (893/1000) julgou `sha256 1f99edbddb3f56b8812a33f2058f57f02b85db45374aa20fd34f074c7dbb3edc`. Depois dela, a frente P3 integrou o Disque 100 e corrigiu erros de
precisão verificáveis; **não houve nova rodada** (a nota 893 NÃO vale para o texto atual). O diff é pequeno e está inteiro num script de trocas
exatas (cada uma exige 1 ocorrência do texto antigo): 21 trocas e 1 parágrafo novo, 18 linhas removidas e 27 acrescentadas em 1.392 linhas (234.680 -> 238.144 bytes);
sha256 atual do estado intermediário `59a5783dae3c495f7c7a4fd66dfad31c44b0dfddfa715eac3c1acc6e9b36ab76` (o texto ainda será refeito por outra frente).

| Troca | Tipo | Origem verificável |
| --- | --- | --- |
| Resumo, Abstract, caixa da seção 3.9, legenda da Figura 22 e tabela de desvios: "p = 0,58 e 0,19" passa a dizer p = 0,58 para 1 de 49 (regra literal) e p = 0,19 para 0 de 49 (regra aplicada) | precisão | `r7_parlamento_sensibilidade.csv` (Fisher 1/49 x 2/38 = 0,5784; 0/49 x 2/38 = 0,1879) |
| Legenda da Figura 10 dizia "o título da figura arredonda para 31,2%" | precisão | o PNG foi aberto: o título mostra 31,3%; o teste proíbe "31,2%" no SVG; só a legenda estava errada (figura não regenerada) |
| Tabela 1: pessoas trans na coluna de orientação "desde o 2º semestre de 2023" | precisão | `dados/disque100/saidas/dicionario_rotulos.csv`: formato C desde 2022S2 (e TRANSEXUAL/TRAVESTI já no formato B, 2020S1) |
| Seção 2.1, nota da Tabela 1, seção 5, referência, Anexos C e E: "só os cabeçalhos foram lidos" | precisão (ficou falso) | os 23 arquivos foram contados (`dados/disque100/`) |
| Seção 3.14: "o 17º ledger não foi distribuído"; "128 + 29 scripts" | precisão (ficou falso) | `manifest/INVENTARIO-PUBLICO.md` (18 ledgers; 180 scripts Python) |
| Anexo C: manifesto "843 registros, 397 com SHA-256" | precisão | `manifest/MANIFESTO-FONTES.csv` regenerado na v0.3: 876 e 430 |
| Seção 3.14: parágrafo do Disque 100; Figura 27 (Anexo F) nova; a figura dos revisores hostis passa de 27 a 28 | conteúdo | `dados/disque100/saidas/d100_serie_anual.csv`, `RELATORIO-DISQUE100.md` |
| Figura 1: a linha do Disque 100 deixa de dizer "sem número usado no paper" | precisão | a Figura 27 usa contagens |

Auditor de números (`P3-scripts/auditor_numeros.py`, fora do repositório): Resumo x Abstract, números do Resumo, do resumo para leigos e das caixas de destaque
presentes no corpo, legenda x texto do SVG de cada figura, chamadas e alvos de Figura e Tabela, e números exclusivos de cada tabela do corpo: sem divergência além das acima.
Nenhum pré-registro foi tocado; título e tese iguais. O Disque 100 não altera nenhum veredito.


## v0.4 e v0.4.1 (2026-10-25): um PDF, segundo exame e correções — gate de 920 NÃO atingido (e sem leitura integral do juiz)

**v0.4** (`sha256 f283475e8853e8cec20278a46503bd756f0f68bc288249e8cc367e9980c7f69f`, 126 páginas, PDF gerado pelo Word, selo do repositório
`5cf914b0…`/721): um PDF só, com os Apêndices A a D. Rodada **v4-1 = 811/1000** (estrutura 132/150, densidade 190/250, fundamentação 135/150,
tese 168/200, consistência 74/100, factual 112/150), sobre o `paper.md` INTEIRO, com os apêndices (prompt de 241.763 B), com uma cópia do juiz
que trocou só a evidência de build (log do build v0.4 no lugar de rodar o pipeline da v0.3), a regra (4b) das referências APA e uma nota sobre a
lista de 78 entradas do E-E-A-T; não comparável com a 893 da v0.3, que julgou só o artigo principal. Vereditos: `build/juiz/rodada-v4-1.json`.

**Segundo exame da v0.4** (relatórios no repositório, em `docs/revisao/`): triagem de 60 itens do juiz e do revisor de outra família
(`S2-TRIAGEM.md`: 29 procedem, 10 em parte, 10 não procedem, 5 limites já declarados, 5 limites a declarar, 1 juízo de rubrica; 3 de
severidade alta: Resumo sem as duas regras da mortalidade, alcance da frase sobre perseguição, Nota da Figura 20) e revisão hostil de um
terceiro modelo (`F-LAUDO.md`: 3 altas, 15 médias, 11 baixas; 20 números recalculados conferem).

**v0.4.1** (`sha256 4a775cccceb6d7b5eb112b98320d938a7358a16c62c78093b60a25f05127bc02`, 128 páginas, 2.595.901 B): aplica todos os itens que procederam ou procederam em parte, sem análise nova
e sem número calculado no texto (lista com o texto anterior ao lado: `docs/historico-de-correcoes.md`, seção 8). Não aplicados, com motivo:
suplemento separado e corte de figuras (contraria a decisão do autor de um PDF único com figuras e tabelas no artigo); "±132 mil incluindo a
incerteza do total" (a decomposição não está no arquivo de origem); "Democratas, hoje União Brasil" (fonte nova); PNS 2026 "em coleta"
(fonte nova com registro no ledger; a agenda cita a edição seguinte da PNS pelo plano de trabalho já referenciado). Selo do repositório
desta versão: `2865eee5b03d640639582ab6d51a812ef02e3ef3ef918af313c9ed27c41124f5` (724 arquivos).

Juiz: `tools/juiz_rubrica.py` corrigido (absorve a cópia da v4-1 sem caminho absoluto; lê o log de build mais recente; E-E-A-T lido das
referências do próprio paper.md), Grok pela assinatura do fornecedor, `JUIZ_MAX_TURNS=14`, texto inteiro com apêndices, como na v4-1.

| Rodada | sha256 (12) | Estrutura | Densidade | Fundamentação | Tese | Consistência | Factual | Total | Hash ok | Observação |
|---|---|---|---|---|---|---|---|---|---|---|
| v4-1 | f283475e8853 | 132 | 190 | 135 | 168 | 74 | 112 | 811 | sim (leitura truncada) | v0.4; texto inteiro no prompt; cópia do juiz (S2) |
| **v4-2** | **4a775cccceb6** | 150 | 140 | 150 | 200 | 100 | 150 | **890** | sim (leitura truncada) | v0.4.1; texto inteiro no prompt; juiz corrigido; única rodada |

- **Leitura truncada nas duas rodadas da v0.4 (achado desta frente, com a linha que prova).** O CLI do juiz entrega à mensagem só o começo do
  prompt (cerca de 94 KB) e o fim; o meio fica fora. Na v4-2 (prompt de 251.724 B), o raciocínio gravado em `build/juiz/rodada-v4-2.raw.txt` (fora do git: traz caminho local e id de sessão)
  diz: "O artigo foi cortado na linha 'O Anuário registra 783, 1.63' e pulou direto para o apêndice de glossário" e "Preciso ler as seções
  omitidas (linhas 658–1760)"; a rodada terminou numa volta (`num_turns` 1), sem ler o trecho. Na v4-1 (241.763 B): "O artigo foi parcialmente
  omitido. Preciso ler as seções faltantes", também numa volta. Logo: (1) a 890 da v4-2 mede o Resumo, o Abstract, as seções 1 a 3.5 (até o
  meio), parte do glossário e as saídas das ferramentas, e não o artigo inteiro; as notas máximas em consistência e correção factual não
  cobrem as seções 3.5 a 7, as Referências e os Apêndices A e B; (2) a 811 da v4-1 tem a mesma limitação, e as duas não são comparáveis como
  medida do texto; (3) parte dos descontos da v4-1 citava trechos que não existem no paper.md ("objeção forte", "ameaça mais séria"; triagem
  S2, J10), compatível com pontuação sobre texto não lido. O registro de 94 KB já constava deste arquivo para a v0.1. Corrigir isso exige mudar
  o procedimento do juiz (por exemplo, julgar em partes menores que 90 KB ou permitir a leitura do arquivo), decisão que fica com o autor;
  esta frente não repetiu a rodada.
  *(Corrigido em 2026-10-26, frente G: medido, o corte começa em 100.000 B de prompt (99.974 B ainda chegam inteiros); "cerca de 94 KB" é o
  começo entregue (94.394 B), seguido do fim (3.988 B). Chegaram ao modelo 35,1% do artigo na v4-1 e 33,0% na v4-2. "O registro de 94 KB já
  constava deste arquivo para a v0.1" não procede: a v0.1 não foi cortada. O procedimento mudou na versão 0.5 de `tools/juiz_rubrica.py`
  (seção final "Frente G").)*
- **Descontos da v4-2 e triagem:** o único desconto é o TDI de 1,94 (0 de 80 no subcritério; densidade 140/250): **limite declarado** (a
  ferramenta não reconhece as grafias por extenso que o texto usa, como "efeitos fixos duplos" e "efeito de desenho", e a abertura em linguagem
  comum fica por decisão do autor; a v0.4 tinha 2,02, e a v0.4.1 acrescentou ressalvas em prosa). Nenhum outro desconto foi apontado, o que,
  pelo item acima, não prova ausência de problema nas seções não lidas.

Gates determinísticos da v0.4.1: TDI 1,94 no corpo (FAIL declarado: a abertura em linguagem comum e a grafia por extenso dos termos, que a
ferramenta não reconhece, ficam por decisão do autor); filler 0,0004; E-E-A-T 80,1 sobre as 97 referências lidas do paper.md (49/97 = 50,5% de
2023 em diante; a 83,7 e os 60,3% da v0.4 eram de uma lista fixa de 78 entradas da v0.3); `verifica_referencias` 97/97, 0 órfãs, 0 vocabulário;
`crivo_texto` 82/82 parágrafos com lastro, 0 jargão, 0 placeholder; `crivo_docx` 0 forma, 0 conteúdo; `pytest -q tests paper/tests` 114 passaram.

**Juiz com leitura integral, rodadas v4-3 (frente S3, 2026-10-25; acréscimo, nada acima foi alterado).** A caixa do topo, reescrita
na v0.4.2, resume as quatro rodadas da v0.4; esta seção detalha as rodadas v4-3.

- **As rodadas v4-1 e v4-2 do Grok foram parciais.** O prompt passa de ~94 KB e o CLI do juiz entrega à mensagem só o começo e o fim (ver o
  item "Leitura truncada" acima). *(Corrigido em 2026-10-26: o limiar é 100.000 B; ~94 KB é o começo entregue.)* `docs/revisao/S2-TRIAGEM.md`, linha 108, afirma que a 811 da v4-1 "julgou o paper.md INTEIRO, com os
  Apêndices A–D (prompt 241.763 B)"; o raciocínio gravado das rodadas mostra o contrário: v4-1 "O artigo foi parcialmente omitido. Preciso
  ler as seções faltantes", v4-2 "O artigo foi cortado na linha 'O Anuário registra 783, 1.63' e pulou direto para o apêndice de glossário",
  ambas com `num_turns` 1. A frase da S2-TRIAGEM descreve o que foi ENVIADO ao juiz, não o que ele leu.
- **Achado novo: o `agy -p` (Gemini pela assinatura Google) também corta.** Na primeira tentativa do Gemini, o agy entregou ao modelo 191.581
  dos 252.930 B do prompt ("<truncated 61349 bytes>", no transcript do próprio agy): saíram o fim das Referências e os Apêndices A a D. O
  modelo percebeu, tentou ler o paper.md do disco (negado) e não respondeu. Juiz por `agy -p` com prompt acima de ~190 KB é tão parcial
  quanto o Grok; o envelope JSON do agy ("num_turns": 1) não prova ausência de ferramenta.
- **Procedimento v4-3.** Prompt = o de `tools/juiz_rubrica.py` para este sha (`build/juiz/rodada-v4-2.prompt.txt`, sha256 `f450110b…`, mesma
  rubrica, pesos, evidência do build v0.4 e marcador "FIM DO ARTIGO") + uma regra (8): julgar sem ferramentas, ler o artigo inteiro, devolver
  o JSON do juiz com o campo `leitura_integral` (última frase do Apêndice D, a frase anterior a ela e uma frase da seção 3.9, verbatim) e
  trecho verbatim em cada desconto (prompt final sha256 `9e219caf…`, 252.930 B). Critério de validade pré-registrado antes de qualquer
  resposta (frases conferidas contra o paper.md, tokens de entrada, ausência de ferramenta, hash). Dois modelos de famílias distintas, pela
  assinatura do fornecedor, custo zero, cwd vazio: Astra (`gpt-6-astra`, codex exec, esforço alto, só leitura, sem web) e Gemini
  (`gemini-4-argon-high`, agy; segunda tentativa entregue em duas mensagens por stream-json, cada uma abaixo do corte).

| Rodada | Estrutura | Densidade | Fundamentação | Tese | Consistência | Factual | Soma | Prova de leitura | Situação |
|---|---|---|---|---|---|---|---|---|---|
| v4-3 Astra | 140 | 160 | 150 | 200 | 74 | 144 | **868** | 3/3 frases; 91.451 tokens de entrada | válida em todos os critérios |
| v4-3 Gemini | 145 | 215 | 145 | 195 | 96 | 145 | **941** (informado 936) | 3/3 frases; 110.411 tokens no turno final | válida pela prova; ressalvas abaixo |

- **Prova de leitura integral (as duas rodadas):** "Fonte: Flores (2026)." e "Caminhos relativos à raiz do repositório
  https://github.com/ulissesflores/lgbt-indicador-violencia." (última linha do Apêndice D) e, da seção 3.9, "O nível mede o tipo de documento
  que registra o ato, e não a certeza do fato nem a originalidade da investigação." (frase que só ocorre ali). A seção 3.9 começa no byte
  121.526 do prompt, dentro da faixa que o Grok não leu. Hash do paper.md igual antes e depois das duas rodadas e igual ao conferido.
- **Ressalvas do Gemini:** o "total" informado (936) não é a soma das dimensões (941; regra 7 do prompt); deu crédito parcial onde a regra (2)
  manda zero (TDI 1,94 < 3 com 50 de 80; latim com 1 uso, 5 de 10; 7 palavras-chave, 5 de 10), o que o Astra e o Grok não fizeram; com a regra
  (2) aplicada, a soma é 881 (891 se só o TDI). Procedimento: a saída estruturada do agy passa por uma ferramenta interna ("finish") e o agy
  injetou dois avisos depois da primeira parte; o modelo respondeu com um JSON vazio de espera e só julgou depois da segunda parte; nenhuma
  leitura de arquivo, web ou comando. O critério pré-registrado de isolamento falhou na letra por isso (adendo pós-hoc datado); a prova de
  leitura passou.
- **Variância entre famílias, por dimensão (Gemini − Astra):** estrutura +5, densidade +55 (quase toda do crédito parcial no TDI),
  fundamentação −5, tese −5, consistência +22, factual +1; soma +73 (+13 com a regra 2 aplicada ao Gemini). As notas NÃO foram tiradas em
  média e não formam série com 811/890 (Grok, leitura parcial) nem com as notas da v0.3.
- **Gate ≥ 920: não demonstrado.** Astra 868; o Gemini só passa de 920 com o crédito parcial que o próprio prompt proíbe.
- **Triagem dos 16 descontos** (contra este sha): 9 procedem ou procedem em parte, nenhum de severidade alta; 4 médios: objeção 7 da seção 4.3
  ("contou episódios de hostilidade e de proteção nos dois lados": a busca foi simétrica, o resultado não: proteção só em mandatos do PT,
  Tabela 8); seção 4.4 (o levantamento de vitimização não letal não calibra contagens de mortes da sociedade civil, contra a seção 3.13);
  seção 3.7 (a janela de 3 + 3 anos é cortada em 2012-2024: 47 das 67 trocas têm janela completa, e esse recorte, já calculado no repositório,
  não aparece no texto); seção 3.10 ("871 itens" contra a soma 811 da Tabela A17: falta a linha F3 × Wikipédia, 60 itens, no laudo de mídia e
  na tabela). Baixos: 7 palavras-chave; latim reduzido a um uso desde a v0.4; rótulo "limite inferior" na Tabela A16 (2,56, com o extremo B
  2,42 abaixo); glossário do numerador B sem a restrição ao numerador A; "atenua o coeficiente" sem a condição de erro clássico. Limites já
  declarados: TDI; fontes de imprensa e instrumento não lido na seção 3.8; leitura por resumo de 12 obras. Não procedem: E-E-A-T (média 80,1
  ≥ 75); "Lei de Campbell" (Campbell, 1979, nomeado). Nenhuma correção foi aplicada nesta frente (o paper.md não foi editado); a lista com o
  texto proposto está no arquivo de trabalho do autor S3-TRIAGEM.md. Vereditos: `build/juiz/rodada-v4-3-astra.json` e
  `build/juiz/rodada-v4-3-gemini.json` (com `_soma_dimensoes`, `_ressalvas` e `_valida_s3`; `_valida` tem o sentido do juiz: hash conferido).

## Rodada final v4-4 (frente E6, 2026-10-25): v0.4.2, Astra, leitura integral — 885/1000

Objeto: `paper.md` v0.4.2, `sha256 3469a16764dc4f5382634a39c6d627b8065a6cbb51666402b64a460d6e01e23b` (antes = depois = conferido pelo
modelo). Prompt: o de `tools/juiz_rubrica.py v4-4 --dry-run` para este sha (`build/juiz/rodada-v4-4.prompt.txt`, sha256 `8fbdca82…`,
252.902 B; evidência do build7) com a mesma regra (8) da v4-3 (só o rótulo da rodada e "cerca de 224 mil caracteres" mudam; prompt final
sha256 `e2d718cc…`, 254.108 B). Critério de validade pré-registrado antes da resposta (o da v4-3 com o objeto novo; sha256 `2e228603…`).
Modelo: `gpt-6-astra` (codex exec pela assinatura ChatGPT, esforço alto, só leitura, sem web, cwd vazio), uma tentativa.

| Rodada | Estrutura | Densidade | Fundamentação | Tese | Consistência | Factual | Soma | Prova de leitura | Situação |
|---|---|---|---|---|---|---|---|---|---|
| v4-3 Astra (v0.4.1) | 140 | 160 | 150 | 200 | 74 | 144 | 868 | 3/3 frases | válida |
| **v4-4 Astra (v0.4.2)** | 150 | 150 | 150 | 200 | 90 | 145 | **885** | 3/3 frases (Apêndice D, paper.md:1471; seção 3.9, paper.md:484, 1 ocorrência); 91.799 tokens de entrada | válida em todos os critérios (A a E) |

Leitura dos 5 descontos (−115), sem edição do texto depois desta rodada (decisão do briefing; ficam como pendências da próxima versão):
- **TDI 1,94 < 3 (−80, densidade):** limite já declarado (caixa do topo).
- **Métricas por subseção (−20, densidade):** a seção 4.2 é interpretação, sem número próprio. Juízo de rubrica, não erro; a seção 4.2 não
  mudou entre a v0.4.1 e a v0.4.2, e o mesmo modelo deu 20 de 20 a esse subcritério na v4-3: variância do juiz dentro da mesma família.
- **Contradição na hipótese 3 (−6, consistência): procede (média).** A seção 4.1 diz que a terceira hipótese "não é sustentada em nenhuma
  das duas formas" e que "não há evidência de invenção"; a Tabela 11 diz "contrariada como invenção". No vocabulário da seção 2.2, "não há
  evidência" é "não sustentada pelo que foi medido", e não "contrariada". Pendência: alinhar a Tabela 11 à prosa (ou o inverso, com o motivo).
- **"nenhum modelo foi usado para gerar dado" (−4, consistência): procede em parte (baixa).** A mesma seção 2.6 diz que modelos codificaram
  itens de discurso; a frase quer dizer que nenhum número foi produzido por modelo sem arquivo de origem. Pendência: "nenhum modelo gerou
  número sem arquivo de origem; a codificação de discurso feita por modelo é dado derivado, descrita na seção 3.10".
- **Intervalo num censo (−5, factual): procede (baixa).** Tabela A17 (cópia de `docs/laudos/MIDIA.md`): "F2 | Parlamento | 56 | 56 (censo)
  | 49 | 49 [43-53]"; as outras células de censo (F1 Parlamento, F2 Wikipédia, F4 Parlamento) não trazem intervalo, e o de Wilson numa
  contagem censitária exige modelo de erro de classificação não declarado. Pendência: tirar o intervalo dessa célula ou declarar o modelo
  (o arquivo está dentro do selo; mudança = selo novo).

Variação v4-3 -> v4-4 (mesmo modelo, texto corrigido): estrutura +10 (seis palavras-chave), densidade −10 (latim +10; métricas por
subseção −20, variância), consistência +16 (as correções C1 a C4 e o vocabulário da A16 e do glossário saíram dos descontos), factual +1.
**Gate ≥ 920: não demonstrado** (885; sem o TDI, que a decisão de escrita para leigos mantém abaixo de 3, a soma seria 965). Nenhuma
nova rodada de edição foi feita nesta frente. Vereditos: `build/juiz/rodada-v4-4-astra.json` e `.md`. Os três descontos que procederam
foram aplicados depois, na v0.4.3 (seção seguinte).

## v0.4.3 (frente E7, 2026-10-25): mudanças de texto sem número novo, listadas abaixo; não re-julgada

Objeto: `paper.md` v0.4.3, `sha256 b21b2dd4a89cc61577bb481c6a9365ee69c49f363ee0e6113499a83011e5d6c3`; PDF `sha256 42326db8b2d9ddc9c5b1c5e1c595c2b9e135f8416effca2c67df05314d2820d3` (129 páginas, 2602178 bytes); selo `7a59d1622c78ba47f36386f6dcac9d2b892f46de077f8c6c9d90f99a09abee46`
(724 arquivos). Nenhuma rodada do juiz sobre esta versão: a 885 da v4-4 vale para a v0.4.2. Lista com o texto anterior ao lado em
`docs/historico-de-correcoes.md`, seção 10.
- **Hipótese 3 (desconto médio da v4-4):** a seção 4.1 passa a usar o veredito da Tabela 11, no vocabulário da seção 2.2: "não sustentada
  como taxa ou total; contrariada como invenção, isto é, como fabricação de casos", pelos mesmos números. O Resumo, o Abstract e a
  Conclusão não trazem o veredito da hipótese 3 e não mudaram.
- **Seção 2.6 (desconto baixo):** os modelos codificaram itens de discurso, com a dupla codificação e o teste exato de Fisher já descritos;
  "nenhum número de resultado foi gerado por modelo". Na mesma seção, o segundo exame passa a dizer que o juiz leu só parte do texto
  (coerente com a seção 9 do histórico), e o terceiro exame é apontado; a Tabela D1 também o aponta.
- **Tabela A17 (desconto baixo):** a célula de censo F2 × Parlamento perde o intervalo [43-53] em `docs/laudos/MIDIA.md` (repositório e
  origem), e a tabela é regenerada por `tools/make_anexos.py` (`--conferir` e `--provar` passam); a soma da amostra segue 871.
- **Página com duas linhas do glossário (pendência de layout da v0.4.2):** o verbete do numerador B foi encurtado sem mudar o sentido; o
  Apêndice C volta a duas páginas, e o PDF passa de 130 para 129 páginas.
- Descontos que não procederam ou são limites declarados (TDI −80; métricas por subseção −20) seguem como na seção anterior. TDI da
  v0.4.3: 1,93 (`tools/densidade_paper.py`; era 1,94 na v0.4.2: o corpo ganhou 127 palavras e nenhum termo técnico novo).
- Gates da v0.4.3: `verifica_referencias` PASS; `crivo_texto` R1 a R3 = 0; `make_anexos --conferir` e `--provar` PASS; build pelo Word
  com 6 faces Times New Roman, `qpdf --check` sem erro e `crivo_docx` 0 de forma e 0 de conteúdo; `make_provenance --verify` OK antes
  e depois do build.

## Frente G (2026-10-26): o corte do juiz medido e o juiz blindado

Nenhuma rodada nova sobre o `paper.md`; o texto, o selo (`7a59d162…`, 724 arquivos) e os vereditos anteriores não mudaram. Esta frente
mediu o corte do programa do juiz (seção "Todas as rodadas do juiz", no começo deste arquivo) e mudou `tools/juiz_rubrica.py` (versão 0.5):

- **`--backend=astra|grok|gemini`, padrão `astra`** (`codex exec -m gpt-6-astra`, prompt pelo stdin, só leitura, sem web; o método das
  rodadas v4-3 e v4-4; fica como padrão mesmo com o `--verbatim` do Grok, porque este foi medido numa só versão do programa e não é
  documentado como garantia, e o Astra já tem duas rodadas com leitura integral comprovada). `grok` passa a usar `--verbatim` (entrega o prompt inteiro, medido com 130.000 e 260.000 B) e `--disallowed-tools`
  com as 25 ferramentas do programa (o `--tools ""` não removia nenhuma); **recusa** rodar prompt acima de 99.974 B se o programa não for a
  versão medida (1.0.62). `gemini` usa o `agy` em stream-json, com o prompt em partes de até 150.000 B (o `agy -p` corta perto de 191.581 B),
  sem `--json-schema`. Os três rodam em pasta vazia e temporária e conferem, no registro do próprio programa, que o prompt chegou inteiro e
  sem ferramenta.
- **Prova de leitura obrigatória:** o script insere a linha `<!-- prova-leitura -->` entre dois parágrafos de prosa perto de 60% do texto
  julgado (no paper.md v0.4.3, antes do primeiro parágrafo da seção 5.1, a 60,4%; no prompt de 254.558 B, no byte 163.863, dentro da faixa
  que o corte omitiria), e o esquema JSON ganha `leitura_integral` com a última frase do texto e a primeira frase depois do marcador, verbatim. A rodada
  só é válida (`_valida`) com hash conferido, as duas frases certas e a entrega conferida; senão grava `_valida: false` e sai com código 3.
- **Julgar por partes (`--partes`) não foi implementado:** a rubrica não prevê somar notas de textos parciais, e o `--verbatim` e os outros
  dois backends tornam isso desnecessário.
- **Testes** (fora do repositório; nenhum julga o artigo inteiro): `--dry-run` nos três backends (prompt de 254.560 B; o artigo no prompt,
  sem o marcador, é igual ao paper.md); recusa exercida com um programa falso de versão 9.9.9. A 2ª linha do prompt deixou de dizer "se a
  interface deixar parte dele fora da mensagem, leia TODO o restante" (contradizia a regra 8); as rodadas de teste abaixo usaram a frase antiga. Rodadas reais curtas sobre trechos do começo
  do paper.md (as notas não medem nada; o que se testou foi a prova e a entrega):

| Backend | Texto julgado | Prompt (B) | Prova de leitura | Entrega conferida | Situação |
|---|---|---|---|---|---|
| astra | primeiros 28.475 B do paper.md | 52.156 | 2/2 frases (marcador a 68,4%) | só raciocínio e mensagem; 28.128 tokens de entrada | válida |
| gemini | idem | 52.156 | 2/2 frases | 1 mensagem, inteira no transcript do agy; 0 marcas de corte | válida |
| grok, 1ª tentativa | primeiros 79.713 B do paper.md | 103.394 (acima do limite) | 2/2 frases (marcador a 62,1%) | sem corte e sem ferramenta, mas a conferência falhou porque o programa tira o `\n` final do prompt | inválida (defeito da conferência, corrigido: compara sem espaço nas pontas) |
| grok, 2ª tentativa | idem | 103.394 | 2/2 frases | mensagem igual ao prompt; 0 ferramentas definidas e chamadas | válida |

No teste do Grok o marcador caiu a cerca de 73 KB do começo do prompt, dentro do trecho que o corte também entregaria: ali a entrega
integral está provada pelo registro de sessão (mensagem igual ao prompt de 103.394 B, sem aviso de corte) e, para prompts maiores, pelas
sentinelas do experimento controlado (260.000 B, sentinela a 130 KB citada).

## Rodada v4-5 e v0.4.4 (frente E8, 2026-10-26): v0.4.3, Grok com `--verbatim`, leitura integral — 928/1000; v0.4.4 não re-julgada

**Rodada v4-5.** Objeto: `paper.md` v0.4.3, `sha256 b21b2dd4a89cc61577bb481c6a9365ee69c49f363ee0e6113499a83011e5d6c3` (antes = depois = devolvido pelo modelo:
hash conferido). Prompt de `tools/juiz_rubrica.py` v0.5 (`build/juiz/rodada-v4-5.prompt.txt`, fora do git; 254.558 B, sha256
`b2b6809b…`), com a 2ª linha nova da frente G ("está inteiro nesta mensagem"). Backend `grok`, modelo `grok-4.7-build`, comando
`grok -p --verbatim --disallowed-tools <25>`, 1 turno, 624,8 s; entrega conferida no registro de sessão do próprio programa: mensagem igual ao
prompt, nenhum aviso de corte, 0 ferramentas definidas e 0 chamadas, 106.952 tokens de entrada. Prova de leitura (marcador a
60,4% do texto, antes do 1º parágrafo da seção 5.1), as duas frases devolvidas verbatim e conferidas:
- última frase: "Fonte: Flores (2026)."
- frase depois do marcador: "A medida de vitimização não letal é autorrelato de adultos classificados pela orientação sexual declarada numa única edição da PNS; a pesquisa não identifica pessoas trans, menores, motivação nem tendência (IBGE, 2022b)."

| Rodada | Estrutura | Densidade | Fundamentação | Tese | Consistência | Factual | Soma | Prova de leitura | Situação |
|---|---|---|---|---|---|---|---|---|---|
| **v4-5 Grok (v0.4.3)** | 145 | 221 | 150 | 182 | 90 | 140 | **928** | 2/2 frases; entrega íntegra | válida (`_valida: true`) |

Triagem dos 7 achados críticos (cada um conferido nos arquivos):

| # | Achado (resumo) | Leitura | Onde está ou o que mudou |
|---|---|---|---|
| 1 | TDI 1,93 < 3 no corpo | limite declarado | caixa do topo; decisão de escrita para leitor não especialista; não corrigido |
| 2 | Veredito de mortalidade fora do Brasil muda de "parcial" para "sustentada" só pela regra complementar, definida depois dos estudos | limite declarado | seção 2.2 ("definida em 24 de outubro de 2026, depois de identificados estudos recentes [...] por isso ela não é prospectiva"); seção 3.2 (o veredito sob as duas regras); Tabela B1 (desvio). Não corrigido |
| 3 | Anterioridade dos oito pré-registros é declaração do autor | limite declarado | seção 2.4 ("sem carimbo de tempo externo, as horas da Tabela 3 são declaração do protocolo do autor") e seção 5.4. Não corrigido |
| 4 | Recência 49/97 = 50,5% no limite; 31 referências com E-E-A-T abaixo de 75 | limite declarado (métrica de gate, fora do texto) | com a referência nova do STF: 49/98 = 50,0%, no limite do ≥ 50% da rubrica; E-E-A-T 80,0 (≥ 75), 32 abaixo de 75 (a nova, 69,5, entre elas). Nenhuma referência foi acrescentada, trocada ou reclassificada para subir a recência ou a média |
| 5 | Tabela A2: 916 + 637 = 1.553 contra 1.554; seção 3.5: 7,1% ao lado de 179/3.291 (5,44% bruto) | **procede (precisão)** | corrigido na v0.4.4: Nota da A2 (1 adulto LGB+ com cor ou raça ignorada, código 9 de C009, conferido no microdado; regra de `dados/pns/seguro_pns2019.py`); seção 3.5 ("parcela ponderada pelo desenho amostral"; "179 de 3.291 vítimas na amostra não ponderada"; `dados/pns/c05_razao_direta.csv`: razão de totais ponderados 7,12; n brutos 3.291 e 179) e Nota da A5 |
| 6 | ADO 26 (STF, 2019) e os dois episódios de hostilidade de 2019 sem fonte primária na lista | **procede em parte** | ADO 26: a fonte primária já estava no registro de fontes (`research-2026-10-21-rodada3/F8-literatura/sources.jsonl`, id `stf-ado-26-mi-4733`, sha256 `1ea52666…`, inteiro teor de 566 p., Plenário, 13/06/2019) e entra nas Referências e na Tabela 1. Episódios: o registro só tem imprensa (`escrutinio/simetria/eventos_C18.csv`, E17 e E20; `SIMETRIA.md`: transcrição oficial não localizada; nenhum ato oficial no registro): sem fonte nova não há correção; o limite segue declarado na seção 3.8 e na Tabela 8 |
| 7 | Nenhum parecerista humano; a ligação caso-fonte da amostra do GGB de 2019 não é reproduzível no repositório | limite declarado | seção 2.6 ("Nenhum parecerista humano revisou o texto"); seção 3.4 ("exige a lista nominal, não distribuída por privacidade"). Não corrigido |

Descontos não críticos da v4-5 não aplicados nesta frente (o briefing da E8 pediu os críticos; ficam como pendências da próxima versão):
tese só no 2º parágrafo da Introdução (−5); "Lei de Campbell" sem o nome e direções futuras sem (i)-(v) nem retomada na Conclusão
(−4 e −4); tese argumentável, insight e solução elegante (−4, −2, −4: juízo de rubrica); Resumo × Conclusão sobre o que falta no óbito
(−2); Resumo × seção 3.7, "não se associou de forma detectável" ao lado do p = 0,016 (Holm 0,073) da mediana das 67 trocas (−2);
"Silva et al. (2026)" sem distinguir as duas referências Silva de 2026 (−2); os 36 testes tratados como independentes no "cerca de 1,8
células por acaso" (−2); URL da Comissão Nacional da Verdade com o carimbo `2016id_` do arquivo da web (−2).

**v0.4.4 (mudanças de precisão, sem número novo; não re-julgada).** Objeto: `paper.md` v0.4.4, `sha256 fdd8e9d48b32a8bef3d0d7f226c95f665677185781f168e69562cf4b7aea0ced`; PDF
`sha256 7a63b6fb4042ac29827ee56f68508bf580f56c828abe3a768d81502288159445` (129 páginas, 2608720 bytes); selo `d1d2e4d77e2be87486b635c230d2e88025b6ac87888682e89f4dcf87942b215b` (724 arquivos). Lista com o texto anterior ao lado em
`docs/historico-de-correcoes.md`, seção 11.
- **Tabela A2:** a Nota (gerada por `tools/make_anexos.py`, mapa `NOTA_EXTRA`) diz a regra de cor ou raça e que 1 adulto LGB+ tem cor ou
  raça ignorada (código 9) e fica fora das duas linhas; as células, copiadas de `dados/pns/seguro_pns2019.md`, não mudam.
- **Seção 3.5 e Tabela A5:** 7,1% é a parcela ponderada pelo desenho amostral; 179 de 3.291 são contagens da amostra não ponderada, e a
  Nota da A5 diz o mesmo da tabela.
- **Tabela 1 e Referências:** "pelo Supremo Tribunal Federal (2019)", com o inteiro teor do acórdão da ADO 26 nas Referências (98 entradas);
  `tools/eeat_referencias.py` classifica a nova como decisão judicial (autoridade 80, como o TEDH 2023).
- **Seção 2.6 e Tabela D1:** o quarto exame (rodada v4-5) é apontado.
- **Dentro do selo:** `docs/revisao/S2-TRIAGEM.md` (cópia), `CHANGELOG.md` e `docs/historico-de-correcoes.md`, seções 9 e 10: os cinco
  "cerca de 94 KB" passam a "corte do programa do juiz em prompts de 100.000 bytes ou mais (descarga do programa grok 1.0.62, corrigida com
  `--verbatim`; correção de 2026-10-26)"; CHANGELOG 0.4.4; README (versão e linha do quarto exame); REPRODUCIBILITY (versão); histórico,
  seção 11; `manifest/MODIFICACOES.tsv` (linha da cópia da triagem).
- Gates da v0.4.4: `verifica_referencias` PASS (98/98 no registro de fontes, 98/98 citadas, 0 órfãs); `eeat_referencias` média 80,0,
  recência 49/98 = 50,0%; `crivo_texto` R1 a R3 = 0; `densidade_paper` TDI 1,93 (abaixo de 3, declarado);
  `make_anexos --conferir` e `--provar` PASS; build pelo Word com 6 faces Times New Roman, `qpdf --check` sem erro e `crivo_docx` 0 de
  forma e 0 de conteúdo; `make_provenance --verify` OK antes e depois do build.

## Nota de publicação (2026-10-31): nome da instituição omitido nos vereditos

A rubrica usada pelos juízes das rodadas v4 cita, como referência de nota, o limiar de trabalho final de uma instituição de
ensino. Os vereditos publicados em `paper/build/juiz/` (rodadas v4-1, v4-2, v4-3-gemini e v4-5) trazem esse nome substituído
por "[instituição omitida]", pela regra da casa de não publicar vínculo acadêmico. Nenhuma nota, número ou trecho do
raciocínio dos juízes mudou além dessa troca; os originais ficam fora do git.
