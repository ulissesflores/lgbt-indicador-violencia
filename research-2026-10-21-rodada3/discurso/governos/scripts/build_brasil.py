"""Brasil 2011-2025: itens (declaracoes e acoes de governos) com citacao VERIFICADA + dados oficiais por governo.
Saidas: ../brasil_itens.csv, ../brasil_dados_governo.csv, ../verificacao-brasil.tsv. ponytail: helpers duplicados de build_paises.py (divida aceita)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, gzip, hashlib, html, os, re, subprocess, sys
ROOT = (REPO_ROOT + "/")
BR = ROOT + "fontes/q1-textointegral/discurso/governos/brasil/"
OUTD = ROOT + "research-2026-10-21-rodada3/discurso/governos/"
F8 = ROOT + "fontes/q1-textointegral/F8-literatura/"

def norm(s):
    s = html.unescape(s).replace("­", "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-").replace("\xa0", " ")
    return re.sub(r"\s+", " ", re.sub(r"-\s*\n\s*", "", s)).strip()
_c = {}
def pages(path):
    if path in _c: return _c[path]
    if path.endswith(".pdf"):
        out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout.split("\f")
    else:
        b = open(path, "rb").read()
        if b[:2] == b"\x1f\x8b": b = gzip.decompress(b)
        try: t = b.decode("utf-8")
        except UnicodeDecodeError: t = b.decode("latin1")
        t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
        out = [re.sub(r"<[^>]+>", " ", t)]
    _c[path] = [norm(p) for p in out]; return _c[path]
def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()
CHECK = []
def ev(file, quote, rid):
    q = norm(quote); hit = [i for i, p in enumerate(pages(file), 1) if q in p]
    loc = (f"PDF p.{hit[0]}" if file.endswith(".pdf") else "pagina web") if hit else "?"
    CHECK.append((rid, "OK" if hit else "FALHOU", os.path.basename(file), loc, q[:120]))
    if not hit: print("NAO ACHOU:", rid, q[:90], file=sys.stderr)
    return loc, sha(file), os.path.relpath(file, ROOT)

ITEMS = []
def item(rid, gov, data, agente, tipo, desc, file, quote, url, juiz=""):
    loc, h, rel = ev(file, quote, rid)
    ITEMS.append(dict(id=rid, governo=gov, data=data, agente=agente, tipo=tipo, descricao=desc, verbatim=norm(quote), url=url, arquivo=rel, locator=loc, sha256=h, julgamento_meu=juiz))

item("D1", "Dilma I", "2011-05-25", "Gilberto Carvalho (Sec.-Geral da Presidencia), relatando decisao de Dilma", "T3",
     "Suspensao da producao e distribuicao do material anti-homofobia (MEC/Saude) apos reuniao com a bancada religiosa", BR + "exame-dilma-kit-2011.html",
     "A presidente decidiu suspender esse material e suspender também a distribuição", "https://exame.com/brasil/apos-pressao-religiosa-dilma-suspende-producao-de-kit-homofobia/")
item("D2", "Dilma II", "2016-04-28", "Presidenta (decreto)", "T4", "Decreto 8.727: uso do nome social e identidade de genero na administracao federal", BR + "planalto-decreto8727-2016.html",
     "Dispõe sobre o uso do nome social e o reconhecimento da identidade de gênero de pessoas travestis e transexuais no âmbito da administração pública federal", "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/decreto/D8727.htm")
item("T1", "Temer", "2017-09-29 (reportagem)", "Governo federal (execucao orcamentaria), apurado por Aos Fatos/UOL", "T3",
     "Repasses para programas especificos LGBT zerados em 2017; queda de R$ 3,06 mi (2008, Lula) para R$ 518 mil (2016, Dilma): o corte comeca em 2015", BR + "aosfatos-temer-zero-homofobia-2017.html",
     "O governo do presidente Michel Temer zerou em 2017 os já escassos repasses federais para programas específicos de defesa da comunidade LGBT", "https://www.aosfatos.org/noticias/temer-reduz-a-zero-repasses-a-politicas-de-combate-homofobia/")
item("T2", "Temer", "2017-11-01 (Lei 13.502)", "Presidente (lei)", "T3?", "Rol de competencias do Ministerio dos Direitos Humanos sem a palavra LGBT ('direitos das minorias'); mesma redacao generica de 2019", BR + "planalto-lei13502-2017.html",
     "direitos da cidadania; b) direitos da criança e do adolescente; c) direitos da pessoa idosa; d) direitos da pessoa com deficiência; e e) direitos das minorias", "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13502.htm", "T3 com ressalva: sem a linha de base de 2015 nao da para chamar de 'retirada'")
item("B1", "Bolsonaro", "2019-01-01 (MP 870); 2019-06-18 (Lei 13.844)", "Presidente (MP 870 -> Lei 13.844/2019, art. 43)", "T3?", "Rol do Ministerio da Mulher, Familia e DH sem LGBT (igual ao de 2017); a Diretoria LGBT foi mantida no Decreto 9.673", BR + "planalto-lei13844-2019.html",
     "Constituem áreas de competência do Ministério da Mulher, da Família e dos Direitos Humanos", "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13844.htm", "T3 com ressalva: texto igual ao de 2017; noticias de 2019 chamam de 'exclusao'")
item("B2", "Bolsonaro", "2019-01-02", "Presidente (Decreto 9.673)", "T4/neutra", "Estrutura mantem 'Diretoria de Promocao dos Direitos de Lesbicas, Gays, Bissexuais, Travestis e Transexuais' na Sec. Nacional de Protecao Global", BR + "planalto-decreto9673-2019.html",
     "Diretoria de Promoção dos Direitos de L é sbicas, Gays, Bissexuais, Travestis e Transexuais", "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/decreto/D9673.htm")
item("B3", "Bolsonaro", "2019-01-03", "Presidente Jair Bolsonaro (Twitter)", "T2", "Garante que ninguem sera 'abandonado' nas diretrizes de DH; cita Sec. Protecao Global e o Conselho", BR + "metropoles-bolsonaro-twitter-minorias-2019-01.html",
     "Não haverá abandono de auxílio a qualquer indivíduo nas diretrizes de Direitos Humanos", "https://www.metropoles.com/brasil/politica-br/no-twitter-bolsonaro-diz-que-minorias-nao-perderao-direitos")
item("B4", "Bolsonaro", "2019-01-02/03", "Ministra Damares Alves", "T2", "Compromisso de dialogo e de nao violar direitos", BR + "congressoemfoco-lider-lgbt-damares-2019-01.html",
     "Teremos um diálogo aberto com a comunidade LGBT. Nenhum direito conquistado pela comunidade LGBT será violado", "https://www.congressoemfoco.com.br/noticia/26477/lider-lgbt-ve-confusao-em-analise-de-nova-estrutura-de-ministerio-e-descarta-prejuizo-para-comunidade")
item("B5", "Bolsonaro", "2019-04-25", "Presidente Jair Bolsonaro (cafe com jornalistas, relatado pela Crusoe)", "T1a", "Frase sobre 'mundo gay' e 'turismo gay'", BR + "congressoemfoco-bolsonaro-mundo-gay-2019.html",
     "o Brasil não pode ser um país do mundo gay, de turismo gay. Temos famílias", "https://congressoemfoco.com.br/noticia/25843/governo-do-maranhao-faz-campanha-contra-turismo-sexual-apos-declaracao-de-bolsonaro", "relato de segunda mao (revista Crusoe via Congresso em Foco); nao e transcricao oficial")
item("B6", "Bolsonaro", "2019-06-14", "Presidente Jair Bolsonaro (cafe com jornalistas)", "T1b", "Critica a decisao do STF que equiparou homofobia ao racismo; alega que prejudica homossexuais", BR + "congressoemfoco-bolsonaro-stf-homofobia-2019-06-14.html",
     "E essa decisão prejudica os próprios homossexuais", "https://www.congressoemfoco.com.br/area/governo/para-bolsonaro-criminalizacao-da-homofobia-prejudica-homossexuais/", "T1b = contesta decisao/politica, nao ataca pessoas; classificacao minha")
item("B7", "Bolsonaro", "2019-06-27", "Presidente (Decreto 9.883)", "T3", "Conselho Nacional de Combate a Discriminacao: 7 membros (1 + 3 orgaos + 3 sociedade civil); sem 'LGBT' no nome", BR + "planalto-decreto9883-2019.html",
     "III - por três representantes da sociedade civil", "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/decreto/D9883.htm")
item("L1", "Lula III", "2023-01-01", "Presidente (Decreto 11.341)", "T4", "Estrutura do MDHC com a Secretaria Nacional dos Direitos das Pessoas LGBTQIA+", BR + "planalto-decreto11341-2023.html",
     "Secretaria Nacional dos Direitos das Pessoas LGBTQIA+", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/decreto/D11341.htm")
item("L2", "Lula III", "2023-04-06", "Presidente (Decreto 11.471)", "T4", "Institui o Conselho Nacional dos Direitos das Pessoas LGBTQIA+ (consultivo e deliberativo)", BR + "planalto-decreto11471-2023.html",
     "órgão colegiado de natureza consultiva e deliberativa", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/decreto/D11471.htm")
item("L3", "Lula III", "2023-06-19", "Presidente (Lei 14.600, art. 28)", "T4", "Rol de competencias do MDHC volta a nomear 'das pessoas LGBTQIA+'", BR + "planalto-lei14600-2023.html",
     "d) das pessoas LGBTQIA+", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/L14600.htm")
item("L4", "Lula III", "2025 (artigo)", "Artigo de opiniao no Congresso em Foco com dados de orcamento", "T3 (contagem declarada)", "Executivo destinou R$ 6,4 mi em 2025 (-20% sobre 2024); emendas parlamentares R$ 23 mi", BR + "congressoemfoco-quem-financia-lgbti-2025.html",
     "Enquanto o Executivo federal destinou apenas R$6,4 milhões para a pauta em 2025", "https://www.congressoemfoco.com.br/artigo/108513/quem-financia-as-politicas-publicas-lgbti-no-brasil", "fonte e opiniao; numero nao conferido no Portal da Transparencia (nao acessado)")
item("C1", "Ditadura 1964-85", "2014 (relatorio)", "Comissao Nacional da Verdade, vol. II", "T5", "'Nao houve politica de Estado formalizada ... de exterminar'; houve perseguicao: 300-500 pessoas/dia levadas a delegacias (SP, 1980)", F8 + "cnv-volume2-oficial-site-cnv-via-wayback.pdf",
     "de 300 a 500 pessoas eram levadas por dia para delegacias", "https://web.archive.org/web/2016id_/http://cnv.memoriasreveladas.gov.br/images/pdf/relatorio/volume_2_digital.pdf")
ev(F8 + "cnv-volume2-oficial-site-cnv-via-wayback.pdf", "Não houve uma política de Estado formalizada e tão coerente no sentido de exterminar os homossexuais", "C1b")
with open(OUTD + "brasil_itens.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(ITEMS[0].keys())); w.writeheader(); w.writerows(ITEMS)

# ---- dados por governo ----
RES = ROOT + "dados/sinan/serie_campo55_uf_ano.csv"
sin = {int(r["ano"]): r for r in csv.DictReader(open(RES)) if r["uf"] == "BR"}
disque = {2017: ("1.720 denuncias (balanco oficial, via CUT; 'numero 8% menor que em 2016')", "cut-disque100-2017.html"),
          2018: ("1.685 denuncias", "mdhc-disque-direitos-humanos-relatorio-2019.pdf"), 2019: ("846 denuncias (-49,8%; total geral +15,4%)", "mdhc-disque-direitos-humanos-relatorio-2019.pdf"),
          2020: ("nao obtido (nao publicado de forma acessivel sem pedir)", ""), 2021: ("nao obtido", ""),
          2022: ("3.948 denuncias (Agencia Brasil citando MDHC)", "agenciabrasil-lgbt-disque-2024-10.html"), 2023: ("6.070 denuncias (idem); ha mudanca de protocolo de coleta segundo o MDHC (pagina nao lida)", "agenciabrasil-lgbt-disque-2024-10.html"),
          2024: ("'mais de 7 mil' denuncias (MPF); jan-set 5.741 (Agencia Brasil)", "mpf-disque100-trans.html")}
anu = {2022: "783 (ed. 2024)", 2023: "2.090 (ed. 2024) / 1.633 (ed. 2025)", 2024: "2.480 (ed. 2025) / 2.567 (ed. 2026)", 2025: "3.481 (ed. 2026)"}
ev(BR + "cut-disque100-2017.html", "Em 2017 foram feitas 1.720 denúncias de violações contra lésbicas, gays, bissexuais, travestis e transexuais, número 8% menor que em 2016", "DQ2017")
ev(F8 + "mdhc-disque-direitos-humanos-relatorio-2019.pdf", "Apenas três grupos (População LGBT, Igualdade Racial e Outros grupos) tiveram diminuição no registro de denúncias (49,8%, 63,4% e 44,2% respectivamente)", "DQ2019")
ev(BR + "agenciabrasil-lgbt-disque-2024-10.html", "No ano anterior, foram feitas 6.070 denúncias, 2.122 a mais que em 2022 (3.948)", "DQ2023")
ev(BR + "mpf-disque100-trans.html", "em 2024, o canal registrou mais de 7 mil denúncias relacionadas à população LGBTI+", "DQ2024")
gov = {2015: "Dilma II", 2016: "Dilma II/Temer", 2017: "Temer", 2018: "Temer", 2019: "Bolsonaro", 2020: "Bolsonaro", 2021: "Bolsonaro", 2022: "Bolsonaro", 2023: "Lula III", 2024: "Lula III", 2025: "Lula III"}
with open(OUTD + "brasil_dados_governo.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["ano", "governo(ano-calendario)", "sinan_notif_interpessoais", "sinan_campo55_lgbtfobia", "pct_lgbtfobia", "sinan_faltante_efetivo_pct", "disque100_lgbt_denuncias", "anuario_racismo_homo_transfobia_BR"])
    for a in range(2015, 2026):
        r = sin[a]; w.writerow([a, gov[a], r["n_interpessoal"], r["m_lgbtfobia"], r["pct_m_lgbt"], round(float(r["pct_m_ign"]) + float(r["pct_m_na"]), 1), disque.get(a, ("", ""))[0], anu.get(a, "")])
with open(OUTD + "verificacao-brasil.tsv", "w") as fh:
    fh.write("row\tstatus\tarquivo\tlocator\ttrecho\n"); [fh.write("\t".join(c) + "\n") for c in CHECK]
bad = [c for c in CHECK if c[1] != "OK"]
print(len(ITEMS), "itens;", len(CHECK), "citacoes;", len(bad), "falharam"); [print(b) for b in bad]
