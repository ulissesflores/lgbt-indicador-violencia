# Números do artigo: origem pública dos números calculados no texto

[English](README.md) · **Português (Brasil)**

Todo número do artigo vem de um *script* e de uma saída deste repositório, de uma fonte de terceiros com a localização
transcrita, ou é limite declarado. Esta pasta guarda os números que o artigo calculou nas próprias frases (razões,
somas, reescalas), os que só saem do dado bruto público e a transcrição dos números de terceiros. As linhas
(`linha_pt`) são da edição em português do Brasil do artigo.

| Arquivo | O que guarda | Como se produz |
|---|---|---|
| `contas_do_texto.py` -> `contas_do_texto.csv` | cada conta feita na frase, com o arquivo e a chave de cada termo, o valor recalculado e se ele bate com o impresso | `python3 -I analysis/article-numbers/contas_do_texto.py` (só biblioteca padrão) |
| `numeros_do_bruto.py` -> `numeros_do_bruto.csv`, `falas_expectativa.csv` | números que exigem o dado bruto público: parcela ponderada de adultos LGB+ de 18 a 29 anos (PNS 2019) e as falas sobre expectativa de vida na Câmara dos Deputados | baixar com `scripts/acquire_pns2019.py` e `analysis/discourse/midia/scripts/camara_baixar.py`, depois `.run/venv/bin/python -I analysis/article-numbers/numeros_do_bruto.py` (precisa de pandas) |
| `terceiros_transcritos.csv` | números de terceiros: referência, DOI ou URL, página/tabela/seção, valor como está na fonte, status | lidos na fonte aberta em 2026-11-24/25; só valor e localização, sem trecho literal (direito autoral) |
| `datas_publicacao_C18.tsv` | data de publicação de cada uma das 51 páginas lidas na busca simétrica (Tabela H1, "publicadas no mandato") | lida na versão atual de cada página em 2026-11-24; as páginas brutas da leitura original não são redistribuídas |

As falas são casadas com a amostra codificada pela mesma chave de `analysis/discourse/midia/scripts/analise_parlamento.py`
(SHA-256 de id do deputado, hora de início e texto): casar significa texto idêntico ao codificado. A regra de idade de
`numeros_do_bruto.py` foi fixada antes da rodada completa; uma emenda datada, feita depois de ver o resultado (número
seguido de "anos a menos/a mais" é diferença, não idade), está declarada no *script*, e as duas saídas ficam gravadas.

## O que não se recalcula a partir deste repositório

- **Checagem da LiHS sobre a lista do GGB de 2016** (31, 127, 159 e 23 de 347 casos; 8,9%, 36,6%, 45,8%; 3 e 14):
  contagem sobre planilha de terceiros com nomes de vítimas e de acusados, que este repositório não redistribui. SHA-256,
  data de leitura e tabulação estão em `analysis/counterpoint/dados/lihs-checagem-ggb2016.META.md`; quem tiver a
  planilha confere o *hash* e reconta.
- **Itens em aberto desta pasta** (linhas cujo `bate` ou `status` não é `sim`/`conferido`): estão listados nos próprios
  CSV, sem esconder nem ajustar.
