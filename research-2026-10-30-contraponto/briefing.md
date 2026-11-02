# Briefing: o "outro lado" das estatísticas de violência LGBT+ no Brasil

> META: language=pt cutoff=null scope=broad deep=on out=research-2026-10-30-contraponto
> PLAN: factual-context + paper-deep-dive, em 3 frentes (A Brasil, B internacional, C academia)
> Frentes completas: `frente-A-brasil.md`, `frente-B-internacional.md`, `frente-C-academia.md` (nesta pasta). Síntese de 2026-10-30.

## Resposta curta

1. No Brasil só existe **uma** contra-base auditável: a checagem caso a caso da lista do GGB de 2016 feita pela Liga Humanista Secular (Vieira et al., 01/05/2019), com planilha pública. [CORROBORATED: frentes A e B]
2. Fora dela, a crítica é opinião em imprensa (Gazeta do Povo, 2019 a 2023), blog ou fala parlamentar, sem base própria. Ninguém critica o Disque 100 ou o Atlas da Violência pelo lado conservador. Não achamos nenhum artigo revisado por pares de autor crítico ao movimento. [frente A]
3. Fora do Brasil o quadro é o mesmo: não achamos fonte conservadora ou religiosa com dado próprio auditável sobre violência ou mortalidade LGBT+. A crítica de método mais forte vem de fora do campo conservador: Dinno (2017, AJPH), Westbrook (2022, 2023) e Heringer & Wagner York (2026, acesso fechado, só o resumo). [frente B]
4. "Quase não há ciência do outro lado" **nunca foi medida no Brasil**. Não há pesquisa sobre a ideologia de docentes brasileiros; os dados que existem são de estudantes da USP. Os números de viés vêm dos EUA e da Europa, e a tese tem contrapontos sérios. Explicações concorrentes que ninguém testou: o contramovimento atua no Parlamento e na mídia (Côrtes & Buzolin, 2024: 46,2% de 93 projetos de lei eram contrários; 48,2% dos autores eram da bancada evangélica), falta infraestrutura de pesquisa, ou ninguém produz sobre o tema fora do ativismo. [frente C] Semente da pesquisa futura: a nota-semente `SEMENTE.md` (pasta de trabalho do autor, fora do repositório).

## Checagem LiHS: tabulação conferida

A planilha (não distribuída, porque tem nomes de vítimas e de acusados; metadados e tabulação em `dados/lihs-checagem-ggb2016.META.md`; sha256 `0dc25783…79d5ad`, 347 linhas e cabeçalho na 2ª linha) foi retabulada nesta síntese e bate com a frente A:

| Motivacao_Homof | Casos | % de 347 |
|---|---|---|
| Sim | 31 | 8,9% |
| Não | 127 | 36,6% |
| Inconclusivo | 159 | 45,8% |
| Não localizado | 23 | 6,6% |
| Exterior | 6 | 1,7% |
| Duplicado | 1 | 0,3% |

Revisor: um por caso (DA 175, CM 81, EV 32, VDB 24, DR 18, em branco 14); só 3 casos têm dois revisores. Não há medida de concordância. O "88% de erro" da página dos autores soma "não" com "inconclusivo" (227 de 258 homicídios). O critério é "indício de motivação". Um dos coautores (Reynaldo) já publicava críticas ao GGB, e outros dois fundaram uma agência de dossiês: não é checagem de terceiros independentes.

## Cross-channel highlights

- [CORROBORATED: frentes A, B; nosso MC5] **A crítica conservadora é de classificação do motivo, não da ocorrência.** A conferência do próprio estudo (2019, 160 casos) acha 73 mortes violentas confirmadas, das quais a fonte atribui 3 ao preconceito e 35 têm motivo desconhecido. A LiHS (2016) acha 31 "sim" e 159 "inconclusivo". As duas apontam na mesma direção: o motivo raramente está documentado. Nenhuma das duas mostra que o número real seja baixo.
- [CORROBORATED: frentes A, B] A cadeia crítica brasileira gira em torno de três pessoas que se citam (Vieira, Reynaldo, Di Martino); a Wikipedia em inglês cita as mesmas. Não é convergência independente.
- [CORROBORATED: frente A, checagens Truco 2018, Lupa 2019, Aos Fatos 2018] A frase "país que mais mata" foi classificada como "impossível de provar", "insustentável" ou "imprecisa", nunca como "falsa".
- [DISPUTED: a página da LiHS diz "estatísticas falsas"; a planilha mostra 45,8% de inconclusivos] Inconclusivo não é ausência de motivo.

## Skipped channels

- Heritage Foundation (relatório sobre a lei federal): 403, `NAO_RESOLVIDO` no verify_ids; não usado.
- Heringer & Wagner York (2026): texto integral fechado (Wiley, ResearchGate só 1 de 12 páginas). Não citar além do resumo.
- Versão primária do "6% de 2017" (Eli Vieira) e do "2 de 126" do Lesbocídio (Reynaldo): não encontradas; tratar como não verificáveis.
- Restrições da frente B: Ruth Institute e ACPeds não devolveram nada, e Retraction Watch não foi consultado diretamente.

## Matriz de expansão multilíngue (PRISMA-S)

Matrizes por frente (termo x idioma x base x hits) em `frente-A-brasil.md` §PRISMA-S (PT, EN, ES; web, OpenAlex, Crossref, BDTD), `frente-B-internacional.md` §PRISMA-S (EN, ES, PT) e `frente-C-academia.md` §PRISMA-S (PT, EN). Idiomas escolhidos por rendimento: PT (objeto brasileiro), EN (literatura de viés e de crime de ódio), ES (América Latina: zero crítica conservadora em 2 consultas).

## Uso no artigo (decisão)

- Parágrafo de simetria na seção 3.5: LiHS como a única contra-base auditável, com os limites acima; o restante como opinião sem base própria; "falta ciência do outro lado" como hipótese não medida.
- Material Complementar MC5: tabulação e limites.
- Referências novas: Vieira et al. (2019) e Cordeiro (2019, Gazeta do Povo). Heringer & Wagner York (2026) só pelo resumo, ou fora.

## Ledger

- `sources.jsonl`: 131 linhas (A 29, B 57, C 45). 3 chaves repetidas entre frentes (doi 10.1590/1413-81232020255.33672019; URL Gazeta 2019; Wikidata Q512983), mesma fonte, unidas na síntese.
- `verify_ids --schema-only` exit=0 (`verify_ids-schema.log`). Online: 121 resolvidos, 1 não resolvido (Heritage, 403), 9 sem resolvedor (`verify_ids-online.log`). ids verificados online: sim.
