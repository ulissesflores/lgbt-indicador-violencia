# Reprodutibilidade e localização de cada resultado no repositório

[English](reproducibility-and-result-locations.md) · **Português (Brasil)**

## Reprodutibilidade

O repositório público é a referência primária deste estudo, e o artigo deriva dele (este estudo; https://github.com/ulissesflores/lgbt-indicador-violencia). O repositório reúne os dados derivados, o código, os pré-registros com suas impressões digitais, os relatórios da revisão adversarial e os testes que travam os números publicados. A integridade do conjunto é verificada por um selo de proveniência, uma cadeia de hashes calculada a partir do SHA-256 de cada arquivo distribuído do repositório, exceto o artigo, seu PDF e as ferramentas que o constroem, que muda se qualquer um desses arquivos mudar e que se confere com um único comando (Tabela M1). O selo da versão atual muda a cada alteração dos arquivos selados; ele está em output/hash-chain.md e se confere com python3 -I make_provenance.py --verify. O PDF do artigo não integra o conjunto selado; sua impressão digital SHA-256 é publicada em arquivo próprio do repositório, de modo que o leitor pode conferir que o PDF lido é o derivado da versão analisada. O selo verifica que os arquivos são os mesmos; não verifica, sozinho, quando foram escritos.

A reprodução tem duas trilhas (este estudo). A trilha leve recalcula, em cerca de seis minutos, os números das etapas listadas na matriz de reprodução do repositório; os demais, como o dimensionamento do Apêndice K, são conferidos por teste. A trilha pesada parte do microdado oficial e foi exercida de ponta a ponta para a PNS de 2019, cujo arquivo foi baixado do IBGE com SHA-256 conferido e reproduziu quatro derivados byte a byte (IBGE, 2022a); os agregados do SIM e do Sinan não foram reexecutados a partir do bruto (DATASUS, 2026a, 2026b). As tabelas do Apêndice C são copiadas por *script* dos arquivos do repositório, sem número digitado, e as figuras são geradas com saída determinística, conferida por testes que comparam os valores desenhados com os arquivos de origem e reprovam quando um valor plotado é alterado, controle negativo exercido.

Não são redistribuídos os microdados brutos do SIM, do Sinan, da PNS, do TSE e do Disque 100, que são arquivos oficiais grandes, baixáveis por *scripts* de aquisição com SHA-256 esperado (DATASUS, 2026a, 2026b; IBGE, 2022a; TSE, 2026; MDHC, 2026); textos de terceiros, por direitos autorais, dos quais o repositório guarda endereço, data de acesso e, quando o arquivo foi salvo, SHA-256; e listas nominais de vítimas, por privacidade, razão pela qual a ligação entre caso e fonte na validação da contagem do GGB de 2019 não é reproduzível publicamente (GGB, 2020). O inventário completo de fontes e *scripts*, o índice do que o repositório contém e o registro de correções ([`docs/corrections.pt-BR.md`](corrections.pt-BR.md)) estão no próprio repositório (Tabela M1).

## Localização dos resultados e dos elementos de verificação no repositório

**Tabela M1**

*Caminho, no repositório público, de cada resultado e de cada elemento de verificação desta versão*

| Resultado ou elemento | Seção, tabela ou figura | Caminho no repositório |
|---|---|---|
| Selo de proveniência e sua conferência | seção 2.4 | `output/hash-chain.md`; `output/provenance.json`; `manifest/SHA256SUMS.txt`; comando `python3 -I make_provenance.py --verify` |
| PDF do artigo e sua impressão digital | todo o artigo | `docs/paper/paper-final.pdf` (edição em português do Brasil); `docs/paper/paper-final-en.pdf` (edição em inglês); `docs/paper/SHA256SUMS.txt` |
| Figuras, valores desenhados e textos das figuras | Figuras 1 a 8; figuras dos Apêndices C a K | `figures/article/`; `figures/` (`make_figures.py`, `valores_plotados.json`, `textos_fora_da_imagem.json`, `fontes/SOURCES.tsv`); `data/exposicao/fig_caminho_v05.py`; `data/pns/fig_pns_v05.py`; `data/pns/fig_agressor_pns2019.py`; `data/disque100/fig_disque_v05.py`; `data/exposicao/fig_series_por_governo.py` |
| Testes que travam os números publicados | seção 2.4 | `tests/` (`tests/test_paper_numbers.py` trava os números do Resumo, da exposição estadual e das correções) |
| Vitimização não letal e quem agrediu (PNS) | seção 3.1; Tabela 3; Tabelas C1 a C12 | `data/pns/` |
| Fichas de saúde e concordância com boletins | seção 3.2; Figura 6 | `data/sinan/`; `data/concordancia/` |
| Disque 100 | seção 3.2; Figura 4; Figura D3 | `data/disque100/` |
| Identificabilidade e dimensionamento de um levantamento | seções 2.3 e 6; Figura 5; Tabela 6; Tabela K1 | `analysis/simulation/`; `analysis/survey-cost/` |
| Taxas padronizadas do SIM e séries por período de governo | seções 3.3 e 3.6; Figura 8; Tabelas E2 a E4; Tabelas G2, G6 e G7 | `data/sim/`; `data/exposicao/` |
| Mortalidade fora do Brasil | seção 3.4; Tabela E1; Figura E1 | `figures/fontes/estudos_mortalidade.tsv`; `analysis/discourse/mortalidade/` |
| Lista do GGB: conferência de 2019, concordância, escala e checagens críticas | seção 3.5; Figura 7; Tabelas F1 a F4 | `data/ggb/`; `figures/fontes/ggb_validacao_resumo.json`; `analysis/ggb-audit/`; `analysis/ggb-series/`; `analysis/counterpoint/` |
| Painel de governadores, estudo de eventos e troca de presidente | seção 3.6; Tabelas G1 e G3 a G11 | `data/painel/`; `data/ideologia/`; `data/presidencia/`; `data/exposicao/` |
| Busca simétrica de atos de governo | seções 1 e 3.7; Tabela H1 | `analysis/robustness/simetria/` |
| Violência de Estado em regimes de tipos distintos | seção 3.7; Tabela 5; Tabela I1 | `data/regimes/` |
| Circulação no Parlamento e na imprensa | seção 3.7; Tabelas J1 e J2 | `analysis/discourse/`; `analysis/robustness/simetria/` |
| Pré-registros e adendos | seção 2.4; Tabelas B2 e B3 | `preregistrations/`; `analysis/robustness/reanalise/`; `analysis/robustness/simetria/`; `data/painel/R6-PREREGISTRO-FORMA.md`; `data/presidencia/`; `data/exposicao/` |
| Inventário de fontes e *scripts* | seção 2.5 | `manifest/INVENTARIO-PUBLICO.md`; `manifest/MANIFESTO-FONTES.csv`; `sources/` |
| Aquisição dos microdados oficiais | seção 2.4 | `scripts/` e `data/disque100/scripts/` (*scripts* de aquisição com SHA-256 esperado) |

*Nota.* Caminhos relativos à raiz do repositório https://github.com/ulissesflores/lgbt-indicador-violencia. Fonte: este estudo.
