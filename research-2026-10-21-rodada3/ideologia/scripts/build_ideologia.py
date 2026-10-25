#!/usr/bin/env python3
"""Rodada 3 / frente IDEOLOGIA — constroi a tabela partido x ano de escores de ideologia partidaria.

Entradas (todas em raw/ ou fontes/, hashes em raw/SHA256SUMS.txt):
  BRC  : raw/df_experts.csv            (Bolognesi, Ribeiro, Codato & Silva 2025, Dataverse 10.7910/DVN/MFIXKW; surveys jul/2018 e jul/2022; 0-10)
  BLS  : fontes/p2-f8-governos/zucco-power-dataverse/bls9_estimates_partiespresidents_long.tab (Zucco & Power 2024; ondas 1990..2021; ~ -1..+1)
  VPARTY: raw/vparty_v2_brazil.csv     (V-Party v2, fev/2022, via pacote vdemdata do V-Dem Institute; eleicoes 2010/2014/2018)
  PREPPS: raw/prepps/PREPPS_Latam_V2.tab (Wiesehomeier, Singer, Ruth-Lovell 2021, Dataverse JLOYIJ; identico ao V1 nas linhas comuns, diff max 0; 2018/19; escala 1-20)
  CHES : raw/ches/la2020_agg.csv       (CHES Latin America 2020; 0-10)
  GPS  : raw/gps/GPS2019_party_level_v2_1.csv (Norris, Global Party Survey 2019; 0-10)
Saidas (pasta ideologia/): ideologia_ondas_observadas.csv, ideologia_partidos_ano.csv, ideologia_correlacoes.csv,
  ideologia_correlacoes_por_ano.csv, ideologia_aliases.csv, impacto_painel_{wiki,tse}.csv, impacto_painel_resumo.md
Somente stdlib. Rodar: python3 -I scripts/build_ideologia.py
"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, math, os, sys, json, collections, itertools
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # .../ideologia
PROJ = REPO_ROOT
RAW = f"{ROOT}/raw"
YEARS = list(range(2010, 2025))

def num(x):
    try:
        v = float(x)
        return None if math.isnan(v) else v
    except (TypeError, ValueError):
        return None

def mean(xs): return sum(xs) / len(xs)
def sd(xs):
    if len(xs) < 2: return None
    m = mean(xs); return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))

# ------------------------------------------------------------------ rotulos canonicos por linhagem
# linhagem -> [(rotulo, ano_ini, ano_fim)]  (rotulo vigente em cada ano; so informativo + flag existia_no_ano)
JANELA = {
 'MDB': [('PMDB', 2010, 2017), ('MDB', 2018, 2024)], 'PSDB': [('PSDB', 2010, 2024)], 'PT': [('PT', 2010, 2024)],
 'PSB': [('PSB', 2010, 2024)], 'PDT': [('PDT', 2010, 2024)], 'PCdoB': [('PCdoB', 2010, 2024)], 'PSOL': [('PSOL', 2010, 2024)],
 'PSTU': [('PSTU', 2010, 2024)], 'PCB': [('PCB', 2010, 2024)], 'PCO': [('PCO', 2010, 2024)], 'UP': [('UP', 2019, 2024)],
 'CID': [('PPS', 2010, 2018), ('Cidadania', 2019, 2024)], 'PV': [('PV', 2010, 2024)],
 'PTB': [('PTB', 2010, 2022)], 'REP': [('PRB', 2010, 2018), ('Republicanos', 2019, 2024)],
 'PL': [('PR', 2010, 2018), ('PL', 2019, 2024)],
 'PP': [('PP', 2010, 2017), ('Progressistas', 2018, 2021), ('PP', 2022, 2024)],
 'DEM': [('DEM', 2010, 2021)], 'PSL': [('PSL', 2010, 2021)], 'UNIAO': [('União Brasil', 2022, 2024)],
 'PSD': [('PSD', 2011, 2024)], 'PODE': [('PTN', 2010, 2015), ('Podemos', 2016, 2024)],
 'PHS': [('PHS', 2010, 2018)], 'PSC': [('PSC', 2010, 2022)], 'PMN': [('PMN', 2010, 2024)],
 'AVANTE': [('PTdoB', 2010, 2016), ('Avante', 2017, 2024)], 'SD': [('SD', 2013, 2024)], 'PROS': [('PROS', 2013, 2022)],
 'PRP': [('PRP', 2010, 2018)], 'PATRIOTA': [('PEN', 2010, 2017), ('Patriota', 2018, 2022)], 'PPL': [('PPL', 2010, 2018)],
 'AGIR': [('PTC', 2010, 2018), ('Agir', 2019, 2024)], 'DC': [('DC', 2010, 2024)], 'PRTB': [('PRTB', 2010, 2024)],
 'PMB': [('PMB', 2015, 2024)], 'NOVO': [('Novo', 2015, 2024)], 'REDE': [('Rede', 2015, 2024)], 'PRD': [('PRD', 2023, 2024)],
}
def existia(lin, y):
    return any(a <= y <= b for _, a, b in JANELA.get(lin, []))
def rotulo(lin, y):
    for r, a, b in JANELA.get(lin, []):
        if a <= y <= b: return r
    return ''

# rotulos como aparecem nos CSV de governadores (wiki e tse) -> linhagem (qualquer ano)
ALIAS = {
 'PMDB': 'MDB', 'MDB': 'MDB', 'PSDB': 'PSDB', 'PT': 'PT', 'PSB': 'PSB', 'PDT': 'PDT', 'PCdoB': 'PCdoB', 'PSOL': 'PSOL',
 'PROS': 'PROS', 'PP': 'PP', 'Progressistas': 'PP', 'DEM': 'DEM', 'PSL': 'PSL', 'União Brasil': 'UNIAO', 'União': 'UNIAO', 'UNIÃO': 'UNIAO',
 'PSD': 'PSD', 'PHS': 'PHS', 'PSC': 'PSC', 'PMN': 'PMN', 'SD': 'SD', 'Solidariedade': 'SD', 'PL': 'PL', 'PR': 'PL',
 'Republicanos': 'REP', 'PRB': 'REP', 'PTB': 'PTB', 'Novo': 'NOVO', 'PPS': 'CID', 'Cidadania': 'CID', 'PV': 'PV', 'Rede': 'REDE',
 'Avante': 'AVANTE', 'Podemos': 'PODE', 'PODE': 'PODE', 'Patriota': 'PATRIOTA', 'PRD': 'PRD',
}
# sucessor quando o rotulo foi incorporado e a onda nao tem o partido (so usado como fallback sinalizado)
SUCESSOR = {'DEM': ('UNIAO', 2021), 'PSL': ('UNIAO', 2021), 'PHS': ('PODE', 2019), 'PSC': ('PODE', 2023), 'PRP': ('PATRIOTA', 2019), 'PPL': ('PCdoB', 2019), 'PROS': ('SD', 2023)}

# ------------------------------------------------------------------ definicao das fontes
# cada fonte: id, dimensao, escala, sentido (+1: maior=direita/conservador; -1: maior=esquerda/liberal), limites (para 0-10) ou None
FONTES = {
 'BRC': dict(nome='Bolognesi-Ribeiro-Codato-Silva (survey ABCP/UFPR de especialistas, jul/2018 e jul/2022)', dim='esq-dir geral', escala='0 (extrema esquerda) a 10 (extrema direita), media de especialistas', sentido=+1, lim=(0, 10)),
 'BLS': dict(nome='Zucco & Power (Brazilian Legislative Surveys; legisladores avaliam os partidos; estimativa bayesiana)', dim='esq-dir geral', escala='aprox. -1 (esquerda) a +1 (direita), estimativa rescalada', sentido=+1, lim=(-1, 1)),
 'VPARTY_ECON': dict(nome='V-Party v2 (V-Dem; v2pariglef, esq-dir ECONOMICA, IRT)', dim='economico', escala='intervalo IRT (0 extrema esquerda .. 6 extrema direita nas categorias; escore continuo ~ -3..+3)', sentido=+1, lim=None),
 'VPARTY_LGBT': dict(nome='V-Party v2 (V-Dem; v2palgbt, apoio a igualdade social LGBT, IRT)', dim='LGBT', escala='intervalo IRT (0 forte oposicao .. 4 forte apoio nas categorias); escore ORIGINAL maior=mais apoio', sentido=-1, lim=None),
 'PREPPS_LR': dict(nome='PREPPS Latam V2 (Wiesehomeier, Singer, Ruth-Lovell; esq-dir geral)', dim='esq-dir geral', escala='1 (esquerda) a 20 (direita)', sentido=+1, lim=(1, 20)),
 'PREPPS_SOC': dict(nome='PREPPS Latam V2 (politica social: aborto, homossexualidade, divorcio, eutanasia)', dim='social/valores (inclui homossexualidade)', escala='1 (liberal) a 20 (contra politicas liberais)', sentido=+1, lim=(1, 20)),
 'CHES_LRGEN': dict(nome='CHES Latin America 2020 (lrgen, ideologia geral)', dim='esq-dir geral', escala='0 (extrema esquerda) a 10 (extrema direita)', sentido=+1, lim=(0, 10)),
 'CHES_SOC': dict(nome='CHES Latin America 2020 (sociallifestyle)', dim='social/valores', escala='0 (liberal) a 10 (conservador) [ver codebook]', sentido=+1, lim=(0, 10)),
 'GPS_ECON': dict(nome='Global Party Survey 2019 (Norris; V4 esq-dir economica)', dim='economico', escala='0 (extrema esquerda economica) a 10 (extrema direita economica)', sentido=+1, lim=(0, 10)),
 'GPS_SOC': dict(nome='Global Party Survey 2019 (Norris; V6 valores sociais)', dim='social/valores', escala='0 (muito liberal) a 10 (muito conservador)', sentido=+1, lim=(0, 10)),
}

# observacoes: lista de dicts  fonte, onda, rotulo_src, linhagem, escore, sd, n, nota
OBS = []
def add_obs(fonte, onda, rot_src, lin, score, sdv=None, n=None, nota=''):
    if score is None: return
    OBS.append(dict(fonte=fonte, onda=onda, rotulo_src=rot_src, linhagem=lin, escore=score, sd=sdv, n=n, nota=nota))

# ---- BRC
BRC18 = {'mdb': 'MDB', 'ptb': 'PTB', 'pdt': 'PDT', 'pt': 'PT', 'dem': 'DEM', 'p_cdo_b': 'PCdoB', 'psb': 'PSB', 'psdb': 'PSDB', 'ptc': 'AGIR', 'psc': 'PSC',
         'pmn': 'PMN', 'prp': 'PRP', 'pps': 'CID', 'pv': 'PV', 'avante': 'AVANTE', 'progressistas': 'PP', 'pstu': 'PSTU', 'pcb': 'PCB', 'prtb': 'PRTB',
         'phs': 'PHS', 'dc': 'DC', 'pco': 'PCO', 'pode': 'PODE', 'psl': 'PSL', 'prb': 'REP', 'psol': 'PSOL', 'pr': 'PL', 'psd': 'PSD', 'ppl': 'PPL',
         'patri': 'PATRIOTA', 'pros': 'PROS', 'sdd': 'SD', 'novo': 'NOVO', 'rede': 'REDE', 'pmb': 'PMB'}
BRC22 = {'mdb': 'MDB', 'uniao': 'UNIAO', 'ptb': 'PTB', 'pdt': 'PDT', 'pt': 'PT', 'p_cdo_b': 'PCdoB', 'psb': 'PSB', 'psdb': 'PSDB', 'agir': 'AGIR', 'psc': 'PSC',
         'pmn': 'PMN', 'cdd': 'CID', 'pv': 'PV', 'avante': 'AVANTE', 'progre': 'PP', 'pstu': 'PSTU', 'pcb': 'PCB', 'prtb': 'PRTB', 'dc': 'DC', 'pco': 'PCO',
         'podemos': 'PODE', 'rep': 'REP', 'psol': 'PSOL', 'pl': 'PL', 'psd': 'PSD', 'patri': 'PATRIOTA', 'pros': 'PROS', 'sdd': 'SD', 'novo': 'NOVO',
         'rede': 'REDE', 'pmb': 'PMB', 'up': 'UP'}
rows = list(csv.DictReader(open(f"{RAW}/df_experts.csv", encoding='utf-8-sig'), delimiter=';'))
BRC_N = {}
for onda, pref, mp in ((2018, 'ideol_18_', BRC18), (2022, 'ideol_22_', BRC22)):
    sel = [r for r in rows if r['id'][:4] == str(onda)]
    BRC_N[onda] = len(sel)
    for k, lin in mp.items():
        vals = [num(r[pref + k]) for r in sel]; vals = [v for v in vals if v is not None]
        add_obs('BRC', onda, pref + k, lin, mean(vals), sd(vals), len(vals), f'n respondentes da onda={len(sel)}')

# ---- BLS
BLS = {'CID': 'CID', 'DEM': 'DEM', 'MDB': 'MDB', 'NOVO': 'NOVO', 'PCDOB': 'PCdoB', 'PDT': 'PDT', 'PL': 'PL', 'PODE': 'PODE', 'PP': 'PP', 'PROS': 'PROS',
       'PSB': 'PSB', 'PSC': 'PSC', 'PSD': 'PSD', 'PSDB': 'PSDB', 'PSL': 'PSL', 'PSOL': 'PSOL', 'PT': 'PT', 'PTB': 'PTB', 'PV': 'PV', 'REDE': 'REDE',
       'REP': 'REP', 'SD': 'SD'}
for r in csv.DictReader(open(f"{PROJ}/fontes/p2-f8-governos/zucco-power-dataverse/bls9_estimates_partiespresidents_long.tab")):
    y = int(r['year']); lin = BLS.get(r['party.or.pres'])
    if y in (2009, 2013, 2017, 2021) and lin:
        add_obs('BLS', y, r['party.or.pres'], lin, num(r['ideo']), num(r['ideo.se']), None, 'ideo.se = erro-padrao posterior; ideo.raw = media bruta')

# ---- V-Party
VP = {'PMDB': 'MDB', 'PSDB': 'PSDB', 'PT': 'PT', 'PSB': 'PSB', 'PDT': 'PDT', 'PFL': 'DEM', 'PR / PL': 'PL', 'PPB': 'PP', 'PTB': 'PTB', 'PRB': 'REP', 'PSD': 'PSD', 'PSL': 'PSL', 'PPS': 'CID'}
SEATS = {}   # (linhagem, ano_eleicao) -> v2paseatshare
for r in csv.DictReader(open(f"{RAW}/vparty_v2_brazil.csv")):
    y = int(float(r['year'])); lin = VP.get(r['v2pashname'])
    if y not in (2010, 2014, 2018) or not lin: continue
    SEATS[(lin, y)] = num(r['v2paseatshare'])
    add_obs('VPARTY_ECON', y, r['v2pashname'], lin, num(r['v2pariglef']), num(r['v2pariglef_sd']), num(r['v2pariglef_nr']), 'eleicao; n = codificadores')
    add_obs('VPARTY_LGBT', y, r['v2pashname'], lin, num(r['v2palgbt']), num(r['v2palgbt_sd']), num(r['v2palgbt_nr']), 'eleicao; n = codificadores; escore original maior=apoio LGBT')

# ---- PREPPS
PP_MAP = {'Democratic Labour Party': 'PDT', 'Democrats': 'DEM', 'Party of the Republic': 'PL', 'Brazilian Democratic Movement': 'MDB', 'Progressives': 'PP',
          'Brazilian Socialist Party': 'PSB', 'Brazilian Social Democracy Party': 'PSDB', "Worker's Party": 'PT', 'Brazilian Labour Party': 'PTB',
          'Brazilian Republican Party': 'REP', 'Social Democratic Party': 'PSD', 'Podemos': 'PODE', 'New Party': 'NOVO', 'Socialism and Liberty Party': 'PSOL',
          'Green Party': 'PV', 'Sustainability Network': 'REDE', 'Social Liberal Party': 'PSL'}
for r in csv.DictReader(open(f"{RAW}/prepps/PREPPS_Latam_V2.tab", encoding='utf-8'), delimiter='\t'):
    if r['country'] != 'Brazil' or not r['partyname_en'].strip(): continue
    lin = PP_MAP.get(r['partyname_en'].strip())
    n = num(r['n_pos'])
    if not lin or n is None or n <= 5: continue          # codebook: filtrar <=5 avaliacoes
    if r['dimensionname'] == 'Left-Right': add_obs('PREPPS_LR', 2018, r['partyname_en'].strip(), lin, num(r['score_pos']), num(r['sd_pos']), int(n), 'survey outono/2018 + meados/2019')
    if r['dimensionname'] == 'Social Policy': add_obs('PREPPS_SOC', 2018, r['partyname_en'].strip(), lin, num(r['score_pos']), num(r['sd_pos']), int(n), 'survey outono/2018 + meados/2019')

# ---- CHES-LA 2020
CH = {'PT': 'PT', 'PSL': 'PSL', 'PP': 'PP', 'PSD': 'PSD', 'MDB': 'MDB', 'PR': 'PL', 'PS': 'PSB', 'PRB': 'REP', 'PSDB': 'PSDB', 'DEM': 'DEM', 'PDT': 'PDT'}
for r in csv.DictReader(open(f"{RAW}/ches/la2020_agg.csv", encoding='latin-1')):
    if r['country_en'] != 'Brazil' or r['president'] == '1': continue
    lin = CH.get(r['party_abb'])
    if not lin: continue
    add_obs('CHES_LRGEN', 2020, r['party_abb'], lin, num(r['lrgen']), None, None, 'survey jul-out/2020; 160 especialistas na regiao')
    add_obs('CHES_SOC', 2020, r['party_abb'], lin, num(r['sociallifestyle']), None, None, 'survey jul-out/2020')

# ---- GPS 2019
GP = {'PRB': 'REP', 'PSB': 'PSB', 'DEM': 'DEM', 'MDB': 'MDB', 'PP': 'PP', 'PSDB': 'PSDB', 'PSL': 'PSL', 'PT': 'PT'}
for r in csv.DictReader(open(f"{RAW}/gps/GPS2019_party_level_v2_1.csv", encoding='utf-8-sig')):
    if r['ISO'] != 'BRA': continue
    lin = GP.get(r['Partyabb'])
    if not lin: continue
    add_obs('GPS_ECON', 2019, r['Partyabb'], lin, num(r['V4_Scale']), None, int(num(r['Experts'])), 'n = especialistas do pais (todos os partidos)')
    add_obs('GPS_SOC', 2019, r['Partyabb'], lin, num(r['V6_Scale']), None, int(num(r['Experts'])), 'n = especialistas do pais')

# ------------------------------------------------------------------ fusoes (regras)
# DEM+PSL -> UNIAO: ponderacao por cadeiras eleitas em 2018 (V-Party v2paseatshare: PFL/DEM 5,7 e PSL 10,1) = pesos .361/.639.
W_DEM = SEATS[('DEM', 2018)] / (SEATS[('DEM', 2018)] + SEATS[('PSL', 2018)])
W_PSL = 1 - W_DEM
by_wave = collections.defaultdict(dict)       # (fonte, onda) -> linhagem -> obs
for o in OBS: by_wave[(o['fonte'], o['onda'])][o['linhagem']] = o
DERIV = []
for (f, w), d in list(by_wave.items()):
    if 'UNIAO' not in d and 'DEM' in d and 'PSL' in d:
        s = d['DEM']['escore'] * W_DEM + d['PSL']['escore'] * W_PSL
        DERIV.append(dict(fonte=f, onda=w, rotulo_src='DEM+PSL', linhagem='UNIAO', escore=s, sd=None, n=None,
                          nota=f'FUSAO DEM+PSL (Uniao Brasil, 2022): media ponderada por cadeiras eleitas em 2018 (DEM {W_DEM:.3f}, PSL {W_PSL:.3f}; V-Party v2 seatshare 5,7 e 10,1). Regra dos autores do BRC: media aritmetica simples'))
    if 'PRD' not in d and 'PTB' in d and 'PATRIOTA' in d:
        s = (d['PTB']['escore'] + d['PATRIOTA']['escore']) / 2
        DERIV.append(dict(fonte=f, onda=w, rotulo_src='PTB+Patriota', linhagem='PRD', escore=s, sd=None, n=None,
                          nota='FUSAO PTB+Patriota (PRD, 2023): media aritmetica simples (cadeiras de 2022 nao obtidas; sem governador do PRD no painel)'))
for o in DERIV:
    OBS.append(o); by_wave[(o['fonte'], o['onda'])][o['linhagem']] = o
# INCORPORACOES (PHS->Podemos 2019, PRP->Patriota 2019, PPL->PCdoB 2019, PSC->Podemos 2023, PROS->SD 2023): o absorvedor MANTEM o proprio escore;
# o absorvido some (nao entra na media). Divergencia explicita com a Tabela 1 de Bolognesi et al. 2025, que usa media aritmetica na coluna 2018 (ver .md).

# ------------------------------------------------------------------ alocacao onda -> ano
def onda_de(fonte, y):
    """devolve (onda, regra) ou None"""
    if fonte == 'BRC':
        return (2018, 'onda mais proxima; <=2020 usa 2018') if y <= 2020 else (2022, 'onda mais proxima; >=2021 usa 2022')
    if fonte == 'BLS':
        # legislaturas: 53a (2007-10) <- onda 2009; 54a (2011-14) <- 2013; 55a (2015-18) <- 2017; 56a (2019-22) <- 2021; 57a (2023-) sem onda publica
        if y <= 2010: return (2009, 'legislatura da onda')
        if y <= 2014: return (2013, 'legislatura da onda')
        if y <= 2018: return (2017, 'legislatura da onda')
        return (2021, 'legislatura da onda' if y <= 2022 else 'EXTRAPOLADO: 57a legislatura sem onda publica (BLS10, 2025, ainda nao liberada)')
    if fonte.startswith('VPARTY'):
        for t in (2018, 2014, 2010):
            if t <= y <= t + 3: return (t, 'mandato da eleicao (t..t+3)')
        return None
    base = {'PREPPS': 2018, 'CHES': 2020, 'GPS': 2019}[fonte.split('_')[0]]
    return (base, f'janela +-2 anos da onda') if abs(y - base) <= 2 else None

def score_row(fonte, y, lin):
    ow = onda_de(fonte, y)
    if not ow: return None
    w, regra = ow; d = by_wave.get((fonte, w), {})
    nota = regra
    o = d.get(lin)
    if o is None and lin in SUCESSOR:
        suc, ano_inc = SUCESSOR[lin]
        if y >= ano_inc and suc in d:
            o = d[suc]; nota += f'; FALLBACK sucessor ({lin} incorporado por {suc} em {ano_inc}; onda sem {lin})'
    if o is None: return None
    return o, w, nota

out_rows = []
for fonte, meta in FONTES.items():
    for lin in JANELA:
        for y in YEARS:
            ex = existia(lin, y)
            if lin in ('UNIAO', 'PRD') and not ex: continue
            r = score_row(fonte, y, lin)
            if not r: continue
            o, w, nota = r
            if o['nota'] and 'FUSAO' in o['nota']: nota += '; ' + o['nota']
            esc = o['escore']
            lim = meta['lim']
            e010 = round((esc - lim[0]) / (lim[1] - lim[0]) * 10, 4) if lim else ''
            out_rows.append(dict(partido=rotulo(lin, y) or lin, linhagem=lin, ano=y, fonte=fonte, dimensao=meta['dim'], escore=round(esc, 4), escala=meta['escala'],
                sentido_original=('maior=direita/conservador' if meta['sentido'] == 1 else 'maior=mais apoio LGBT'),
                escore_direita=round(esc * meta['sentido'], 4), escore_0_10=e010, onda_origem=w, tipo=('onda' if y == w else 'alocado'), dist_anos=abs(y - w),
                n_avaliadores=o['n'] if o['n'] is not None else '', dp=round(o['sd'], 3) if o['sd'] is not None else '', existia_no_ano=int(ex), nota_mapeamento=nota))
with open(f"{ROOT}/ideologia_partidos_ano.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys())); w.writeheader(); w.writerows(out_rows)

with open(f"{ROOT}/ideologia_ondas_observadas.csv", "w", newline='', encoding='utf-8') as f:
    cols = ['fonte', 'dimensao', 'onda', 'linhagem', 'rotulo_src', 'escore', 'escala', 'sd', 'n', 'nota']
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for o in sorted(OBS, key=lambda o: (o['fonte'], o['onda'], o['linhagem'])):
        m = FONTES[o['fonte']]
        w.writerow(dict(fonte=o['fonte'], dimensao=m['dim'], onda=o['onda'], linhagem=o['linhagem'], rotulo_src=o['rotulo_src'], escore=round(o['escore'], 4), escala=m['escala'],
                        sd=round(o['sd'], 3) if o['sd'] is not None else '', n=o['n'] if o['n'] is not None else '', nota=o['nota']))

with open(f"{ROOT}/ideologia_aliases.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['rotulo_nos_csv_de_governadores', 'linhagem', 'rotulos_vigentes']);
    for a, l in sorted(ALIAS.items()): w.writerow([a, l, ';'.join(f'{r} {x}-{y}' for r, x, y in JANELA[l])])

# ------------------------------------------------------------------ correlacoes
def ranks(v):
    idx = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and v[idx[j + 1]] == v[idx[i]]: j += 1
        for k in range(i, j + 1): r[idx[k]] = (i + j) / 2 + 1
        i = j + 1
    return r
def pearson(a, b):
    ma, mb = mean(a), mean(b); sa = math.sqrt(sum((x - ma) ** 2 for x in a)); sb = math.sqrt(sum((x - mb) ** 2 for x in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else None
def fisher_ci(r, n):
    if r is None or n < 4 or abs(r) >= 1: return ('', '')
    z = math.atanh(r); se = 1 / math.sqrt(n - 3); return (round(math.tanh(z - 1.96 * se), 3), round(math.tanh(z + 1.96 * se), 3))

ESQ_CORE = {'PT', 'PSB', 'PDT', 'PCdoB', 'PSOL', 'PSTU', 'PCB', 'PCO', 'UP'}   # nucleo de esquerda p/ variante binaria (share de meses de governo)
ESQ = {'PT', 'PSB', 'PDT', 'PCdoB', 'PSOL', 'PSTU', 'PCB', 'PCO', 'UP', 'REDE', 'PV'}   # bloco de esquerda/centro-esquerda (para testar discriminacao DENTRO do centro-direita)
def corr_pair(fa, wa, fb, wb, exclude_derived=True, sem_esquerda=False):
    da, db = by_wave.get((fa, wa), {}), by_wave.get((fb, wb), {})
    common = [l for l in da if l in db and not (exclude_derived and ('FUSAO' in (da[l]['nota'] or '') or 'FUSAO' in (db[l]['nota'] or ''))) and not (sem_esquerda and l in ESQ)]
    if len(common) < (5 if sem_esquerda else 4): return None
    a = [da[l]['escore'] * FONTES[fa]['sentido'] for l in common]; b = [db[l]['escore'] * FONTES[fb]['sentido'] for l in common]
    rs = pearson(ranks(a), ranks(b)); rp = pearson(a, b)
    lo, hi = fisher_ci(rs, len(common))
    return dict(n=len(common), spearman=round(rs, 3), spearman_ic95_aprox=f'[{lo}, {hi}]', pearson=round(rp, 3), partidos=' '.join(sorted(common)))

waves = sorted({(o['fonte'], o['onda']) for o in OBS})
corr_rows = []
for (fa, wa), (fb, wb) in itertools.combinations(waves, 2):
    if fa == fb and wa == wb: continue
    if fa.split('_')[0] == fb.split('_')[0] and fa != fb and wa == wb and fa.startswith('VPARTY') is False and fa.split('_')[0] in ('CHES', 'GPS', 'PREPPS'):
        pass  # permite pares de dimensoes da mesma pesquisa (ex.: economico x social) — sao informativos
    for sub, flag in (('todos', False), ('sem bloco de esquerda (PT,PSB,PDT,PCdoB,PSOL,PV,Rede,...)', True)):
        c = corr_pair(fa, wa, fb, wb, sem_esquerda=flag)
        if c: corr_rows.append(dict(fonteA=fa, ondaA=wa, dimA=FONTES[fa]['dim'], fonteB=fb, ondaB=wb, dimB=FONTES[fb]['dim'], defasagem_anos=abs(wa - wb), subconjunto=sub, **c))
with open(f"{ROOT}/ideologia_correlacoes.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(corr_rows[0].keys())); w.writeheader(); w.writerows(sorted(corr_rows, key=lambda r: (r['subconjunto'], r['fonteA'], r['ondaA'], r['fonteB'], r['ondaB'])))

# por ano calendario: usa os escores ALOCADOS (so linhagens sem fusao/fallback, existia_no_ano) e compara fontes entre si
by_year = collections.defaultdict(lambda: collections.defaultdict(dict))   # ano -> fonte -> lin -> escore_direita
for r in out_rows:
    if 'FUSAO' in r['nota_mapeamento'] or 'FALLBACK' in r['nota_mapeamento']: continue
    by_year[r['ano']][r['fonte']][r['linhagem']] = r['escore_direita']
py = []
for y in YEARS:
    fs = sorted(by_year[y])
    for fa, fb in itertools.combinations(fs, 2):
        common = [l for l in by_year[y][fa] if l in by_year[y][fb]]
        if len(common) < 5: continue
        a = [by_year[y][fa][l] for l in common]; b = [by_year[y][fb][l] for l in common]
        rs = pearson(ranks(a), ranks(b)); py.append(dict(ano=y, fonteA=fa, fonteB=fb, n=len(common), spearman=round(rs, 3), pearson=round(pearson(a, b), 3)))
with open(f"{ROOT}/ideologia_correlacoes_por_ano.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['ano', 'fonteA', 'fonteB', 'n', 'spearman', 'pearson']); w.writeheader(); w.writerows(py)

# ------------------------------------------------------------------ impacto no painel (NAO altera o painel; recomputa por outro caminho)
D = f"{PROJ}/dados"
LEG = {}   # ideologia_partidos.csv (Bolognesi 2023, 2018) como o painel usa
for r in csv.DictReader(open(f"{D}/ideologia_partidos.csv")):
    if 'Bolognesi' in r['fonte']: LEG[r['partido']] = float(r['escore'])
PAINEL_MAP = {'PMDB': 'MDB', 'PP': 'Progressistas', 'Republicanos': 'PRB', 'PL': 'PR', 'PROS': 'Pros', 'Cidadania': 'PPS', 'Solidariedade': 'SDD', 'SD': 'SDD', 'União Brasil': 'DEM', 'UNIÃO': 'DEM', 'União': 'DEM', 'PSD': 'PSD'}
def painel_atual(p):
    for cand in (p, PAINEL_MAP.get(p, ''), {v: k for k, v in PAINEL_MAP.items()}.get(p, '')):
        if cand in LEG: return LEG[cand]
    return None

def lin_of(p): return ALIAS.get(p.strip())
def alloc_score(fonte, y, lin, as_0_10=False):
    r = score_row(fonte, y, lin)
    if not r: return None
    o = r[0]; m = FONTES[fonte]
    return (o['escore'] - m['lim'][0]) / (m['lim'][1] - m['lim'][0]) * 10 if as_0_10 else o['escore']

resumo = []
for modo, fname in (('wiki', 'governadores_uf_2011_2026.csv'), ('tse', 'governadores_uf_2011_2026_tse.csv')):
    painel = {(r['uf'], int(r['ano'])): float(r['ideologia']) for r in csv.DictReader(open(f"{D}/painel/painel_uf_ano{'_tse' if modo == 'tse' else ''}.csv"))}
    gov = collections.defaultdict(list)
    for r in csv.DictReader(open(f"{D}/{fname}")):
        try:
            a = date.fromisoformat(r['inicio']); b = date.fromisoformat(r['fim']); meses = max(1, (b - a).days / 30.4)
        except Exception:
            meses = 12
        gov[(r['uf'], int(r['ano']))].append((r['partido'].strip(), meses))
    def agg(uf, y, fn):
        num_, den = 0.0, 0.0
        for p, m in gov[(uf, y)]:
            s = fn(p, y)
            if s is None: continue
            num_ += s * m; den += m
        return num_ / den if den else None
    f_atual = lambda p, y: painel_atual(p)
    f_brc = lambda p, y: (alloc_score('BRC', y, lin_of(p)) if lin_of(p) else None)
    f_bls = lambda p, y: (alloc_score('BLS', y, lin_of(p), True) if lin_of(p) else None)
    def f_brc22(p, y):          # limite superior de "safra": onda 2022 para TODOS os anos (com sucessor para partidos extintos)
        lin = lin_of(p); d = by_wave[('BRC', 2022)]
        if lin in d: return d[lin]['escore']
        suc = SUCESSOR.get(lin); return d[suc[0]]['escore'] if suc and suc[0] in d else None
    f_esq = lambda p, y: (1.0 if lin_of(p) in ESQ_CORE else 0.0) if lin_of(p) else None
    out = []; chk = 0; nchk = 0
    for (uf, y) in sorted(painel):
        a = agg(uf, y, f_atual); b = agg(uf, y, f_brc); c = agg(uf, y, f_bls); g22 = agg(uf, y, f_brc22); esq = agg(uf, y, f_esq)
        nchk += 1; chk += (a is not None and abs(round(a, 2) - painel[(uf, y)]) < 1e-9)
        e = (b + c) / 2 if (b is not None and c is not None) else None
        out.append(dict(uf=uf, ano=y, partidos='|'.join(sorted({p for p, _ in gov[(uf, y)]})), ideo_painel_atual=round(a, 3) if a is not None else '', ideo_painel_csv=painel[(uf, y)],
                        ideo_BRC_periodo=round(b, 3) if b is not None else '', ideo_BLS_periodo_0_10=round(c, 3) if c is not None else '', ideo_media_BRC_BLS=round(e, 3) if e is not None else '', ideo_BRC_2022_todos=round(g22, 3) if g22 is not None else '', esq_share=round(esq, 3) if esq is not None else ''))
    with open(f"{ROOT}/impacto_painel_{modo}.csv", "w", newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    both = [(r['ideo_painel_atual'], r['ideo_BRC_periodo']) for r in out if r['ideo_painel_atual'] != '' and r['ideo_BRC_periodo'] != '']
    bb = [(r['ideo_painel_atual'], r['ideo_BLS_periodo_0_10']) for r in out if r['ideo_painel_atual'] != '' and r['ideo_BLS_periodo_0_10'] != '']
    diff = [abs(a - b) for a, b in both]
    resumo.append(dict(modo=modo, uf_anos=len(out), replica_atual_ok=f'{chk}/{nchk}', com_BRC=len(both), com_BLS=len(bb),
        pearson_atual_vs_BRCper=round(pearson([a for a, _ in both], [b for _, b in both]), 4), spearman_atual_vs_BRCper=round(pearson(ranks([a for a, _ in both]), ranks([b for _, b in both])), 4),
        mudam_gt_0_5=sum(d > 0.5 for d in diff), mudam_gt_1=sum(d > 1 for d in diff), mudam_max=round(max(diff), 2),
        pearson_atual_vs_BLS=round(pearson([a for a, _ in bb], [b for _, b in bb]), 4), spearman_atual_vs_BLS=round(pearson(ranks([a for a, _ in bb]), ranks([b for _, b in bb])), 4)))
with open(f"{ROOT}/impacto_painel_resumo.json", "w") as f: json.dump(resumo, f, indent=1, ensure_ascii=False)

print('BRC n respondentes:', BRC_N, ' pesos DEM/PSL:', round(W_DEM, 3), round(W_PSL, 3))
print('linhas partidos_ano:', len(out_rows), '| ondas observadas:', len(OBS), '| pares de correlacao:', len(corr_rows), '| por ano:', len(py))
print(json.dumps(resumo, ensure_ascii=False, indent=1))
