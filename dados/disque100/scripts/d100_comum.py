"""Leitura harmonizada dos microdados do Disque 100 (3 formatos, 2011-2026).

Formatos (detectados pelo cabeçalho, nunca pelo nome do arquivo):
- A: 2011-2019, 35 colunas, sem chave (`data_atendimento` ...).
- B: 1º semestre de 2020, 34 colunas, chave `hash_par_vitima_suspeito`.
- C: 2º semestre de 2020 a 3º trimestre de 2026, 62 colunas, chave `hash`; 5 grafias de cabeçalho
  (espaço x sublinhado, `Sexo_`/`Genero_`/`Gênero_`, `(Nenhum nome de coluna)` na posição 13 de
  2023S1). As 62 posições têm o mesmo conteúdo; o nome canônico é o do 2º semestre de 2022.

Só stdlib. Leitura em fluxo (arquivos de até 1,9 GB). Nenhuma função devolve a chave (hash) para
fora: quem precisa dela recebe só para contar, dentro do processo.
"""

import csv
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "raw"
csv.field_size_limit(sys.maxsize)

PERIODOS = [
    ("2011", "disque100-2011.csv"), ("2012", "disque100-2012.csv"), ("2013", "disque100-2013.csv"),
    ("2014", "disque100-2014.csv"), ("2015", "disque100-2015.csv"), ("2016", "disque100-2016.csv"),
    ("2017", "disque100-2017.csv"), ("2018", "disque100-2018.csv"), ("2019", "disque100-2019.csv"),
    ("2020S1", "disque100-primeiro-semestre-2020.csv"), ("2020S2", "disque100-segundo-semestre-2020.csv"),
    ("2021S1", "disque100-primeiro-semestre-2021.csv"), ("2021S2", "disque100-segundo-semestre-2021.csv"),
    ("2022S1", "disque100-primeiro-semestre-2022.csv"), ("2022S2", "disque100-segundo-semestre-2022.csv"),
    ("2023S1", "disque100-primeiro-semestre-2023.csv"), ("2023S2", "disque100-segundo-semestre-2023.csv"),
    ("2024S1", "disque100-primeiro-semestre-2024.csv"), ("2024S2", "disque100-segundo-semestre-2024.csv"),
    ("2025S1", "disque100-primeiro-semestre-2025.csv"), ("2025S2", "disque100-segundo-semestre-2025.csv"),
    ("2026S1", "disque100-primeiro-semestre-2026.csv"), ("2026T3", "disque100-terceiro-trimestre-2026.csv"),
]

CAB_C = (
    "hash;Data_de_cadastro;Canal_de_atendimento;Denúncia_emergencial;Denunciante;Cenário_da_violação;País;UF;"
    "Município;Frequência;Início_das_violações;sl_quantidade_vitimas;Grupo_vulnerável;Motivação;"
    "Relação_vítima_suspeito;sl_vitima_cadastro;Gênero_da_vítima;Orientação_sexual_da_vítima;"
    "Faixa_etária_da_vítima;Nacionalidade_da_vítima;sl_vitima_naturalidade;sl_vitima_naturalizado_uf;"
    "sl_vitima_naturalizado_municipio;Deficiência_da_vítima;Doença_rara_da_vítima;"
    "Deficiência_relacionada_a_doença_rara;Vítima_preso_a;País_da_vítima;UF_da_vítima;Município_da_vítima;"
    "Profissão_da_vítima;Grau_de_instrução_da_vítima;Religião_da_vítima;Raça_Cor_da_vítima;Etnia_da_vítima;"
    "Faixa_de_renda_da_vítima;Natureza_Jurídica_do_Suspeito;Gênero_do_suspeito;Orientação_sexual_do_suspeito;"
    "Faixa_etária_do_suspeito;Suspeito_nacionalidade;sl_suspeito_naturalidade;sl_suspeito_naturalizado_uf;"
    "sl_suspeito_naturalizado_municipio;Deficiência_do_suspeito;Doença_rara_do_suspeito;"
    "Deficiência_relacionada_a_doença_rara_suspeito;Suspeito_preso;País_do_suspeito;UF_do_suspeito;"
    "sl_suspeito_municipio;Profissão_do_suspeito;Grau_de_instrução_do_suspeito;Religião_do_suspeito;"
    "Raça_Cor_do_suspeito;Suspeito_Etnia;Faixa_de_renda_do_suspeito;Vínculo_Órgão_PJ_do_suspeito;"
    "sl_suspeito_ramo;suspeito_especificacao_etnia;vitima_especificacao_etnia;violacao"
).split(";")
assert len(CAB_C) == 62

