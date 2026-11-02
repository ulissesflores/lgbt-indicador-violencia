"""Procura identificadores (DOI ou URL) nos ledgers sources.jsonl do repositório (raiz = pasta acima de paper/, ou REPO_ROOT)."""
import json
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("REPO_ROOT") or Path(__file__).resolve().parents[2])


def norm(x: str) -> str:
    """Normaliza DOI/URL para comparacao."""
    x = (x or "").strip().lower().rstrip("/")
    for p in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "doi:"):
        if x.startswith(p):
            x = x[len(p):]
    return x


def load():
    """Carrega todos os registros dos ledgers, indexados por id e url normalizados."""
    idx = {}
    for f in sorted(ROOT.glob("**/sources.jsonl")):
        if "/fontes/" in str(f) or "/.run/" in str(f):
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            for k in ("id", "url"):
                v = norm(str(r.get(k, "")))
                if v:
                    idx.setdefault(v, []).append((str(f.relative_to(ROOT)), r))
    return idx


if __name__ == "__main__":
    idx = load()
    for q in sys.argv[1:]:
        qn = norm(q)
        hits = idx.get(qn, [])
        if not hits:
            hits = [h for k, v in idx.items() if qn in k for h in v][:3]
        print(("OK " if hits else "-- ") + q)
        for f, r in hits[:2]:
            print("    ", f, "|", r.get("ano"), "|", str(r.get("titulo"))[:150])
