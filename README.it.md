<div align="center">

# Mortalità e violenza contro le persone LGBT+ in Brasile: che cosa i dati pubblici consentono di affermare

**Un audit delle fonti e degli indicatori, 2010–2026**

[English](README.md) · [Português (Brasil)](README.pt-BR.md) · [Español](README.es.md) · **Italiano** · [עברית](README.he.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23873858.svg)](https://doi.org/10.5281/zenodo.23873858)
![License: Apache-2.0 (code)](https://img.shields.io/badge/code-Apache--2.0-blue)
![License: CC BY 4.0 (data, text, figures)](https://img.shields.io/badge/data%20%26%20text-CC%20BY%204.0-lightgrey)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![Tests: 182 passing](https://img.shields.io/badge/tests-182_passing-brightgreen)
![Reproducible: SHA-256 chain](https://img.shields.io/badge/reproducible-SHA--256_chain-green)

</div>

> [!IMPORTANT]
> Nell'Indagine nazionale sulla salute del 2019, il 14,70% degli adulti lesbiche, gay, bisessuali o di altro orientamento
> non eterosessuale (LGB+) ha dichiarato violenza fisica nell'anno precedente, contro il 3,82% degli adulti
> eterosessuali; il rapporto aggiustato è 2,82 (intervallo al 95%, da 2,16 a 3,68). I registri di morte brasiliani non
> riportano né l'orientamento sessuale né l'identità di genere, quindi non esiste un tasso nazionale di mortalità LGBT+.
> Dei 160 casi campionati dalla lista del Grupo Gay da Bahia per il 2019, 50 sono stati confermati dalla fonte citata (48
> da notizie): la lista non è né un tasso né un totale, e i casi non verificati non sono casi inventati. Dopo 67 cambi di
> partito del governatore, il tasso di omicidi dello stato, in rapporto a quello nazionale, è variato del −0,7% (mediana), contro il
> +4,6% senza cambio; solo nei 21 cambi senza un altro cambio vicino il calo è marcato (−10,2%, contro +6,7%). Il
> confronto è esplorativo e mostra una coincidenza, non un effetto del governo.

## L'articolo

*Mortalità e violenza contro le persone LGBT+ in Brasile: che cosa i dati pubblici permettono di affermare.* L'edizione
italiana uscirà con un DOI proprio; fino ad allora, l'articolo è in inglese e in portoghese:

| Edizione | File |
|---|---|
| Inglese | [`docs/paper/paper-final-en.pdf`](docs/paper/paper-final-en.pdf) |
| Portoghese (Brasile), originale | [`docs/paper/paper-final.pdf`](docs/paper/paper-final.pdf) |

Le edizioni spagnola e italiana della v1.2.0 non fanno parte di questa versione: riportano due letture corrette in
[`docs/corrections.md`](docs/corrections.md) (in portoghese, [`docs/corrections.pt-BR.md`](docs/corrections.pt-BR.md)) e
torneranno ciascuna con un proprio DOI. Ogni edizione ha un proprio DOI e figure con etichette nella propria lingua; il codice delle figure in
`figures/` mantiene le etichette in portoghese dello studio.

## Che cosa contiene questo repository

| Cartella o file | Contenuto |
|---|---|
| `data/` | Dati derivati e il codice che li produce: rianalisi dell'indagine (`pns/`), tassi di mortalità (`sim/`), notifiche di violenza (`sinan/`), denunce alla polizia (`anuario/`), la linea telefonica Disque 100 (`disque100/`), il panel dei governatori (`painel/`, `presidencia/`, `exposicao/`) |
| `analysis/` | Le altre analisi su cui si basa l'articolo: audit della lista del Grupo Gay da Bahia (`ggb-audit/`, `ggb-series/`, `counterpoint/`), potenza e costo dell'indagine (`survey-cost/`), simulazione di identificabilità (`simulation/`), discorso pubblico (`discourse/`), verifiche di robustezza (`robustness/`), punteggi di ideologia (`ideology/`), letteratura (`literature/`, `full-text/`) |
| `figures/` | Codice e dati di ogni figura (`make_figures.py`, `fontes/` con i valori rappresentati) e le figure dell'articolo (`article/`) |
| `preregistrations/` | Preregistrazioni con le relative marche temporali e SHA-256, come citate nell'articolo |
| `sources/` | Copie delle fonti pubbliche usate dagli script (`public/`), i registri delle fonti (`ledgers/`) e i quartili delle riviste |
| `manifest/` | Manifesto delle fonti (URL, data di accesso e, quando un file è stato salvato, SHA-256), inventario pubblico e i checksum del sigillo |
| `docs/` | Riproducibilità e posizione di ciascun risultato (`reproducibility-and-result-locations.md`), uso di modelli linguistici (`language-model-use.md`) e correzioni (`corrections.md`), in inglese e in portoghese (`.pt-BR.md`); l'articolo (`paper/`) |
| `tests/` | Test che vincolano ogni numero pubblicato al file che lo ha prodotto |
| `scripts/` | Download dei microdati ufficiali (con lo SHA-256 atteso), l'esecutore della riproduzione e gli audit |
| `run_all.py`, `make_provenance.py`, `output/` | Verifica di integrità, ricalcolo e la catena SHA-256 |

Il manifesto delle fonti (`manifest/MANIFESTO-FONTES.csv`) e l'inventario pubblico (`manifest/INVENTARIO-PUBLICO.md`)
contano 1022 identificatori provenienti da 20 registri; il repository contiene 174 script. Codice, commenti e colonne dei
dati mantengono il portoghese originale dello studio.

## Come verificarlo

```bash
python3 -m pip install -r requirements.txt
python3 -I make_provenance.py --verify     # SHA-256 of every distributed file and the chain hash
python3 -I run_all.py --rapido             # integrity, tests and seal (seconds)
python3 -I run_all.py                      # also recomputes the derived results in a separate copy (minutes)
shasum -a 256 -c docs/paper/SHA256SUMS.txt # the paper PDF
```

Output atteso del primo comando:

```text
provenance verified: <chain hash> (<n> arquivos)
```

L'hash della catena di questa versione si trova in [`output/hash-chain.md`](output/hash-chain.md). Che cosa può e che
cosa non può essere rieseguito, e perché, è indicato in [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Che cosa si afferma e che cosa no

| Si afferma | Non si afferma |
|---|---|
| Gli adulti LGB+ dichiarano più violenza fisica, sessuale e psicologica degli adulti eterosessuali (2019) | Che questo divario misuri discriminazione o stile di vita: i dati non distinguono le due cose |
| Nessun registro pubblico consente un tasso nazionale di mortalità LGBT+ | Che le persone LGBT+ vengano o non vengano uccise più spesso di altre |
| Denunce alla polizia, segnalazioni alla linea telefonica e notifiche misurano la registrazione | Che la violenza contro le persone LGBT+ sia aumentata o diminuita sotto un qualsiasi governo |
| Il tasso di omicidi dello stato, in rapporto a quello nazionale, è diminuito dopo i 21 cambi di partito del governatore senza un altro cambio vicino (−10,2%, contro +6,7%); confronto esplorativo | Che questo calo sia un effetto del governo |
| 50 dei 160 casi campionati dalla lista del 2019 (31,3%) sono verificabili dalla fonte che la lista stessa cita | Che la lista sia completa, o che sia inventata |

## Autore

Carlos Ulisses Flores · Codex Hash Research Laboratory ·
[ORCID 0000-0002-6034-7765](https://orcid.org/0000-0002-6034-7765) · [ulissesflores.com](https://ulissesflores.com) ·
[Lattes](https://lattes.cnpq.br/6905246706890561)

## Citazione

```bibtex
@dataset{flores_lgbt_indicador_violencia,
  author    = {Flores, Carlos Ulisses},
  title     = {Mortality and violence against LGBT+ people in Brazil: what public data allow us to claim --- an audit of sources and indicators, 2010--2026},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.23873858},
  url       = {https://doi.org/10.5281/zenodo.23873858}
}
```

Il DOI qui sopra rimanda sempre alla versione più recente. Vedi anche [`CITATION.cff`](CITATION.cff).

## Licenza

Codice: Apache-2.0 ([`LICENSE`](LICENSE), [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt)). Dati derivati, testo e
figure: CC BY 4.0 ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)). I microdati ufficiali di IBGE, DATASUS e TSE
mantengono i propri termini e non vengono ridistribuiti. Vedi [`NOTICE`](NOTICE).
