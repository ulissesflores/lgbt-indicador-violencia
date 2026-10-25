"""C08 (TRIAGEM, rodada 3) — Cobertura implícita do GGB com numeradores COMPARÁVEIS (cópia estendida de cobertura_implicita.py, que não é alterado).
Critérios de decisão escritos ANTES de rodar: research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md (hash em CRITERIOS.sha256).
Método do esperado E e todos os LIMITES: idênticos ao cobertura_implicita.py (SIM pareado por sexo x raça x faixa de 5 anos, composição LGB+ da PNS 2019; E = soma(pop LGB+ da célula x taxa da célula) x RR; RR = 1, 2,82, 3,84;
  prevalência 1,89% e 1,96%; NÃO é estimativa de mortes nem taxa; pareamento sem escolaridade, UF, urbano/rural; menores no numerador; autorrelato; denominador 2023-24 extrapolado).
Numeradores (releases em fontes/p3-ggb/_raw/txt/ggb20NN.txt; perfil em research-2026-10-21-rodada3/GGB-completo/perfil/GGB-O-QUE-E.md):
  N0 = total declarado (257, 291, 257). N1 = homicídios + latrocínios declarados, sem suicídios e sem "outras causas": 2023 = 204+17 = 221 (tabela "Causa mortis" e texto "221 (85,9%) homicídios, incluídos aqui os latrocínios");
  2024 = 239+30 = 269 (tabela "Causa mortis" p. 11; o "273 homicídios" do texto de abertura inclui as 4 "outras causas"); 2025 = 204+17 = 221 (tabela do release; o destaque "237 homicídios" inclui as 16 "outras").
  N2 = N1 menos todas as pessoas trans da tabela de identidade: 2023 = 127 ("Travestis e Transgêneros"); 2024 = 96 ("Travestis/Trans") + 6 (homens trans) = 102; 2025 = 46 + 18 + 3 = 67 (mulher trans + travesti + homem trans).
  N2 é um CENÁRIO DE SUBTRAÇÃO (correção v0.3, 2026-10-24, depois do escrutínio do Astra), NÃO um limite inferior demonstrado: subtrai trans que podem estar
  fora de N1 (suicidas: 6 em 2023 [4 trans/travestis + 2 homens trans], 3 em 2024), não subtrai os heterossexuais incluídos pelo GGB (6 em 2024, 3 em 2025) nem os
  "não informados" (16 em 2025), e não harmoniza a idade (menores e idade não informada no numerador). A versão anterior dizia "N2 é LIMITE INFERIOR" e
  "a cobertura cis LGB está entre cobertura(N2) e cobertura(N1)": a seção 5 da saída mostra, só com as marginais publicadas, que em 2024 o mínimo compatível
  é 164 < N2 = 167 (contraexemplo do Astra: 269 - 99 trans - 6 heterossexuais), e em 2023 o mínimo é 100 > N2 = 94. N2 não é limite em nenhuma direção.
  Além disso, a PNS 2019 não perguntou identidade de gênero: pessoas trans que declararam orientação LGB estão no denominador sem identificação; subtrair
  todas as trans do numerador não produz o numerador comparável ao denominador. Os números de N0, N1 e N2 e as linhas do CSV ficam INALTERADOS.
Anomalias de fonte registradas: (1) as tabelas de causa de 2023 e 2025 são IDÊNTICAS (204/20/17/16; 257) com composição por identidade muito diferente (já anotado em GGB-completo/series/analises.md, l. 109); (2) o script antigo usa
  "homicidios_decl" = 221 em 2023 (homicídio + latrocínio) mas 273 em 2024 (homicídio + latrocínio + outras): definições diferentes; N1 corrige para 269.
SIM só existe até 2024 (dados/sim/sim_agressoes_agregado.csv): 2025 não tem esperado verificável; a linha PROXY usa as taxas por célula de 2024 e a população extrapolada de 2025, fora de qualquer veredito.
Reprodução obrigatória (aborta): todas as linhas de dados/ggb/cobertura_implicita.csv (agressão e agressão+indet, 2023-24, 4 prevalências, 3 RR, 2 medidas), esperado ±0,1 e cobertura ±0,001.
Rodar: /opt/homebrew/bin/python3.14 -I dados/ggb/ggb_c08_numeradores.py   Saídas: dados/ggb/c08_numeradores.md, c08_numeradores.csv e (v0.3) c08_cenarios_marginais.csv"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import importlib.util, csv, re
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(REPO_ROOT)
spec_ = importlib.util.spec_from_file_location("pi", BASE / "dados/sim/padroniza_idade.py"); pi = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(pi)
NEG, NNEG = ["preta", "parda"], ["branca", "amarela", "indigena"]
G17 = pi.G17

# ---- PNS 2019: prevalência LGB+ por sexo x raça x faixa
P = BASE / "fontes/q1-textointegral/F2/pns2019"
pat = re.compile(r"^@(\d+)\s+(\w+)\s+\$?(\d+)(?:\.(\d+))?\.")
sp = {m.group(2): (int(m.group(1)), int(m.group(3))) for l in (P / "input_PNS_2019_utf8.txt").read_text(encoding="utf8", errors="replace").splitlines() if (m := pat.match(l))}
want = ["C006", "C008", "C009", "Y008", "V00291", "V001"]
raw = pd.read_fwf(P / "x/PNS_2019.txt", colspecs=[(sp[k][0] - 1, sp[k][0] - 1 + sp[k][1]) for k in want], names=want, header=None, dtype=str)
d = raw[raw.V001.notna() & raw.Y008.isin(["1", "2", "3", "4"])].copy()
assert d.V001.notna().all()
d["w"] = d.V00291.astype(float); d["age"] = d.C008.astype(int)
d["sx"] = d.C006.map({"1": "M", "2": "F"}); d["rc"] = np.where(d.C009.isin(["2", "4"]), "neg", np.where(d.C009.isin(["1", "3", "5"]), "nneg", None))
d = d[d.sx.notna() & d.rc.notna()]
def faixa(a):
    if a < 20: return "15-19"
    if a >= 80: return "80+"
    return f"{a//5*5}-{a//5*5+4}"
d["g"] = d.age.map(faixa); d["lgb"] = d.Y008.isin(["2", "3", "4"])
tot = d.groupby(["sx", "rc", "g"]).w.sum(); lg = d[d.lgb].groupby(["sx", "rc", "g"]).w.sum()
prev = (lg / tot).fillna(0.0)
pesos_lgb = d[d.lgb].w.sum(); pesos_tot = d.w.sum()
prev_global = pesos_lgb / pesos_tot
# distribuição etária/racial dos LGB+ x geral (para o texto)
comp = {}
for nome, sel in {"18-29": d.age < 30, "30-44": (d.age >= 30) & (d.age < 45), "45+": d.age >= 45}.items():
    comp[nome] = (d[d.lgb & sel].w.sum() / pesos_lgb, d[sel].w.sum() / pesos_tot)
comp_neg = (d[d.lgb & (d.rc == "neg")].w.sum() / pesos_lgb, d[d.rc == "neg"].w.sum() / pesos_tot)
comp_h = (d[d.lgb & (d.sx == "M")].w.sum() / pesos_lgb, d[d.sx == "M"].w.sum() / pesos_tot)

# ---- SIM
def esperado(ano, mortes, escala_prev=1.0, ano_taxa=None):
    """ano_taxa: ano cujas taxas por célula são usadas (None = o próprio ano); só a linha PROXY de 2025 usa 2024."""
    at = ano if ano_taxa is None else ano_taxa
    E = 0.0; lgb_pop = 0.0
    for sx in "MF":
        for rc, racas in (("neg", NEG), ("nneg", NNEG)):
            for g in G17:
                if g not in prev.index.get_level_values(2).unique(): continue
                pop = sum(pi.pop_ano(ano, sx, r, g) for r in racas)
                if g == "15-19": pop *= 0.4
                taxa = sum(mortes.get((at, sx, r, g), 0.0) for r in racas) / sum(pi.pop_ano(at, sx, r, g) for r in racas)
                p = prev.get((sx, rc, g), 0.0) * escala_prev
                E += pop * p * taxa; lgb_pop += pop * p
    return E, lgb_pop

PREV = [("1,89%", 0.0189 / prev_global), ("1,96%", 1.0)]
RRS = (1.0, 2.82, 3.84)

# ---- reprodução do publicado (todas as linhas de cobertura_implicita.csv)
pub = pd.read_csv(BASE / "dados/ggb/cobertura_implicita.csv")
GGBV = {2023: {"todas": 257, "homicidios_decl": 221}, 2024: {"todas": 291, "homicidios_decl": 273}}
ESC_PUB = {"1,89% (PNS 2019, publicado; não resposta = não LGB+)": 0.0189 / prev_global, f"{100*prev_global:.2f}% (PNS, só respostas válidas)".replace(".", ","): 1.0, "3% (cenário)": 0.03 / prev_global, "5% (cenário)": 0.05 / prev_global}
nchk = 0
MORT = {}
for desf, grp in (("agressao", ["agressao"]), ("agressao+indet", ["agressao", "indet"])):
    MORT[desf], _ = pi.redistribui(pi.carrega_mortes(grp))
    for ano in (2023, 2024):
        for lab, esc in ESC_PUB.items():
            E, pl = esperado(ano, MORT[desf], esc)
            for rr in RRS:
                for medida, ggb in GGBV[ano].items():
                    r = pub[(pub.desfecho == desf) & (pub.ano == ano) & (pub.prevalencia_LGB == lab) & (pub.RR_cenario == rr) & (pub.medida_GGB == medida)]
                    assert len(r) == 1, (desf, ano, lab, rr, medida)
                    r = r.iloc[0]; nchk += 1
                    assert abs(r.mortes_esperadas - E * rr) <= 0.1 and abs(r.cobertura_implicita - ggb / (E * rr)) <= 0.001, (desf, ano, lab, rr, medida, r.mortes_esperadas, E * rr)

# ---- numeradores novos
NUM = {2023: {"N0": 257, "N1": 204 + 17, "TRANS": 127}, 2024: {"N0": 291, "N1": 239 + 30, "TRANS": 96 + 6}, 2025: {"N0": 257, "N1": 204 + 17, "TRANS": 46 + 18 + 3}}
for a, v in NUM.items(): v["N2"] = v["N1"] - v["TRANS"]
rows = []
for desf in ("agressao", "agressao+indet"):
    for ano in (2023, 2024, 2025):
        for plab, esc in PREV:
            proxy = ano == 2025
            E, pl = esperado(ano, MORT[desf], esc, ano_taxa=2024 if proxy else None)
            for nome in ("N0", "N1", "N2"):
                n = NUM[ano][nome]
                rows.append(dict(desfecho=desf, ano=ano, prevalencia=plab, numerador=nome, n=n, pop_LGB=round(pl), proxy=proxy, **{f"E_RR{rr}": E * rr for rr in RRS}, **{f"cob_RR{rr}": n / (E * rr) for rr in RRS}))
df = pd.DataFrame(rows); df.to_csv(BASE / "dados/ggb/c08_numeradores.csv", index=False)

# ---- vereditos (convenção pré-escrita; agressão; prevalência 1,89%; RR=1; só anos com SIM)
V = []
for ano in (2023, 2024):
    r = {n: df[(df.desfecho == "agressao") & (df.ano == ano) & (df.prevalencia == "1,89%") & (df.numerador == n)].iloc[0] for n in ("N0", "N1", "N2")}
    V.append((ano, r))

L = ["# C08 — cobertura implícita do GGB com numeradores comparáveis (gerado por ggb_c08_numeradores.py)", "",
     "> [!NOTE]", "> **Exercício de escala, não estimativa de mortes nem taxa.** Cabeçalho do script traz os numeradores, as fontes e todos os LIMITES. Critérios pré-escritos em `research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md`. N2 é um cenário de subtração (todas as pessoas trans da tabela de identidade), não limite inferior nem superior demonstrado (correção v0.3; seção 5).", "",
     f"## 0. Reprodução: {nchk} linhas de `dados/ggb/cobertura_implicita.csv` reproduzidas (esperado ±0,1; cobertura ±0,001); senão o script aborta.", "",
     "## 1. Numeradores (de onde vem cada número)", "",
     "| ano | N0 total | N1 homicídio + latrocínio | trans na tabela de identidade | N2 = N1 - trans | observação |", "|---|---|---|---|---|---|",
     f"| 2023 | 257 | 204 + 17 = {NUM[2023]['N1']} | 127 (\"Travestis e Transgêneros\") | {NUM[2023]['N2']} | script antigo: 221 = mesmo N1 |",
     f"| 2024 | 291 | 239 + 30 = {NUM[2024]['N1']} | 96 + 6 homens trans = 102 | {NUM[2024]['N2']} | script antigo usa 273 (inclui 4 \"outras\"): definição diferente da de 2023 |",
     f"| 2025 | 257 | 204 + 17 = {NUM[2025]['N1']} | 46 + 18 + 3 = 67 | {NUM[2025]['N2']} | tabela de causa IDÊNTICA à de 2023; sem SIM 2025: sem veredito |", "",
     "## 2. Resultado principal: desfecho agressão X85-Y09, prevalência 1,89%, cobertura = n / E", "",
     "| ano | numerador | n | E (RR=1) | cobertura RR=1 | cobertura RR=2,82 | cobertura RR=3,84 |", "|---|---|---|---|---|---|---|"]
for ano in (2023, 2024, 2025):
    for nome in ("N0", "N1", "N2"):
        r = df[(df.desfecho == "agressao") & (df.ano == ano) & (df.prevalencia == "1,89%") & (df.numerador == nome)].iloc[0]
        L.append(f"| {ano}{' (PROXY: taxas SIM 2024)' if ano == 2025 else ''} | {nome} | {r.n} | {r['E_RR1.0']:.0f} | {100*r['cob_RR1.0']:.1f}% | {100*r['cob_RR2.82']:.1f}% | {100*r['cob_RR3.84']:.1f}% |")
L += ["", "## 3. Prevalência 1,96% (só respostas válidas) e desfecho agressão + indeterminada (sensibilidade)", "", "| desfecho | ano | prevalência | numerador | n | E (RR=1) | cobertura RR=1 | cobertura RR=2,82 | cobertura RR=3,84 |", "|---|---|---|---|---|---|---|---|---|"]
for _, r in df[~((df.desfecho == "agressao") & (df.prevalencia == "1,89%"))].iterrows():
    L.append(f"| {r.desfecho} | {r.ano}{' PROXY' if r.proxy else ''} | {r.prevalencia} | {r.numerador} | {r.n} | {r['E_RR1.0']:.0f} | {100*r['cob_RR1.0']:.1f}% | {100*r['cob_RR2.82']:.1f}% | {100*r['cob_RR3.84']:.1f}% |")
L += ["", "## 4. Vereditos pelas convenções pré-escritas (agressão; 1,89%; RR=1; anos com SIM)", ""]
for ano, r in V:
    c0, c1, c2 = r["N0"]["cob_RR1.0"], r["N1"]["cob_RR1.0"], r["N2"]["cob_RR1.0"]
    L.append(f"- {ano}: cobertura N0 {100*c0:.1f}%, N1 {100*c1:.1f}%, N2 {100*c2:.1f}%. N0 e N1 < 100%: {'sim' if c0 < 1 and c1 < 1 else 'NÃO'}. N2 < 15%: {'sim' if c2 < 0.15 else 'NÃO'}. Entre os cenários N2 e N1: [{100*c2:.1f}%; {100*c1:.1f}%] (cenários, não intervalo demonstrado; v0.3, seção 5).")
# ---- 5. (v0.3, 2026-10-24, POST HOC, depois do escrutínio do Astra) faixas compatíveis com as MARGINAIS publicadas -----------------------------
# Só tabelas e frases dos releases do GGB (o cruzamento causa x identidade x idade não é publicado). Cada número tem âncora literal no release;
# se o .txt do release estiver no disco (projeto privado; não é distribuído porque traz nomes), o script confere a âncora e aborta se faltar.
MARG = {
    2023: dict(cis=118 + 9 + 3, trans=127, het=0, ni=0, suic=20, outras=16, cis_suic=11 + 1, trans_suic=4 + 2, nb_suic=2, menores=8, idade_ni=36,
               anc=["Travestis e Transgêneros           127", "Gay                                118", "Lésbica                            9",
                    "Bissexual                          3", "Outras causas            16", "11 gays suicidas, 4 transexuais e travestis, 2",
                    "homens trans, 2 não binaries e 1 lésbica", "13-18                       8", "NI                          36"]),
    2024: dict(cis=165 + 11 + 7, trans=96 + 6, het=6, ni=0, suic=18, outras=4, cis_suic=14 + 1, trans_suic=3, nb_suic=0, menores=16, idade_ni=57,
               anc=["Gay                         165", "Travestis/Trans              96", "Lésbicas                     11", "Bissexual                     7",
                    "Homem trans                   6", "Heterossexual                 6", "Outras causas                 4",
                    "sobre 14 gays suicidas, 3 transexuais e travestis, e 1 lésbica", "5-18                          16"]),
}
TXT = BASE / "fontes/p3-ggb/_raw/txt"
for ano, m in MARG.items():
    f = TXT / f"ggb{ano}.txt"
    if f.exists():
        tx = " ".join(f.read_text(encoding="utf-8", errors="replace").split())     # espaços colapsados (tabelas extraídas do PDF)
        for a in m["anc"]:
            assert " ".join(a.split()) in tx, (ano, a)
    m["ancoras_conferidas"] = f.exists()
CEN = []
for ano, m in MARG.items():
    n1 = NUM[ano]["N1"]; n2 = NUM[ano]["N2"]
    assert m["cis"] + m["trans"] + m["het"] + m["ni"] == NUM[ano]["N0"] and n1 + m["suic"] + m["outras"] == NUM[ano]["N0"], ano
    E = float(df[(df.desfecho == "agressao") & (df.ano == ano) & (df.prevalencia == "1,89%") & (df.numerador == "N1")].iloc[0]["E_RR1.0"])
    # não binários suicidas: a tabela de 2023 não tem a categoria; contados (a) entre trans ou (b) entre cis. A faixa é a união.
    cis_fora_min = m["cis_suic"]; cis_fora_max = m["cis_suic"] + m["nb_suic"]
    cis_n1_max = m["cis"] - cis_fora_min                                   # nenhuma "outra causa" é cis LGB
    cis_n1_min = m["cis"] - cis_fora_max - min(m["outras"], m["cis"] - cis_fora_max)   # todas as "outras causas" são cis LGB
    trans_n1_max = m["trans"] - m["trans_suic"]
    linhas = [("N1 homicídio + latrocínio (inclui trans e heterossexuais)", n1),
              ("N2 cenário: N1 menos TODAS as trans da tabela (publicado)", n2),
              ("cis LGB dentro de N1: mínimo compatível com as marginais", cis_n1_min),
              ("cis LGB dentro de N1: máximo compatível com as marginais", cis_n1_max),
              ("mínimo compatível menos toda a faixa etária até 18 anos do release (cenário de idade; idade não informada fica)", cis_n1_min - m["menores"])]
    if ano == 2024:
        linhas.insert(2, ("contraexemplo do Astra: 269 - 99 trans (102 - 3 suicidas) - 6 heterossexuais", n1 - trans_n1_max - m["het"]))
    for rot, n in linhas:
        CEN.append(dict(ano=ano, cenario=rot, n=n, E_RR1=E, cob_RR1=n / E, ancoras_conferidas=m["ancoras_conferidas"]))
    m.update(cis_n1_min=cis_n1_min, cis_n1_max=cis_n1_max, n2=n2, E=E)
assert next(c["n"] for c in CEN if c["ano"] == 2024 and c["cenario"].startswith("contraexemplo")) == 164
pd.DataFrame(CEN).to_csv(BASE / "dados/ggb/c08_cenarios_marginais.csv", index=False)
L += ["", "## 5. Correção v0.3 (2026-10-24, post hoc): N2 é cenário, não limite (faixas pelas marginais publicadas do GGB)", "",
      "> [!WARNING]", "> A versão anterior chamava N2 de \"limite inferior do numerador cis LGB\" e lia a cobertura cis LGB \"entre N2 e N1\". Isso não está demonstrado: "
      "o GGB inclui heterossexuais (6 em 2024), não publica causa x identidade x idade e o numerador tem menores. Os números acima ficam; a leitura muda. "
      "Além disso, a PNS 2019 não perguntou identidade de gênero: pessoas trans que declararam orientação LGB estão no denominador, sem identificação.", "",
      "Faixas abaixo: só tabelas de identidade, causa e idade e a frase sobre suicídios por identidade de cada release; agressão X85-Y09, prevalência 1,89%, RR = 1. "
      "Em 2023, os 2 suicidas não binários foram contados ora entre trans, ora entre cis (a faixa é a união). 2025 fica de fora: a tabela de identidade soma 255, não 257, "
      "e o release não separa os 20 suicídios entre gays e trans.", "",
      "| ano | cenário | n | E (RR=1) | cobertura RR=1 |", "|---|---|---|---|---|"]
for c in CEN:
    L.append(f"| {c['ano']} | {c['cenario']} | {c['n']} | {c['E_RR1']:.0f} | {100*c['cob_RR1']:.1f}% |")
for ano, m in MARG.items():
    pos = "abaixo do mínimo compatível" if m["n2"] < m["cis_n1_min"] else ("dentro da faixa" if m["n2"] <= m["cis_n1_max"] else "acima do máximo")
    L.append(f"- {ano}: N2 = {m['n2']} está {pos} [{m['cis_n1_min']}; {m['cis_n1_max']}] de cis LGB dentro de N1.")
L += ["- Conclusão: N2 não é limite em nenhuma direção (abaixo da faixa em 2023, dentro dela em 2024). Nenhum cenário muda a leitura de escala: "
      "em todos, a contagem fica muito abaixo das mortes esperadas sob risco igual. O numerador comparável ao denominador da PNS (adultos que se declarariam LGB, "
      "inclusive pessoas trans) não é obtenível sem cruzamento público de causa x orientação x identidade x idade."]
(BASE / "dados/ggb/c08_numeradores.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
