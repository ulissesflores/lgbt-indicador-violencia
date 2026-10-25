"""R6 (v0.3, 2026-10-24) — IC95% por INVERSÃO do teste wild-cluster bootstrap-t para os 6 desfechos do painel de governadores.
Forma pré-registrada ANTES deste script: dados/painel/R6-PREREGISTRO-FORMA.md (sha256 e hora UTC em R6-PREREGISTRO-FORMA.sha256; o script confere o hash).
Modelo idêntico ao painel principal: ln(taxa) = b x ideologia + EF(UF) + EF(ano), EP CR1 agrupado por UF (G = 27), funções importadas de painel_diagnosticos.py
sem alterá-lo. Não substitui nada: o IC normal publicado (b ± 1,96 EP) fica ao lado do invertido e do t(26).
Álgebra (FWL): com u = M(y - b0 x) e pesos w por UF, M y* = b0 xt + M(u w); como u = yt - b0 xt, M(u w) = M(yt w) - b0 M(xt w): as duas matrizes B x n
são calculadas uma vez por desfecho e cada b0 custa O(B x G). Pesos Rademacher iguais para todos os b0 do desfecho (números aleatórios comuns).
Rodar: /opt/homebrew/bin/python3.14 -I dados/painel/painel_r6_ic_wild_invertido.py   Saídas: dados/painel/r6_ic_wild_invertido.csv e .md"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, hashlib, importlib.util, math
from pathlib import Path
import numpy as np

AQUI = Path((REPO_ROOT + "/dados/painel"))
spec = importlib.util.spec_from_file_location("pdg", AQUI / "painel_diagnosticos.py")
pdg = importlib.util.module_from_spec(spec); spec.loader.exec_module(pdg)

# ---- o pré-registro de forma tem de estar intacto
pre = (AQUI / "R6-PREREGISTRO-FORMA.sha256").read_text(encoding="utf-8").split()[0]
assert hashlib.sha256((AQUI / "R6-PREREGISTRO-FORMA.md").read_bytes()).hexdigest() == pre, "pré-registro alterado"

B, SEMENTE, ALFA, K = 9999, 20261024, 0.05, 5
GRUPOS = [("total", "tx_total"), ("homens", "tx_homens"), ("mulheres", "tx_mulheres"), ("negros", "tx_negros"), ("nao_negros", "tx_nao_negros"), ("arma", "tx_arma")]
rows0 = pdg.carrega("painel_uf_ano_tse_brc.csv")
assert len(rows0) == 351
pub = {r["grupo"]: r for r in csv.DictReader(open(AQUI / "c02_indet_resultados.csv", encoding="utf-8")) if r["desfecho"] == "registrado_ln"}
RNG = np.random.default_rng(SEMENTE)


def t_quantil(q, nu):
    """quantil da t de Student por bisseção sobre a CDF integrada numericamente (Simpson, 20.000 intervalos): sem tabela digitada."""
    c = math.exp(math.lgamma((nu + 1) / 2) - math.lgamma(nu / 2)) / math.sqrt(nu * math.pi)
    f = lambda t: c * (1 + t * t / nu) ** (-(nu + 1) / 2)
    def cdf(t, n=20000):
        h = t / n
        s = f(0) + f(t) + sum((4 if i % 2 else 2) * f(i * h) for i in range(1, n))
        return 0.5 + s * h / 3
    lo, hi = 0.0, 10.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if cdf(mid) < q else (lo, mid)
    return (lo + hi) / 2


T26 = t_quantil(0.975, 26)
pct = lambda b: 100 * (math.exp(K * b) - 1)
saida = []
for g, col in GRUPOS:
    rows = [r for r in rows0 if float(r[col]) > 0]
    y = np.log(np.array([float(r[col]) for r in rows])); x = np.array([float(r["ideologia"]) for r in rows])
    cl = np.array([r["uf"] for r in rows]); F = pdg.dummies(rows); M = pdg.residuador(F); kfe = np.linalg.matrix_rank(F)
    b_arr, se_arr, _, xt2, yt2 = pdg.ols_fwl(y, x, M, cl, kfe)
    b, se = float(b_arr[0]), float(se_arr[0]); xt = xt2[:, 0]; yt = yt2
    assert abs(b - float(pub[g]["b"])) < 1e-9 and abs(se - float(pub[g]["ep"])) < 1e-9, (g, b, se, pub[g]["b"], pub[g]["ep"])
    n = len(y); ufs = sorted(set(cl)); G = len(ufs); gi = np.array([ufs.index(c) for c in cl])
    k = kfe + 1; fator = (G / (G - 1)) * ((n - 1) / (n - k))
    Sxx = float(xt @ xt)
    W = RNG.choice([-1.0, 1.0], size=(B, G))[:, gi]                         # B x n, mesmo sinal dentro da UF
    P = (W * yt) @ M; Q = (W * xt) @ M                                       # M simétrica: linhas = M(yt w), M(xt w)
    H = np.zeros((n, G)); H[np.arange(n), gi] = xt                           # soma por UF ponderada por xt
    Pg, Qg = P @ H, Q @ H                                                    # B x G
    Sg = np.bincount(gi, weights=xt * xt, minlength=G)                       # G
    a, c2 = W @ (xt * yt), W @ (xt * xt)                                     # B

    def p_de(b0):
        db = (a - b0 * c2) / Sxx                                             # b* - b0
        R = (Pg - b0 * Qg) - db[:, None] * Sg[None, :]                       # xt_g . e*_g
        se_s = np.sqrt(fator * (R ** 2).sum(axis=1)) / Sxx
        t_s = db / se_s; t_o = (b - b0) / se
        return (1 + int((np.abs(t_s) >= abs(t_o) - 1e-12).sum())) / (B + 1)

    def limite(lado):
        dentro, fora = b, b + lado * 1.96 * se
        while p_de(fora) > ALFA:
            fora += lado * se
        while abs(fora - dentro) > 1e-7:
            m = (dentro + fora) / 2
            dentro, fora = (m, fora) if p_de(m) > ALFA else (dentro, m)
        return (dentro + fora) / 2

    lo, hi = limite(-1), limite(+1)
    grade = np.linspace(b - 6 * se, b + 6 * se, 481)
    aceita = np.array([p_de(v) > ALFA for v in grade])
    idx = np.where(aceita)[0]
    contiguo = bool(len(idx) and (idx[-1] - idx[0] + 1) == len(idx))
    saida.append(dict(grupo=g, desfecho=col, n=n, b=b, ep=se,
                      ic_normal_lo=b - 1.96 * se, ic_normal_hi=b + 1.96 * se, ic_wild_inv_lo=lo, ic_wild_inv_hi=hi,
                      ic_t26_lo=b - T26 * se, ic_t26_hi=b + T26 * se,
                      pct5_normal_lo=pct(b - 1.96 * se), pct5_normal_hi=pct(b + 1.96 * se), pct5_wild_inv_lo=pct(lo), pct5_wild_inv_hi=pct(hi),
                      pct5_t26_lo=pct(b - T26 * se), pct5_t26_hi=pct(b + T26 * se),
                      p0_grade=p_de(0.0), p_wild_publicado=float(pub[g]["p_wild"]), inclui_zero=lo < 0 < hi, intervalo_contiguo=contiguo,
                      B=B, semente=SEMENTE, t26=T26))

with open(AQUI / "r6_ic_wild_invertido.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(saida[0]), lineterminator="\n"); w.writeheader()
    for r in saida:
        w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in r.items()})
br = lambda v, d=1: f"{v:+.{d}f}".replace(".", ",")
L = ["# R6 — IC95% por inversão do teste wild-cluster bootstrap-t (painel de governadores; adendo v0.3, 2026-10-24)", "",
     f"Forma pré-registrada em `R6-PREREGISTRO-FORMA.md` (sha256 `{pre}`, hora em `R6-PREREGISTRO-FORMA.sha256`). B = {B}, semente {SEMENTE}, Rademacher por UF, "
     f"H0 imposta em cada valor testado; t(0,975; 26) = {T26:.4f} calculado numericamente. Modelo e dados idênticos ao painel principal (b e EP conferidos com "
     "`c02_indet_resultados.csv`). Os números antigos (IC normal) continuam publicados; este adendo só acrescenta.", "",
     "Troca de 5 pontos de ideologia (por exemplo PT -> DEM ou PL), variação na taxa registrada, em %:", "",
     "| grupo | b (EP) | normal b ± 1,96 EP (publicado) | wild-cluster invertido | t(26) | p(0) da grade / p wild publicado | inclui 0 |",
     "|---|---|---|---|---|---|---|"]
for r in saida:
    L.append(f"| {r['grupo']} | {r['b']:+.5f} ({r['ep']:.5f}) | {br(r['pct5_normal_lo'])} a {br(r['pct5_normal_hi'])} | {br(r['pct5_wild_inv_lo'])} a {br(r['pct5_wild_inv_hi'])} | "
             f"{br(r['pct5_t26_lo'])} a {br(r['pct5_t26_hi'])} | {r['p0_grade']:.3f} / {r['p_wild_publicado']:.3f} | {'sim' if r['inclui_zero'] else 'NÃO'} |")
L += ["", f"- Conjunto de aceitação contíguo na grade de ±6 EP (481 pontos) em todos os desfechos: {'sim' if all(r['intervalo_contiguo'] for r in saida) else 'NÃO (ver CSV)'}.",
      f"- Veredito pela regra pré-registrada: {'todos os 6 intervalos invertidos contêm 0; o veredito publicado (não distinguível de zero) fica' if all(r['inclui_zero'] for r in saida) else 'ALGUM intervalo invertido exclui 0: ver CSV'}.",
      "- Leitura: o intervalo invertido reflete os 27 clusters; o normal (CR1) é o publicado. Nenhum deles é limite causal garantido: são intervalos da associação "
      "condicionais ao modelo (efeitos fixos de UF e ano, ideologia BRC por período)."]
(AQUI / "r6_ic_wild_invertido.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
