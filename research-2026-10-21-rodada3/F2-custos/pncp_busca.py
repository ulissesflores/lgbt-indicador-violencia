#!/opt/homebrew/bin/python3.14
"""Varre contratos do PNCP (API publica de consulta) por orgao e ano e filtra o objeto por regex. Uso: pncp_busca.py <cnpj> <ano_ini> <ano_fim> <regex>"""
import json, re, sys, time, urllib.parse, urllib.request
cnpj, a0, a1, rx = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), re.compile(sys.argv[4], re.I)
tot = 0; hit = []
for ano in range(a0, a1 + 1):
    pag = 1
    while True:
        u = "https://pncp.gov.br/api/consulta/v1/contratos?" + urllib.parse.urlencode({"dataInicial": f"{ano}0101", "dataFinal": f"{ano}1231", "cnpjOrgao": cnpj, "pagina": pag, "tamanhoPagina": 500})
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}), timeout=90))
        except Exception as e:
            print("ERRO", ano, pag, e); break
        d = r.get("data") or []
        tot += len(d)
        for c in d:
            if rx.search(c.get("objetoContrato") or ""):
                hit.append((ano, c["orgaoEntidade"]["razaoSocial"][:30], c.get("nomeRazaoSocialFornecedor", "")[:40], c.get("valorGlobal"), c.get("dataAssinatura"), (c.get("objetoContrato") or "")[:160], c.get("numeroControlePNCP")))
        if pag >= (r.get("totalPaginas") or 1): break
        pag += 1; time.sleep(0.3)
print(f"{cnpj} {a0}-{a1}: {tot} contratos varridos; {len(hit)} casam /{rx.pattern}/")
for h in hit: print(h)
