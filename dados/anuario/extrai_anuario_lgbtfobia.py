"""Extrai a coluna 'Racismo por homofobia ou transfobia' (Ns. Absolutos) por UF e ano das 3 edições do Anuário FBSP.

Substitui o parser perdido (README antigo apontava para um scratchpad que não existe mais). Determinístico, só stdlib.
Entrada: fontes/t2-anuario-{2024,2025,2026}-*/anuario.txt (pdftotext -layout).
Saída: dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv com a coluna `marca` que o CSV legado perdeu:
  valor      = número informado
  nd         = '...'  (Informação não disponível)  -> NA, nunca zero
  inexistente= '-'    (Fenômeno inexistente, legenda do Anuário) -> ambíguo: zero real OU UF que não tipifica; tratar em análise de sensibilidade
Travas: (1) a linha de âncora tem de conter o cabeçalho esperado; (2) 27 UFs + Brasil por edição; (3) soma das UFs == linha Brasil.
Verificação contra o CSV legado (colunas edicao, ano_dado, uf, registros, linha_txt): ver `confere_com_legado()`.
Rodar: /opt/homebrew/bin/python3.14 -I dados/anuario/extrai_anuario_lgbtfobia.py
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, re, sys, os

BASE = REPO_ROOT
ED = {  # edicao: (arquivo, linha de âncora 1-based do cabeçalho, trecho esperado na âncora, (ano_col1, ano_col2))
    2024: ("fontes/t2-anuario-2024-dados2023/anuario.txt", 5541, "Racismo por homofobia ou transfobia", (2022, 2023)),
    2025: ("fontes/t2-anuario-2025-dados2024/anuario.txt", 5998, "Racismo por homofobia ou transfobia", (2023, 2024)),
    2026: ("fontes/t2-anuario-2026-dados2025/anuario.txt", 6761, "Racismo por homofobia ou", (2024, 2025)),
}
UF = {"Acre": "AC", "Alagoas": "AL", "Amapá": "AP", "Amazonas": "AM", "Bahia": "BA", "Ceará": "CE", "Distrito Federal": "DF",
      "Espírito Santo": "ES", "Goiás": "GO", "Maranhão": "MA", "Mato Grosso do Sul": "MS", "Mato Grosso": "MT", "Minas Gerais": "MG",
      "Pará": "PA", "Paraíba": "PB", "Paraná": "PR", "Pernambuco": "PE", "Piauí": "PI", "Rio de Janeiro": "RJ",
      "Rio Grande do Norte": "RN", "Rio Grande do Sul": "RS", "Rondônia": "RO", "Roraima": "RR", "Santa Catarina": "SC",
      "São Paulo": "SP", "Sergipe": "SE", "Tocantins": "TO", "Brasil": "BR"}
NOMES = sorted(UF, key=len, reverse=True)  # 'Mato Grosso do Sul' antes de 'Mato Grosso'
TOK = r"(\d{1,3}(?:\.\d{3})*|\.\.\.|-)"
LINHA = re.compile(r"^(" + "|".join(re.escape(n) for n in NOMES) + r")(?:\s*\(\d\))?\s+" + TOK + r"\s+" + TOK + r"(?:\s|$)")


def marca(t):
    return "nd" if t == "..." else ("inexistente" if t == "-" else "valor")


def valor(t):
    return int(t.replace(".", "")) if marca(t) == "valor" else ""


def extrai():
    saida = []
    for ed, (arq, ancora, trecho, anos) in ED.items():
        L = open(f"{BASE}/{arq}", encoding="utf-8").read().split("\n")
        assert trecho in L[ancora - 1], f"âncora quebrada em {arq}:{ancora}: {L[ancora-1]!r}"
        achados = {}
        for i in range(ancora, ancora + 60):  # tabela cabe em ~45 linhas após a âncora
            m = LINHA.match(L[i])
            if m and UF[m.group(1)] not in achados:
                achados[UF[m.group(1)]] = (m.group(2), m.group(3), i + 1)
        assert set(achados) == set(UF.values()), f"{ed}: faltam {set(UF.values()) - set(achados)}"
        for a, col in zip(anos, (0, 1)):
            soma = sum(valor(v[col]) for u, v in achados.items() if u != "BR" and marca(v[col]) == "valor")
            br = valor(achados["BR"][col])
            assert soma == br, f"{ed}/{a}: soma UFs {soma} != Brasil {br}"
        for u, v in achados.items():
            for a, col in zip(anos, (0, 1)):
                saida.append([ed, a, u, valor(v[col]), marca(v[col]), v[2]])
    return saida


def confere_com_legado(novo):
    leg = {(int(r["edicao"]), int(r["ano_dado"]), r["uf"]): (r["registros"], int(r["linha_txt"]))
           for r in csv.DictReader(open(f"{BASE}/dados/anuario/anuario_lgbtfobia_uf_ano.csv", encoding="utf-8"))}
    dif = [(k, leg.get(k), (str(v[3]), v[5])) for v in novo for k in [(v[0], v[1], v[2])] if leg.get(k) != (str(v[3]), v[5])]
    return len(leg), dif


if __name__ == "__main__":
    novo = extrai()
    with open(f"{BASE}/dados/anuario/anuario_lgbtfobia_uf_ano_v2.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["edicao", "ano_dado", "uf", "registros", "marca", "linha_txt"])
        w.writerows(novo)
    n_leg, dif = confere_com_legado(novo)
    print(f"linhas novas: {len(novo)} | linhas legado: {n_leg} | divergências vs legado (registros, linha_txt): {len(dif)}")
    for d in dif[:10]:
        print("  DIVERGE", d)
    print("marcas:", {m: sum(1 for r in novo if r[4] == m) for m in ("valor", "nd", "inexistente")})
    sys.exit(1 if dif or n_leg != len(novo) else 0)
