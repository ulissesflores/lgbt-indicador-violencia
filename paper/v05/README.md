# Artigo v0.5: Mortalidade e violência contra pessoas LGBT+ no Brasil

Texto da versão 0.5 do artigo, com os Apêndices B a M (o antigo Material Complementar) e o quadro de afirmações. O PDF,
no padrão Codex Hash e em APA 7, entra em `docs/paper/paper-final.pdf` na versão 1.0.0 final, já com o DOI (gerado por `paper/tools/build_v05.sh`). O repositório vem primeiro e o artigo deriva dele: todo
número do texto tem arquivo que o produz em `dados/` (o quadro `QUADRO-E2.md` liga cada afirmação ao arquivo, e `tests/test_numeros_v05.py`
trava os números novos de LiHS, variação da taxa por governo, causa indeterminada e coabitação; os demais números vêm dos arquivos de `dados/` e de seus testes).

| Arquivo | O que é |
|---|---|
| `MANUSCRITO.md` | texto do artigo (revisão r10), com as 8 figuras e o Apêndice A (glossário) |
| `revisao/` | pareceres dos modelos revisores e a matriz de respostas de cada rodada |
| `MATERIAL-COMPLEMENTAR.md` | Apêndices B a M (tabelas, métodos e reanálises que não cabem no texto; até a revisão r8 chamados MC1 a MC12) |
| `mapa-apendices.json` | rótulo antigo de cada tabela e figura (Tabela MC2.A1, usado nos pareceres r5–r8) e o rótulo APA no PDF (Tabela C1) |
| `QUADRO-E2.md` | quadro de afirmações: cada número conferido por script contra o arquivo que o produziu |
| `referencias.md` | lista única de referências (APA 7: inclui as obras citadas só nos apêndices); `referencias-mc.md` ficou só com a nota da fusão |
| `figures/` | as 9 figuras em PNG de fundo branco: `fig_v05_*` são novas; `fig1`, `fig10`, `fig18` e `fig26` repetem `paper/figures/` |
| `SHA256SUMS.txt` | SHA-256 dos arquivos acima (`shasum -a 256 -c SHA256SUMS.txt`, dentro desta pasta) |

Geradores das figuras novas: `dados/exposicao/fig_caminho_v05.py` (fig_v05_01), `dados/pns/fig_pns_v05.py` (fig_v05_02),
`dados/pns/fig_agressor_pns2019.py` (fig_v05_03), `dados/disque100/fig_disque_v05.py` (fig_v05_04) e
`dados/exposicao/fig_series_por_governo.py` (fig_v05_08); `fig10`, `fig18` e `fig26` vêm de `paper/figures/make_figures.py`.

## Como esta pasta foi feita

O manuscrito é montado fora do repositório, a partir de blocos de texto, por scripts do autor que têm caminhos absolutos da máquina dele;
esses scripts não estão aqui. A pasta traz o resultado montado, com as mudanças de caminho que a distribuição exige (links de figura do
Material Complementar, que aponta para `../figures/`, isto é, `paper/figures/`; dois caminhos de pasta no `QUADRO-E2.md`), registradas em
`manifest/MODIFICACOES.tsv`.

- **Fora do selo.** Os cinco `.md` e `SHA256SUMS.txt` ficam fora do selo de proveniência, como `paper/paper.md`: o Material Complementar cita o selo
  da versão anterior do repositório, e o selo não pode cobrir o texto que o cita. As figuras e este arquivo entram no selo.
- **Planilha da LiHS.** Não é distribuída: traz nomes de vítimas e de acusados. O Apêndice F (nota da Tabela F4)
  diz isso e dá o SHA-256; endereço, SHA-256 e tabulação em
  [`../../research-2026-10-30-contraponto/dados/lihs-checagem-ggb2016.META.md`](../../research-2026-10-30-contraponto/dados/lihs-checagem-ggb2016.META.md).
- **Pesquisa do contraponto.** [`../../research-2026-10-30-contraponto/`](../../research-2026-10-30-contraponto/) (briefing, três frentes, registro de fontes).