# Campo harmonizado -> coluna de origem em cada formato (None = não existe no formato).
HARMONIZADO = {
    "data": {"A": "data_atendimento", "B": "Data_da_denúncia", "C": "Data_de_cadastro"},
    "uf": {"A": "vitima_uf", "B": "UF", "C": "UF"},
    "grupo": {"A": "grupo_violacao", "B": "Grupo_vulnerável", "C": "Grupo_vulnerável"},
    "sexo_vitima": {"A": "vitima_sexo", "B": "Gênero_da_vítima", "C": "Gênero_da_vítima"},
    "orientacao_vitima": {"A": "vitima_orientacao_sexual", "B": "orientacao_sexual", "C": "Orientação_sexual_da_vítima"},
    "identidade_vitima": {"A": "vitima_identidade_genero", "B": None, "C": None},
    "sexo_suspeito": {"A": "suspeito_pf_sexo", "B": "Gênero_do_suspeito", "C": "Gênero_do_suspeito"},
    "orientacao_suspeito": {"A": "suspeito_pf_orientacao_sexual", "B": None, "C": "Orientação_sexual_do_suspeito"},
    "violacao": {"A": "violacoes", "B": "violacoes", "C": "violacao"},
    "motivacao": {"A": None, "B": "motivacoes", "C": "Motivação"},
    "chave": {"A": None, "B": "hash_par_vitima_suspeito", "C": "hash"},
    "qtd_vitimas": {"A": None, "B": None, "C": "sl_quantidade_vitimas"},
}


def formato(cab):
    if cab[0] == "data_atendimento" and len(cab) == 35:
        return "A"
    if cab[0] == "hash_par_vitima_suspeito" and len(cab) == 34:
        return "B"
    if cab[0] == "hash" and len(cab) == 62:
        return "C"
    raise ValueError(f"cabeçalho desconhecido: {cab[:3]} ({len(cab)} colunas)")


def caminho(periodo):
    return RAW / dict(PERIODOS)[periodo]


def ler(periodo, path=None):
    """Gera (formato, dict canônico) por linha. Em C, os nomes vêm de CAB_C por posição."""
    p = Path(path) if path else caminho(periodo)
    with open(p, encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f, delimiter=";", quotechar='"')
        cab = [c.strip() for c in next(r)]
        fmt = formato(cab)
        nomes = CAB_C if fmt == "C" else cab
        n = len(nomes)
        for lin in r:
            if len(lin) != n:
                yield fmt, None  # linha malformada: quem chama conta, não descarta em silêncio
                continue
            yield fmt, dict(zip(nomes, lin))


def campo(fmt, row, nome):
    col = HARMONIZADO[nome][fmt]
    return None if col is None else row[col].strip()


_ESP = re.compile(r"\s+")


def norm(v):
    """Rótulo normalizado: maiúsculas, espaços colapsados (só para comparar rótulos)."""
    return _ESP.sub(" ", (v or "").strip()).upper()


_D1 = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
_D2 = re.compile(r"^(\d{2})/(\d{2})/(\d{4})")


def data_iso(v):
    """'AAAA-MM-DD' a partir das duas grafias dos arquivos (ISO e dd/mm/aaaa); None se não reconhece."""
    v = (v or "").strip()
    m = _D1.match(v)
    if m:
        return f"{m[1]}-{m[2]}-{m[3]}"
    m = _D2.match(v)
    if m:
        return f"{m[3]}-{m[2]}-{m[1]}"
    return None


# ---------------------------------------------------------------------------------------------
# REGRAS DE CLASSIFICAÇÃO (pré-registradas: o sha256 deste arquivo entra no PREREGISTRO-D100.md).
# Todas recebem o rótulo VERBATIM e trabalham sobre norm(rótulo). Ordem das regras = ordem de teste.
# ---------------------------------------------------------------------------------------------

