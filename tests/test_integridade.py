"""Integridade e privacidade: pré-registros com hash travado, ausência de dado nominal/segredo/texto de terceiros, manifestos coerentes."""
import csv
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _util import RAIZ, csv_rows  # noqa: E402

PRE = RAIZ / "docs" / "PRE-REGISTROS"
# PDFs de autoria própria (figuras do paper), não de terceiros. O PDF do artigo (paper/build/) não é distribuído neste commit
PDF_PROPRIO = re.compile(r"^paper/figures/fig\d+_[a-z0-9_]+\.pdf$")
# pré-registros com hash gravado ANTES dos dados: reescrever o caminho de pasta quebraria o hash
CAMINHO_HASH_TRAVADO = {"docs/PRE-REGISTROS/midia/PRE-REGISTRO.md", "docs/PRE-REGISTROS/midia/PRE-REGISTRO.original.md",
                        "research-2026-10-21-rodada3/escrutinio/reanalise/CRITERIOS.md",
                        # v0.3: pré-registros C09/C10 (linha 3 cita a pasta de trabalho; o corpo tem sha256 gravado antes dos desfechos)
                        "dados/presidencia/PREREGISTRO-C09.md", "dados/exposicao/PREREGISTRO-C10.md",
                        # v0.3 (P3): pré-registro do Disque 100 (linha 3: pasta de trabalho de origem; hash do corpo gravado antes das contagens)
                        "dados/disque100/PREREGISTRO-D100.md"}


