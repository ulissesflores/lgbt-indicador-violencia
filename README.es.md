<div align="center">

# Mortalidad y violencia contra personas LGBT+ en Brasil: lo que los datos públicos permiten afirmar

**Una auditoría de fuentes e indicadores, 2010–2026**

[English](README.md) · [Português (Brasil)](README.pt-BR.md) · **Español** · [Italiano](README.it.md) · [עברית](README.he.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23873858.svg)](https://doi.org/10.5281/zenodo.23873858)
![License: Apache-2.0 (code)](https://img.shields.io/badge/code-Apache--2.0-blue)
![License: CC BY 4.0 (data, text, figures)](https://img.shields.io/badge/data%20%26%20text-CC%20BY%204.0-lightgrey)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![Reproducible: SHA-256 chain](https://img.shields.io/badge/reproducible-SHA--256_chain-green)

</div>

> [!IMPORTANT]
> En la Encuesta Nacional de Salud de 2019, el 14,70% de los adultos lesbianas, gais, bisexuales u otros no
> heterosexuales (LGB+) declaró violencia física en el año anterior, frente al 3,82% de los adultos heterosexuales; la
> razón ajustada es 2,82 (intervalo del 95%, 2,16 a 3,68). Los registros de defunción brasileños no recogen ni la
> orientación sexual ni la identidad de género, por lo que no existe una tasa nacional de mortalidad LGBT+. De 160 casos
> muestreados de la lista del Grupo Gay da Bahia de 2019, 50 se confirmaron en noticias sobre el propio caso: la lista no
> es ni una tasa ni un total, y los casos no verificados no son casos inventados.

## El artículo

| Idioma | Archivo |
|---|---|
| Portugués (Brasil), original | [`docs/paper/paper-final.pdf`](docs/paper/paper-final.pdf) |
| Inglés, traducción | [`docs/paper/paper-final.en.pdf`](docs/paper/paper-final.en.pdf) |
| Español, traducción | [`docs/paper/paper-final.es.pdf`](docs/paper/paper-final.es.pdf) |
| Italiano, traducción | [`docs/paper/paper-final.it.pdf`](docs/paper/paper-final.it.pdf) |

Las figuras del artículo están en portugués; la nota de cada figura explica sus etiquetas. Los lectores de hebreo cuentan
con la versión en inglés.

## Qué hay en este repositorio

| Carpeta o archivo | Contenido |
|---|---|
| `data/` | Datos derivados y el código que los produce: reanálisis de la encuesta (`pns/`), tasas de mortalidad (`sim/`), notificaciones de violencia (`sinan/`), denuncias policiales (`anuario/`), la línea telefónica Disque 100 (`disque100/`), el panel de gobernadores (`painel/`, `presidencia/`, `exposicao/`) |
| `analysis/` | Los demás análisis en los que se apoya el artículo: auditoría de la lista del Grupo Gay da Bahia (`ggb-audit/`, `ggb-series/`, `counterpoint/`), potencia y costo de la encuesta (`survey-cost/`), simulación de identificabilidad (`simulation/`), discurso público (`discourse/`), pruebas de robustez (`robustness/`), puntuaciones de ideología (`ideology/`), literatura (`literature/`, `full-text/`) |
| `figures/` | Código y datos de cada figura (`make_figures.py`, `fontes/` con los valores representados) y las figuras del artículo (`article/`) |
| `preregistrations/` | Prerregistros con sus marcas de tiempo y SHA-256, tal como se citan en el artículo |
| `sources/` | Copias de fuentes públicas usadas por los scripts (`public/`), los registros de fuentes (`ledgers/`) y los cuartiles de revistas |
| `manifest/` | Manifiesto de fuentes (URL, fecha de acceso y, cuando se guardó un archivo, SHA-256), inventario público y las sumas de verificación del sello |
| `tests/` | Pruebas que vinculan cada número publicado con el archivo que lo produjo |
| `scripts/` | Descarga de los microdatos oficiales (con el SHA-256 esperado), el ejecutor de la reproducción y las auditorías |
| `run_all.py`, `make_provenance.py`, `output/` | Verificación de integridad, recálculo y la cadena SHA-256 |

El manifiesto de fuentes (`manifest/MANIFESTO-FONTES.csv`) y el inventario público (`manifest/INVENTARIO-PUBLICO.md`)
cuentan 1025 identificadores de 20 registros; el repositorio contiene 172 scripts. El código, los comentarios y las
columnas de datos conservan el portugués original del estudio.

## Cómo verificarlo

```bash
python3 -m pip install -r requirements.txt
python3 -I make_provenance.py --verify     # SHA-256 of every distributed file and the chain hash
python3 -I run_all.py --rapido             # integrity, tests and seal (seconds)
python3 -I run_all.py                      # also recomputes the derived results in a separate copy (minutes)
shasum -a 256 -c docs/paper/SHA256SUMS.txt # the paper PDF
```

Salida esperada del primer comando:

```text
provenance verified: <chain hash> (<n> arquivos)
```

El hash de la cadena de esta versión está en [`output/hash-chain.md`](output/hash-chain.md). Qué puede y qué no puede
volver a ejecutarse, y por qué, está en [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Qué se afirma y qué no

| Se afirma | No se afirma |
|---|---|
| Los adultos LGB+ declaran más violencia física, sexual y psicológica que los adultos heterosexuales (2019) | Que esta brecha mida discriminación o estilo de vida: los datos no separan una cosa de la otra |
| Ningún registro público permite una tasa nacional de mortalidad LGBT+ | Que las personas LGBT+ sean o no asesinadas con más frecuencia que otras |
| Las denuncias policiales, las denuncias a la línea telefónica y las notificaciones miden el registro | Que la violencia haya subido o bajado bajo cualquier gobierno |
| 50 de los 160 casos muestreados de la lista de 2019 (31,3%) son verificables a partir de la fuente que la propia lista cita | Que la lista sea completa, o que sea inventada |

## Autor

Carlos Ulisses Flores · Codex Hash Research Laboratory ·
[ORCID 0000-0002-6034-7765](https://orcid.org/0000-0002-6034-7765) · [ulissesflores.com](https://ulissesflores.com) ·
[Lattes](https://lattes.cnpq.br/6905246706890561)

## Cita

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

El DOI anterior siempre resuelve a la versión más reciente. Véase también [`CITATION.cff`](CITATION.cff).

## Licencia

Código: Apache-2.0 ([`LICENSE`](LICENSE), [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt)). Datos derivados, texto y
figuras: CC BY 4.0 ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)). Los microdatos oficiales de IBGE, DATASUS y TSE
conservan sus propios términos y no se redistribuyen. Véase [`NOTICE`](NOTICE).
