"""2a etapa: para cada janela anual com perda (500 persistente na ultima pagina), repete mes a mes (itens=100)
e, se ainda 500, quinzena. Salva {id}_m{AAAAMM}_{pag}.json. Perdas finais em _recuperacao_perdas2.json."""
import calendar, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import camara_recupera as c
RAW = c.RAW


def main():
    perdas = json.load(open(RAW + "/_recuperacao_perdas.json"))
    janelas = sorted({(p[0], int(p[2][:4])) for p in perdas})
    novas = []
    for did, ano in janelas:
        for m in range(1, 13):
            if (ano, m) > (2026, 10):
                break
            ult = calendar.monthrange(ano, m)[1]
            p2 = []
            c.janela(did, f"m{ano}{m:02d}", f"{ano}-{m:02d}-01", f"{ano}-{m:02d}-{ult:02d}", p2)
            if p2:
                # quinzenas
                p3 = []
                c.janela(did, f"q{ano}{m:02d}a", f"{ano}-{m:02d}-01", f"{ano}-{m:02d}-15", p3)
                c.janela(did, f"q{ano}{m:02d}b", f"{ano}-{m:02d}-16", f"{ano}-{m:02d}-{ult:02d}", p3)
                novas += p3
        print(did, ano, len(novas), flush=True)
    json.dump(novas, open(RAW + "/_recuperacao_perdas2.json", "w"))
    print("PERDAS2", len(novas))


main()
