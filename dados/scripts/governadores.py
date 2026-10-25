"""Gera dados/governadores_uf_2011_2026.csv: uma linha por governador por ano (UF x ano), com o trecho
do mandato naquele ano (troca de governador no meio do ano = duas linhas).
Fonte: listas 'Lista de governadores do/da <UF>' da Wikipédia pt (HTML baixado em fontes/p2-f8-dados-uf/governadores/).
Curadoria manual das linhas de mandato a partir das tabelas baixadas (ver coluna confianca).
Partido = o que a tabela da fonte indica para o mandato (sigla como na fonte). Vazio = a fonte não trouxe.
TSE não foi cruzado nesta rodada (ver README)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import csv, datetime, os

BASE = REPO_ROOT
OUT = os.path.join(BASE, "dados/governadores_uf_2011_2026.csv")
DL = datetime.date(2026, 10, 11)  # data da coleta
D = lambda s: datetime.date.fromisoformat(s) if s else DL
WIKI = "https://pt.wikipedia.org/wiki/Lista_de_governadores_"

# UF: (URL-slug, [(governador, partido, inicio, fim|None=em exercício na coleta, confianca, obs)])
MANDATOS = {
 "Acre": ("do_Acre", [
   ("Tião Viana", "PT", "2011-01-01", "2019-01-01", "alta", ""),
   ("Gladson Cameli", "PP", "2019-01-01", "2026-04-02", "alta", ""),
   ("Mailza Assis", "PP", "2026-04-02", None, "alta", "")]),
 "Alagoas": ("de_Alagoas", [
   ("Teotônio Vilela Filho", "PSDB", "2011-01-01", "2015-01-01", "alta", ""),
   ("Renan Filho", "PMDB", "2015-01-01", "2022-04-02", "alta", ""),
   ("Klever Loureiro", "sem partido", "2022-04-02", "2022-05-15", "alta", "interino"),
   ("Paulo Dantas", "MDB", "2022-05-15", None, "alta", "")]),
 "Amapá": ("do_Amapá", [
   ("Camilo Capiberibe", "PSB", "2011-01-01", "2015-01-01", "alta", ""),
   ("Waldez Góes", "PDT", "2015-01-01", "2023-01-01", "alta", ""),
   ("Clécio Luís", "União Brasil", "2023-01-01", None, "alta", "")]),
 "Amazonas": ("do_Amazonas", [
   ("Omar Aziz", "PSD", "2011-01-01", "2014-04-04", "alta", ""),
   ("José Melo", "PROS", "2014-04-04", "2017-05-09", "alta", "cassado pelo TSE"),
   ("David Almeida", "PSD", "2017-05-09", "2017-10-04", "alta", "interino"),
   ("Amazonino Mendes", "PDT", "2017-10-04", "2019-01-01", "alta", ""),
   ("Wilson Lima", "PSC", "2019-01-01", "2023-01-01", "alta", ""),
   ("Wilson Lima", "União Brasil", "2023-01-01", "2026-04-04", "alta", "reeleito; renúncia 2026"),
   ("Roberto Cidade", "União Brasil", "2026-04-04", None, "alta", "eleito pela ALE")]),
 "Bahia": ("da_Bahia", [
   ("Jaques Wagner", "PT", "2011-01-01", "2015-01-01", "alta", ""),
   ("Rui Costa", "PT", "2015-01-01", "2023-01-01", "media",
    "linha 2019 da fonte truncada; término 2022 não confirmado no trecho baixado"),
   ("Jerônimo Rodrigues", "PT", "2023-01-01", None, "alta", "")]),
 "Ceará": ("do_Ceará", [
   ("Cid Gomes", "PROS", "2011-01-01", "2015-01-01", "alta", ""),
   ("Camilo Santana", "PT", "2015-01-01", "2022-04-02", "alta", ""),
   ("Izolda Cela", "PDT", "2022-04-02", "2023-01-01", "alta", ""),
   ("Elmano de Freitas", "PT", "2023-01-01", None, "alta", "")]),
 "Distrito Federal": ("do_Distrito_Federal", [
   ("Agnelo Queiroz", "PT", "2011-01-01", "2015-01-01", "alta", ""),
   ("Rodrigo Rollemberg", "PSB", "2015-01-01", "2019-01-01", "alta", ""),
   ("Ibaneis Rocha", "MDB", "2019-01-01", "2023-01-09", "alta", "afastado"),
   ("Celina Leão", "PP", "2023-01-09", "2023-03-15", "alta", "interina"),
   ("Ibaneis Rocha", "MDB", "2023-03-15", "2026-03-30", "alta", "retorno"),
   ("Celina Leão", "PP", "2026-03-30", None, "alta", "")]),
 "Espírito Santo": ("do_Espírito_Santo", [
   ("Renato Casagrande", "PSB", "2011-01-01", "2015-01-01", "alta", ""),
   ("Paulo Hartung", "PMDB", "2015-01-01", "2019-01-01", "alta", ""),
   ("Renato Casagrande", "PSB", "2019-01-01", "2023-01-01", "alta", ""),
   ("Renato Casagrande", "PSB", "2023-01-01", "2026-04-01", "media", "CORRIGIDO 2026-10-21: o CSV tinha Ricardo Ferraço (vice) em 2023; TSE 2022: eleito governador = Renato Casagrande (PSB). Data de saída 2026-04 herdada, não conferida"),
   ("Ricardo Ferraço", "MDB", "2026-04-02", None, "alta", "vice assumiu")]),
 "Goiás": ("de_Goiás", [
   ("Marconi Perillo", "PSDB", "2011-01-01", "2018-04-07", "alta", "reeleito 2014"),
   ("José Eliton Júnior", "", "2018-04-07", "2019-01-01", "media",
    "vice assumiu; partido do vice não aparece no trecho baixado"),
   ("Ronaldo Caiado", "DEM", "2019-01-01", "2023-01-01", "alta", ""),
   ("Ronaldo Caiado", "União Brasil", "2023-01-01", "2026-03-31", "media", "CORRIGIDO 2026-10-21: o CSV tinha Daniel Vilela (vice) em 2023; TSE 2022: eleito governador = Ronaldo Caiado (UNIÃO). Data de saída 2026-03 herdada, não conferida"),
   ("Daniel Vilela", "MDB", "2026-03-31", None, "alta", "vice assumiu; partido como listado")]),
 "Maranhão": ("do_Maranhão", [
   ("Roseana Sarney", "PMDB", "2011-01-01", "2014-12-10", "alta", ""),
   ("Arnaldo Melo", "PMDB", "2014-12-10", "2015-01-01", "alta", "interino"),
   ("Flávio Dino", "PCdoB", "2015-01-01", "2022-04-02", "alta", ""),
   ("Carlos Brandão", "PSB", "2022-04-02", None, "alta", "")]),
 "Mato Grosso": ("de_Mato_Grosso", [
   ("Silval Barbosa", "PMDB", "2011-01-01", "2015-01-01", "alta", ""),
   ("Pedro Taques", "PDT", "2015-01-01", "2019-01-01", "alta", ""),
   ("Mauro Mendes", "DEM", "2019-01-01", "2023-01-01", "alta", ""),
   ("Mauro Mendes", "União Brasil", "2023-01-01", "2026-03-31", "alta", "renúncia 2026"),
   ("Otaviano Pivetta", "Republicanos", "2026-03-31", None, "alta", "vice assumiu")]),
 "Mato Grosso do Sul": ("de_Mato_Grosso_do_Sul", [
   ("André Puccinelli", "PMDB", "2011-01-01", "2015-01-01", "alta", ""),
   ("Reinaldo Azambuja", "PSDB", "2015-01-01", "2023-01-01", "alta", ""),
   ("Eduardo Riedel", "PSDB", "2023-01-01", None, "alta", "")]),
 "Minas Gerais": ("de_Minas_Gerais", [
   ("Antônio Anastasia", "PSDB", "2011-01-01", "2014-04-04", "alta", ""),
   ("Alberto Pinto Coelho", "PP", "2014-04-04", "2015-01-01", "alta", "vice assumiu"),
   ("Fernando Pimentel", "PT", "2015-01-01", "2019-01-01", "alta", ""),
   ("Romeu Zema", "Novo", "2019-01-01", "2026-03-22", "alta", ""),
   ("Mateus Simões", "PSD", "2026-03-22", None, "alta", "vice assumiu")]),
 "Pará": ("do_Pará", [
   ("Simão Jatene", "PSDB", "2011-01-01", "2019-01-01", "alta", "reeleito 2014"),
   ("Helder Barbalho", "MDB", "2019-01-01", "2026-04-02", "alta", "reeleito 2022"),
   ("Hana Ghassan", "MDB", "2026-04-02", None, "alta", "vice assumiu")]),
 "Paraíba": ("da_Paraíba", [
   ("Ricardo Coutinho", "PSB", "2011-01-01", "2019-01-01", "alta", ""),
   ("João Azevêdo", "PSB", "2019-01-01", "2026-04-02", "alta", ""),
   ("Lucas Ribeiro", "PP", "2026-04-02", None, "alta", "vice assumiu")]),
 "Paraná": ("do_Paraná", [
   ("Beto Richa", "PSDB", "2011-01-01", "2018-04-06", "alta", ""),
   ("Cida Borghetti", "PP", "2018-04-06", "2019-01-01", "alta", "vice assumiu"),
   ("Ratinho Júnior", "PSD", "2019-01-01", None, "alta", "")]),
 "Pernambuco": ("de_Pernambuco", [
   ("Eduardo Campos", "PSB", "2011-01-01", "2014-04-04", "alta", ""),
   ("João Lyra Neto", "PSB", "2014-04-04", "2015-01-01", "alta", "vice assumiu"),
   ("Paulo Câmara", "PSB", "2015-01-01", "2023-01-01", "alta", ""),
   ("Raquel Lyra", "PSDB", "2023-01-01", None, "alta", "")]),
 "Piauí": ("do_Piauí", [
   ("Wilson Martins", "PSB", "2011-01-01", "2014-04-04", "alta", ""),
   ("Zé Filho", "PMDB", "2014-04-04", "2015-01-01", "alta", "vice assumiu"),
   ("Wellington Dias", "PT", "2015-01-01", "2022-03-31", "alta", ""),
   ("Regina Sousa", "PT", "2022-03-31", "2023-01-01", "alta", "vice assumiu"),
   ("Rafael Fonteles", "PT", "2023-01-01", None, "alta", "")]),
 "Rio de Janeiro": ("do_Rio_de_Janeiro", [
   ("Sérgio Cabral", "PMDB", "2011-01-01", "2014-04-03", "alta", ""),
   ("Luiz Fernando Pezão", "PMDB", "2014-04-04", "2019-01-01", "alta", ""),
   ("Wilson Witzel", "PSC", "2019-01-01", "2021-04-30", "alta", "afastado"),
   ("Cláudio Castro", "PSC", "2021-05-01", "2026-03-23", "alta", "partido como listado na fonte"),
   ("Ricardo Couto", "", "2026-03-23", None, "alta", "presidente do TJ-RJ no cargo, interino")]),
 "Rio Grande do Norte": ("do_Rio_Grande_do_Norte", [
   ("Rosalba Ciarlini", "DEM", "2011-01-01", "2015-01-01", "alta", ""),
   ("Robinson Faria", "PSD", "2015-01-01", "2019-01-01", "alta", ""),
   ("Fátima Bezerra", "PT", "2019-01-01", None, "alta", "reeleita 2022")]),
 "Rio Grande do Sul": ("do_Rio_Grande_do_Sul", [
   ("Tarso Genro", "PT", "2011-01-01", "2015-01-01", "alta", ""),
   ("José Ivo Sartori", "PMDB", "2015-01-01", "2019-01-01", "alta", ""),
   ("Eduardo Leite", "PSDB", "2019-01-01", "2022-03-31", "alta", ""),
   ("Ranolfo Vieira Júnior", "PSDB", "2022-03-31", "2023-01-01", "alta", "interino"),
   ("Eduardo Leite", "PSDB", "2023-01-01", None, "alta", "reeleito 2022")]),
 "Rondônia": ("de_Rondônia", [
   ("Confúcio Moura", "PMDB", "2011-01-01", "2018-04-05", "alta", ""),
   ("Daniel Pereira", "PSB", "2018-04-06", "2019-01-01", "alta", "vice assumiu"),
   ("Marcos Rocha", "PSL", "2019-01-01", None, "alta", "")]),
 "Roraima": ("de_Roraima", [
   ("José Anchieta Júnior", "PSDB", "2011-01-01", "2014-04-04", "alta", ""),
   ("Chico Rodrigues", "PSB", "2014-04-04", "2015-01-01", "alta", "vice assumiu"),
   ("Suely Campos", "PP", "2015-01-01", "2018-12-10", "alta", ""),
   ("Antônio Denarium", "PSL", "2019-01-01", "2026-03-27", "alta", ""),
   ("Edilson Damião", "União Brasil", "2026-03-27", "2026-04-30", "alta", "vice assumiu"),
   ("Soldado Sampaio", "Republicanos", "2026-04-30", None, "alta", "")]),
 "Santa Catarina": ("de_Santa_Catarina", [
   ("Raimundo Colombo", "DEM", "2011-01-01", "2015-01-01", "alta", ""),
   ("Raimundo Colombo", "PSD", "2015-01-01", "2018-04-05", "alta", "reeleito; partido mudou para PSD"),
   ("Eduardo Moreira", "MDB", "2018-04-05", "2019-01-01", "alta", "vice assumiu"),
   ("Carlos Moisés", "PSL", "2019-01-01", "2023-01-01", "alta", "fonte lista PSL e depois Republicanos"),
   ("Jorginho Mello", "PL", "2023-01-01", None, "alta", "")]),
 "São Paulo": ("de_São_Paulo", [
   ("Geraldo Alckmin", "PSDB", "2011-01-01", "2018-04-06", "alta", ""),
   ("Márcio França", "PSB", "2018-04-06", "2019-01-01", "alta", "vice assumiu"),
   ("João Doria", "PSDB", "2019-01-01", "2022-04-01", "alta", ""),
   ("Rodrigo Garcia", "PSDB", "2022-04-01", "2023-01-01", "alta", ""),
   ("Tarcísio de Freitas", "Republicanos", "2023-01-01", None, "alta", "")]),
 "Sergipe": ("de_Sergipe", [
   ("Marcelo Déda", "PT", "2011-01-01", "2013-12-02", "alta", "falecido no cargo"),
   ("Jackson Barreto", "PMDB", "2013-12-02", "2018-04-06", "alta", "vice assumiu; reeleito 2014"),
   ("Belivaldo Chagas", "PSD", "2018-04-06", "2023-01-01", "alta", "vice assumiu"),
   ("Fábio Mitidieri", "PSD", "2023-01-01", None, "alta", "")]),
 "Tocantins": ("do_Tocantins", [
   ("Siqueira Campos", "PSDB", "2011-01-01", "2014-04-04", "alta", ""),
   ("Sandoval Cardoso", "SD", "2014-04-04", "2015-01-01", "alta", "indireto"),
   ("Marcelo Miranda", "PMDB", "2015-01-01", "2018-03-27", "alta", ""),
   ("Mauro Carlesse", "PHS", "2018-03-27", "2018-04-06", "media", "interino; datas do trecho truncadas"),
   ("Marcelo Miranda", "PMDB", "2018-04-06", "2018-04-19", "media", "retorno breve"),
   ("Mauro Carlesse", "PHS", "2018-04-19", "2022-03-11", "alta", "indireto em 2018 e reeleito"),
   ("Wanderlei Barbosa", "Republicanos", "2022-03-11", None, "alta", "")]),
}


def linhas():
    ano_ini, ano_fim = 2011, 2026
    out = []
    for uf, (slug, mands) in MANDATOS.items():
        url = WIKI + slug
        for ano in range(ano_ini, ano_fim + 1):
            a0, a1 = datetime.date(ano, 1, 1), datetime.date(ano, 12, 31)
            for gov, part, ini, fim, conf, obs in mands:
                i, f = D(ini), D(fim)
                if f <= a0 or i > a1 or (fim and f == a0):
                    continue
                lo, hi = max(i, a0), min(f, a1)
                out.append({"uf": uf, "ano": ano, "governador": gov, "partido": part,
                            "inicio": lo.isoformat(), "fim": ("" if fim is None and hi >= DL else hi.isoformat()),
                            "fonte_url": url, "confianca": conf, "obs": obs})
    return out


def main():
    rows = linhas()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["uf", "ano", "governador", "partido", "inicio", "fim", "fonte_url", "confianca", "obs"])
        w.writeheader(); w.writerows(rows)
    print("linhas:", len(rows), "| UFs:", len({r["uf"] for r in rows}), "| anos:", min(r["ano"] for r in rows), "-", max(r["ano"] for r in rows))


if __name__ == "__main__":
    main()
