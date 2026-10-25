# Dados UF x ano (painel LGBT, F8): proveniência

Gerado em 2026-10-11. Pasta do projeto: ``.
Brutos: `fontes/p2-f8-dados-uf/` (hashes em `fontes/p2-f8-dados-uf/SHA256SUMS.txt`). Scripts: `dados/scripts/`. Ledger: `research-2026-10-11/sources.jsonl`.

## Rota que funcionou (e as que falharam)

| Rota | Resultado |
|---|---|
| Atlas da Violência (IPEA) | **Falhou.** `www.atlasviolencia.ipea.gov.br` e `atlasviolencia.ipea.gov.br` dão NXDOMAIN. O caminho antigo `www.ipea.gov.br/atlasviolencia/` respondeu 200 uma vez, mas depois ficou sem resposta. A API `ipea.gov.br/cms/api` deu timeout. Não há série baixada do Atlas. |
| TabNet/DATASUS (SIM, óbitos por residência) | **Funcionou.** POST em `tabcgi.exe?sim/cnv/ext10uf.def`, campos Linha=UF, Coluna=Ano, filtro de grupo CID/sexo/cor-raça. |
| TabNet/DATASUS (população por sexo) | **Parcial.** `popuf.def` só tem arquivos até 2012 no servidor. |
| IBGE SIDRA (população total) | **Funcionou** para 2011–2021, 2024–2025 (tabela 6579), Censo 2010 (1378) e Censo 2022 (9514). **2023 não existe** nas tabelas testadas. |

O CSV `atlas_uf_series.csv` tem esse nome por causa do plano, mas **o conteúdo é do TabNet/SIM, não do Atlas**. Definição: "homicídio" = CID-10 X85–Y09 (agressões), por UF de residência. O Atlas usa outra definição; as séries não são comparáveis diretamente com as dele.

## Arquivos entregues

| Arquivo | Linhas x colunas | Conteúdo | Cobertura |
|---|---|---|---|
| `dados/atlas_uf_series.csv` | 3456 x 9 | UF x ano x variável | 27 UFs, 2010–2025 (2025 = preliminar; 2026 parcial, fora) |
| `dados/governadores_uf_2011_2026.csv` | 475 x 9 | uma linha por governador por ano (troca no meio do ano = duas linhas) | 27 UFs, 2011–2026 |
| `dados/ideologia_partidos.csv` | 95 x 6 | escore por partido e fonte | Bolognesi et al. 2018 (35 linhas); Power & Zucco 1990–2005 (60 linhas) |
| `dados/pns_2024_status.md` | - | status da PNS | ver arquivo |

### Variáveis do `atlas_uf_series.csv`

| Variável | Unidade | Fonte da conta |
|---|---|---|
| homicidios_total_n | casos | SIM, X85–Y09 |
| homicidios_total_taxa | por 100 mil hab | SIM / população total (SIDRA) |
| homicidios_mulheres_n | casos | SIM, X85–Y09, sexo feminino |
| homicidios_mulheres_taxa | por 100 mil mulheres | SIM / população feminina (TabNet popuf, só até 2012) |
| homicidios_negros_n | casos | SIM, preta + parda |
| homicidios_nao_negros_n | casos | SIM, branca + amarela + indígena (exclui "ignorado") |
| homicidios_arma_fogo_n | casos | SIM, X93–X95 |
| homicidios_arma_fogo_taxa | por 100 mil hab | SIM / população total |

Coluna extra `status_dado`: `final` (2010–2024) ou `preliminar` (2025). Coluna `codigo_uf` também é extra.

## Lacunas (o que faltou)

