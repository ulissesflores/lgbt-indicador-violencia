# Código das figuras do artigo

Estes scripts desenham as figuras que ilustram o artigo, em cinco idiomas (pt-BR, en, es, it, he), em SVG e PDF sem fundo.
Eles leem só arquivos deste pacote e não gravam nada fora da pasta de saída.

> [!NOTE]
> Isto não é o mesmo que as figuras do repositório (`figures/*.svg`, `figures/*.pdf`, `figures/*.png`, geradas por
> `figures/make_figures.py` e travadas por `tests/test_figuras.py`). Aquelas ilustram a análise do repositório; as daqui
> são as versões do artigo, com rótulos traduzidos e desenho adaptado ao texto.

## O que cada script desenha

| Script | Figuras (arquivo de saída -> função) |
|---|---|
| `make_figuras_v05.py` | `fig_v05_01_caminho` -> `fig1` (caminho do dado até a contagem); `fig_v05_02_pns` -> `fig2` (PNS 2019); `fig_v05_03_agressor` -> `fig3` (agressor); `fig_v05_04_disque100` -> `fig4` (Disque 100); `fig_v05_08_governos_series` -> `fig8` (séries por governo) |
| `make_figuras.py` | `fig1_pns2019_vitimizacao` -> `figura1`; `fig2_ggb_cobertura_implicita` -> `figura2`; `fig3_governos_painel_eventos` -> `figura3`; `fig6_proporcao_1_em_7` -> `figura6`; `fig8_taxas_sim_grupos` -> `figura8`; `fig9_governos_forest` -> `figura9`; `fig10_identificabilidade` -> `figura10`; `fig11_circulacao_parlamento` -> `figura11`; `fig13_pns_sinan_janelas` -> `figura13`; `fig14_concordancia_sinan_anuario` -> `figura14`; `fig15_ideologia_taxa_residuos` -> `figura15`; `fig17_tamanho_de_survey` -> `figura17`; `fig18_motivacao_sinan` -> `figura18`; `fig19_ggb_homicidio_uf` -> `figura19`; `fig20_serie_nacional_trocas` -> `figura20`; `fig21_alinhamento_governador_presidente` -> `figura21`; `fig22_taxa_nacional_por_governo` -> `figura22`; `fig23_trocas_de_governador_exposicao` -> `figura23`; `fig25_mortalidade_internacional` -> `figura25`; `fig26_ggb_verificabilidade` -> `figura26`; `fig27_ggb_curva_de_hipoteses` -> `figura27`; `fig28_disque100_serie` -> `figura28` |
| `bidi_he.py` | regras de desenho do hebraico (direção da leitura, números com sinal, fórmulas); carregado pelos dois scripts quando `--lang he` |
| `rotulos/{es,it,he}.json` | tabelas de rótulos por idioma (o inglês fica dentro dos scripts) |
| `rotulos/fonte-pt-en.json` | tabela de rótulos pt-BR/en (nenhum dos três scripts a lê; copiada junto por pertencer ao conjunto) |

## Como rodar

Da raiz do pacote, uma chamada por script e por idioma:

```bash
PYTHONDONTWRITEBYTECODE=1 python -I figures/article/code/make_figuras.py     --lang en
PYTHONDONTWRITEBYTECODE=1 python -I figures/article/code/make_figuras_v05.py --lang en --saida minha/pasta
```

- `--lang`: `pt-BR`, `en`, `es`, `it` ou `he`.
- `--saida <pasta>`: padrão `<raiz>/.run/figuras-artigo/` (pasta fora do controle de versão). A raiz vem do próprio arquivo
  (`Path(__file__).resolve().parents[3]`); a variável de ambiente `REPO_ROOT` a substitui.
- Requer `matplotlib` e `numpy` (`requirements.txt`) e `pdftotext` (poppler) no PATH. Para `--lang he` exige também
  `matplotlib` 3.11 ou mais novo (com libraqm) e `python-bidi` 0.4.2; os scripts abortam se a versão for menor.

## Onde sai

- `<saida>/<idioma>/<nome>.svg` e `.pdf` (54 arquivos por idioma, os dois scripts juntos);
- `<saida>/valores/<idioma>/valores_plotados.json` e `textos_fora_da_imagem.json` (só `make_figuras.py`): os valores
  desenhados e os textos que ficam fora da imagem (título, fonte).

## Entradas (todas dentro do pacote)

`figures/fontes/*` e, só em `make_figuras_v05.py`, `data/pns/`, `data/sim/asr_brasil.csv`,
`analysis/ggb-series/series/painel_mortes_lgbt.csv`, `data/disque100/saidas/d100_serie_anual.csv`,
`data/sinan/serie_campo55_uf_ano.csv` e `data/anuario/anuario_lgbtfobia_uf_ano_v2.csv`.
