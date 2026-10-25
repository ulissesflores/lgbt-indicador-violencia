"""Triangulação PNS 2019 x Sinan VIVA (LGB+ entre vítimas de violência física, adultos) - script gerador COMPLETO.

Substitui o que antes vivia só em dados/sinan/resumo.md (seções 'Denominador só INTERPESSOAL', 'Triangulação PNS x Sinan',
'Sensibilidade') sem script no repositório e com insumos digitados à mão (sensibilidade_pns_sinan.py).
Entrada : fontes/p2-sinan-microdados/VIOLBR23.dbf e VIOLBR24.dbf (convertidos dos .dbc do FTP DATASUS; sha256 em SHA256SUMS.txt).
Saída   : dados/sinan/triangulacao_pns_sinan.md e .csv (arquivos NOVOS; não toca resumo.md).
Rodar   : python  # venv com pyreaddbc + dbfread -I dados/sinan/triangulacao_pns_sinan.py
Definições (fixadas antes de comparar com os números já publicados):
  interpessoal  = LES_AUTOP != '1'
  violência física = VIOL_FISIC == '1'
  adulto        = NU_IDADE_N com unidade '4' (anos) e idade >= 18
  orientação válida = ORIENT_SEX in {1 hetero, 2 homo, 3 bi}; LGB+ = {2,3}; 8 'não se aplica', 9 e vazio = não respondida
  campo 55 'válida' = VIOL_MOTIV fora de {99, vazio, 88}
PNS 2019 (Vasconcelos et al. 2023, Tabelas 1-2, fontes/pns-vasconcelos/vasconcelos.html): prevalências e IC95% copiados abaixo.
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import collections, csv, math, os, random, statistics
from dbfread import DBF

BASE = REPO_ROOT
SRC = f"{BASE}/fontes/p2-sinan-microdados"
OUT = f"{BASE}/dados/sinan"

# --- PNS 2019: (estimativa, IC95% inf, IC95% sup) em % ---
PNS = {
    "lgb": (1.89, 1.73, 2.07), "hetero": (94.75, 94.46, 95.03),            # Tabela 1 (distribuição, adultos 18+)
    "fis_lgb": (14.70, 11.16, 19.12), "fis_het": (3.82, 3.57, 4.09), "fis_total": (4.15, 3.89, 4.42),  # Tabela 2 (violência física, 12 meses)
}

# --- números publicados em dados/sinan/resumo.md (2026-10-12) para o teste de reprodução ---
PUBLICADO = {
    2023: dict(n_interp=405941, f55_ign=29.3, f55_na=14.9, sexismo=20.3, lgbtf=2173, lgbtf_pct=0.54, lgbtf_valid=0.96,
               f36_ign=19.0, f36_na=24.7, homo=1.80, bi=0.67, hb_valid=4.39, f37_ign=26.1, f37_na=72.5, trans=5659, trans_pct=1.39,
               n_fis=197779, o_ign=20.4, o_na=3.9, o_valid=75.7, hb_fis=4.12, hb_fis_n=6169, f55_fis_ign=27.5, f55_fis_na=11.5),
    2024: dict(n_interp=426622, f55_ign=27.7, f55_na=14.8, sexismo=20.4, lgbtf=2264, lgbtf_pct=0.53, lgbtf_valid=0.92,
               f36_ign=18.4, f36_na=25.6, homo=1.74, bi=0.67, hb_valid=4.31, f37_ign=25.7, f37_na=73.0, trans=5716, trans_pct=1.34,
               n_fis=202416, o_ign=20.2, o_na=4.0, o_valid=75.8, hb_fis=4.08, hb_fis_n=6260, f55_fis_ign=27.0, f55_fis_na=11.5),
}


def adulto(idade):
    s = str(idade or "").strip()
    return len(s) == 4 and s[0] == "4" and int(s[1:]) >= 18


def le_ano(ano):
    c = collections.Counter()
    for r in DBF(f"{SRC}/VIOLBR{str(ano)[2:]}.dbf", encoding="latin-1", load=False):
        if str(r.get("LES_AUTOP") or "").strip() == "1":
            continue
        m = str(r.get("VIOL_MOTIV") or "").strip(); o = str(r.get("ORIENT_SEX") or "").strip(); g = str(r.get("IDENT_GEN") or "").strip()
        c["n_interp"] += 1
        c["f55_ign"] += m in ("99", ""); c["f55_na"] += m == "88"; c["sexismo"] += m == "01"; c["lgbtf"] += m == "02"
        c["f55_valid"] += m not in ("99", "", "88")
        c["f36_ign"] += o in ("9", ""); c["f36_na"] += o == "8"; c["homo"] += o == "2"; c["bi"] += o == "3"; c["f36_valid"] += o in ("1", "2", "3")
        c["f37_ign"] += g in ("9", ""); c["f37_na"] += g == "8"; c["trans"] += g in ("1", "2", "3")
        if str(r.get("VIOL_FISIC") or "").strip() == "1" and adulto(r.get("NU_IDADE_N")):
            c["n_fis"] += 1
            c["o_ign"] += o in ("9", ""); c["o_na"] += o == "8"; c["o_valid"] += o in ("1", "2", "3"); c["hb_fis_n"] += o in ("2", "3")
            c["f55_fis_ign"] += m in ("99", ""); c["f55_fis_na"] += m == "88"
    return c


def pct(a, b):
    return 100 * a / b


def metricas(c):
    return dict(n_interp=c["n_interp"], f55_ign=pct(c["f55_ign"], c["n_interp"]), f55_na=pct(c["f55_na"], c["n_interp"]),
                sexismo=pct(c["sexismo"], c["n_interp"]), lgbtf=c["lgbtf"], lgbtf_pct=pct(c["lgbtf"], c["n_interp"]),
                lgbtf_valid=pct(c["lgbtf"], c["f55_valid"]), f36_ign=pct(c["f36_ign"], c["n_interp"]), f36_na=pct(c["f36_na"], c["n_interp"]),
                homo=pct(c["homo"], c["n_interp"]), bi=pct(c["bi"], c["n_interp"]), hb_valid=pct(c["homo"] + c["bi"], c["f36_valid"]),
                f37_ign=pct(c["f37_ign"], c["n_interp"]), f37_na=pct(c["f37_na"], c["n_interp"]), trans=c["trans"], trans_pct=pct(c["trans"], c["n_interp"]),
                n_fis=c["n_fis"], o_ign=pct(c["o_ign"], c["n_fis"]), o_na=pct(c["o_na"], c["n_fis"]), o_valid=pct(c["o_valid"], c["n_fis"]),
                hb_fis=pct(c["hb_fis_n"], c["o_valid"]), hb_fis_n=c["hb_fis_n"],
                f55_fis_ign=pct(c["f55_fis_ign"], c["n_fis"]), f55_fis_na=pct(c["f55_fis_na"], c["n_fis"]))


def pns_implicita(lgb, het, fl, fh):
    """parcela LGB+ entre adultos com violência física: lgb*fl / (lgb*fl + het*fh), tudo em %."""
    return lgb * fl / (lgb * fl + het * fh)


def pns_intervalo(n=200000, seed=20261021):
    """Monte Carlo: cada insumo ~ Normal(log-escala) ajustada ao IC95% publicado; insumos tratados como independentes (hipótese declarada).
    Cenário A (comparável ao Sinan, só orientação válida): lgb*fl / (lgb*fl + het*fh).  Cenário B (denominador antigo, todos os demais = het): (lgb*fl)/(lgb*fl+(100-lgb)*fh)."""
    rnd = random.Random(seed)

    def amostra(est, lo, hi):
        mu, sd = math.log(est), (math.log(hi) - math.log(lo)) / (2 * 1.96)
        return math.exp(rnd.gauss(mu, sd))
    A, B = [], []
    for _ in range(n):
        lgb, het = amostra(*PNS["lgb"]), amostra(*PNS["hetero"])
        fl, fh = amostra(*PNS["fis_lgb"]), amostra(*PNS["fis_het"])
        A.append(pns_implicita(lgb, het, fl, fh)); B.append(pns_implicita(lgb, 100 - lgb, fl, fh))
    q = lambda x: (statistics.quantiles(x, n=40)[0], statistics.median(x), statistics.quantiles(x, n=40)[-1])  # p2,5 / mediana / p97,5
    return q(A), q(B)


def main():
    res = {a: metricas(le_ano(a)) for a in (2023, 2024)}
    L = ["# Triangulação PNS 2019 x Sinan VIVA, adultos 18+, violência física interpessoal (gerado por triangulacao_pns_sinan.py)", ""]
    L += ["## 1. Reprodução dos números já publicados em resumo.md (2026-10-12)", "",
          "| indicador | ano | publicado | recalculado | confere |", "|---|---|---|---|---|"]
    falhas = 0
    for a in (2023, 2024):
        for k, pub in PUBLICADO[a].items():
            val = res[a][k]
            ok = (val == pub) if isinstance(pub, int) else abs(val - pub) <= 0.051  # percentuais publicados com 1 decimal (0,01 p.p. p/ lgbtf_pct/hb)
            if isinstance(pub, float) and pub < 10 and k not in ("o_na", "f55_fis_na"):
                ok = abs(val - pub) <= 0.0051
            falhas += (not ok)
            L.append(f"| {k} | {a} | {pub} | {val:.2f} | {'sim' if ok else '**NÃO**'} |" if not isinstance(val, int) else f"| {k} | {a} | {pub} | {val} | {'sim' if ok else '**NÃO**'} |")
    L.append(f"\nDivergências: {falhas}.\n")

    p_exato = pns_implicita(*[PNS[k][0] for k in ("lgb", "hetero", "fis_lgb", "fis_het")])
    p_antigo = pns_implicita(1.89, 98.11, 14.70, 3.82)
    (a_lo, a_md, a_hi), (b_lo, b_md, b_hi) = pns_intervalo()
    L += ["## 2. PNS 2019: parcela LGB+ implícita entre adultos com violência física (12 meses)", "",
          "| cenário | estimativa pontual | IC95% (Monte Carlo, 200 mil sorteios) |", "|---|---|---|",
          f"| B. denominador antigo do dossiê (todos os não-LGB+ com a taxa dos heterossexuais) | {100*p_antigo:.2f}% | {100*b_lo:.2f}% a {100*b_hi:.2f}% |",
          f"| A. só respondentes de orientação válida (hetero + LGB+), comparável ao Sinan | {100*p_exato:.2f}% | {100*a_lo:.2f}% a {100*a_hi:.2f}% |",
          "", "Insumos (PNS, % e IC95%): " + "; ".join(f"{k} {v[0]} ({v[1]}-{v[2]})" for k, v in PNS.items()) +
          ". Insumos independentes entre si (hipótese; a PNS é uma só amostra, a covariância não é publicada, logo o intervalo é aproximado).", ""]

    L += ["## 3. Sinan: parcela LGB+ entre notificações de violência física de adultos, e razão com a PNS", "",
          "| ano | n | orientação válida | LGB+ entre válidas | razão Sinan/PNS(A) | cenário MCAR | pior caso (0% LGB+ entre não respondidas) | melhor caso (100%) |", "|---|---|---|---|---|---|---|---|"]
    linhas_csv = []
    for a in (2023, 2024):
        m = res[a]; v = m["o_valid"] / 100; hb = m["hb_fis"] / 100; nr = 1 - v
        pior, melhor = v * hb, v * hb + nr
        L.append(f"| {a} | {m['n_fis']:,} | {m['o_valid']:.1f}% | {m['hb_fis']:.2f}% | {m['hb_fis']/(100*p_exato):.2f} | {m['hb_fis']:.2f}% | {100*pior:.2f}% | {100*melhor:.2f}% |")
        # parcela necessária entre não respondidas para igualar a PNS(A)
        nec = (p_exato - v * hb) / nr
        linhas_csv.append([a, m["n_fis"], round(m["o_valid"], 2), round(m["hb_fis"], 3), round(100 * p_exato, 3), round(100 * nec, 2)])
        L.append(f"|  | para igualar a PNS(A), as {100*nr:.1f}% não respondidas precisariam ter {100*nec:.1f}% LGB+ | | | | | | |")
    L += ["", "Leitura: ver dossiê. O Sinan é registro da população que procurou serviço de saúde, não amostra; por isso não se atribui IC amostral à parcela do Sinan (é contagem de notificações, não estimativa). "
          "A comparação de interesse é a razão em relação à prevalência populacional (LGB+ = 1,89% de todos os adultos; 1,96% entre os que responderam hetero/LGB+).", ""]
    open(f"{OUT}/triangulacao_pns_sinan.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    with open(f"{OUT}/triangulacao_pns_sinan.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["ano", "n_fisica_adultos", "pct_orient_valida", "pct_lgb_entre_validas_sinan", "pct_lgb_implicito_pns_cenarioA", "pct_lgb_necessaria_entre_nao_respondidas"]); w.writerows(linhas_csv)
    print("\n".join(L))
    return falhas


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
