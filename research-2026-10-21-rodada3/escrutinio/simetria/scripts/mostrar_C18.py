"""Imprime, por arquivo baixado de um governante, as frases com (tema LGBT) E (marca temporal/ator). Uso: mostrar_C18.py G1 [maxfrases]"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import re, sys, glob, os
D = (REPO_ROOT + "/fontes/q1-textointegral/discurso/simetria/brasil")
g = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 14
ALVO = {"G1": r"Lula|governo|presidente|Brasil sem Homofobia|Ministério|Secretaria|decreto|Pelotas", "G2": r"Lula|governo|presidente|decreto|Conferência|Conselho", "G3": r"Dilma|governo|presidente|decreto|kit|veto", "G4": r"Temer|governo|presidente|decreto|Ministério|orçamento|verba|repasses", "G5": r"Bolsonaro|governo|presidente|decreto|ministr|Ancine|MP 870", "G6": r"Lula|governo|presidente|decreto|ministr|Conselho"}[g]
TEMA = re.compile(r"homossex|gays?\b|LGBT|homofob|lésbic|travest|transex|Brasil sem Homofobia", re.I)
for f in sorted(glob.glob(f"{D}/{g}_Q*.txt")):
    t = open(f).read()
    frases = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕ“\"])", t)
    sel = [s.strip() for s in frases if TEMA.search(s) and re.search(ALVO, s) and 40 < len(s) < 700]
    print(f"\n#### {os.path.basename(f)}  chars={len(t)} frases_candidatas={len(sel)}")
    for s in sel[:mx]:
        print("  -", s[:520])