def _prov():
    """Carrega make_provenance.py da raiz auditada (regra única de exclusão: ver make_provenance.excluido)."""
    spec = importlib.util.spec_from_file_location("_prov_integridade", RAIZ / "make_provenance.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _arquivos():
    # mesmo conjunto do selo: sem caches, sem bruto, sem o artigo (paper.md, build/, tools/) e sem o próprio selo
    excluido = _prov().excluido
    for p in RAIZ.rglob("*"):
        if p.is_file() and not excluido(p.relative_to(RAIZ).as_posix()):
            yield p


def _sha(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------ pré-registros (hash gravado ANTES dos dados)
def test_prereg_governos_texto_original_e_com_adendo():
    b = (PRE / "governos" / "PRE-REGISTRO.md").read_bytes()
    pre = b[: b.index(b"\n---\n\n**ADENDO")]
    gravado = (PRE / "governos" / "PRE-REGISTRO.sha256").read_text().split()[0]
    assert _sha(pre) == gravado == "dc231b3f9cf016ed84582c9fb44b2fc33cd0e4b88e96cb871586537cd5bb40dc"
    assert _sha(b) == (PRE / "governos" / "PRE-REGISTRO-COM-ADENDO.sha256").read_text().split()[0]


def test_prereg_mortalidade_e_midia_original_intacto_e_adendo_so_acrescenta():
    for frente, esperado in (("mortalidade", "a17cf2f7d994ccf4e0cfea86f7abb601750473319765d0d2c0d0918a7d0065f3"),
                             ("midia", "1d1856c0286acb4c61c653c397b7c4fd6976cb235c6a94c383a14965adb4f40b")):
        orig = (PRE / frente / "PRE-REGISTRO.original.md").read_bytes()
        assert _sha(orig) == esperado, frente
        gravado = (PRE / frente / "PRE-REGISTRO.sha256.txt").read_text()
        assert esperado in gravado, frente
        assert (PRE / frente / "PRE-REGISTRO.md").read_bytes().startswith(orig[:2000]), frente  # versão emendada parte do original


# ------------------------------------------------------------------ privacidade
def test_nenhuma_coluna_nominal():
    proibidas = {"nome", "name", "nome_ggb", "nome_tdor", "nome_vitima", "cpf", "email", "telefone"}
    # única exceção: governadores e vices ELEITOS (agentes públicos; dado aberto do TSE), não vítimas
    excecao = {"dados/governadores_tse_eleitos.csv"}
    # coluna 'nome' = nome da FONTE citada na fala (instituição/documento), não de pessoa; conferido abaixo
    fonte_citada = {"research-2026-10-21-rodada3/escrutinio/simetria/baseline_resultado_C27.csv": ("nome", {"", "IBGE", "o Guia",
                                                                                                    "Conselho Federal de Medicina, Sociedade Brasileira de Pediatria e Associação Brasileira de Medicina de Tráfego"})}
    for p in _arquivos():
        rel = p.relative_to(RAIZ).as_posix()
        if p.suffix == ".csv" and rel not in excecao:
            with open(p, encoding="utf-8-sig", newline="") as fh:
                cab = next(csv.reader(fh), [])
            nominais = {c.strip().lower() for c in cab} & proibidas
            if rel in fonte_citada:
                col, permitidos = fonte_citada[rel]
                assert {r[col] for r in csv_rows(rel)} <= permitidos, rel
                nominais -= {col}
            assert not nominais, f"{rel}: coluna nominal {cab}"


def test_ids_de_casos_sao_hash_de_10_hex():
    for rel, col in (("research-2026-10-21-rodada3/F3-ggb/dados/cr_ggb_trans_hash.csv", "id_ggb"),
                     ("research-2026-10-21-rodada3/F3-ggb/dados/ggb2019_universo_hash.csv", "id"),
                     ("research-2026-10-21-rodada3/F3-ggb/dados/codificacao_A.csv", "id"),
                     ("research-2026-10-21-rodada3/F3-ggb/dados/fonte_checks.csv", "id")):
        assert all(re.fullmatch(r"[0-9a-f]{10}", r[col]) for r in csv_rows(rel)), rel


def test_sem_segredo_email_cpf_ou_caminho_de_home():
    padroes = {
        "chave/token": re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_|xox[bap]-|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xai-[A-Za-z0-9]{20,}"
                                  r"|BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|AIza[0-9A-Za-z_-]{30,})"),
        "e-mail": re.compile(r"[A-Za-z0-9._%+-]+@(?!exemplo\.org)(?!\d+x\.(?:png|jpe?g|svg)\b)[A-Za-z0-9-]+\.[A-Za-z]{2,}"),  # '@2x.png' é nome de imagem
        "CPF": re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"),
    }
    for p in _arquivos():
        if p.suffix.lower() in {".png", ".pdf", ".zip", ".gz", ".docx"} or p.name == "test_integridade.py":
            continue  # binários (o DOCX do artigo, conferido por dentro, não é distribuído neste commit: ver REPRODUCIBILITY.md)
        t = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(RAIZ).as_posix()
        for nome, pat in padroes.items():
            achou = pat.search(t)
            assert not achou, f"{rel}: {nome}: {achou.group(0)[:30]}"
        if "/Users/" in t:
            # única exceção: pré-registros com hash gravado (reescrever o caminho quebraria o hash); o caminho é de pasta do projeto
            assert rel in CAMINHO_HASH_TRAVADO and t.count("/Users/") == 1, f"{rel}: caminho de home"


def test_nada_de_terceiros_nem_microdado_bruto():
    proibidos_ext = {".pdf", ".dbc", ".dbf", ".zip", ".xlsx", ".xls", ".html", ".htm"}
    for p in _arquivos():
        rel = p.relative_to(RAIZ).as_posix()
        assert p.suffix.lower() not in proibidos_ext or PDF_PROPRIO.match(rel), rel
        assert not rel.startswith(("fontes/p3-ggb", "fontes/q1-textointegral", "fontes/p2-sim-microdados", "fontes/p2-sinan-microdados")), rel
        assert p.stat().st_size < 10 * 1024 * 1024, f"{rel} grande demais"
        assert "/raw/" not in "/" + rel or rel.startswith("fontes/p2-f8-dados-uf/tabnet/raw/"), rel


# ------------------------------------------------------------------ manifestos
def test_manifesto_de_fontes():
    rows = csv_rows("manifest/MANIFESTO-FONTES.csv")
    a = [r for r in rows if r["parte"] == "A-ledger"]
    b = [r for r in rows if r["parte"] == "B-bruto"]
    assert len(a) >= 800 and len(b) >= 80
    assert all(r["url"] and r["data_acesso_utc"] for r in a)
    assert all(re.fullmatch(r"[0-9a-f]{64}", r["sha256"]) for r in b if r["grupo"] != "GGB 2019")
    ggb = [r for r in b if r["grupo"] == "GGB 2019"]
    assert len(ggb) == 1 and ggb[0]["distribuido_no_repo"] == "nao" and ggb[0]["sha256"] == ""


def test_modificacoes_apontam_arquivos_existentes():
    with open(RAIZ / "manifest" / "MODIFICACOES.tsv", encoding="utf-8") as fh:
        linhas = list(csv.DictReader(fh, delimiter="\t"))
    assert len(linhas) > 100
    for r in linhas:
        assert (RAIZ / r["arquivo"]).exists(), r["arquivo"]
        # "-" só para arquivo criado no repositório na v0.3 (nativo, ou gerado de vários arquivos privados cujos sha256 estão no tipo)
        nativo_novo = r["sha256_original_privado"] == "-" and ("nativo do repositório" in r["tipo"] or "gerado no repositório" in r["tipo"])
        assert (nativo_novo or re.fullmatch(r"[0-9a-f]{64}", r["sha256_original_privado"])) and re.fullmatch(r"[0-9a-f]{64}", r["sha256_publicado"])


def test_scripts_usam_repo_root_em_vez_de_caminho_absoluto():
    for p in _arquivos():
        if p.suffix in {".py", ".sh"} and p.name != "test_integridade.py":
            assert "/Users/" not in p.read_text(encoding="utf-8"), p.relative_to(RAIZ)


# ------------------------------------------------------------------ verificação independente (outra álgebra, outra biblioteca)
def test_verificacao_independente_tudo_ok():
    r = subprocess.run([sys.executable, "-B", "-I", str(RAIZ / "dados" / "verificacao_independente.py")], capture_output=True, text=True,
                       env=dict(os.environ, REPO_ROOT=str(RAIZ)))
    assert r.returncode == 0, r.stdout[-1500:] + r.stderr[-500:]
    assert "RESULTADO: TUDO OK" in r.stdout
    assert r.stdout.count("  OK ") >= 39 and "FALHA" not in r.stdout  # V1 (4) + V2 (3) + V3 (12) + V4 (20) conferências
