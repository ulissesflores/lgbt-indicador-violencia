"""Baixa os casos publicos do TGEU Trans Murder Monitoring (API publica do app Uwazi, sem login; titulos ja anonimizados).
Filtra Brasil localmente. Saida: _raw/tmm/tmm_all.json (sha256 no log) e _raw/tmm/tmm_brasil.csv."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import urllib.request, json, hashlib, csv, pathlib, time, datetime
RAW = pathlib.Path((REPO_ROOT + "/fontes/p3-ggb/_raw/tmm")); RAW.mkdir(parents=True, exist_ok=True)
base = "https://transmurdermonitoring.tgeu.org/api/search?limit=200&from=%d&order=asc&sort=creationDate"
rows, frm = [], 0
while True:
    req = urllib.request.Request(base % frm, headers={"User-Agent": "Mozilla/5.0 (pesquisa academica; leitura publica)"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    rows += d["rows"]; tot = d["totalRows"]; frm += 200
    if frm >= tot: break
    time.sleep(0.5)
blob = json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()
(RAW / "tmm_all.json").write_bytes(blob)
def g(m, k):
    v = m.get(k) or []
    return v[0].get("label") or v[0].get("value") if v else ""
out = []
for r in rows:
    m = r.get("metadata", {})
    if g(m, "country_territory_of_the_murder") != "Brazil": continue
    ts = (m.get("date_of_the_incident") or [{}])[0].get("value")
    dt = datetime.datetime.fromtimestamp(ts, datetime.UTC).date().isoformat() if ts else ""
    out.append(dict(id=r["title"], sharedId=r["sharedId"], data=dt, ano=g(m, "calendar_year"), tdor_period=g(m, "tdor_period__oct_sept_"),
                    cidade=g(m, "city_of_the_murder"), identidade=g(m, "gender_identity_or_expression"), ocupacao=g(m, "occupation"),
                    tipo=g(m, "type_of_homicide_murder"), fonte_info=g(m, "source_of_information_about_the_murder"), reported_by=g(m, "reported_by")))
with (RAW / "tmm_brasil.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print("total", len(rows), "brasil", len(out), "sha256_all", hashlib.sha256(blob).hexdigest())
(RAW / "fetch_log.json").write_text(json.dumps(dict(url_base=base, total_rows=len(rows), brasil=len(out), sha256=hashlib.sha256(blob).hexdigest(), data=datetime.date.today().isoformat())))
