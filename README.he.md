<div align="center">

# תמותה ואלימות כלפי אנשים להט״ב+ בברזיל: מה הנתונים הציבוריים מאפשרים לנו לטעון

**ביקורת של מקורות ומדדים, 2010–2026**

[English](README.md) · [Português (Brasil)](README.pt-BR.md) · [Español](README.es.md) · [Italiano](README.it.md) · **עברית**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23873858.svg)](https://doi.org/10.5281/zenodo.23873858)
![License: Apache-2.0 (code)](https://img.shields.io/badge/code-Apache--2.0-blue)
![License: CC BY 4.0 (data, text, figures)](https://img.shields.io/badge/data%20%26%20text-CC%20BY%204.0-lightgrey)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![Tests: 182 passing](https://img.shields.io/badge/tests-182_passing-brightgreen)
![Reproducible: SHA-256 chain](https://img.shields.io/badge/reproducible-SHA--256_chain-green)

</div>

<div dir="rtl">

> [!IMPORTANT]
> בסקר הבריאות הלאומי של 2019 דיווחו 14.70% מהמבוגרים הלסביות, ההומואים, הביסקסואלים או בעלי נטייה לא־הטרוסקסואלית
> אחרת (LGB+‎) על אלימות פיזית בשנה הקודמת, לעומת 3.82% מהמבוגרים ההטרוסקסואלים; היחס המתוקנן הוא 2.82 (רווח של 95%,
> 2.16 עד 3.68). רישומי הפטירה בברזיל אינם כוללים לא נטייה מינית ולא זהות מגדרית, ולכן אין שיעור תמותה לאומי של אנשים
> להט״ב+. מתוך 160 מקרים שנדגמו מרשימת Grupo Gay da Bahia לשנת 2019, 50 אומתו על ידי המקור המצוטט (48 מהם בדיווחים
> חדשותיים): הרשימה אינה שיעור ואינה סך כולל, ומקרים שלא אומתו אינם מקרים מומצאים. לאחר 67 החלפות של מפלגת המושל,
> שיעור הרצח במדינה, ביחס לשיעור הארצי, השתנה ב־‎−0.7%‎ (חציון), לעומת ‎+4.6%‎ ללא החלפה; רק ב־21 ההחלפות שאין
> בקרבתן החלפה אחרת הירידה ניכרת (‎−10.2%‎, לעומת ‎+6.7%‎). ההשוואה היא גישושית ומראה צירוף מקרים, לא השפעה של
> הממשלה.

## המאמר

קוראי עברית יכולים להיעזר במהדורה האנגלית:

| מהדורה | קובץ |
|---|---|
| אנגלית | [`docs/paper/paper-final-en.pdf`](docs/paper/paper-final-en.pdf) |
| פורטוגזית (ברזיל), מקור | [`docs/paper/paper-final.pdf`](docs/paper/paper-final.pdf) |

לכל מהדורה DOI משלה, והתוויות באיורים שלה כתובות בשפתה; קוד האיורים ב־`figures/` שומר על התוויות בפורטוגזית של
המחקר. המהדורות בספרדית ובאיטלקית של גרסה v1.2.0 אינן חלק מגרסה זו: הן כוללות שתי קריאות שתוקנו
ב־[`docs/corrections.md`](docs/corrections.md); הן ישובו, כל אחת עם DOI משלה.

## מה יש במאגר הזה

| תיקייה או קובץ | תוכן |
|---|---|
| `data/` | נתונים נגזרים והקוד שמפיק אותם: ניתוח חוזר של הסקר (`pns/`), שיעורי תמותה (`sim/`), דיווחים על אלימות (`sinan/`), תלונות במשטרה (`anuario/`), קו הפניות Disque 100 (`disque100/`), פאנל המושלים (`painel/`, `presidencia/`, `exposicao/`) |
| `analysis/` | שאר הניתוחים שהמאמר נשען עליהם: ביקורת על רשימת Grupo Gay da Bahia (`ggb-audit/`, `ggb-series/`, `counterpoint/`), עוצמה סטטיסטית ועלות של הסקר (`survey-cost/`), סימולציה של יכולת הזיהוי (`simulation/`), שיח ציבורי (`discourse/`), בדיקות חוסן (`robustness/`), ציוני אידאולוגיה (`ideology/`), ספרות (`literature/`, `full-text/`) |
| `figures/` | קוד ונתונים לכל איור (`make_figures.py`, `fontes/` עם הערכים המוצגים) והאיורים של המאמר (`article/`) |
| `preregistrations/` | רישומים מוקדמים עם חותמות הזמן וערכי ה־SHA-256 שלהם, כפי שהם מצוטטים במאמר |
| `sources/` | עותקים של מקורות ציבוריים שהסקריפטים משתמשים בהם (`public/`), פנקסי המקורות (`ledgers/`) ורבעוני כתבי העת |
| `manifest/` | מניפסט המקורות (URL, תאריך גישה, וכאשר נשמר קובץ, SHA-256), המלאי הציבורי וסכומי הביקורת של החותם |
| `docs/` | שחזוריות ומיקום כל תוצאה (`reproducibility-and-result-locations.md`), שימוש במודלי שפה (`language-model-use.md`) ותיקונים (`corrections.md`), באנגלית ובפורטוגזית (`.pt-BR.md`); המאמר (`paper/`) |
| `tests/` | בדיקות שקושרות כל מספר שפורסם לקובץ שהפיק אותו |
| `scripts/` | הורדת המיקרו־נתונים הרשמיים (עם ערך ה־SHA-256 הצפוי), מריץ השחזור והביקורות |
| `run_all.py`, `make_provenance.py`, `output/` | בדיקת שלמות, חישוב מחדש ושרשרת ה־SHA-256 |

מניפסט המקורות (`manifest/MANIFESTO-FONTES.csv`) והמלאי הציבורי (`manifest/INVENTARIO-PUBLICO.md`) מונים 1022 מזהים
מתוך 20 פנקסים; המאגר מכיל 174 סקריפטים. הקוד, ההערות ועמודות הנתונים שומרים על הפורטוגזית המקורית של המחקר.

## איך לבדוק

<div dir="ltr">

```bash
python3 -m pip install -r requirements.txt
python3 -I make_provenance.py --verify     # SHA-256 of every distributed file and the chain hash
python3 -I run_all.py --rapido             # integrity, tests and seal (seconds)
python3 -I run_all.py                      # also recomputes the derived results in a separate copy (minutes)
shasum -a 256 -c docs/paper/SHA256SUMS.txt # the paper PDF
```

</div>

הפלט הצפוי של הפקודה הראשונה:

<div dir="ltr">

```text
provenance verified: <chain hash> (<n> arquivos)
```

</div>

ערך הגיבוב של השרשרת בגרסה זו נמצא ב־[`output/hash-chain.md`](output/hash-chain.md). מה ניתן ומה לא ניתן להריץ מחדש,
ומדוע, מפורט ב־[`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## מה נטען ומה אינו נטען

| נטען | לא נטען |
|---|---|
| מבוגרים LGB+‎ מדווחים על יותר אלימות פיזית, מינית ופסיכולוגית ממבוגרים הטרוסקסואלים (2019) | שהפער הזה מודד אפליה או אורח חיים: הנתונים אינם מפרידים בין השניים |
| אף רישום ציבורי אינו מאפשר שיעור תמותה לאומי של אנשים להט״ב+ | שאנשים להט״ב+ נהרגים, או אינם נהרגים, לעתים קרובות יותר מאחרים |
| תלונות במשטרה, פניות לקו הפניות ודיווחים מודדים רישום | שהאלימות נגד אנשים להט״ב+ עלתה או ירדה תחת ממשלה כלשהי |
| שיעור הרצח במדינה, ביחס לשיעור הארצי, ירד לאחר 21 ההחלפות של מפלגת המושל שאין בקרבתן החלפה אחרת (‎−10.2%‎, לעומת ‎+6.7%‎); השוואה גישושית | שהירידה הזו היא השפעה של הממשלה |
| 50 מתוך 160 המקרים שנדגמו מרשימת 2019 (31.3%) ניתנים לאימות מהמקור שהרשימה עצמה מצטטת | שהרשימה שלמה, או שהיא מומצאת |

## מחבר

Carlos Ulisses Flores · Codex Hash Research Laboratory ·
[ORCID 0000-0002-6034-7765](https://orcid.org/0000-0002-6034-7765) · [ulissesflores.com](https://ulissesflores.com) ·
[Lattes](https://lattes.cnpq.br/6905246706890561)

## ציטוט

<div dir="ltr">

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

</div>

ה־DOI שלמעלה מפנה תמיד לגרסה העדכנית ביותר. ראו גם [`CITATION.cff`](CITATION.cff).

## רישיון

קוד: Apache-2.0 ([`LICENSE`](LICENSE), [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt)). נתונים נגזרים, טקסט
ואיורים: CC BY 4.0 ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)). המיקרו־נתונים הרשמיים של IBGE, DATASUS ו־TSE
כפופים לתנאים שלהם ואינם מופצים מחדש. ראו [`NOTICE`](NOTICE).

</div>
