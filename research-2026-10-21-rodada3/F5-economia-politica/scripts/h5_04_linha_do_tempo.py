"""H5: linha do tempo de medição/orçamento. Cada evento documental tem trecho verbatim CONFERIDO no arquivo local (normalização de espaços) + sha256 do arquivo; cada evento orçamentário
é RECALCULADO dos CSVs desta pasta (h5_orcamento_acoes.csv, h5_acoes_lgbt_rdf_2007_2013.csv, h5_series_chave_acoes.csv) e traz a conta. Saída: dados/h5_linha_do_tempo.csv.
Rodar: /opt/homebrew/bin/python3.14 -I scripts/h5_04_linha_do_tempo.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, hashlib, re, json
import pandas as pd
P = REPO_ROOT; B = f"{P}/research-2026-10-21-rodada3/F5-economia-politica"; D = f"{B}/dados/raw/h5_docs"
norm = lambda s: re.sub(r"\s+", " ", s.replace("­", "")).strip().lower()
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
docs = [
 ("1988", "PNAD 1988: primeiro suplemento nacional de vitimização e justiça (IBGE)", "existiu", "cnj_panorama_pnad2009.txt", "cnj_panorama_pnad2009.pdf", "as pesquisas sobre vitimização e justiça do IBGE de 1988 e 2009"),
 ("2009", "PNAD 2009: reedição do suplemento de vitimização e acesso à justiça, 21 anos depois (cooperação IBGE-CNJ)", "existiu", "cnj_panorama_pnad2009.txt", "cnj_panorama_pnad2009.pdf", "reedição, vinte e um anos depois, do suplemento sobre vitimização e acesso à justiça da Pesquisa Nacional por Amostra de Domicílios (PNAD) de 2009"),
 ("2012-07-04", "Lei 12.681/2012 institui o SINESP (sistema nacional de informações de segurança pública)", "marco legal", "lei12681_2012.html.txt", "lei12681_2012.html", "É instituído o Sistema Nacional de Informações de Segurança Pública, Prisionais e sobre Drogas - SINESP"),
 ("2012-2013", "PNV (MJ/Senasp, Datafolha, CRISP): 'única e primeira' pesquisa de abrangência nacional do Ministério", "existiu", "mj_pnv_estudo.txt", "mj_pnv_estudo.pdf", "Trata-se da única e primeira pesquisa de abrangência nacional já produzida no país"),
 ("2018-06-11", "Lei 13.675/2018 (SUSP), art. 13, VI: o ministério deve 'realizar estudos e pesquisas nacionais ... sobre criminalidade e vitimização'", "marco legal", "lei13675_2018.html.txt", "lei13675_2018.html", "VI - realizar estudos e pesquisas nacionais e consolidar dados e informações estatísticas sobre criminalidade e vitimização"),
 ("2021-T4", "PNAD Contínua 4T/2021: furtos e roubos investigados 'pela primeira vez' (IBGE + MJSP); não abrange violência interpessoal nem motivação", "existiu", "ibge_pnadc2021_furtos_roubos.txt", "ibge_pnadc2021_furtos_roubos.pdf", "investigou, pela primeira vez, no quarto trimestre de 2021"),
 ("2025-08", "FBSP: 'o Brasil ainda não produz pesquisas de vitimização sistemáticas e regulares'; MJSP fez uma única grande pesquisa, em 2012", "nunca repetido", "fbsp_vitimizacao.txt", "fbsp_vitimizacao.pdf", "o Brasil ainda não produz pesquisas de vitimização sistemáticas e regulares"),
 ("2025-08", "FBSP (mesmo documento): MJSP só produziu uma única grande pesquisa de vitimização em sua história, em 2012", "nunca repetido", "fbsp_vitimizacao.txt", "fbsp_vitimizacao.pdf", "só produziu uma única grande pesquisa do tipo em sua história, em 2012"),
]
rows = []
for dt, ev, tp, txt, raw, trecho in docs:
    ok = norm(trecho) in norm(open(f"{D}/{txt}", encoding="utf-8", errors="ignore").read())
    rows.append(dict(data=dt, evento=ev, tipo=tp, conferido_verbatim=ok, trecho=trecho, arquivo=f"dados/raw/h5_docs/{raw}", sha256=sha(f"{D}/{raw}"), conta=""))
    print("OK " if ok else "FALHOU", dt, trecho[:60])
# PNS 2019: orientação 'experimental'
v = open(f"{P}/fontes/pns-vasconcelos/vasconcelos.html", encoding="utf-8", errors="ignore").read(); t = "data on sexual orientation are considered experimental"
rows.append(dict(data="2019-2020", evento="PNS 2019: orientação sexual medida pela 1a vez, rotulada 'experimental' pelo IBGE; sem recorte de identidade de gênero", tipo="existiu", conferido_verbatim=t in v, trecho=t, arquivo="fontes/pns-vasconcelos/vasconcelos.html", sha256=sha(f"{P}/fontes/pns-vasconcelos/vasconcelos.html"), conta=""))
rows.append(dict(data="2026-10-11", evento="PNDS 2023 (orientação sexual e identidade de gênero, 133 mil domicílios): resultados NÃO publicados até esta data", tipo="nunca publicado (evidência negativa)", conferido_verbatim="", trecho="registro de andamento do projeto, NEG:v1 2026-10-11", arquivo="LGBT-INDICADOR-STATE.md", sha256=sha(f"{P}/LGBT-INDICADOR-STATE.md"), conta="reverificar antes de fechar o dossiê (fila-aquisicao F5-H5-pndS2023)"))
# orçamento (recalculado)
o = pd.read_csv(f"{B}/dados/h5_orcamento_acoes.csv"); s = pd.read_csv(f"{B}/dados/h5_series_chave_acoes.csv"); l = pd.read_csv(f"{B}/dados/h5_acoes_lgbt_rdf_2007_2013.csv")
pes = s[s.categoria.str.startswith("IBGE: pesquisas")].groupby("ano").empenhado_real_dez2025.sum() / 1e6
rows.append(dict(data="2019->2020", evento="IBGE, ação 'Pesquisas e estudos estatísticos': execução (empenhado) cai em termos reais", tipo="corte", conferido_verbatim="", trecho="",
    arquivo="dados/h5_series_chave_acoes.csv", sha256=sha(f"{B}/dados/h5_series_chave_acoes.csv"), conta=f"R$ milhões de dez/2025: 2019={pes[2019]:.1f}; 2020={pes[2020]:.1f}; 2021={pes[2021]:.1f}; 2022={pes[2022]:.1f}; 2023={pes[2023]:.1f}; 2024={pes[2024]:.1f}; 2025={pes[2025]:.1f}; variação 2019->2020={(pes[2020]/pes[2019]-1)*100:.0f}%"))
cen = s[s.categoria.str.startswith("IBGE: censos")].groupby("ano").empenhado.sum() / 1e6
rows.append(dict(data="2020-2022", evento="IBGE, ação de Censos: empenhado nominal (Censo 2020 adiado para 2022)", tipo="adiamento", conferido_verbatim="", trecho="", arquivo="dados/h5_series_chave_acoes.csv", sha256=sha(f"{B}/dados/h5_series_chave_acoes.csv"),
    conta=f"R$ milhões nominais: 2019={cen[2019]:.0f}; 2020={cen[2020]:.0f}; 2021={cen[2021]:.0f}; 2022={cen[2022]:.0f}; 2023={cen[2023]:.0f}"))
import unicodedata
sem = lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().upper()
l["acao_n"] = l.acao.map(sem); lg = l[l.acao_n.str.contains("HOMOF|HOMOSS|LGBT|LESBICAS")]
for nome, filt in (("Banco de Dados sobre Cidadania Homossexual e Combate à Homofobia", "BANCO DE DADOS"), ("Núcleos de Pesquisa sobre Cidadania Homossexual e Combate à Homofobia", "NUCLEOS"), ("Produção e Disseminação de Conhecimento para Promoção e Defesa dos Direitos de LGBT (2012) / Promoção e Defesa dos Direitos de LGBT (2013); mesmo código 8810", "PRODUCAO E DISSEMINACAO|PROMOCAO E DEFESA DOS DIREITOS DE LESBICAS")):
    x = lg[lg.acao_n.str.contains(filt)]
    x = x.groupby("ano")[["dotacao_atualizada", "empenhado", "pago"]].sum()
    rows.append(dict(data=f"{x.index.min()}-{x.index.max()}", evento=f"Linha orçamentária específica: {nome}", tipo="existiu (dados/pesquisa LGBT)", conferido_verbatim="", trecho="", arquivo="dados/h5_acoes_lgbt_rdf_2007_2013.csv", sha256=sha(f"{B}/dados/h5_acoes_lgbt_rdf_2007_2013.csv"),
        conta="; ".join(f"{a}: dotação {r.dotacao_atualizada/1e6:.2f}M, empenhado {r.empenhado/1e6:.2f}M, pago {r.pago/1e6:.3f}M" for a, r in x.iterrows()) + " (R$ nominais; 'pago' = valorPago do RDF no exercício, restos a pagar posteriores não aparecem)"))
srv = l[l.acao_n.str.contains("SERVICOS DE PREVENCAO E COMBATE A HOMOFOBIA")].groupby("ano")[["dotacao_atualizada", "empenhado", "pago"]].sum()
rows.append(dict(data=f"{srv.index.min()}-{srv.index.max()}", evento="Linha 'Apoio a Serviços de Prevenção e Combate à Homofobia' (execução, não medição)", tipo="existiu", conferido_verbatim="", trecho="", arquivo="dados/h5_acoes_lgbt_rdf_2007_2013.csv", sha256=sha(f"{B}/dados/h5_acoes_lgbt_rdf_2007_2013.csv"),
    conta="; ".join(f"{a}: dotação {r.dotacao_atualizada/1e6:.2f}M, empenhado {r.empenhado/1e6:.2f}M, pago {r.pago/1e6:.2f}M" for a, r in srv.iterrows())))
c = pd.read_csv(f"{B}/dados/h5_acoes_lgbt_cgu_2014_2025.csv"); cl = c[c.acao.str.contains("LESBICAS|LGBT")].groupby("ano").empenhado_nominal.sum()
anos_com = sorted(cl.index); anos_sem = [a for a in range(2014, 2026) if a not in anos_com]
rows.append(dict(data="2014-2025", evento="Ações orçamentárias com nome LGBT ('Lésbicas, Gays, Bissexuais, Travestis e Transexuais' / 'LGBTQIA+') nos 12 arquivos anuais da CGU: presentes só em alguns anos; todas de promoção/defesa de direitos, nenhuma de pesquisa/medição pelo nome",
    tipo="existiu e interrompido (espaço enumerado: 316.210 linhas, regex sobre NOME AÇÃO)", conferido_verbatim="", trecho="", arquivo="dados/h5_acoes_lgbt_cgu_2014_2025.csv", sha256=sha(f"{B}/dados/h5_acoes_lgbt_cgu_2014_2025.csv"),
    conta="empenhado nominal R$ milhões nos anos com a ação: " + "; ".join(f"{a}={v/1e6:.2f}" for a, v in cl.items()) + f" | anos SEM ação com esse nome: {anos_sem}"))
pd.DataFrame(rows).to_csv(f"{B}/dados/h5_linha_do_tempo.csv", index=False); print(len(rows), "eventos")