def faltante(v):
    """Taxonomia de faltante: 'ausente' (NULL/vazio), 'nao_informado' (N/D, não informado, não sabe),
    'nao_se_aplica', ou None (é valor). Zero NÃO é faltante: é contagem 0 de uma categoria que existe."""
    n = norm(v)
    if n in ("", "NULL"):
        return "ausente"
    if re.search(r"N[AÃ]O SE APLICA", n):
        return "nao_se_aplica"
    if n in ("N/D", "NA", "NI", "( )", "()") or re.search(r"N[AÃ]O INFORMAD|N[AÃ]O SABE|N[AÃ]O SOUBE|ATENDIMENTO INTERROMPIDO", n):
        return "nao_informado"
    return None


RE_LGBT_GRUPO = re.compile(r"LGBT")
RE_SOGI = re.compile(r"ORIENTA[CÇ][AÃ]O SEXUAL|IDENTIDADE DE G[EÊ]NERO|IDEOLOGIA DE G[EÊ]NERO|LGBT|HOMOFOB|TRANSFOB|"
                     r"LESBOFOB|BIFOB")
RE_TRANS = re.compile(r"TRANS|TRAVESTI|N[AÃ]O.BIN[AÁ]RI")
RE_LGB = re.compile(r"HOMOSSEXUAL|\bGAY\b|L[EÉ]SBICA|BISSEXUAL|PANSEXUAL|ASSEXUAL")


def grupo_lgbt(v):
    """I1: a linha está no grupo/módulo LGBT do Disque 100 (A: 'LGBT'; B/C: '... LGBTQIA+')."""
    return bool(RE_LGBT_GRUPO.search(norm(v)))


def sogi_vitima(fmt, row):
    """I2: SOGI DECLARADA da vítima, por formato (classes NÃO harmonizadas entre formatos).
    Devolve uma classe: trans | lgb | intersexo | lgbt_genero (B: Gênero 'LGBTQIA+') | nao_lgbt (hétero
    declarado) | nao_rotulo_nao (C: rótulo literal 'NÃO', sentido não documentado) | cis_ou_indef (A: identidade
    Feminina/Masculina) | nao_informado | ausente | nao_se_aplica | outro."""
    if fmt == "A":
        o, i = norm(row["vitima_orientacao_sexual"]), norm(row["vitima_identidade_genero"])
        if RE_TRANS.search(i):
            return "trans"
        if RE_LGB.search(o) or RE_LGB.search(i):
            return "lgb"
        if "HETEROSSEXUAL" in o or "HETEROSSEXUAL" in i:
            return "nao_lgbt"
        if i in ("FEMININA", "MASCULINA"):
            return "cis_ou_indef"
        fs = {faltante(o), faltante(i)}
        for k in ("nao_informado", "nao_se_aplica", "ausente"):  # se um dos campos foi perguntado, vale 'nao_informado'
            if k in fs:
                return k
        return "outro"
    if fmt == "B":
        o, g = norm(row["orientacao_sexual"]), norm(row["Gênero_da_vítima"])
        if RE_TRANS.search(o):
            return "trans"
        if RE_LGB.search(o):
            return "lgb"
        if RE_LGBT_GRUPO.search(g):
            return "lgbt_genero"
        return faltante(o) or "outro"
    o, g = norm(row["Orientação_sexual_da_vítima"]), norm(row["Gênero_da_vítima"])
    if RE_TRANS.search(o) or RE_TRANS.search(g):
        return "trans"
    if RE_LGB.search(o):
        return "lgb"
    if "INTERSEX" in o or "INTERSEX" in g:
        return "intersexo"
    if "HETEROSSEXUAL" in o:
        return "nao_lgbt"
    if o == "NÃO":
        return "nao_rotulo_nao"
    return faltante(o) or "outro"


SOGI_LGBT = ("trans", "lgb", "intersexo", "lgbt_genero")  # classes que contam como "LGBT declarado"


