#!/opt/homebrew/bin/python3.14
"""Gera custos-fontes.csv: cada valor com moeda, ano, fonte, pagina/secao, trecho verbatim, sha256 do arquivo local.

Rodar: /opt/homebrew/bin/python3.14 -I custos_fontes.py   (sem argumentos; caminhos fixos do projeto)
Regra: o `trecho_verbatim` TEM de existir no texto extraido do arquivo local (espacos normalizados); se nao existir,
a linha sai com verificado_no_arquivo=NAO e status vira 'ALERTA'. O sha256 e do arquivo baixado (bytes), nao do texto.
Linhas sem arquivo local (ex.: captura por WebFetch) saem com status 'ALERTA' e nota.
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, hashlib, html, re, subprocess, sys
from pathlib import Path

RAIZ = Path((REPO_ROOT + "/fontes/q1-textointegral/F2"))
OUT = Path((REPO_ROOT + "/research-2026-10-21-rodada3/F2-custos/custos-fontes.csv"))
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def texto_pdf_paginas(p):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True).stdout).group(1))
    return [norm(subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", str(p), "-"], capture_output=True, text=True).stdout) for i in range(1, n + 1)]


def texto_html(p):
    b = p.read_bytes()
    try: t = b.decode("utf8")
    except UnicodeDecodeError: t = b.decode("latin1")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S | re.I)
    t = re.sub(r"<(br|/p|/div|/li|/tr|/h\d)[^>]*>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(t)


def localizar(arq, trecho):
    p = RAIZ / arq
    t = norm(trecho)
    if p.suffix == ".pdf":
        for i, pg in enumerate(texto_pdf_paginas(p), 1):
            if t in pg:
                return True, f"p.{i}"
        return False, ""
    txt = texto_html(p) if p.suffix in (".html", ".htm") else p.read_text(encoding="utf8", errors="replace")
    linhas = txt.splitlines()
    full = norm(txt)
    if t in full:
        # secao = linha (aprox.) onde o trecho comeca
        pri = norm(trecho).split(" ")[0]
        for i, l in enumerate(linhas, 1):
            if pri in l:
                return True, f"linha {i} do texto extraido"
        return True, "texto extraido"
    return False, ""


# id, item, valor, moeda, ano, unidade, tipo, url, arquivo, trecho, status_base, nota
R = []
def r(*a): R.append(a)

IBGE = "https://www.ibge.gov.br/np_download/novoportal/documentos_institucionais"
r("C01", "TED MS-IBGE 'PNS-2024': valor global (MINUTA, n.o XX/2023)", 22291444, "BRL", 2023, "R$ total", "custo",
  f"{IBGE}/ted/Plano_de_Trabalho_TED_119_2023_PNS.pdf", "custos/Plano_de_Trabalho_TED_119_2023_PNS.pdf", "22.291.444,00", "OK",
  "Documento e MINUTA ('TED n.o XX/2023'; metadata 'MINUTA_Plano_de_Trabalho'); objeto 'PNS-2024', coleta nov/2024-fev/2025, mas a coleta real da PNS e jul-nov/2026: valor final/aditivos NAO verificados. Naturezas 3390.14/30/33/36/39/40 = custeio marginal ao MS (sem folha permanente do IBGE). URL: so abre com www.ibge.gov.br.")
r("C02", "TED 'PNS-2024': objeto", "", "", 2023, "texto", "desenho",
  f"{IBGE}/ted/Plano_de_Trabalho_TED_119_2023_PNS.pdf", "custos/Plano_de_Trabalho_TED_119_2023_PNS.pdf", "Realização da Pesquisa Nacional da Saúde - 2024", "OK", "")
r("C03", "TED 'PNS-2024': custos indiretos (manutencao de veiculos)", 2721724, "BRL", 2023, "R$", "custo",
  f"{IBGE}/ted/Plano_de_Trabalho_TED_119_2023_PNS.pdf", "custos/Plano_de_Trabalho_TED_119_2023_PNS.pdf", "Manutenção de veículos no valor de R$ 2.721.724,00 que correspondem a 12,20% do valor global pactuado", "OK", "")
r("C04", "TED 02/2021 MJSP-IBGE: modulos PNAD Continua (Furtos e Roubos + Sensacao de Seguranca) valor total", 3596904, "BRL", 2021, "R$ total", "custo",
  f"{IBGE}/Termo_de_Execucao_Descentralizada_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "custos/TED_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "RECEITA PREVISTA - R$ 3.596.904,00", "OK",
  "Coleta out-dez/2021 (1 trimestre). Custeio marginal ao MJSP (diarias, gasolina, passagens, TI); sem folha do IBGE. Nao e a 'Pesquisa de vitimizacao 2021' com violencia contra a pessoa: so patrimonial + percepcao.")
r("C05", "TED 02/2021: diarias (8.062 diarias x R$177)", 1426974, "BRL", 2021, "R$", "custo",
  f"{IBGE}/Termo_de_Execucao_Descentralizada_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "custos/TED_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "Planejadas 8.062 diárias para a execução do plano de trabalho, cerca de 5,4 diárias", "OK", "1.500 entrevistadores")
r("C06", "TED 02/2021: material de consumo (gasolina)", 616280, "BRL", 2021, "R$", "custo",
  f"{IBGE}/Termo_de_Execucao_Descentralizada_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "custos/TED_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "3390.30 Material de Consumo 616.280,00", "OK", "")
r("C07", "TED 02/2021: passagens e locomocao", 777600, "BRL", 2021, "R$", "custo",
  f"{IBGE}/Termo_de_Execucao_Descentralizada_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "custos/TED_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "3390.33 Passagens 777.600,00", "OK", "")
r("C08", "TED 02/2021: servicos de TI (1.870 pontos de funcao x R$415; unico, nao recorrente)", 776050, "BRL", 2021, "R$", "custo",
  f"{IBGE}/Termo_de_Execucao_Descentralizada_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "custos/TED_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "3390.40 Serviços de Tecnologia da Informação e Comunicação 776.050,00", "OK", "")
r("C09", "TED 02/2021: setores visitados por trimestre", 15000, "", 2021, "setores", "parametro",
  f"{IBGE}/Termo_de_Execucao_Descentralizada_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "custos/TED_02_2021_MJ_IBGE_Plano_de_Trabalho.pdf", "Número de setores a serem visitados no trimestre: 15.000", "OK", "")
r("C10", "TED MDS-IBGE 2023: modulo tematico na PNAD Continua (seguranca alimentar) valor total", 3797283, "BRL", 2023, "R$ total", "custo",
  "https://www.gov.br/mds/pt-br/acesso-a-informacao/licitacoes-e-contratos/termos-de-cooperacao-e-termos-de-execucao-descentralizada/CadastroTEDIBGE2023EspelhoTransferegov.pdf", "custos/MDS_CadastroTEDIBGE2023_Transferegov.pdf", "3.797.283,00", "OK",
  "Espelho Transferegov publicado pelo MDS; vigencia 07/08/2023-31/10/2024. Segundo precedente independente de modulo em PNADC (mesma ordem de grandeza de C04).")
r("C11", "PNAD Continua: amostra-base de domicilios (por trimestre)", 211000, "", 2020, "domicilios", "parametro",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101726.pdf", "custos/liv101726.pdf", "a amostra de domicílios considerada como base tinha 211.000 domicílios", "OK",
  "Texto do plano amostral da PNAD COVID19 (2020), derivada da amostra da PNAD Continua; usado como ordem de grandeza p/ 2021+.")
r("C12", "PNAD Continua: rotacao 1-2(5), tema alocavel a uma visita especifica", "", "", 2023, "texto", "desenho",
  "https://biblioteca.ibge.gov.br/visualizacao/periodicos/3100/rdpc_2023.pdf", "custos/IBGE_rdpc_2023.pdf", "é o 1-2(5), onde um domicílio selecionado para pesquisa é entrevistado um (1) mês e sai da", "OK", "")
r("C13", "PNAD Continua modulo Sensacao de Seguranca: opcao de entrevista por telefone quando ha risco com terceiros", "", "", 2022, "texto", "desenho",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101988.pdf", "custos/liv101988.pdf", "foi oferecida a opção de se fazer a entrevista por telefone mesmo quando o morador selecionado estivesse no", "OK", "Nota tecnica 05/2022")
r("C14", "PNS 2019: domicilios selecionados (amostra planejada)", 108525, "", 2019, "domicilios", "parametro",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101800.pdf", "pns2019/liv101800.pdf", "Brasil 15 096 7 968 8 036 107 628 108 525", "OK", "Tabela de tamanhos de amostra; ultimo numero = domicilios selecionados")
r("C15", "PNS 2019: entrevistas individuais e resposta (Vasconcelos et al. 2023)", 90846, "", 2019, "entrevistas", "parametro",
  "https://doi.org/10.1590/1980-549720230005.supl.1", "../../pns-vasconcelos/vasconcelos.html", "A total of 108,525 households were selected for the interview, and the final sample comprised 90,846 interviews conducted, with a response rate of 96.5%", "OK", "")
r("C16", "PNDS 2023: amostra de domicilios (SOGI p/ 18+; mulheres 15-49 e homens 15-59)", 133000, "", 2023, "domicilios", "parametro",
  "https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/db450d396a021e9bebabb1b436dcd7f8.pdf", "sogi/IBGE_PNDS2023_lancamento.pdf", "Contará com uma amostra de 133 mil", "OK",
  "Custo da PNDS: NAO localizado em fonte primaria (ver fila-aquisicao.jsonl)")
r("C17", "CSEW (Inglaterra e Pais de Gales): contrato PU-18/0001, valor na adjudicacao (sem indexacao)", 18315399, "GBP", 2018, "contrato total", "custo",
  "https://www.find-tender.service.gov.uk/Notice/019482-2022", "custos/FT-019482-2022.html", "Total value of the procurement: £18,315,399", "OK", "Contratado TNS; adjudicado 9/3/2018")
r("C18", "CSEW: valor apos indexacao", 19234018.23, "GBP", 2018, "contrato total", "custo",
  "https://www.find-tender.service.gov.uk/Notice/019482-2022", "custos/FT-019482-2022.html", "£19,234,018.23", "OK", "")
r("C19", "CSEW: valor apos modificacao de julho/2021 (prorroga a 31/3/2024)", 28849818.23, "GBP", 2021, "contrato total", "custo",
  "https://www.find-tender.service.gov.uk/Notice/019482-2022", "custos/FT-019482-2022.html", "Total value of the contract/lot/concession: £28,849,818.23", "OK", "")
r("C20", "CSEW: valor apos modificacao de 2022 (aumento p/ 70.000 entrevistas/ano; painel telefonico)", 34099818.23, "GBP", 2022, "contrato total", "custo",
  "https://www.find-tender.service.gov.uk/Notice/019482-2022", "custos/FT-019482-2022.html", "Value excluding VAT: £34,099,818.23", "OK", "Kantar Public")
r("C21", "CSEW 2024-2029: valor estimado (aviso previo)", 40000000, "GBP", 2022, "contrato total (5 anos)", "custo",
  "https://www.find-tender.service.gov.uk/Notice/017318-2022", "custos/FT-017318-2022.html", "Value excluding VAT: £40,000,000", "OK", "")
r("C22", "CSEW 2024-2029: minimo de entrevistas por ano (modo misto)", 70000, "", 2022, "entrevistas/ano", "parametro",
  "https://www.find-tender.service.gov.uk/Notice/017318-2022", "custos/FT-017318-2022.html", "The contract will require a mixed mode approach to fieldwork to deliver at least 70,000 interviews a year", "OK", "")
r("C23", "CSEW: valor total apos aviso de modificacao de 2025 (Verian)", 40678319, "GBP", 2025, "contrato total", "custo",
  "https://www.find-tender.service.gov.uk/Notice/013329-2025", "custos/FT-013329-2025.html", "Total value of the contract/lot/concession: £40,678,319", "OK", "Verian Group Ltd (ex-Kantar Public UK)")
r("C24", "NCVS (EUA): dotacao FY2013 alocada a operacao e redesenho da NCVS", 36000000, "USD", 2013, "dotacao anual", "custo",
  "https://obamawhitehouse.archives.gov/omb/statistical-programs-2014", "custos/OMB_stat2014.html", "$36.0 million of the appropriation was allocated for the operation and redesign of the National Crime Victimization Survey (NCVS)", "OK",
  "Inclui redesenho; custo real posterior nao verificado (BJS CBJ recente nao localizado)")
r("C25", "NCVS 2013: domicilios e pessoas 12+ entrevistados", 160040, "", 2013, "pessoas 12+", "parametro",
  "https://bjs.ojp.gov/content/pub/pdf/cv13.pdf", "custos/BJS_cv13.pdf", "In 2013, 90,630 households and 160,040 persons age 12 or", "OK", "90.630 domicilios")
r("C26", "FRA EU-LGBTIQ III (survey ONLINE aberto, nao probabilistico): valor total do aviso de adjudicacao", 800000, "EUR", 2022, "contrato total", "custo",
  "https://ted.europa.eu/en/notice/732580-2022", "custos/TEDAPI-732580-2022.json", '"total-value": 800000', "OK", "Dado da API publica do TED (campo total-value, EUR). ~100.000 respostas segundo ILGA-Europe (secundaria, nao lida na fonte): ~EUR 8/resposta, NAO comparavel a amostra probabilistica.")
r("C27", "FRA 'Violence against Women Survey II': valor total do aviso de adjudicacao", 2100000, "EUR", 2022, "contrato total", "custo",
  "https://ted.europa.eu/en/notice/732639-2022", "custos/TEDAPI-732639-2022.json", '"total-value": 2100000', "OK", "Escopo alem do titulo do aviso nao lido (pagina do TED bloqueada por verificacao humana).")
r("C28", "StatCan SSPPS 2018: financiamento (Estrategia federal de violencia de genero)", 9600000, "CAD", 2019, "investimento total", "custo",
  "https://search.open.canada.ca/qpnotes/record/wage%2CWAGE-2019-QP-00021", "custos/QP-2019-00021.html", "Using roughly $9.6M of funding from It", "OK", "Question Period Note de 9/12/2019 (WAGE); 'roughly'; inclui desenvolvimento e analise; nao e custo por entrevista.")
r("C29", "Gambling Survey for Great Britain (push-to-web probabilistico por enderecos): valor do contrato 2025-2029", 4500000, "GBP", 2025, "contrato total (4 anos)", "custo",
  "https://www.contractsfinder.service.gov.uk/Notice/380ef02e-39ac-4210-8d17-375ec5697b11", "custos/CF_GSGB.html", "Value of contract £4,500,000", "OK", "NatCen; 1/11/2025-31/12/2029")
r("C30", "GSGB ano 2 (2024): adultos respondentes", 19714, "", 2024, "respondentes", "parametro",
  "https://www.gamblingcommission.gov.uk/statistics-and-research/publication/statistics-on-gambling-participation-annual-report-year-2-2024-official", "custos/GC_GSGB_year2.html", "data collected from 19,714 adults aged 18 years and older living in Great Britain", "OK", "Resposta por endereco 19% (2023, 2024), alvo 22%")
for _m, _v in (("GBP", "6.70720"), ("USD", "5.01400"), ("EUR", "5.63170"), ("CAD", "3.56920")):
    r("C31" + _m[0], f"Cambio PTAX BCB 2026-10-20 (fechamento, venda): {_m}", float(_v), f"BRL/{_m}", 2026, "taxa", "parametro",
      "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/", f"custos/ptax_{_m}_2026-10-20.json", f'"cotacaoVenda":{_v}', "OK",
      "Conversao nominal de benchmarks estrangeiros p/ R$ (sem correcao de inflacao); so ordem de grandeza")
r("C32", "IPCA (numero-indice, SIDRA 1737 v2266): serie 2018-01 a 2026-09", "", "", 2026, "indice", "parametro",
  "https://apisidra.ibge.gov.br/values/t/1737/n1/1/v/2266/p/201801-202609?formato=json", "custos/sidra1737_ipca_indice.json", '"D3N":"setembro 2026"', "OK", "usado para corrigir R$ para set/2026")
r("C33", "PNS 2026: ~140 mil domicilios (coleta 7/7-30/11/2026)", 140000, "", 2026, "domicilios", "parametro",
  "https://www.otempo.com.br/brasil/2026/7/2/ibge-e-ministerio-lancam-pesquisa-nacional-da-saude-2026", "", "Mais de 140 mil domicílios serão visitados para a coleta de dados", "ALERTA",
  "Captura por WebFetch (resumo por modelo), nao arquivada em bytes; pagina original do IBGE (agencia de noticias 47518) bloqueada a curl/WebFetch (Cloudflare): ver fila-aquisicao.jsonl. Modulos de SOGI/violencia na PNS 2026: NAO verificados.")

linhas = []
for (i, item, val, moeda, ano, un, tipo, url, arq, trecho, st, nota) in R:
    sha = ""; ver = "NAO"; pg = ""
    if arq:
        p = RAIZ / arq
        if not p.exists():
            st = "ALERTA"; nota = (nota + " | ARQUIVO AUSENTE").strip(" |")
        else:
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            ok, pg = localizar(arq, trecho)
            ver = "SIM" if ok else "NAO"
            if not ok:
                st = "ALERTA"; nota = (nota + " | trecho nao encontrado no texto extraido").strip(" |")
    else:
        st = "ALERTA"
    linhas.append(dict(id=i, item=item, valor=val, moeda=moeda, ano=ano, unidade=un, tipo=tipo, fonte_url=url,
                       arquivo_local=str(RAIZ / arq) if arq else "", pagina_ou_secao=pg, trecho_verbatim=trecho, sha256=sha,
                       verificado_no_arquivo=ver, status=st, nota=nota))
with open(OUT, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
    w.writeheader(); w.writerows(linhas)
n_ok = sum(1 for x in linhas if x["status"] == "OK")
print(f"{len(linhas)} linhas; {n_ok} OK; {len(linhas)-n_ok} ALERTA")
for x in linhas:
    if x["status"] != "OK": print("ALERTA", x["id"], x["nota"][:120])
