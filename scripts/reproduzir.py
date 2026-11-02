"""Trilha 1: recalcula os derivados a partir dos derivados distribuídos.

Confere contra o que está commitado. Copia o repositório para .run/replica (ignorado pelo git), roda
cada script abaixo LÁ (REPO_ROOT=réplica, python -I) e compara cada arquivo da réplica com o
original. Nada do repositório é sobrescrito. Exit 0 só se todo script terminar e nenhum arquivo
divergir.

Comparação: bytes idênticos; se diferirem (libm/BLAS de outro sistema), aceita diferença de no
máximo 1 unidade na última casa decimal impressa de cada número (arredondamento), e diz que aceitou.
Número impresso em precisão total (repr do float, >= 15 algarismos significativos): aceita diferença
relativa <= 1e-10 (BLAS multithread muda a ordem das somas entre execuções; observado em
painel_c02/c03 na mesma máquina). PNG (matplotlib) é informativo: não entra na comparação.

Uso: python3 -I scripts/reproduzir.py [--only <trecho do caminho>]
Tempo: ~6 min (s06_analises 2 min; painel_diagnosticos, concordancia_v2, h1_03 e h2_02 30-40 s cada;
C09/C10/R6 na v0.3).
"""

import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
REPLICA = RAIZ / ".run" / "replica"
R3 = "analysis"

# (script, argumentos). Só entram scripts cujas ENTRADAS estão no repositório (derivados, SIDRA,
# Power & Zucco) e que são idempotentes.
PASSOS = [
    ("data/concordancia/concordancia_v2.py", []),
    ("data/painel/painel_f8.py", []),
    ("data/painel/painel_f8.py", ["tse"]),
    ("data/painel/painel_f8.py", ["tse", "brc"]),
    ("data/painel/painel_diagnosticos.py", []),
    (
        "data/painel/painel_c02_indet.py",
        [],
    ),  # reanálise pré-registrada C02 (escrutinio/reanalise/CRITERIOS.md)
    ("data/painel/painel_c03_event_pesos.py", []),  # reanálise pré-registrada C03
    (
        "data/painel/painel_r6_ic_wild_invertido.py",
        [],
    ),  # v0.3 R6: IC por inversão do wild-cluster (forma pré-registrada, R6-PREREGISTRO-FORMA.md)
    # v0.3 C09 (troca de presidente) e C10 (exposição por governo); ordem obrigatória: d1 lê d2 e a
    # estrutura; c10 lê c09_d1
    ("data/presidencia/c09_estrutura.py", []),
    ("data/presidencia/c09_d2_painel.py", []),
    ("data/presidencia/c09_d1_its.py", []),
    ("data/exposicao/c10_estrutura.py", []),
    ("data/exposicao/c10_exposicao.py", []),
    # v0.3 Disque 100: séries e comparações a partir de saidas/d100_por_periodo.csv (a tabulação do
    # microdado bruto, 13 GB, é Trilha 2: data/disque100/README.md)
    ("data/disque100/scripts/d100_series.py", []),
    # C05 (pns_c05_razao_direta.py) e C08 (ggb_c08_numeradores.py) leem o microdado da PNS 2019:
    # Trilha 2 (REPRODUCIBILITY.md)
    ("data/sim/padroniza_idade.py", []),
    ("data/sim/projecao_grupos.py", []),
    ("data/sim/contexto_local.py", []),
    ("data/sinan/serie_tabelas.py", []),
    ("data/scripts/governadores.py", []),
    ("data/scripts/governadores_partido_tse.py", []),
    (f"{R3}/ggb-audit/scripts/s03_sorteio.py", []),
    (f"{R3}/ggb-audit/scripts/s13_sensibilidade_manchete.py", []),
    (f"{R3}/political-economy/scripts/h1_03_analise.py", []),
    (f"{R3}/political-economy/scripts/h1_04_exposicao_2023_exploratorio.py", []),
    (f"{R3}/political-economy/scripts/h2_02_analise.py", []),
    (f"{R3}/ggb-series/series/scripts/s06_analises.py", []),
    (f"{R3}/ideology/scripts/sensibilidade_twfe.py", []),
    (f"{R3}/ideology/scripts/gerar_mapeamento_md.py", []),
    ("analysis/simulation/sim_identificabilidade.py", ["analysis/simulation"]),
]
IGNORA = {".git", ".work", ".run", "__pycache__"}
NUM = re.compile(r"-?\d+\.\d+(?:[eE][-+]?\d+)?")


def arquivos(raiz):
    """Mapa caminho-relativo -> Path de todos os arquivos sob raiz (sem caches)."""
    out = {}
    for p in raiz.rglob("*"):
        if p.is_file() and not (IGNORA & set(p.relative_to(raiz).parts)) and p.suffix != ".pyc":
            out[p.relative_to(raiz).as_posix()] = p
    return out


