"""Monta paises.csv (linhas curadas) a partir de: V-Dem v16 (vdemdata), V-Party v2, ILGA DB (GraphQL publico, 2026-10-22),
BRC (dados/ideologia) e uma lista de EVIDENCIAS verbatim. Cada citacao e VERIFICADA contra o arquivo local (falha alto se nao achar)
e a pagina (PDF) e achada automaticamente. Saidas: ../paises.csv e ../verificacao-citacoes.tsv. Requer pyreadr, pandas (venv do scratchpad).
Regras de classificacao: PRE-REGISTRO.md (+ ADENDO). Nada aqui atribui esquerda/direita por julgamento proprio."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, hashlib, html, json, math, os, re, subprocess, sys
import pandas as pd, pyreadr

ROOT = (REPO_ROOT + "/")
F = ROOT + "fontes/q1-textointegral/discurso/governos/"
F8 = ROOT + "fontes/q1-textointegral/F8-literatura/"
OUTD = ROOT + "research-2026-10-21-rodada3/discurso/governos/"

vd = pyreadr.read_r(F + "vdemdata-vdem.RData")["vdem"]
vp = pyreadr.read_r(F + "vdemdata-vparty.RData")["vparty"]
ilga = {}
for e in json.load(open(F + "ilga-db-csssa-all.json"))["data"]["entriesCsssa"]:
    m = e["motherEntry"]
    if not m["subjurisdiction"]:
        ilga[m["jurisdiction"]["name"]] = e
ilga_enf = json.load(open(F + "ilga-db-enforcement-dp-countries.json"))
brc = [r for r in csv.DictReader(open(ROOT + "dados/ideologia/ideologia_partidos_ano.csv")) if r["fonte"] == "BRC"]

ROW = {0: "autocracia fechada", 1: "autocracia eleitoral", 2: "democracia eleitoral", 3: "democracia liberal"}
LEG = ["nacionalista", "socialista/comunista", "restauradora/conservadora", "separatista/autonomista", "religiosa"]
LR = {0: "extrema esquerda", 1: "esquerda", 2: "centro-esquerda", 3: "centro", 4: "centro-direita", 5: "direita", 6: "extrema direita"}
LGBT = {0: "opoe-se fortemente", 1: "opoe-se", 2: "ambigua/sem posicao", 3: "apoia", 4: "apoia fortemente"}


def norm(s):
    s = html.unescape(s)
    s = s.replace("­", "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-").replace("\xa0", " ")
    s = re.sub(r"-\s*\n\s*", "", s)  # hifenizacao de fim de linha
    return re.sub(r"\s+", " ", s).strip()


def strip_html(t, enc="utf-8"):
    if isinstance(t, bytes):
        t = t.decode(enc, "ignore")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<span class=\"replace\" id=\"(\d+)\">\d+</span>", r"[fn\1]", t)
    return norm(re.sub(r"<[^>]+>", " ", t))


_cache = {}


def pages_of(path, kind):
    if path in _cache:
        return _cache[path]
    if kind == "pdf":
        out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout.split("\f")
    elif kind == "pdfraw":
        out = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout.split("\f")
    elif kind == "txt":
        out = open(path, errors="ignore").read().split("\f")
    elif kind == "html":
        b = open(path, "rb").read()
        if b[:2] == b"\x1f\x8b":
            import gzip; b = gzip.decompress(b)
        try:
            b.decode("utf-8"); enc = "utf-8"
        except UnicodeDecodeError:
            enc = "latin1"
        out = [strip_html(b, enc)]
    else:
        raise ValueError(kind)
    out = [norm(p) for p in out]
    _cache[path] = out
    return out


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def ilga_text(country, field):
    if field == "dp":
        return norm(ilga[country]["dp"] or "")
    return strip_html(ilga_enf[country]["enf"]["data"]["enforcement"]["enforcement"])


CHECK = []  # linhas para verificacao-citacoes.tsv


def ev(file, quote, kind="pdf", rowid="", note="", ilga_c=None, ilga_f=None):
    """Retorna string 'arquivo | locator | sha256' depois de verificar a citacao."""
    q = norm(quote)
    if ilga_c:
        txt = ilga_text(ilga_c, ilga_f)
        ok = q in txt
        path = F + ("ilga-db-csssa-all.json" if ilga_f == "dp" else "ilga-db-enforcement-dp-countries.json")
        loc = f"ILGA DB entry id={ilga[ilga_c]['id']} campo {ilga_f}"
    else:
        path = file if file.startswith("/") else F + file
        pgs = pages_of(path, kind)
        hit = [i for i, p in enumerate(pgs, 1) if q in p]
        ok = bool(hit)
        loc = ("PDF p." + str(hit[0])) if (hit and kind != "html") else ("pagina web unica" if hit else "?")
        if kind == "txt" and hit:
            loc = f"OCR/txt p.{hit[0]}"
    CHECK.append((rowid, "OK" if ok else "FALHOU", os.path.basename(path), loc, q[:140]))
    if not ok:
        print("CITACAO NAO ENCONTRADA:", rowid, path, q[:100], file=sys.stderr)
    return f"{os.path.relpath(path, ROOT)} | {loc} | {sha(path)}"


def vdem_row(iso, y):
    r = vd[(vd.country_text_id == iso) & (vd.year == y)]
    return r.iloc[0] if len(r) else None


def regime_txt(iso, y):
    r = vdem_row(iso, y)
    if r is None or pd.isna(r.v2x_regime):
        return "sem_dado"
    return f"{int(r.v2x_regime)} {ROW[int(r.v2x_regime)]} ({y})"


def legit_txt(iso, y):
    r = vdem_row(iso, y)
    if r is None or pd.isna(r.v2exl_legitideolcr_0):
        return "sem_dado"
    fr = ";".join(f"{LEG[i][:5]}={r[f'v2exl_legitideolcr_{i}']:.2f}" for i in range(5))
    return f"{fr} (ideologia oficial intens.={r.v2exl_legitideol:.2f}z, {y})"


def exec_txt(iso, y):
    r = vdem_row(iso, y)
    if r is None or pd.isna(r.v2exnamhos):
        return "sem_dado", ""
    hog = "" if pd.isna(r.v2exnamhog) else f"; HoG {r.v2exnamhog}"
    return f"HoS {r.v2exnamhos} [{r.v2extithos}] partido V-Dem: {r.v2exparhos}{hog} ({y})", str(r.v2exparhos)


def toks(x):
    return {w for w in re.sub(r"[^a-z0-9 ]", " ", str(x).lower()).split() if len(w) > 2}


def vparty_for(iso, y, party_label, overrides=None, cont_override=None):
    """Melhor casamento por tokens do rotulo V-Dem do partido do chefe com um partido V-Party da eleicao mais recente <= y.
    Retorna (nome, ano_eleicao, lr_ord, lgbt_ord, texto, classe)."""
    if str(party_label).lower() in ("technical", "independent", "nan", "", "none"):
        return None
    pv = vp[vp.country_text_id == iso]
    best = None
    for n, g in pv.groupby("v2paenname"):
        sc = len(toks(n) & toks(party_label)) / max(1, len(toks(n) | toks(party_label)))
        if overrides and n in overrides:
            sc = 1.0
        if sc >= 0.5 and (best is None or sc > best[0]):
            best = (sc, n)
    if not best:
        return ("sem_correspondencia_V-Party",)
    g = pv[pv.v2paenname == best[1]].sort_values("year")
    cand = g[g.year <= y]
    row = cand.iloc[-1] if len(cand) else g.iloc[0]  # sem eleicao <= y: primeira disponivel (defasagem declarada)
    ye = int(row.year)
    # continuidade do partido do chefe (V-Dem v2exparhos) entre y e ye
    lo, hi = min(y, ye), max(y, ye)
    labs = vd[(vd.country_text_id == iso) & (vd.year >= lo) & (vd.year <= hi)].v2exparhos.tolist()
    cont = all((isinstance(l, str) and len(toks(l) & toks(party_label)) / max(1, len(toks(l) | toks(party_label))) >= 0.5) for l in labs) if labs else False
    if cont_override is not None:
        cont = cont_override
    lag = abs(y - ye)
    lr = row.v2pariglef_ord; lg = row.v2palgbt_ord
    if pd.isna(lr):
        cls = "nao_classificado(V-Party sem escore)"
    else:
        cls = "esquerda" if lr <= 2 else ("centro" if lr == 3 else "direita")
        if lag > 4 and not cont:
            cls = "nao_classificado(defasado sem continuidade)"
        elif lag > 4:
            cls += "(defasado>4a, partido continuo no V-Dem)"
    cs = row.get("v2paculsup_ord"); rl = row.get("v2parelig_ord")
    cult = (f"; [ADENDO cultural] superioridade-cultural {'NA' if pd.isna(cs) else int(cs)}(0=promove forte..4=opoe forte), religiao-como-justificativa {'NA' if pd.isna(rl) else int(rl)}(0=sempre..4=nunca)")
    txt = (f"V-Party {best[1]} eleicao {ye} (lag {lag}a): econ {'' if pd.isna(lr) else int(lr)}={LR.get(int(lr), '?') if not pd.isna(lr) else 'NA'}; "
           f"LGBT {'' if pd.isna(lg) else int(lg)}={LGBT.get(int(lg), '?') if not pd.isna(lg) else 'NA'}" + cult)
    return (best[1], ye, lr, lg, txt, cls)


def vparty_hog(iso, y):
    """ADENDO A2b: quando o poder efetivo e do chefe de GOVERNO (v2ex_hogw >= 0,5 e v2ex_hosw < 0,5), o partido vem do V-Party
    (pagovsup == 0: 'o chefe de governo pertence a este partido') da eleicao mais recente <= y; continuidade = nome do HoG (V-Dem) constante entre eleicao e y."""
    pv = vp[(vp.country_text_id == iso) & (vp.year <= y) & (vp.v2pagovsup == 0)]
    if not len(pv):
        return ("sem_eleicao_V-Party<=ano",)
    ye = int(pv.year.max()); top = pv[pv.year == ye].sort_values("v2paseatshare", ascending=False).iloc[0]
    nomes = vd[(vd.country_text_id == iso) & (vd.year >= ye) & (vd.year <= y)].v2exnamhog.dropna().unique().tolist()
    cont = len(nomes) == 1
    res = vparty_for(iso, y, top.v2paenname, overrides={top.v2paenname: 1}, cont_override=cont)
    if res and len(res) > 4:
        res = res[:4] + (res[4] + f" [via HoG: pagovsup=0; HoG constante {ye}-{y}: {'sim' if cont else 'nao ('+'; '.join(nomes)+')'}]", res[5])
    return res


def brc_txt(partido, ano):
    for r in brc:
        if r["partido"] == partido and r["ano"] == str(ano):
            e = float(r["escore_0_10"]); cl = "esquerda" if e < 4 else ("centro" if e <= 6 else "direita")
            return f"BRC {partido} {ano} = {e:.2f}/10 (onda {r['onda_origem']}, {r['tipo']}) -> {cl}", cl
    return f"BRC {partido} {ano}: sem escore", "nao_classificado"


ROWS = []


def add(**kw):
    ROWS.append(kw)


UN43 = "onu/A_HRC_43_61.pdf"; UN46 = "onu/A_HRC_46_50.pdf"
LOU = "ilga-laws-on-us-2024.raw.txt"
NEWS26 = "ilga-news-pride-2026.txt"
OSCE = F8 + "osce-moscow-mechanism-chechnya-2018.pdf"; TEDH = F8 + "tedh-lapunov-v-russia-2023.pdf"
CNV = F8 + "cnv-volume2-oficial-site-cnv-via-wayback.pdf"; GARC = F8 + "10.7440_histcrit71.2019.05.pdf"
KOND = F8 + "kondakov-2022-violent-affections-uclpress.pdf"
STEN = ROOT + "fontes/q1-textointegral/entregues-pelo-autor/36_10.1177_10780874251382453_publishedVersion.pdf"
BR = F + "brasil/"; PR = F + "primarias/"


def ilga_pm(c, nat=None):
    e = ilga[c]; v = (e["entry_csssa_death_penalty_value"] or {}).get("name", "")
    return {"Yes": "legal" if not nat else "legal_subnacional", "No legal certainty": "possivel(sem certeza legal)"}.get(v, "nao") + f" [ILGA DB 2026-10-22: {(e['entry_csssa_penalty'] or {}).get('name')}]"


def base(pais, iso, caso, y, uni, **kw):
    ex, plabel = exec_txt(iso, y)
    kw.setdefault("regime", regime_txt(iso, y) + " | atual " + regime_txt(iso, 2025))
    kw.update(pais=pais, iso3=iso, caso=caso, ano_ref=y, universo=uni, executivo=ex, legitimacao_vdem=legit_txt(iso, y), _plabel=plabel)
    return kw


# ---------- U1: pena de morte (ILGA DB) ----------
add(**base("Uganda", "UGA", "Anti-Homosexuality Act 2023 (AHA)", 2023, "U1+U2", pena_morte=ilga_pm("Uganda"), nivel="L2",
    execucoes="E0: nenhuma execucao por atos consensuais achada nas fontes lidas; ILGA conta ~65 casos de aplicacao/alvo estatal 2005-2023 (L3_declarado)",
    fontes=[ev(PR + "uganda-aha-2023-parlamento.ocr.txt", "liable, on conviction, to suffer death", "txt", "UGA"),
            ev(None, "Consensual same-sex sexual acts are punished with the death penalty when", rowid="UGA", ilga_c="Uganda", ilga_f="dp"),
            ev(None, "Almost 65 examples of enforcement or State-backed targeting between 2005 and 2023 were identified by ILGA World", rowid="UGA", ilga_c="Uganda", ilga_f="enf")]))
add(**base("Irã", "IRN", "Código Penal Islâmico: pena de morte prevista", 2023, "U1", pena_morte=ilga_pm("Iran"), nivel="L2 (L3_declarado)",
    execucoes="E1_declarado: IHRDC (1979-81: ~20 de ~760 execucoes por atos entre pessoas do mesmo sexo) e Monash (>=241 entre 1979-2020) via ILGA; ILGA 2020 marca 'executions: YES (UNCLEAR)'; ONU (SR) nao conta execucoes especificas",
    fontes=[ev(UN43, "The death penalty may be applied for example in some cases of adultery, for certain cases of consensual same-sex intercourse between men", "pdf", "IRN"),
            ev(UN46, "The death penalty can be imposed for consensual sexual activity between members of the same sex in the Islamic Republic of Iran", "pdf", "IRN"),
            ev(UN46, "Senior officials describe the community in hateful terms, including by labelling individuals as \"subhuman\" and \"diseased\"", "pdf", "IRN"),
            ev(None, "between 1979 and 1981 nearly 760 people were executed, of whom 20 were killed for engaging in same-sex sexual activity", rowid="IRN", ilga_c="Iran", ilga_f="enf"),
            ev(None, "between 1979 and 2020 at least 241 executions for same-sex sexual conduct took place", rowid="IRN", ilga_c="Iran", ilga_f="enf")]))
add(**base("Arábia Saudita", "SAU", "Sharia (liwat) aplicada pelos tribunais", 2023, "U1", pena_morte=ilga_pm("Saudi Arabia"), nivel="L2 (L3_declarado)",
    execucoes="E1_declarado: 3 homens executados em Asir em 01/01/2002 (comunicado do Min. Interior segundo Amnesty; Embaixada saudita nega motivo); opacidade judicial; ILGA conta >40 casos 2000-2021",
    fontes=[ev(None, "On 1 January 2002, three men in Asir province were executed.", rowid="SAU", ilga_c="Saudi Arabia", ilga_f="enf"),
            ev(None, "ILGA World has identified more than 40 examples of criminal enforcement between 2000 and 2021", rowid="SAU", ilga_c="Saudi Arabia", ilga_f="enf")]))
add(**base("Iêmen", "YEM", "Tribunais huthis (Dhamar/Ibb) 2024; Art. 264", 2023, "U1", pena_morte=ilga_pm("Yemen"), nivel="L3",
    execucoes="E2: autoridade de fato (huthis). 23/01/2024 Dhamar: 9 sentencas de morte (7 apedrejamento, 2 crucificacao); 01/02/2024 Ibb: 13 estudantes condenados a morte (Amnesty). ILGA: >=4 execucoes 2012-14 por milicias. Execucao de 2024 NAO confirmada nas fontes lidas",
    fontes=[ev(PR + "amnesty-yemen-2024-02.html", "On 23 January, the criminal court in Dhamar in northern Yemen sentenced nine individuals to death", "html", "YEM"),
            ev(PR + "amnesty-yemen-2024-02.html", "the court of first instance in Ibb in southern Yemen handed death sentences to 13 students", "html", "YEM"),
            ev(None, "at least four instances of enforcement of the death penalty between 2012 and 2014 by radical religious militia groups", rowid="YEM", ilga_c="Yemen", ilga_f="enf")]))
add(**base("Afeganistão", "AFG", "Talibã (1996-2001 e desde 2021)", 2023, "U1", pena_morte=ilga_pm("Afghanistan"), nivel="L3_declarado",
    execucoes="E1/E2_declarado: 1998 (Kandahar, 3 condenados a morte; Herat, 2 executados por muro derrubado, via radio do Talibã) e relato ILGA 2023-24; juiz talibã disse ao Bild que gays seriam mortos (2021). Fonte primaria da ONU nao localizada nos documentos lidos (A/HRC/53/21 nao cita LGBT)",
    fontes=[ev(None, "In February 1998 three men in Kandahar were sentenced to death by the Taliban", rowid="AFG", ilga_c="Afghanistan", ilga_f="enf"),
            ev(None, "a Taliban judge confirmed to the German newspaper Bild that gay men would be killed under their regime", rowid="AFG", ilga_c="Afghanistan", ilga_f="enf"),
            ev(LOU, "Reports of extreme forms of capital punishment emerged in Afghanistan (death by \"toppling of the wall\")", "txt", "AFG")]))
add(**base("Brunei", "BRN", "Syariah Penal Code Order (art. 82), 2019", 2019, "U1", pena_morte=ilga_pm("Brunei"), nivel="L2",
    execucoes="E0: governo diz moratoria de fato (sem execucoes desde 1996); ILGA nao achou evidencia em contrario; V-Dem nao cobre Brunei",
    fontes=[ev(None, "According to the government, no executions have been carried out since 1996, and ILGA World was unable to identify any evidence to the contrary", rowid="BRN", ilga_c="Brunei", ilga_f="enf"),
            ev(None, "Article 82 of the Syariah Penal Code (2019)", rowid="BRN", ilga_c="Brunei", ilga_f="dp"),
            ev(PR + "muller-2020-brunei-spco-jil.pdf", "Brunei's \"de facto moratorium on the death penalty\" would continue under the SPCO", "pdf", "BRN")]))
add(**base("Mauritânia", "MRT", "Código Penal arts. 306/308", 2023, "U1", pena_morte=ilga_pm("Mauritania"), nivel="L2",
    execucoes="E0: nenhuma execucao achada; ILGA conta >=3 casos de aplicacao 2008-2023",
    fontes=[ev(None, "punishable with death by public stoning", rowid="MRT", ilga_c="Mauritania", ilga_f="dp"),
            ev(None, "at least three distinct examples of criminal enforcement between 2008 and 2023", rowid="MRT", ilga_c="Mauritania", ilga_f="enf")]))
add(**base("Nigéria (12 estados do norte)", "NGA", "Códigos penais da Sharia (nível estadual)", 2023, "U1", pena_morte=ilga_pm("Nigeria", nat=True), nivel="L2 (subnacional)",
    execucoes="E0/raras: 'death sentences have been carried out only rarely' (ILGA); 2020: sentencas reportadas como anuladas em apelacao. Executivo avaliado = federal (Tinubu/APC), NAO os governadores dos estados",
    fontes=[ev(None, "it appears that death sentences have been carried out only rarely", rowid="NGA", ilga_c="Nigeria", ilga_f="enf"),
            ev(None, "The death penalty for consensual same-sex sexual acts legally prescribed in the following 12 provinces", rowid="NGA", ilga_c="Nigeria", ilga_f="dp")]))
add(**base("Paquistão", "PAK", "Hudood/zina (aplicabilidade questionada)", 2023, "U1", pena_morte=ilga_pm("Pakistan"), nivel="L2(incerto)",
    execucoes="E0: nenhuma achada", fontes=[ev(None, "The applicability of this provision to consensual same-sex sexual acts between adults", rowid="PAK", ilga_c="Pakistan", ilga_f="dp")]))
add(**base("Catar", "QAT", "Art. 1 do Código Penal (Sharia/zina)", 2023, "U1", pena_morte=ilga_pm("Qatar"), nivel="L2(incerto)",
    execucoes="E0: nenhuma achada", fontes=[ev(None, "Courts could in theory rely on this provision to impose the death penalty for consensual same-sex sexual acts", rowid="QAT", ilga_c="Qatar", ilga_f="dp")]))
add(**base("Emirados Árabes Unidos", "ARE", "Art. 354 / Sharia (zina)", 2023, "U1", pena_morte=ilga_pm("United Arab Emirates"), nivel="L2(incerto)",
    execucoes="E0: 'ILGA World has found no evidence of such a punishment being meted out in recent years'",
    fontes=[ev(None, "ILGA World has found no evidence of such a punishment being meted out in recent years", rowid="ARE", ilga_c="United Arab Emirates", ilga_f="enf")]))
add(**base("Somália", "SOM", "Sharia acima da Constituição; Al-Shabaab", 2023, "U1", pena_morte=ilga_pm("Somalia"), nivel="L3_declarado",
    execucoes="E2_declarado: Al-Shabaab (2013 apedrejamento; 2017 duas execucoes publicas em Buale, motivo 'atos imorais'); governo central nao controla o territorio",
    fontes=[ev(None, "tried by an Al-Shabaab judge in southern Somalia and found guilty of \"sodomy\"", rowid="SOM", ilga_c="Somalia", ilga_f="enf"),
            ev(None, "executed in public in the town of Buale", rowid="SOM", ilga_c="Somalia", ilga_f="enf")]))

# ---------- U2: leis recentes de repressao ----------
add(**base("Rússia", "RUS", "Corte Suprema declara 'movimento LGBT' extremista (30/11/2023)", 2023, "U2", pena_morte="nao", nivel="LE (restricao de expressao/associacao; extremismo)",
    execucoes="E0 (federal): sem execucoes; ILGA 2026: 'dozens of raids against clubs', acusacoes de extremismo",
    fontes=[ev(LOU, "on 30 November 2023, the Supreme Court handed down a decision where it categorised the \"international LGBT movement\" [sic] as \"extremist\"", "txt", "RUS23"),
            ev(NEWS26, "In Russia , the repression has been escalating since the State declared the LGBTI movement an \"extremist organisation\": authorities conducted dozens of raids against clubs", "txt", "RUS23")]))
add(**base("Rússia/Chechênia", "RUS", "Campanha anti-gay na Chechênia (2017)", 2017, "U2", pena_morte="nao", nivel="L3 (detencao/tortura confirmadas pela OSCE e pelo TEDH); mortes: alegadas",
    execucoes="E3_alegado: OSCE: detencoes e tortura 'confirmadas'; mortes 'allegedly'/'in extreme cases ... killed'; 27 execucoes extrajudiciais de jan/2017 foram de 'presumed jihadists' segundo a ONU (CAT), nao de gays; frase 'exterminated by Ramadan' atribuida a Kadyrov via PACE (nota 33 da OSCE); Russia rejeita o relatorio",
    fontes=[ev(OSCE, "Persons suspected of being homosexuals were picked up without any particular reason", "pdf", "CHE"),
            ev(OSCE, "This demonstrates that the campaign had happened with the support of the state.", "pdf", "CHE"),
            ev(OSCE, "In extreme cases they were raped and killed.", "pdf", "CHE"),
            ev(OSCE, "extrajudicial killings of 27 presumed jihadists in Grozny in 2017", "pdf", "CHE"),
            ev(TEDH, "the applicant has made out a prima facie claim that between 16 and 28 March 2017 he was detained by the police in Grozny and ill-treated", "pdf", "CHE")]))
add(**base("Hungria", "HUN", "Lei de 'proteção da criança' (2021) e proibição da Parada (2025)", 2025, "U2", pena_morte="nao", nivel="LE (restricao de expressao/associacao)",
    execucoes="E0: sem violencia fisica de Estado achada; multas a livrarias (2023) e ameaca de prisoes (ILGA 2026)",
    fontes=[ev(LOU, "Hungarian authorities enforced this law on at least two occasions in May 2023, targeting at least two stores selling books and comics", "txt", "HUN"),
            ev(NEWS26, "Hungary and Slovakia passed constitutional amendments undermining our communities' rights, with the former going as far as banning Pride marches and threatening arrests for defiance", "txt", "HUN")]))
add(**base("Polônia", "POL", "'Zonas livres de LGBT' municipais (2019-20)", 2019, "U2", pena_morte="nao", nivel="LE-local (resolucoes nao vinculantes; 64 unidades locais)",
    execucoes="E0: Stenberg & O'Dwyer: resolucoes sem criminalizacao nem incentivo expresso a ofensas; 'violencia simbolica'. Efeitos em saude (Meyerhoefer) estao no README F8, nao aqui",
    fontes=[ev(STEN, "non-binding resolutions against the spread of gender and LGBT ideology", "pdf", "POL"),
            ev(STEN, "such resolutions were passed in 64 local government units", "pdf", "POL"),
            ev(STEN, "they nevertheless constitute a kind of symbolic violence", "pdf", "POL")]))
add(**base("Iraque", "IRQ", "Lei de 2024 criminaliza atos consensuais", 2024, "U2", pena_morte="nao (pena de morte rejeitada na emenda, segundo ILGA)", nivel="L1",
    execucoes="E0: nenhuma achada",
    fontes=[ev(LOU, "One (1) UN Member State (Iraq) criminalised consensual same-sex sexual acts by law", "txt", "IRQ")]))
add(**base("Burkina Faso", "BFA", "Primeira lei de criminalizacao (2025)", 2025, "U2", pena_morte="nao", nivel="L1",
    execucoes="ND", fontes=[ev(NEWS26, "Burkina Faso introduced such a law for the first time in its history", "txt", "BFA")]))
add(**base("Senegal", "SEN", "Endurecimento da lei (2025-26)", 2025, "U2", pena_morte="nao", nivel="L1 (L3_declarado: 'onda de prisoes e violencia')",
    execucoes="ND", fontes=[ev(NEWS26, "Senegal tightened its criminalising provisions, triggering a wave of arrests and violence across the country", "txt", "SEN")]))
add(**base("Trinidad e Tobago", "TTO", "Tribunal reverte descriminalizacao (2025)", 2025, "U2", pena_morte="nao", nivel="L1",
    execucoes="ND", fontes=[ev(NEWS26, "Trinidad and Tobago reversed its decriminalisation ruling", "txt", "TTO")]))
# ---------- U4: historicos ----------
add(**base("Alemanha nazista", "DEU", "Parágrafo 175 e campos (1933-45)", 1936, "U4", pena_morte="nao (lei); mortes em campos", nivel="L4 PROVISORIO (fonte institucional USHMM; primaria/Q1 pendente)",
    execucoes="E1/E3: 5.000-15.000 homens presos em campos como 'homossexuais' (USHMM, fonte institucional; Q1 pendente: Giles 2002, Lautmann 1981 na fila)",
    fontes=[ev(PR + "ushmm-persecution-of-homosexuals-in-the-third-reich.html", "between 5,000 and 15,000 men were imprisoned in concentration camps as", "html", "DEU"),
            ev(PR + "ushmm-persecution-of-homosexuals-in-the-third-reich.html", "arrested and tried tens of thousands of gay men using Paragraph 175", "html", "DEU")]))
add(**base("Espanha franquista", "ESP", "Lei de Perigosidade e Reabilitação Social (1970)", 1970, "U4", pena_morte="nao (medidas de seguranca)", nivel="L3 (perseguicao de Estado reconhecida em lei de 2022)",
    execucoes="ND (sem contagem de mortes na fonte)",
    fontes=[ev(PR + "boe-ley-20-2022-memoria-democratica.html", "singularizadas en normas como la modificación en 1954 de la Ley de Vagos y Maleantes para incluir a «los homosexuales»", "html", "ESP")]))
add(**base("URSS", "RUS", "Art. 121 do Código Penal (recriminalização em 1934)", 1979, "U4", pena_morte="nao", nivel="L1 documentado (lei de 1934); L3 pendente (fila: Healey 2002)",
    execucoes="ND (prisao; sem contagem de mortes na fonte lida)",
    fontes=[ev(KOND, "same-sex intercourse between men returned to the Criminal Code in 1934 in the form of a ban on buggery", "pdf", "URSS")]))
add(**base("Cuba (UMAP)", "CUB", "Unidades Militares de Ajuda à Produção (1965-68)", 1966, "U4", pena_morte="nao", nivel="L3 (internacao em trabalho agricola)",
    execucoes="ND (sem estatistica de vitimas; nao e extermínio)",
    fontes=[ev(GARC, "es decir, homosexuales, religiosos, sin vínculo estudiantil o laboral, delincuentes y desafectos", "pdf", "CUB")]))
add(**base("Irã pós-1979", "IRN", "Revolução Islâmica: primeiras execuções", 1980, "U4", pena_morte="sim (lei islamica)", nivel="L3_declarado",
    execucoes="E1_declarado: IHRDC via ILGA (20 de ~760 execucoes em 1979-81)",
    fontes=[ev(None, "between 1979 and 1981 nearly 760 people were executed, of whom 20 were killed for engaging in same-sex sexual activity", rowid="IRN80", ilga_c="Iran", ilga_f="enf")]))
add(**base("Brasil, ditadura", "BRA", "Ditadura militar 1964-85 (CNV vol. II)", 1975, "U4+U5", pena_morte="nao", nivel="L3 (perseguicao de Estado; sem politica formal de exterminio)",
    execucoes="E0 (exterminio): CNV: 'Não houve uma política de Estado formalizada ... de exterminar os homossexuais'",
    fontes=[ev(CNV, "Não houve uma política de Estado formalizada e tão coerente no sentido de exterminar os homossexuais", "pdf", "BRA64"),
            ev(CNV, "de 300 a 500 pessoas eram levadas por dia para delegacias", "pdf", "BRA64")]))

# ---------- U5: governos brasileiros ----------
def brasil(nome, y, partido_brc, brc_year, gov_note, nivel, execucoes, fontes, vp_party):
    b, cl = brc_txt(partido_brc, brc_year)
    vpt = vparty_for("BRA", y, vp_party[0], overrides={vp_party[1]: 1})
    vtxt = vpt[4] if vpt and len(vpt) > 4 else "V-Party: n/a"
    add(**base(nome, "BRA", gov_note, y, "U5", pena_morte="nao", nivel=nivel, execucoes=execucoes, fontes=fontes, extra_ideo=f"{b} | {vtxt}", cls_override=cl))

brasil("Brasil: Dilma II", 2016, "PT", 2016, "Dilma 2015-ago/2016: kit anti-homofobia suspenso (2011, governo Dilma I); Decreto 8.727/2016 (nome social)", "T3 (2011) + T4 (2016)",
       "E0: nenhuma perseguicao/execucao por agentes do Estado achada",
       [ev(BR + "exame-dilma-kit-2011.html", "A presidente decidiu suspender esse material e suspender também a distribuição", "html", "BRA-DIL"),
        ev(BR + "planalto-decreto8727-2016.html", "DECRETO Nº 8.727, DE 28 DE ABRIL DE 2016", "html", "BRA-DIL"),
        ev(BR + "aosfatos-temer-zero-homofobia-2017.html", "saíram de R$ 3.061.540,13 em 2008 para R$ 518.565,23 em 2016", "html", "BRA-DIL")],
       ("Workers' Party", "Workers' Party"))
brasil("Brasil: Temer", 2017, "MDB", 2018, "Temer set/2016-2018: repasses LGBT zerados em 2017; Lei 13.502/2017 sem 'LGBT' no rol do MDH", "T3",
       "E0: nenhuma perseguicao/execucao por agentes do Estado achada",
       [ev(BR + "aosfatos-temer-zero-homofobia-2017.html", "O governo do presidente Michel Temer zerou em 2017 os já escassos repasses federais para programas específicos de defesa da comunidade LGBT", "html", "BRA-TEM"),
        ev(BR + "planalto-lei13502-2017.html", "Constitui área de competência do Ministério dos Direitos Humanos: I - formulação, coordenação e execução de políticas e diretrizes voltadas à promoção dos direitos humanos, incluídos: a) direitos da cidadania; b) direitos da criança e do adolescente; c) direitos da pessoa idosa; d) direitos da pessoa com deficiência; e e) direitos das minorias", "html", "BRA-TEM")],
       ("Brazilian Democratic Movement Party", "Partido do Movimento Democrático Brasileiro"))
brasil("Brasil: Bolsonaro", 2019, "PSL", 2019, "Bolsonaro 2019-22: MP 870 (rol sem LGBT, igual a 2017), Dec. 9.883 (conselho), retorica", "T1 + T3 (T2 tambem presente)",
       "E0: nenhuma perseguicao/execucao por agentes do Estado achada; T5/T6 nao documentados no espaco de busca",
       [ev(BR + "congressoemfoco-bolsonaro-mundo-gay-2019.html", "o Brasil não pode ser um país do mundo gay, de turismo gay. Temos famílias", "html", "BRA-BOL"),
        ev(BR + "congressoemfoco-bolsonaro-stf-homofobia-2019-06-14.html", "E essa decisão prejudica os próprios homossexuais", "html", "BRA-BOL"),
        ev(BR + "metropoles-bolsonaro-twitter-minorias-2019-01.html", "Não haverá abandono de auxílio a qualquer indivíduo nas diretrizes de Direitos Humanos", "html", "BRA-BOL"),
        ev(BR + "congressoemfoco-lider-lgbt-damares-2019-01.html", "Teremos um diálogo aberto com a comunidade LGBT. Nenhum direito conquistado pela comunidade LGBT será violado", "html", "BRA-BOL"),
        ev(BR + "planalto-decreto9673-2019.html", "Diretoria de Promoção dos Direitos de L é sbicas, Gays, Bissexuais, Travestis e Transexuais", "html", "BRA-BOL"),
        ev(BR + "planalto-lei13844-2019.html", "Constituem áreas de competência do Ministério da Mulher, da Família e dos Direitos Humanos", "html", "BRA-BOL"),
        ev(BR + "planalto-decreto9883-2019.html", "Dispõe sobre o Conselho Nacional de Combate à Discriminação", "html", "BRA-BOL")],
       ("Social Liberal Party", "Social Liberal Party"))
brasil("Brasil: Lula III", 2023, "PT", 2023, "Lula III 2023-24: Secretaria Nacional LGBTQIA+ (Dec. 11.341), Conselho (Dec. 11.471), Lei 14.600 com LGBTQIA+; verba federal baixa", "T4 (+T3 de execucao orcamentaria, segundo a fonte)",
       "E0: nenhuma perseguicao/execucao por agentes do Estado achada",
       [ev(BR + "planalto-decreto11471-2023.html", "Fica instituído o Conselho Nacional dos Direitos das Pessoas Lésbicas, Gays , Bissexuais, Travestis, Transexuais, Queers , Intersexos, Assexuais e Outras", "html", "BRA-LUL"),
        ev(BR + "planalto-decreto11341-2023.html", "Secretaria Nacional dos Direitos das Pessoas LGBTQIA+", "html", "BRA-LUL"),
        ev(BR + "planalto-lei14600-2023.html", "das pessoas LGBTQIA+", "html", "BRA-LUL"),
        ev(BR + "congressoemfoco-quem-financia-lgbti-2025.html", "Enquanto o Executivo federal destinou apenas R$6,4 milhões para a pauta em 2025", "html", "BRA-LUL")],
       ("Workers' Party", "Workers' Party"))

# ---------- classificacao + saida ----------
OUT = []
for r in ROWS:
    iso, y = r["iso3"], r["ano_ref"]
    ideo, cls = "", ""
    if r.get("extra_ideo"):
        ideo = r["extra_ideo"]; cls = r["cls_override"]
    else:
        pl = r["_plabel"]
        rr = vdem_row(iso, y)
        hosw = None if rr is None else rr.get("v2ex_hosw"); hogw = None if rr is None else rr.get("v2ex_hogw")
        if rr is not None and pd.notna(hogw) and pd.notna(hosw) and hogw >= 0.5 and hosw < 0.5:
            vpt = vparty_hog(iso, y)
        elif rr is not None and pd.notna(hogw) and hogw == 0.5 and hosw == 0.5 and str(pl).lower() not in ("technical", "independent"):
            ideo = f"poder dividido HoS/HoG (0,5/0,5); partido do HoG ausente no V-Dem (HoS: {pl})"; cls = "nao_classificado"; vpt = "FEITO"
        else:
            vpt = vparty_for(iso, y, pl) if pl else None
        if vpt == "FEITO":
            pass
        elif vpt is None:
            ideo = f"nao_aplicavel/sem partido na base (V-Dem v2exparhos='{pl or 'sem_dado'}')"; cls = "nao_aplicavel" if pl else "nao_classificado"
        elif len(vpt) == 1:
            ideo = f"partido '{pl}' sem correspondencia no V-Party v2"; cls = "nao_classificado"
        else:
            ideo = vpt[4]; cls = vpt[5]
    OUT.append(dict(pais=r["pais"], iso3=iso, caso=r["caso"], universo=r["universo"], ano_ref=y, regime_RoW=r["regime"],
                    pena_morte=r["pena_morte"], nivel=r["nivel"], execucoes_documentadas=r["execucoes"], executivo=r["executivo"],
                    ideologia_executivo=ideo, **{"classificacao_eixo(V-Party econ; BRC geral)": cls}, legitimacao_oficial_vdem=r["legitimacao_vdem"],
                    fonte_pagina_sha256=" ;; ".join(r["fontes"])))
with open(OUTD + "paises.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(OUT[0].keys())); w.writeheader(); w.writerows(OUT)
with open(OUTD + "verificacao-citacoes.tsv", "w") as fh:
    fh.write("row\tstatus\tarquivo\tlocator\ttrecho\n")
    for c in CHECK:
        fh.write("\t".join(c) + "\n")
bad = [c for c in CHECK if c[1] != "OK"]
print(len(OUT), "linhas;", len(CHECK), "citacoes;", len(bad), "falharam")
for b in bad:
    print("  FALHOU:", b)
