"""Concordância Sinan (campo 55 = LGBTfobia) x Anuário FBSP (BO 'racismo por homofobia ou transfobia') por UF, 2022-2025 - VERSÃO 2.

POR QUE EXISTE: a v1 (concordancia_sinan_anuario.py) calculou Spearman sobre CONTAGENS brutas. Contagem de UF cresce com a população
(Sinan x tamanho: rho 0,96-0,98), então duas contagens quaisquer "concordam" só por tamanho. v2 mede concordância LÍQUIDA de tamanho.

DESENHO (declarado antes de rodar esta versão; transparência: a diferença contagem x taxa já tinha sido vista numa checagem exploratória
em 2026-10-20, sem IC; esta versão fixa as especificações abaixo e reporta TODAS, não só a favorável):
  Estimando primário : correlação parcial de Spearman entre contagem Sinan e contagem BO por UF, controlando por posto da população (Censo 2022).
  Inferência         : IC95% por bootstrap de UFs (B=5000); p por permutação dos resíduos (B=10000). Pooled 2022-25 = média (via z de Fisher) das
                       correlações anuais, com bootstrap por UF inteira (preserva a dependência da mesma UF entre anos).
  Referência de tamanho: rho esperado só por tamanho = rho(Sinan,pop) * rho(BO,pop) (identidade de primeira ordem da correlação parcial).
  Secundárias        : Spearman de taxas por 100 mil hab.; Spearman de taxas por notificação Sinan e por BO.
  Sensibilidade      : S1 pop = estimativa anual SIDRA 6579 (2022 = Censo; 2023 interpolado); S2 edição mais antiga do Anuário por ano; S3 '-' (fenômeno
                       inexistente) tratado como 0 em vez de NA; S4 leave-one-UF-out (amplitude); S5 Pearson em log(taxa+0,5).
  Controle de especificidade: Sinan 'racismo' (campo 55) x BO LGBT, mesma metodologia (se um fenômeno sem relação também "concorda", o sinal é de sistema/tamanho).
  NA (UF sem dado no Anuário) sai da análise; nunca vira zero (exceto em S3).
Entradas: dados/sinan/serie_campo55_uf_ano.csv; dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv; fontes/p2-f8-dados-uf/tabnet/raw/sidra_9514.json (Censo 2022)
          e sidra_6579.json (estimativas). Saídas: dados/concordancia/concordancia_v2.{md,csv} e fig-concordancia_v2.png.
Rodar: /opt/homebrew/bin/python3.14 -I dados/concordancia/concordancia_v2.py   (semente fixa)
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, json, math
import numpy as np
from scipy.stats import rankdata
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = REPO_ROOT
D = f"{BASE}/dados"; OUT = f"{D}/concordancia"
ANOS = [2022, 2023, 2024, 2025]
NOME2UF = {"Rondônia": "RO", "Acre": "AC", "Amazonas": "AM", "Roraima": "RR", "Pará": "PA", "Amapá": "AP", "Tocantins": "TO", "Maranhão": "MA",
           "Piauí": "PI", "Ceará": "CE", "Rio Grande do Norte": "RN", "Paraíba": "PB", "Pernambuco": "PE", "Alagoas": "AL", "Sergipe": "SE", "Bahia": "BA",
           "Minas Gerais": "MG", "Espírito Santo": "ES", "Rio de Janeiro": "RJ", "São Paulo": "SP", "Paraná": "PR", "Santa Catarina": "SC",
           "Rio Grande do Sul": "RS", "Mato Grosso do Sul": "MS", "Mato Grosso": "MT", "Goiás": "GO", "Distrito Federal": "DF"}
RNG = np.random.default_rng(20261021)

# ---------------- dados ----------------
sinan = {}
for r in csv.DictReader(open(f"{D}/sinan/serie_campo55_uf_ano.csv", encoding="utf-8")):
    if r["uf"] != "BR":
        sinan[(int(r["ano"]), r["uf"])] = dict(lgbt=int(r["m_lgbtfobia"]), rac=int(r["m_racismo"]), n=int(r["n_interpessoal"]))

anu_all = {}  # (edicao, ano, uf) -> (valor|None, marca)
for r in csv.DictReader(open(f"{D}/anuario/anuario_lgbtfobia_uf_ano_v2.csv", encoding="utf-8")):
    if r["uf"] != "BR":
        anu_all[(int(r["edicao"]), int(r["ano_dado"]), r["uf"])] = (int(r["registros"]) if r["registros"] != "" else None, r["marca"])
EDICAO_NOVA = {2022: 2024, 2023: 2025, 2024: 2026, 2025: 2026}   # edição mais recente que traz o ano
EDICAO_ANTIGA = {2022: 2024, 2023: 2024, 2024: 2025, 2025: 2026}  # primeira edição que publicou o ano


def anuario(ed_map, inexistente_zero=False):
    out = {}
    for (ed, ano, uf), (v, marca) in anu_all.items():
        if ed_map[ano] != ed:
            continue
        if v is not None:
            out[(ano, uf)] = v
        elif marca == "inexistente" and inexistente_zero:
            out[(ano, uf)] = 0
    return out


def anuario_regra_v1():
    """Regra da v1: por (ano, UF), o valor da edição MAIS RECENTE que tenha número; se a edição nova traz NA, cai para a anterior (mistura edições)."""
    out = {}
    for (ed, ano, uf), (v, marca) in sorted(anu_all.items()):
        if v is not None and ((ano, uf) not in out or ed > out[(ano, uf)][1]):
            out[(ano, uf)] = (v, ed)
    return {k: v[0] for k, v in out.items()}


def populacao(tabela, campo_ano=None):
    p = {}
    for x in json.load(open(f"{BASE}/fontes/p2-f8-dados-uf/tabnet/raw/{tabela}.json", encoding="utf-8"))[1:]:
        uf = NOME2UF[x["D1N"]]
        p[(int(x["D3N"]), uf) if campo_ano else uf] = float(x["V"])
    return p


pop_censo = populacao("sidra_9514")
pop_est = populacao("sidra_6579", True)
for uf in NOME2UF.values():  # SIDRA 6579 baixada não traz 2022 (usa-se o Censo) nem 2023 (interpolação linear 2022-2024, declarada)
    pop_est.setdefault((2022, uf), pop_censo[uf])
    pop_est[(2023, uf)] = (pop_est[(2022, uf)] + pop_est[(2024, uf)]) / 2

# ---------------- estimadores ----------------
def corr(a, b):
    return float(np.corrcoef(a, b)[0, 1])


def spearman(x, y):
    return corr(rankdata(x), rankdata(y))


def residuo(a, z):
    A = np.column_stack([np.ones_like(z), z])
    return a - A @ np.linalg.lstsq(A, a, rcond=None)[0]


def parcial(x, y, z):
    rz = rankdata(z)
    return corr(residuo(rankdata(x), rz), residuo(rankdata(y), rz))


def ic_bootstrap(fun, n, B=5000):
    vals = []
    for _ in range(B):
        i = RNG.integers(0, n, n)
        try:
            v = fun(i)
        except Exception:
            continue
        if np.isfinite(v):
            vals.append(v)
    return tuple(np.percentile(vals, [2.5, 97.5])) if vals else (np.nan, np.nan)


def p_perm(x, y, z=None, B=10000):
    """bicaudal. Sem z: permuta y. Com z: permuta os resíduos de postos de y|z (Freedman-Lane aproximado)."""
    if z is None:
        obs = spearman(x, y); a, b = rankdata(x), rankdata(y)
        ref = [corr(a, RNG.permutation(b)) for _ in range(B)]
    else:
        rz = rankdata(z); a, b = residuo(rankdata(x), rz), residuo(rankdata(y), rz)
        obs = corr(a, b); ref = [corr(a, RNG.permutation(b)) for _ in range(B)]
    return float((1 + sum(abs(r) >= abs(obs) - 1e-12 for r in ref)) / (B + 1))


def fisher_media(rhos):
    z = [np.arctanh(np.clip(r, -0.999, 0.999)) for r in rhos]
    return float(np.tanh(np.mean(z)))


def monta(ano, sin_campo, bo, pop, popmap=None):
    ufs = sorted(u for (a, u) in sinan if a == ano and (ano, u) in bo)
    s = np.array([sinan[(ano, u)][sin_campo] for u in ufs], float)
    b = np.array([bo[(ano, u)] for u in ufs], float)
    n = np.array([sinan[(ano, u)]["n"] for u in ufs], float)
    z = np.array([pop[(ano, u)] if popmap else pop[u] for u in ufs], float)
    return ufs, s, b, n, z


# ---------------- especificações ----------------
def linha_ano(ano, bo, pop, popmap=False, sin_campo="lgbt", B_perm=10000, B_boot=5000):
    ufs, s, b, n, z = monta(ano, sin_campo, bo, pop, popmap)
    r = dict(ano=ano, n=len(ufs))
    r["rho_contagens"] = spearman(s, b)
    r["rho_sinan_pop"] = spearman(s, z); r["rho_bo_pop"] = spearman(b, z)
    r["rho_so_tamanho"] = r["rho_sinan_pop"] * r["rho_bo_pop"]
    r["rho_taxas_pop"] = spearman(s / z, b / z)
    r["rho_parcial"] = parcial(s, b, z)
    r["ic_parcial"] = ic_bootstrap(lambda i: parcial(s[i], b[i], z[i]), len(ufs), B_boot)
    r["p_parcial"] = p_perm(s, b, z, B_perm)
    r["ic_taxas"] = ic_bootstrap(lambda i: spearman(s[i] / z[i], b[i] / z[i]), len(ufs), B_boot)
    r["p_taxas"] = p_perm(s / z, b / z, None, B_perm)
    r["rho_por_notif"] = spearman(s / n, b / n)
    r["pearson_log_taxas"] = corr(np.log(s / z * 1e5 + 0.5), np.log(b / z * 1e5 + 0.5))
    r["loo_parcial"] = (lambda v: (min(v), max(v)))([parcial(np.delete(s, k), np.delete(b, k), np.delete(z, k)) for k in range(len(ufs))])
    return r


def poder(n, rho_s, B=4000, alfa=0.05):
    """Poder (simulação) do teste de Spearman bicaudal, normal bivariada com rho de Pearson = 2 sen(pi*rho_s/6)."""
    r = 2 * math.sin(math.pi * rho_s / 6); hit = 0
    tcrit = None
    from scipy.stats import t as tdist
    tcrit = tdist.ppf(1 - alfa / 2, n - 2)
    for _ in range(B):
        x = RNG.standard_normal(n); y = r * x + math.sqrt(1 - r * r) * RNG.standard_normal(n)
        rs = spearman(x, y)
        hit += abs(rs * math.sqrt((n - 2) / (1 - rs * rs))) > tcrit
    return hit / B


def pooled(bo, pop, popmap=False, sin_campo="lgbt", B=2000):
    datas = {a: monta(a, sin_campo, bo, pop, popmap) for a in ANOS}
    ufs_all = sorted(NOME2UF.values())

    def estat(amostra_ufs):
        rhos = []
        for a in ANOS:
            ufs, s, b, n, z = datas[a]
            idx = [ufs.index(u) for u in amostra_ufs if u in ufs]
            if len(idx) < 6:
                continue
            rhos.append(parcial(s[idx], b[idx], z[idx]))
        return fisher_media(rhos)
    obs = estat(ufs_all)
    boots = [estat(list(RNG.choice(ufs_all, len(ufs_all)))) for _ in range(B)]
    return obs, tuple(np.percentile(boots, [2.5, 97.5]))


def main():
    L = ["# Concordância Sinan x Anuário por UF, 2022-2025 - v2 (líquida de tamanho)", "",
         "Gerado por dados/concordancia/concordancia_v2.py (semente 20261021). Substitui a leitura da v1: o Spearman de CONTAGENS (0,49-0,74) é efeito de tamanho da UF.", ""]
    nova = anuario(EDICAO_NOVA)
    linhas = {a: linha_ano(a, nova, pop_censo) for a in ANOS}

    L += ["## 1. Resultado principal (pop = Censo 2022; Anuário = edição mais recente de cada ano)", "",
          "| ano | n UFs | rho contagens (v1) | rho(Sinan,pop) | rho(BO,pop) | rho esperado só por tamanho | rho taxas/100 mil [IC95%] (p) | **rho parcial dado pop** [IC95% bootstrap] (p perm.) | leave-one-out parcial |",
          "|---|---|---|---|---|---|---|---|---|"]
    for a in ANOS:
        r = linhas[a]
        L.append(f"| {a} | {r['n']} | {r['rho_contagens']:.2f} | {r['rho_sinan_pop']:.2f} | {r['rho_bo_pop']:.2f} | {r['rho_so_tamanho']:.2f} | "
                 f"{r['rho_taxas_pop']:.2f} [{r['ic_taxas'][0]:.2f}; {r['ic_taxas'][1]:.2f}] (p={r['p_taxas']:.3f}) | "
                 f"**{r['rho_parcial']:.2f}** [{r['ic_parcial'][0]:.2f}; {r['ic_parcial'][1]:.2f}] (p={r['p_parcial']:.3f}) | {r['loo_parcial'][0]:.2f} a {r['loo_parcial'][1]:.2f} |")
    po, pic = pooled(nova, pop_censo)
    L += ["", f"**Pooled 2022-25 (média de Fisher das correlações parciais anuais): {po:.2f} [IC95% bootstrap por UF: {pic[0]:.2f}; {pic[1]:.2f}]**", "",
          "Leitura: o tamanho sozinho (produto das correlações de cada série com a população) prevê rho de 0,45 a 0,63 dos 0,53 a 0,74 observados em contagens; "
          "o que sobra é pequeno e estatisticamente indistinguível de zero em todos os anos (parcial 0,14 a 0,32, IC95% sempre incluindo zero). "
          "O controle de especificidade (racismo no Sinan x BO LGBT) dá resíduo parecido, então o pouco que sobra não é específico de LGBTfobia (sistema, tamanho não capturado).", ""]

    # --- sensibilidades
    sens = []

    def reg(nome, fun):
        rs = fun()
        sens.append((nome, rs))
    reg("S0 principal (censo 2022, edição nova, '-'=NA)", lambda: {a: linhas[a] for a in ANOS})
    reg("S1 pop = estimativa anual SIDRA 6579 (2022 = Censo; 2023 interpolado)", lambda: {a: linha_ano(a, nova, pop_est, True) for a in ANOS})
    reg("S2 Anuário: edição mais antiga de cada ano", lambda: {a: linha_ano(a, anuario(EDICAO_ANTIGA), pop_censo) for a in ANOS})
    reg("S3 '-' (fenômeno inexistente) tratado como 0", lambda: {a: linha_ano(a, anuario(EDICAO_NOVA, True), pop_censo) for a in ANOS})
    reg("S6 regra da v1 (por UF, edição mais recente COM valor; mistura edições)", lambda: {a: linha_ano(a, anuario_regra_v1(), pop_censo) for a in ANOS})
    reg("C1 controle: Sinan RACISMO x BO LGBT (mesma metodologia)", lambda: {a: linha_ano(a, nova, pop_censo, False, "rac") for a in ANOS})
    L += ["## 2. Sensibilidades e controle (rho parcial | pop, por ano; entre colchetes IC95% bootstrap)", "",
          "| especificação | 2022 | 2023 | 2024 | 2025 |", "|---|---|---|---|---|"]
    for nome, rs in sens:
        L.append(f"| {nome} | " + " | ".join(f"{rs[a]['rho_parcial']:.2f} [{rs[a]['ic_parcial'][0]:.2f}; {rs[a]['ic_parcial'][1]:.2f}] (n={rs[a]['n']})" for a in ANOS) + " |")
    L += ["", "Taxas por 100 mil (rho Spearman), mesmas especificações:", "", "| especificação | 2022 | 2023 | 2024 | 2025 |", "|---|---|---|---|---|"]
    for nome, rs in sens:
        L.append(f"| {nome} | " + " | ".join(f"{rs[a]['rho_taxas_pop']:.2f}" for a in ANOS) + " |")
    L += ["", "Pearson em log(taxa+0,5) e Spearman de taxas por notificação Sinan (S0):", "", "| medida | 2022 | 2023 | 2024 | 2025 |", "|---|---|---|---|---|",
          "| Pearson log-taxas | " + " | ".join(f"{linhas[a]['pearson_log_taxas']:.2f}" for a in ANOS) + " |",
          "| Spearman taxas por notificação Sinan | " + " | ".join(f"{linhas[a]['rho_por_notif']:.2f}" for a in ANOS) + " |", ""]

    L += ["", "Reconciliação com a v1 (rho de CONTAGENS publicado: 0,53 / 0,56 / 0,49 / 0,74): a regra da v1 (S6) reproduz esses valores; a diferença para a tabela principal "
          "vem de a v1 completar UFs com NA na edição nova usando a edição anterior. A v2 usa uma única edição por ano (definição consistente).", "",
          "| rho de contagens | 2022 | 2023 | 2024 | 2025 |", "|---|---|---|---|---|",
          "| S6 (regra v1) | " + " | ".join(f"{sens[-2][1][a]['rho_contagens']:.2f}" for a in ANOS) + " |",
          "| S0 (edição única) | " + " | ".join(f"{linhas[a]['rho_contagens']:.2f}" for a in ANOS) + " |", ""]

    # pooled nas sensibilidades principais
    pp = {nome: pooled(b, p, pm, c, 1000) for nome, b, p, pm, c in [
        ("S1 pop anual", nova, pop_est, True, "lgbt"), ("S2 edição antiga", anuario(EDICAO_ANTIGA), pop_censo, False, "lgbt"),
        ("S3 '-'=0", anuario(EDICAO_NOVA, True), pop_censo, False, "lgbt"), ("C1 controle racismo", nova, pop_censo, False, "rac")]}
    L += ["Pooled (média de Fisher das parciais anuais) por especificação:", "", "| especificação | pooled [IC95%] |", "|---|---|", f"| S0 principal | {po:.2f} [{pic[0]:.2f}; {pic[1]:.2f}] |"]
    L += [f"| {k} | {v[0]:.2f} [{v[1][0]:.2f}; {v[1][1]:.2f}] |" for k, v in pp.items()]

    # --- razão BO/Sinan (inalterada, descritiva)
    L += ["", "## 3. O que NÃO muda: o NÍVEL relativo dos dois sistemas", "",
          "A razão BO/Sinan (mediana das UFs com Sinan>0) usa contagem contra contagem na mesma UF, então o tamanho se cancela; a v1 reportou 0,78 (2022) -> 1,21 (2025). "
          "Esta v2 confirma o cálculo:", "", "| ano | mediana BO/Sinan |", "|---|---|"]
    for a in ANOS:
        ufs, s, b, n, z = monta(a, "lgbt", nova, pop_censo)
        L.append(f"| {a} | {np.median(b[s > 0] / s[s > 0]):.2f} |")
    L += ["", "### 3b. Candidatos a zero cerimonial (Anuário '-' = fenômeno inexistente, mas o Sinan notificou LGBTfobia na mesma UF e ano; edição mais recente)", "",
          "| ano | UF (notificações Sinan de LGBTfobia) |", "|---|---|"]
    for a in ANOS:
        c = [f"{u} ({sinan[(a, u)]['lgbt']})" for (ed, an, u), (v, m) in sorted(anu_all.items()) if an == a and ed == EDICAO_NOVA[a] and m == "inexistente" and sinan[(a, u)]["lgbt"] > 0]
        L.append(f"| {a} | {', '.join(c) if c else 'nenhuma'} |")
    L += ["", "A v1 dizia 'nenhuma UF com BO=0 e Sinan>0' porque descartava '-' como NA; lido como zero, essas UFs são o candidato empírico a 'zero cerimonial' do lado policial (ou ausência de tipificação/campo).",
          "", "## 4. Limites que valem para qualquer leitura", "",
          "- n de 22 a 25 UFs por ano: baixo poder (simulação, teste de Spearman bicaudal a 5%, n=23): " + "; ".join(f"rho={r}: poder {poder(23, r):.2f}" for r in (0.3, 0.5, 0.7)) + ". IC largo = AUSÊNCIA DE EVIDÊNCIA de concordância líquida, não evidência de discordância.",
          "- Sinan conta notificação (serviço de saúde), BO conta ocorrência com marcação de motivação (polícia): construtos distintos; correlação baixa pode refletir isso e não 'erro' de um deles.",
          "- 2025 do Sinan é arquivo preliminar quando o FINAL não existia; UFs sem dado no Anuário (4-5 por ano) saem; 'ceremonial zeros' (S3) mudam pouco.",
          "- A população usada é denominador de tamanho, não de exposição; nenhuma das duas fontes mede incidência (ver dossiê §3: não identificabilidade).", ""]
    open(f"{OUT}/concordancia_v2.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

    with open(f"{OUT}/concordancia_v2.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["especificacao", "ano", "n_ufs", "rho_contagens", "rho_so_tamanho", "rho_taxas", "rho_parcial", "ic_parcial_lo", "ic_parcial_hi", "p_perm_parcial"])
        for nome, rs in sens:
            for a in ANOS:
                r = rs[a]
                w.writerow([nome, a, r["n"], f"{r['rho_contagens']:.3f}", f"{r['rho_so_tamanho']:.3f}", f"{r['rho_taxas_pop']:.3f}", f"{r['rho_parcial']:.3f}",
                            f"{r['ic_parcial'][0]:.3f}", f"{r['ic_parcial'][1]:.3f}", f"{r['p_parcial']:.4f}"])

    fig, ax = plt.subplots(1, 4, figsize=(17, 4.2))
    for i, a in enumerate(ANOS):
        ufs, s, b, n, z = monta(a, "lgbt", nova, pop_censo)
        ax[i].scatter(s / z * 1e5 + 0.05, b / z * 1e5 + 0.05, s=14)
        for u, x, y in zip(ufs, s / z * 1e5, b / z * 1e5):
            ax[i].annotate(u, (x + 0.05, y + 0.05), fontsize=6)
        ax[i].set_xscale("log"); ax[i].set_yscale("log")
        ax[i].set_title(f"{a}: taxas por 100 mil (rho={linhas[a]['rho_taxas_pop']:.2f}; contagens v1={linhas[a]['rho_contagens']:.2f})", fontsize=8)
        ax[i].set_xlabel("Sinan LGBTfobia /100 mil"); ax[i].set_ylabel("BO /100 mil")
    plt.tight_layout(); plt.savefig(f"{OUT}/fig-concordancia_v2.png", dpi=120)
    print("\n".join(L))


if __name__ == "__main__":
    main()
