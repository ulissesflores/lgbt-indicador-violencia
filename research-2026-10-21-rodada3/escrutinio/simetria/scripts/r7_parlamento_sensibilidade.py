"""R7 (v0.3, 2026-10-24): Parlamento F2 — as duas codificações de "fonte primária" (0/49 e 1/49) como sensibilidade, com Fisher exato,
e a separação entre "fonte nomeada", "fonte primária" e "fonte capaz de sustentar a afirmação". NENHUMA recodificação: só contagens já gravadas.
Entradas: ../recontagem_x49_C27.csv (contagens por codificador), ../baseline_resumo_C27.json (linha de base: 60 falas da Câmara com estatística fora
dos 4 temas, codificadas pelo SEGUNDO codificador, Grok) e ../SIMETRIA.md (regra literal do codebook: o relatório com nome e ano conta como primária -> 1/49).
Fisher exato bicaudal = mesma função de fisher_C27.py (hipergeométrica; soma das probabilidades <= a observada).
Saídas: ../r7_parlamento_sensibilidade.csv e .md.   Rodar: /opt/homebrew/bin/python3.14 -I r7_parlamento_sensibilidade.py
Limite: a linha de base foi codificada pelo segundo codificador; só "Grok x Grok" compara o mesmo codificador. "Fonte capaz de sustentar a afirmação"
não é variável codificada (codificá-la seria recodificar): fica declarada como não medida."""
import ast, csv, json
from math import comb
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent


def fisher(a, n1, b, n2):
    K = a + b; N = n1 + n2
    p = lambda x: comb(n1, x) * comb(n2, K - x) / comb(N, K)
    p0 = p(a)
    return sum(p(x) for x in range(max(0, K - n2), min(n1, K) + 1) if p(x) <= p0 + 1e-12)


rec = {r["codificador"]: r for r in csv.DictReader(open(AQUI / "recontagem_x49_C27.csv", encoding="utf-8")) if r["estrato"] == "F2-Parlamento"}
o, g = rec["original(Claude)"], rec["segundo(Grok)"]
base = json.load(open(AQUI / "baseline_resumo_C27.json", encoding="utf-8"))
assert "nome+ano localizáveis" in (AQUI / "SIMETRIA.md").read_text(encoding="utf-8")   # a regra literal citada
dist_o = ast.literal_eval(o["distribuicao_fonte_nos_AFIRMA+ATRIBUI"])
n_o, n_g, n_b = int(o["n_AFIRMA+ATRIBUI"]), int(g["n_AFIRMA+ATRIBUI"]), int(base["den_AFIRMA+ATRIBUI"])
nomeada_o = n_o - dist_o["nenhuma"]
assert (n_o, n_g, n_b, int(o["n_primaria_verificavel"]), int(g["n_primaria_verificavel"]), base["primaria_verificavel"]) == (49, 50, 38, 0, 1, 2)
assert nomeada_o == int(o["n_com_alguma_fonte"]) == 8 and base["alguma_fonte"] == 3 and int(g["n_com_alguma_fonte"]) == 5

linhas = [  # variável, codificação F2, a, n1, codificação da base, b, n2, mesmo codificador?
    ("fonte primária", "original, regra aplicada (relatório tratado como ONG)", 0, n_o, "base (Grok)", base["primaria_verificavel"], n_b, "não"),
    ("fonte primária", "original, regra literal do codebook (nome + ano)", 1, n_o, "base (Grok)", base["primaria_verificavel"], n_b, "não"),
    ("fonte primária", "segundo codificador (Grok)", int(g["n_primaria_verificavel"]), n_g, "base (Grok)", base["primaria_verificavel"], n_b, "sim"),
    ("fonte nomeada (qualquer fonte)", "original", nomeada_o, n_o, "base (Grok)", base["alguma_fonte"], n_b, "não"),
    ("fonte nomeada (qualquer fonte)", "segundo codificador (Grok)", int(g["n_com_alguma_fonte"]), n_g, "base (Grok)", base["alguma_fonte"], n_b, "sim"),
]
rows = [dict(variavel=v, codificacao_F2=c, a=a, n1=n1, codificacao_base=cb, b=b, n2=n2, mesmo_codificador=mc, p_fisher=fisher(a, n1, b, n2))
        for v, c, a, n1, cb, b, n2, mc in linhas]
with open(AQUI / "r7_parlamento_sensibilidade.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
L = ["# R7 — Parlamento (F2): fonte nomeada, fonte primária e fonte capaz de sustentar a afirmação (v0.3, 2026-10-24)", "",
     "Gerado por `scripts/r7_parlamento_sensibilidade.py` a partir de contagens já gravadas (nenhuma recodificação). Denominador: falas F2 do Parlamento que afirmam "
     "ou atribuem o número (AFIRMA + ATRIBUI). Linha de base: 38 falas da Câmara com estatística fora dos 4 temas, codificadas pelo segundo codificador.", "",
     "| variável | F2 | a/n | linha de base | b/n | mesmo codificador | p (Fisher exato, bicaudal) |", "|---|---|---|---|---|---|---|"]
for r in rows:
    L.append(f"| {r['variavel']} | {r['codificacao_F2']} | {r['a']}/{r['n1']} | {r['codificacao_base']} | {r['b']}/{r['n2']} | {r['mesmo_codificador']} | {r['p_fisher']:.4f} |")
L += ["", f"- **Fonte nomeada** (qualquer fonte mencionada): {nomeada_o}/{n_o} no original ({dist_o.get('secundaria_ONG', 0)} de ONG, "
      f"{dist_o.get('oficial_sem_referencia', 0)} oficial sem referência localizável).",
      "- **Fonte primária** (nome + ano localizáveis): 0/49 pela regra aplicada pelo codificador original; 1/49 pela letra do codebook (um relatório com título e ano, "
      "cuja autoria não foi conferida); 1/50 pelo segundo codificador. As duas codificações do original ficam como sensibilidade; nenhuma é \"a verdadeira\".",
      "- **Fonte capaz de sustentar a afirmação** (a fonte mede o que a fala afirma, por exemplo uma comparação internacional de incidência): **não codificada** "
      "como variável. Medi-la exigiria recodificar as 49 falas; fica declarada como não medida.",
      "- Nenhum p acima de 0,05 é prova de equivalência com a linha de base; n pequeno. Só as linhas \"mesmo codificador = sim\" comparam o mesmo codificador."]
(AQUI / "r7_parlamento_sensibilidade.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