def itens(v):
    """Violações/motivações multivaloradas (A e B): itens separados por ';' dentro do campo."""
    return [x.strip() for x in (v or "").split(";") if x.strip() and norm(x) != "NULL"]


def motivacao_sogi(fmt, row):
    """I3a: motivação por orientação/identidade (B: item de `motivacoes`; C: `Motivação`). A: None (não existe)."""
    if fmt == "A":
        return None
    vals = itens(row["motivacoes"]) if fmt == "B" else [row["Motivação"]]
    return any(RE_SOGI.search(norm(x)) for x in vals)


def violacoes(fmt, row):
    """Lista de rótulos de violação da linha (A/B: itens; C: o único rótulo)."""
    return itens(row["violacoes"]) if fmt in ("A", "B") else ([row["violacao"]] if norm(row["violacao"]) not in ("", "NULL") else [])


MACRO = [  # primeira que casa vence
    ("vida", r"^VIDA>|HOMIC[IÍ]DIO|FEMINIC[IÍ]DIO|LATROC[IÍ]NIO|GENOC[IÍ]DIO|CHACINA|EXECU[CÇ][AÃ]O SUM[AÁ]RIA|SUIC[IÍ]DIO|"
             r"CRIME_VIDA|ABORTO"),
    ("sexual", r"(?<!ORIENTA[CÇ][AÃ]O )SEXUAL|ESTUPRO|GROOMING|SEXTING|PORNOGRAFIA|PEDOFILIA"),
    ("discriminacao", r"DISCRIMINA|IGUALDADE|RACISMO|INJ[UÚ]RIA RACIAL|HOMOFOBIA"),
    ("institucional", r"INSTITUCIONAL|VIOL[EÊ]NCIA POLICIAL|ABUSO DE AUTORIDADE|PRIS[AÃ]O ILEGAL"),
    ("negligencia", r"NEGLIG[EÊ]NCIA|ABANDONO|INSUBSIST[EÊ]NCIA"),
    ("psicologica", r"PS[IÍ] ?QUICA|PSICOL[OÓ]GICA|AMEA[CÇ]A|HUMILHA|CONSTRANGIMENTO|INJ[UÚ]RIA|CAL[UÚ]NIA|DIFAMA|HONRA|"
                    r"ASS[EÉ]DIO MORAL|PERSEGUI|HOSTILIZA|BULLYING|STALKING|CHANTAGEM|ALIENA[CÇ][AÃ]O PARENTAL"),
    ("fisica", r"F[IÍ]SIC|LES[AÃ]O CORPORAL|MAUS TRATOS|VIAS DE FATO"),
    ("patrimonial", r"PATRIMONI|FINANCEIR|ECON[OÔ]MIC|FURTO|ROUBO|ESTELIONATO|EXTORS|\bBENS\b|PROPRIEDADE"),
    ("liberdade_trabalho", r"LIBERDADE|C[AÁ]RCERE|SEQUESTRO|TR[AÁ]FICO|ESCRAV|TRABALHO|EXPLORA[CÇ][AÃ]O"),
    ("direitos_sociais_civis", r"^DIREITOS SOCIAIS|^DIREITOS CIVIS|DIREITO [AÀ] MEM[OÓ]RIA|SEGURAN[CÇ]A"),
]
_MACRO = [(k, re.compile(p)) for k, p in MACRO]


def macro_violacao(v):
    n = norm(v)
    for k, p in _MACRO:
        if p.search(n):
            return k
    return "outros"


def violacao_sogi(v):
    """I3b: o rótulo da violação nomeia orientação/identidade/LGBT/homofobia (ex.: A 'DISCRIMINAÇÃO.POR ORIENTAÇÃO SEXUAL')."""
    return bool(RE_SOGI.search(norm(v)))


def sexo(v):
    """Sexo/gênero (vítima ou suspeito): feminino | masculino | lgbt_ou_outro | <faltante>."""
    n = norm(v)
    if n.startswith("FEMININ"):
        return "feminino"
    if n.startswith("MASCULIN"):
        return "masculino"
    return faltante(v) or "lgbt_ou_outro"


UFS = ("AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO").split()


def uf(v):
    n = norm(v)
    return n if n in UFS else (faltante(v) or "nao_informado")
