"""Grava titulo e autor nas propriedades do DOCX (docProps/core.xml) sem renderizar bloco de titulo.

Passar `-M title` ao pandoc escreve o titulo no corpo, acima da capa da casa; por isso os
metadados entram aqui, depois do pandoc. Uso: python3 -I set_core_props.py <docx> <titulo> <autor>
"""
import html
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

path, titulo, autor = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
with zipfile.ZipFile(path) as z:
    names = z.namelist()
    data = {n: z.read(n) for n in names}
core = data["docProps/core.xml"].decode("utf-8")
for tag, val in (("dc:title", titulo), ("dc:creator", autor)):
    novo = f"<{tag}>{html.escape(val)}</{tag}>"
    if re.search(rf"<{tag}>.*?</{tag}>|<{tag}\s*/>", core, flags=re.S):
        core = re.sub(rf"<{tag}>.*?</{tag}>|<{tag}\s*/>", novo, core, count=1, flags=re.S)
    else:
        core = core.replace("</cp:coreProperties>", novo + "</cp:coreProperties>")
data["docProps/core.xml"] = core.encode("utf-8")
tmp = Path(tempfile.mkstemp(suffix=".docx")[1])
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.writestr(n, data[n])
shutil.move(tmp, path)
print(f"[OK] core props: {titulo[:50]}... / {autor}")