def equivalentes(a, b):
    """Compara o original ``a`` com o recalculado ``b``.

    Devolve "exato" se iguais; uma descrição da tolerância usada se diferem só em até 1 unidade da
    última casa decimal impressa dos números (ou em precisão total, relativa <= 1e-10); None se
    divergem.
    """
    if a == b:
        return "exato"
    try:
        ta, tb = a.decode("utf-8"), b.decode("utf-8")
    except UnicodeDecodeError:
        return None
    na, nb = NUM.findall(ta), NUM.findall(tb)
    if len(na) != len(nb) or NUM.sub("#", ta) != NUM.sub("#", tb):
        return None
    ulp = False
    for x, y in zip(na, nb, strict=True):  # mesmo tamanho: conferido acima
        casas = len(x.split(".")[1].split("e")[0].split("E")[0])
        if abs(float(x) - float(y)) <= 1.0000001 * 10 ** (-casas):
            continue
        # número impresso em precisão total (repr do float, >= 15 algarismos significativos): a soma
        # em BLAS multithread (Accelerate/OpenBLAS) muda a ordem das parcelas e mexe nos últimos
        # bits de uma execução para outra, mesmo na mesma máquina. Aceita diferença relativa <=
        # 1e-10; números arredondados para impressão continuam na regra de 1 unidade da última casa.
        if len(re.sub(r"\D", "", x.split("e")[0].split("E")[0]).lstrip("0")) >= 15 and abs(
            float(x) - float(y)
        ) <= 1e-10 * max(abs(float(x)), 1e-300):
            ulp = True
            continue
        return None
    return "numérico (<= 1 unidade da última casa" + (
        "; precisão total: diferença relativa <= 1e-10)" if ulp else ")"
    )


def prepara():
    """Recria a réplica do repositório (sem .git, .work, .run)."""
    if REPLICA.exists():
        shutil.rmtree(REPLICA)
    pesados = (
        "sources/public/p3-ggb",
        "sources/public/q1-textointegral",
        "sources/public/p2-sim-microdados",
        "sources/public/p2-sinan-microdados",
        "sources/public/p2-f8-governos/tse",
        "sources/public/pns2019",
    )  # microdado bruto baixado pelos acquire_* (nunca copiar)

    def ignora(pasta, nomes):
        """Nomes a não copiar para a réplica (caches, estado local e microdado bruto)."""
        rel = Path(pasta).relative_to(RAIZ).as_posix()
        return [
            n
            for n in nomes
            if n in (".git", ".work", ".run", "__pycache__", "BUILD-STATE.md")
            or (rel + "/" + n).lstrip("./") in pesados
            or n.endswith((".dbc", ".dbf"))
        ]

    shutil.copytree(RAIZ, REPLICA, ignore=ignora)


def main():
    """Recalcula os passos na réplica, compara arquivo a arquivo e devolve 0 se nada divergir."""
    filtro = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    passos = [p for p in PASSOS if not filtro or filtro in p[0]]
    prepara()
    env = dict(os.environ, REPO_ROOT=str(REPLICA), PYTHONDONTWRITEBYTECODE="1")
    antes = {k: p.stat().st_mtime_ns for k, p in arquivos(REPLICA).items()}
    falhas = 0
    for rel, args in passos:
        t = time.time()
        r = subprocess.run(
            [sys.executable, "-B", "-I", str(REPLICA / rel), *args],
            cwd=str(REPLICA),
            env=env,
            capture_output=True,
            text=True,
        )
        rotulo = rel + (" " + " ".join(args) if args else "")
        if r.returncode:
            falhas += 1
            print(
                f"[FALHOU] {rotulo} (rc={r.returncode}): "
                f"{r.stderr.strip().splitlines()[-1][:200] if r.stderr.strip() else ''}"
            )
        else:
            print(f"[ok] {rotulo} ({time.time() - t:.0f}s)")
        sys.stdout.flush()
    orig, rep = arquivos(RAIZ), arquivos(REPLICA)
    n_exato = n_num = n_png = 0
    for k, p in sorted(orig.items()):
        if k.startswith((".run/", ".work/")) or k == "BUILD-STATE.md" or k not in rep:
            continue
        if rep[k].stat().st_mtime_ns == antes.get(k):
            continue  # o passo não reescreveu este arquivo: não é evidência de recálculo
        if p.suffix == ".png":
            n_png += 1
            continue
        if (a := p.read_bytes()) == (b := rep[k].read_bytes()):
            n_exato += 1
            continue
        eq = equivalentes(a, b)
        if eq:
            n_num += 1
            print(f"[~] {k}: {eq}")
        else:
            falhas += 1
            print(f"[DIVERGE] {k}")
    novos = sorted(k for k in rep if k not in orig)
    if novos:
        print(
            "[info] arquivos gerados que não existem no repositório (não são erro):",
            ", ".join(novos),
        )
    print(
        f"arquivos RECALCULADOS pelos scripts e conferidos com o commitado: "
        f"{n_exato} idênticos byte a byte, {n_num} equivalentes numéricos, "
        f"{n_png} figuras PNG regeneradas (informativas); {falhas} falha(s)/divergência(s)"
    )
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
