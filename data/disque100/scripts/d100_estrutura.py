"""ESTRUTURA dos microdados do Disque 100 (antes do pré-registro): rótulos e unidade, sem desfecho.

Para cada período: formato, linhas lidas e malformadas, intervalo de datas, RÓTULOS distintos (sem
frequência) das colunas categóricas da lista abaixo e o diagnóstico de unidade (quantas linhas por
chave e o que varia dentro da chave). Nenhuma contagem por categoria é gravada aqui (isso é
desfecho e só vem depois do pré-registro). Nenhuma chave (hash), município ou texto livre é gravado.

Uso: /opt/homebrew/bin/python3.14 -I scripts/d100_estrutura.py <periodo>[=<arquivo-amostra>] ...
Saída: saidas/estrutura/<periodo>.json
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d100_comum as dc  # noqa: E402

ROTULOS = {
    "A": ["tipo_atendimento", "grupo_violacao", "sub_grupo_violacao", "vitima_uf", "vitima_faixa_etaria",
          "vitima_sexo", "vitima_identidade_genero", "vitima_orientacao_sexual", "suspeito_pf_sexo",
          "suspeito_pf_identidade_genero", "suspeito_pf_orientacao_sexual", "relacao_suspeito"],
    "B": ["Denunciante", "Canal_de_atendimento", "UF", "Grupo_vulnerável", "Gênero_da_vítima", "idade_vitima",
          "Gênero_do_suspeito", "orientacao_sexual", "Relação_Suspeito_x_Vítima"],
    "C": ["Canal_de_atendimento", "Denunciante", "UF", "UF_da_vítima", "sl_quantidade_vitimas", "Grupo_vulnerável",
          "Motivação", "sl_vitima_cadastro", "Gênero_da_vítima", "Orientação_sexual_da_vítima",
          "Faixa_etária_da_vítima", "Natureza_Jurídica_do_Suspeito", "Gênero_do_suspeito",
          "Orientação_sexual_do_suspeito", "Relação_vítima_suspeito"],
}
MULTI = {"A": ["violacoes"], "B": ["violacoes", "motivacoes", "agravantes"], "C": ["violacao"]}
TETO = 600  # acima disso grava só o número de rótulos distintos

# perfis para o diagnóstico de unidade
VIT = {"A": ["vitima_sexo", "vitima_faixa_etaria", "vitima_orientacao_sexual", "vitima_identidade_genero",
             "vitima_cor_raca", "vitima_cod_municipio"],
       "B": ["Gênero_da_vítima", "idade_vitima", "Raça_cor_da_vítima", "orientacao_sexual"],
       "C": ["Gênero_da_vítima", "Orientação_sexual_da_vítima", "Faixa_etária_da_vítima", "Raça_Cor_da_vítima",
             "sl_vitima_cadastro"]}
SUS = {"A": ["suspeito_pf_sexo", "suspeito_pf_faixa_etaria", "suspeito_pf_cor_raca", "relacao_suspeito"],
       "B": ["Gênero_do_suspeito", "idade_suspeito", "Raça_cor_do_suspeito", "Relação_Suspeito_x_Vítima"],
       "C": ["Gênero_do_suspeito", "Faixa_etária_do_suspeito", "Raça_Cor_do_suspeito", "Natureza_Jurídica_do_Suspeito",
             "Relação_vítima_suspeito"]}
CHAVE = {"A": "data_atendimento", "B": "hash_par_vitima_suspeito", "C": "hash"}  # A: só um substituto


def itens(v):
    return [x.strip() for x in v.split(";") if x.strip()] if v else []


def rodar(periodo, path=None, prefixo=""):
    rot = defaultdict(set)
    linhas = mal = 0
    dmin = dmax = None
    grupos = {}  # chave -> [linhas, set(vit), set(sus), set(viol), qtd]
    trocas = 0
    sem_data = 0
    ult = None
    fmt = None
    for fmt, row in dc.ler(periodo, path):
        if row is None:
            mal += 1
            continue
        linhas += 1
        for c in ROTULOS[fmt]:
            if len(rot[c]) <= TETO:
                rot[c].add(row[c].strip())
        for c in MULTI[fmt]:
            if len(rot[c]) <= TETO:
                rot[c].update(itens(row[c]))
        d = dc.data_iso(dc.campo(fmt, row, "data"))
        if d is None:
            sem_data += 1
        else:
            dmin = d if dmin is None or d < dmin else dmin
            dmax = d if dmax is None or d > dmax else dmax
        k = hash(row[CHAVE[fmt]])
        if k != ult:
            trocas += 1
            ult = k
        g = grupos.get(k)
        if g is None:
            g = grupos[k] = [0, set(), set(), set(), set(), set()]
        g[0] += 1
        g[1].add(hash(tuple(row[c] for c in VIT[fmt])))
        g[2].add(hash(tuple(row[c] for c in SUS[fmt])))
        g[3].add(hash(row[MULTI[fmt][0]]))
        g[5].add(dc.campo(fmt, row, "grupo"))
        if fmt == "C":
            g[4].add(row["sl_quantidade_vitimas"].strip())
    nk = len(grupos)
    rep = [g for g in grupos.values() if g[0] > 1]
    diag = {
        "chave_usada": CHAVE[fmt] + (" (SUBSTITUTO: carimbo de data-hora; não é chave pública)" if fmt == "A" else ""),
        "chaves_distintas": nk,
        "razao_linhas_por_chave": round(linhas / nk, 4) if nk else None,
        "max_linhas_por_chave": max((g[0] for g in grupos.values()), default=0),
        "frac_chaves_com_mais_de_1_linha": round(len(rep) / nk, 4) if nk else None,
        "linhas_da_mesma_chave_contiguas": trocas == nk,
        "entre_chaves_repetidas_frac_com_perfil_de_vitima_variando": round(sum(len(g[1]) > 1 for g in rep) / len(rep), 4) if rep else None,
        "entre_chaves_repetidas_frac_com_perfil_de_suspeito_variando": round(sum(len(g[2]) > 1 for g in rep) / len(rep), 4) if rep else None,
        "entre_chaves_repetidas_frac_com_grupo_vulneravel_variando": round(sum(len(g[5]) > 1 for g in rep) / len(rep), 4) if rep else None,
        "entre_chaves_repetidas_frac_com_violacao_variando": round(sum(len(g[3]) > 1 for g in rep) / len(rep), 4) if rep else None,
    }
    if fmt == "C":
        def qmax(g):
            q = [int(x) for x in g[4] if x.isdigit()]
            return max(q) if q else None
        com_q = [g for g in grupos.values() if qmax(g) is not None]
        diag["frac_chaves_com_qtd_vitimas_constante"] = round(sum(len(g[4]) == 1 for g in grupos.values()) / nk, 4)
        diag["frac_chaves_perfis_de_vitima_distintos_le_qtd_vitimas"] = (
            round(sum(len(g[1]) <= qmax(g) for g in com_q) / len(com_q), 4) if com_q else None)
    out = {
        "periodo": periodo, "formato": fmt, "linhas_lidas": linhas, "linhas_malformadas": mal,
        "data_min": dmin, "data_max": dmax, "linhas_sem_data_reconhecida": sem_data, "unidade": diag,
        "rotulos": {c: (sorted(v) if len(v) <= TETO else f"> {TETO} rótulos distintos") for c, v in rot.items()},
    }
    dest = dc.BASE / "saidas" / "estrutura"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{prefixo}{periodo}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                          encoding="utf-8")
    print(periodo, fmt, linhas, mal, flush=True)


if __name__ == "__main__":
    # "periodo" ou "periodo=caminho" (amostra: grava como amostra-<periodo>.json)
    for a in sys.argv[1:]:
        if "=" in a:
            p, c = a.split("=", 1)
            rodar(p, c, "amostra-")
        else:
            rodar(a)