| Item | Lacuna |
|---|---|
| Atlas (série oficial) | Não obtido (DNS e API fora do ar). |
| Feminicídio | **Não existe** no SIM por CID-10 (ext10uf). Não entregue. |
| Taxa de negros e não negros | **Sem denominador** por raça/cor por UF e ano. Só contagens. |
| Taxa de mulheres 2013–2025 | **Sem população feminina** por UF e ano. Só 2010–2012. |
| População total 2023 | Não publicada nas tabelas SIDRA testadas. Taxas de 2023 ficaram vazias (27 UFs). |
| 2026 | Excluído: é segunda prévia parcial do SIM. |
| Governadores: partido | Vem só da coluna "Partido" da Wikipédia. Nem todas as listas têm essa coluna. **TSE não foi cruzado.** |
| Governadores: confiança | 4 mandatos marcados `media` (Bahia 2019–2022; Goiás 2018–2019, partido do vice não aparece; Mauro Carlesse/Tocantins 2018, datas truncadas). |
| Ideologia (Power & Zucco) | Onda mais recente baixada = 2005. A base BLS9 (1990–2021) foi baixada depois (fontes/p2-f8-governos/zucco-power-dataverse/) e é usada na robustez do painel (nota de 2026-10-21; a linha original dizia 'não baixei'). |
| Ideologia (Bolognesi) | Survey de 2018 (ABCP/UFPR), escala 0–10 (média de especialistas). Errata do artigo afeta só a Figura 2, não a Tabela 1. |

## Proveniência por arquivo

| Arquivo | Data/hora do download (UTC) | Comando/script | URL-fonte | sha256 do bruto |
|---|---|---|---|---|
| `atlas_uf_series.csv` | 2026-10-11T17:59:20Z | `python3 -I dados/scripts/tabnet_sim_uf.py` | `http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sim/cnv/ext10uf.def`; `...?ibge/cnv/popuf.def`; `https://apisidra.ibge.gov.br/values/t/6579/n3/all/v/9324/p/2011-2025`; `.../t/1378/n3/all/v/93/p/2010`; `.../t/9514/n3/all/v/93/p/2022` | ver `SHA256SUMS.txt` (`fontes/p2-f8-dados-uf/tabnet/raw/sim_*.prn`, `pop_feminino.prn`, `sidra_*.json`) |
| `governadores_uf_2011_2026.csv` | 2026-10-11 (páginas em `fontes/p2-f8-dados-uf/governadores/`) | `python3 -I dados/scripts/governadores.py` (curadoria manual; parser automático descartado por erro) | 27 páginas `https://pt.wikipedia.org/wiki/Lista_de_governadores_<UF>` | ver `SHA256SUMS.txt` (`wiki_*.html`) |
| `ideologia_partidos.csv` | 2026-10-11 | `python3 -I dados/scripts/ideologia.py` | `https://doi.org/10.1590/dados.2023.66.2.303` (HTML SciELO); `https://dataverse.harvard.edu/api/access/datafile/1412580` (party.estimates.csv; página `doi:10.7910/DVN/ZLAV8S`) | ver `SHA256SUMS.txt` (`ideologia/doi_303.html`, `ideologia/party.estimates.csv`) |
| `pns_2024_status.md` | 2026-10-11 | WebSearch (ibge.gov.br) + curl (403) | `https://www.ibge.gov.br/estatisticas/sociais/saude/10586-pesquisa-nacional-de-saude.html` (403) | `fontes/p2-f8-dados-uf/pns/` |

Notas de proveniência:
- A Wikipédia respondeu 429 em lote; as páginas restantes foram baixadas com User-Agent identificado e backoff.
- O `atlas-js/` em `fontes/p2-f8-dados-uf/` são bundles JS do Atlas baixados para inspeção; não geraram dados.
- `api-probe/` e `sidra/7358_*` são sondagens que não entraram no CSV.

## Ledger

`emit_sources.py`: **35 registros emitidos** (34 na primeira passada e 1 após correção do valor de `acesso`: `restrito` não existe no enum, usei `closed`). **0 rejeições finais.** Antes disso, a primeira tentativa escreveu 35 falhas por erro meu de redirecionamento para `/tmp` (somente leitura); nada foi gravado nessa tentativa.
