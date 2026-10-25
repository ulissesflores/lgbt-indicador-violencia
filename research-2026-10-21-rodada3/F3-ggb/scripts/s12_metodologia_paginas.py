"""S12. Localiza (pagina do PDF) cada trecho verbatim usado na tabela de metodologia/criterios do GGB por ano.
Saida: dados/metodologia_trechos.csv (ano, arquivo, sha256, pagina_pdf, trecho verbatim, achado). Uso: python3.14 -I s12_metodologia_paginas.py"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[3])  # raiz configurável
import csv, re, subprocess, hashlib
from pathlib import Path
ROOT = Path(REPO_ROOT); PDF = ROOT/"fontes/p3-ggb/_raw/pdf"; D = ROOT/"research-2026-10-21-rodada3/F3-ggb/dados"
def norm(s): return re.sub(r"-\s+(?=[a-zà-ú])", "", re.sub(r"\s+", " ", s))   # junta hifenizacao de fim de linha
def pages(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
    return [norm(subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", str(pdf), "-"], capture_output=True, text=True).stdout) for p in range(1, n+1)]
ITENS = [
 (2017, "ggb2017.pdf", "387 assassinatos e 58 suicídios", "total 445 = 387 homicidios + 58 suicidios; contagem por midia; sem lista nominal"),
 (2018, "ggb2018.pdf", "320 homicídios (76%) e 100 suicídios (24%)", "suicidios 24% (58 em 2017 -> 100 em 2018): composicao muda"),
 (2018, "ggb2018.pdf", "hemeroteca digital", "coleta/sistematizacao por hemeroteca digital 'Homotransfobia Mata' (autor: advogado)"),
 (2019, "ggb2019.pdf", "329 LGBT+ (lésbicas, gays, bissexuais, travestis e transexuais) tiveram morte violenta", "total 2019; 297 homicidios (90,3%) + 32 suicidios (9,7%)"),
 (2019, "ggb2019.pdf", "158 casos com indícios de se tratar de sinistro envolvendo LGBT+, casos posteriormente descartados", "exclusao declarada 1: 158 casos descartados"),
 (2019, "ggb2019.pdf", "termos retirado 58 casos da nossa lista original", "exclusao declarada 2: 58 casos retirados por duvida"),
 (2019, "ggb2019.pdf", "uma planilha no Excel com os seguintes dados: número de registro, data, cidade, estado, região, nome", "variaveis da planilha: inclui fonte e link por caso"),
 (2019, "ggb2019.pdf", "Google ter sinalizado a data de publicação da matéria", "busca diaria no Google com palavras-chave 'encontrado morto', 'professor morto', 'travesti morta'"),
 (2019, "ggb2019.pdf", "profissão mais associada ao segmento", "criterio de inclusao por inferencia: 'se a vitima morava sozinho ou era solteiro, profissao mais associada ao segmento'"),
 (2019, "ggb2019.pdf", "Anexo 3 – Lista de LGBT+ vítimas de mortes violentas no Brasil, em 2019", "UNICA edicao 2017-2025 com lista nominal publicada (329 casos) + Anexo 4 (fonte/link por caso)"),
 (2019, "ggb2019.pdf", "Latrocínio 19", "tipificacao 2019: 272 homicidio, 32 suicidio, 19 latrocinio, 5 atropelamento, 1 silicone industrial"),
 (2020, "ggb2020.pdf", "Google Alerts", "coleta via Google Alerts; leitura e avaliacao em grupo (clipagem -> planilha)"),
 (2020, "ggb2020.pdf", "237 mortes violentas documentas em nossa pesquisa, predominaram os homicídios com 215 (90,71%) registros, seguido de 13 (5,48%) suicídios e, por fim, latrocínio com 9", "2020: 237 = 215 H + 13 S + 9 L (suicidios caem de 32 para 13; relatorio assinado por Acontece + GGB)"),
 (2021, "ggb2021.pdf", "276 homicídios (92%) e 24 suicí", "2021: 300 = 276 H (inclui 34 latrocinios) + 24 S"),
 (2021, "ggb2021.pdf", "listas de óbito de serviços fúnebres", "fontes adicionais declaradas: delegacias, sites de seguranca publica, listas de obito de servicos funebres, familiares/amigos no Facebook e Instagram"),
 (2021, "ggb2021.pdf", "Incluímos assim novos conceitos, como “mulher trans”, “homem trans”", "criterio de busca ampliado; inclusao de 'morte suspeita', 'estado de putrefacao'"),
 (2022, "ggb2022.pdf", "135 mortes violentas de LGBT+, nos primeiros seis meses de 2022", "NAO e o anual: balanco do 1o semestre; anual 2022 so aparece indiretamente (2023: 'um caso a mais')"),
 (2023, "ggb2023.pdf", "257 mortes violentas documentadas, um caso a mais do registrado em 2022", "2023: 257; 2022 = 256 (derivado); 20 casos 'em limbo' fora da contagem"),
 (2023, "ggb2023.pdf", "221 (85,9%) homicídios, incluídos aqui os latrocínios e feminicídios", "homicidio inclui latrocinio e feminicidio; tabela: 204 H + 20 S + 17 L + 16 outras"),
 (2024, "ggb2024.pdf", "273 homicídios e 18 suicídios", "2024: 291 = 273 + 18; 32 casos 'no limbo'"),
 (2024, "ggb2024.pdf", "aprimoramento nas técnicas de coleta e depuração dos dados", "mudanca declarada de metodo em 2024 sem reconciliacao com a serie"),
 (2024, "ggb2024.pdf", "Os seis (6) heterossexuais foram incluídos neste rol", "heterossexuais incluidos (confundidos com LGBT+, defenderam alguem, associados ao espaço)"),
 (2025, "ggb2025.pdf", "237homicídios e 20 suicídio", "destaque 2025: 237 homicidios + 20 suicidios"),
 (2025, "ggb2025.pdf", "204 homicídios, 20 suicídios, 17 latrocínios e 16 casos de outras causas", "corpo 2025: 204 H + 20 S + 17 L + 16 outras = 257; 237 = 204+17+16 (inclui latrocinio e outras)"),
 (2025, "ggb2025.pdf", "Latrocínio contra LGBT devem sempre ser incluídos como crimes homofóbicos", "regra de inclusao declarada: latrocinio entra como crime homofobico"),
 (2025, "ggb2025.pdf", "toda profissional do sexo trans ou travesti vítima de morte violenta na “pista” ou na cena de prostituição, deve ser incluída nessa estatística de crimes homotransfóbicos", "regra de inclusao declarada: toda profissional do sexo trans morta entra"),
 (2025, "ggb2025.pdf", "mais de 10% da população brasileira que é LGBT+", "denominador declarado >10% (PNS 2019: 1,89% LGB+)"),
 (2024, "ggb2024.pdf", "mais de 10% dos brasileiros LGBT+", "denominador declarado >10%"),
 (2025, "ggb2025.pdf", "Lista Geral - 2025 - GGB.xlsx", "planilha caso a caso existe e NAO e publicada"),
 (2025, "ggb2025.pdf", "Não informado 84", "regiao nao informada em 84/257 (32,7%); idade NI 154/257 (59,9%); meio NI 58,4%; local NI 41,2%"),
]
cache = {}; out = []
for ano, arq, trecho, achado in ITENS:
    pdf = PDF/arq
    if arq not in cache: cache[arq] = pages(pdf)
    pg = [i+1 for i, t in enumerate(cache[arq]) if norm(trecho) in t]
    sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    out.append(dict(ano=ano, arquivo=f"fontes/p3-ggb/_raw/pdf/{arq}", sha256=sha, pagina_pdf=";".join(map(str, pg)) or "NAO_LOCALIZADO", trecho_verbatim=trecho, achado=achado))
with (D/"metodologia_trechos.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
for o in out: print(o["ano"], o["pagina_pdf"], "|", o["trecho_verbatim"][:60])
