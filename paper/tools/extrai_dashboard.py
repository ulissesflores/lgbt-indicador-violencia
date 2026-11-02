"""Extrai do dashboard_dados.json (projeto privado de publicacao) so os numeros das Figuras 4 e 5.

O JSON original traz caminhos locais de maquina nos campos `origem`; o extrato publico leva so
os valores e o sha256 do original, para que o teste de figura confira extrato -> original
quando o original estiver disponivel.

Uso: python3 -I extrai_dashboard.py <caminho/dashboard_dados.json> <saida.json>
"""
import hashlib
import json
import os
import sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
raw = src.read_bytes()
d = json.loads(raw)
n = d["numeros"]
idiomas = d["datasets_ptbr"]["countryBars"]["lgbt-violencia-fontes-idiomas"]["groups"][0]["items"]
extrato = {
    "origem": "dashboard_dados.json do painel do artigo (projeto de publicação, não distribuído; extrato público completo em dashboard/dashboard_dados.publico.json)",
    "origem_sha256": hashlib.sha256(raw).hexdigest(),
    "fontes_unicas": n["fontes_unicas"]["valor"],
    "funil": n["funil"]["valor"],
    "tipos": n["tipos"]["valor"],
    "faixas_ano": n["faixas_ano"]["valor"],
    "idiomas": {i["name"]: i["value"] for i in idiomas},
}
out.write_text(json.dumps(extrato, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"[OK] {out} (origem sha256 {extrato['origem_sha256'][:12]}...)")
