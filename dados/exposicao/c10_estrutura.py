"""C10 (frente E, exposição por governo) — ESTRUTURA do desenho. Roda ANTES do pré-registro e NÃO lê nenhum desfecho.
Lê só exposições: colunas uf, ano, ideologia, partido de dados/painel/painel_uf_ano_tse_brc.csv (as colunas tx_* são descartadas na leitura)
e as datas de dados/presidencia/presidentes_2007_2024.csv.
Calcula: as 67 trocas reais de governador (mesma regra do C03: partido muda E ideologia BRC muda), o bloco BRC (cortes do próprio artigo:
esquerda < 4,5; centro 4,5 a 5,5; direita > 5,5), a direção, a disponibilidade de janela completa (3 anos antes, 3 depois) e de UFs de referência
sem troca por ano; e as janelas federais (ano-base e ano-fim por mandato).
Rodar: /opt/homebrew/bin/python3.14 -I c10_estrutura.py   Saída: c10_estrutura.md e c10_trocas.csv"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import sys; sys.dont_write_bytecode = True
import csv, collections
from datetime import date

BASE = REPO_ROOT
AQUI = f"{BASE}/dados/exposicao"
PRES = f"{BASE}/dados/presidencia/presidentes_2007_2024.csv"
Y0, Y1 = 2012, 2024          # faixa do painel UF x ano
PRE, POS = 3, 3              # janela: anos e-3..e-1 (antes) e e..e+2 (depois)


def bloco(s):
    """Cortes de Bolognesi, Ribeiro & Codato (2023), fontes/p2-f8-governos/bolognesi.txt linhas 601-607, agrupados em 3 blocos."""
    return "esquerda" if s < 4.5 else ("centro" if s <= 5.5 else "direita")


def exposicoes():
    by = collections.defaultdict(dict)
    for r in csv.DictReader(open(f"{BASE}/dados/painel/painel_uf_ano_tse_brc.csv", encoding="utf-8")):
        by[r["uf"]][int(r["ano"])] = {"ideologia": float(r["ideologia"]), "partido": r["partido"]}   # desfechos NÃO são lidos
    return by


def trocas(by):
    """[(uf, e, partido_antes, partido_depois, ideo_antes, ideo_depois)]; e = primeiro ano com o partido novo (regra do C03)."""
    out = []; onda = 0
    for u, d in sorted(by.items()):
        ys = sorted(d)
        for a, b in zip(ys, ys[1:]):
            di = d[b]["ideologia"] - d[a]["ideologia"]
            if abs(di) > 1e-9:
                if d[b]["partido"] != d[a]["partido"]: out.append((u, b, d[a]["partido"], d[b]["partido"], d[a]["ideologia"], d[b]["ideologia"]))
                else: onda += 1
    return out, onda


def direcao_bloco(ia, ib):
    a, b = bloco(ia), bloco(ib)
    if a == "esquerda" and b == "direita": return "esquerda->direita"
    if a == "direita" and b == "esquerda": return "direita->esquerda"
    if "centro" in (a, b): return "envolve centro"
    return "mesmo bloco"


def janela_completa(e): return e - PRE >= Y0 and e + POS - 1 <= Y1


def anos_troca(ev):
    d = collections.defaultdict(set)
    for u, e, *_ in ev: d[u].add(e)
    return d


def contaminada(u, e, at):
    """outra troca real da mesma UF em e-2..e+2 (exceto e): o antes ou o depois mistura governos."""
    return any(y != e and e - PRE + 1 <= y <= e + POS - 1 for y in at[u])


def referencias(by, at, e):
    """UFs SEM troca real em e-2..e+2 (antes e depois com o mesmo governo) e com janela completa: referência de acaso do ano e."""
    return sorted(u for u in by if not any(e - PRE + 1 <= y <= e + POS - 1 for y in at[u]))


def janelas_federais():
    """ano-base = último ano civil completo ANTES do 1º dia do mandato; ano-fim = último ano civil completo DENTRO do mandato (2024 se em curso)."""
    out = []
    for p in csv.DictReader(open(PRES, encoding="utf-8")):
        i, f = date.fromisoformat(p["inicio"]), date.fromisoformat(p["fim"])
        base = i.year - 1   # se a posse é 1º/jan, o ano anterior é o último completo; se é no meio do ano, também (o ano da posse é parcial)
        fim = f.year if f == date(f.year, 12, 31) else f.year - 1
        out.append(dict(presidente=p["presidente"], partido=p["partido_eleicao"], inicio=p["inicio"], fim_exercicio=p["fim"], ano_base=base, ano_fim=fim,
                        tendencia_de=base - 3, em_curso=p["fim"] == "2024-12-31"))
    return out


if __name__ == "__main__":
    by = exposicoes(); ev, onda = trocas(by); at = anos_troca(ev)
    assert len(by) == 27 and len(ev) == 67 and onda == 27, (len(by), len(ev), onda)
    rows = []
    for u, e, pa, pb, ia, ib in ev:
        rows.append(dict(uf=u, ano_troca=e, partido_antes=pa, partido_depois=pb, ideologia_antes=ia, ideologia_depois=ib, delta=round(ib - ia, 2),
                         sentido="direita" if ib > ia else "esquerda", bloco_antes=bloco(ia), bloco_depois=bloco(ib), direcao_bloco=direcao_bloco(ia, ib),
                         janela_completa=int(janela_completa(e)), contaminada=int(contaminada(u, e, at)), n_referencias=len(referencias(by, at, e))))
    with open(f"{AQUI}/c10_trocas.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    L = ["# C10 — estrutura do desenho (gerado por c10_estrutura.py; NÃO lê desfecho)", "",
         f"Trocas reais de governador (partido muda E ideologia BRC muda): {len(ev)}; trocas de onda (mesmo partido, só o escore muda): {onda}.", ""]
    L += ["| ano da troca | trocas | com janela completa (3+3) | contaminadas (outra troca da UF em e-2..e+2) | UFs de referência sem troca em e-2..e+2 |", "|---|---|---|---|---|"]
    for e in sorted({r["ano_troca"] for r in rows}):
        rr = [r for r in rows if r["ano_troca"] == e]
        L.append(f"| {e} | {len(rr)} | {sum(r['janela_completa'] for r in rr)} | {sum(r['contaminada'] for r in rr)} | {rr[0]['n_referencias']} |")
    c = collections.Counter(r["direcao_bloco"] for r in rows); s = collections.Counter(r["sentido"] for r in rows)
    cc = collections.Counter(r["direcao_bloco"] for r in rows if r["janela_completa"]); sc = collections.Counter(r["sentido"] for r in rows if r["janela_completa"])
    L += ["", f"Direção por bloco (todas): {dict(sorted(c.items()))}; com janela completa: {dict(sorted(cc.items()))}.",
          f"Sentido do escore (todas): {dict(sorted(s.items()))}; com janela completa: {dict(sorted(sc.items()))}.",
          f"Janela completa e não contaminada: {sum(1 for r in rows if r['janela_completa'] and not r['contaminada'])}.", "",
          "Janelas federais (ano-base = último ano completo antes do mandato; ano-fim = último ano completo dentro dele):", "",
          "| presidente | partido | início | fim | ano-base | ano-fim | tendência pré desde | em curso |", "|---|---|---|---|---|---|---|---|"]
    for j in janelas_federais():
        L.append(f"| {j['presidente']} | {j['partido']} | {j['inicio']} | {j['fim_exercicio']} | {j['ano_base']} | {j['ano_fim']} | {j['tendencia_de']} | {'sim' if j['em_curso'] else 'não'} |")
    open(f"{AQUI}/c10_estrutura.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
