"""C18: monta eventos_C18.csv. Cada evento aponta arquivo baixado + ancora (regex) e o trecho verbatim e extraido do TEXTO do arquivo
(nunca digitado a mao). Python: /opt/homebrew/bin/python3.14 -I"""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[4])  # raiz configurável
import csv, hashlib, re, os
B = (REPO_ROOT + "/fontes/q1-textointegral/discurso/simetria")
OUT = (REPO_ROOT + "/research-2026-10-21-rodada3/escrutinio/simetria")
dl = {}
for r in csv.DictReader(open(OUT + "/downloads_C18.tsv"), delimiter="\t"):
    dl[f"{r['gov']}_{r['qid']}"] = r
# (id, governante_do_mandato, data, tipo, agente, arquivo (chave de download ou caminho rel.), ancora, achado_na_leitura_de, julgamento_meu)
E = [
 ("E01","G1","2004","P","norma_ou_orgao","G1_Q9","propõe o Programa\s+Brasil Sem\s+Homofobia","G1","programa federal Brasil sem Homofobia (SEDH); fonte academica"),
 ("E02","G2","2008-06","P","governante","G1_Q2","perhaps the most perverse disease","G1","fala do presidente na 1a Conferencia LGBT (relato de imprensa religiosa critica; 2008)"),
 ("E03","G2","2008-06","P","norma_ou_orgao","G1_Q1","1ª Conferência Nacional de Políticas Públicas e Direitos Humanos","G1","1a Conferencia Nacional LGBT, com Lula na abertura"),
 ("E04","G2","2010","P","norma_ou_orgao","G1_Q1","instituir 17 de maio como o Dia Nacional","G1","Dia Nacional de Combate a Homofobia (decreto de 2010 segundo a fonte)"),
 ("E05","G2","2010","P","norma_ou_orgao","G1_Q1","portaria, estendeu o direito de declara","G1","portaria da Fazenda: declaracao conjunta de casais homossexuais (IR)"),
 ("E06","G2","2010-12-09","P","governante","G1_Q10","signed a decree Dec. 9 creating the National LGBT Council","G1","decreto cria o Conselho Nacional LGBT; imprensa LGBT dos EUA"),
 ("E07","G2","2010","T3","norma_ou_orgao","G6_Q7","recursos insignificantes para políticas LGBT","G6","critica de entidade LGBT (contagem declarada): LOA 2011 com R$ 1,1 mi na SDH; falta de institucionalizacao"),
 ("E08","G3","2011-05","T3","governante","G1_Q1","suspendeu a produção e distribuição de materiais","G1","suspensao do kit Escola sem Homofobia, apos pressao religiosa"),
 ("E09","G3","2011-05","T3","governante","G3_Q1","Dilma tinha ordenado a não distribuição","G3","mesmo evento E08 (outra fonte); nao conta de novo"),
 ("E10","G3","2013-2016","T3","norma_ou_orgao","G3_Q4","nem a tal política de saúde LGBT","G3","verba errática/descontinuada segundo checagem Aos Fatos (2016); contagem declarada"),
 ("E11","G3","2011-05-18","P","governante","G3_Q9","Convoca a II Conferência","G3","decreto convoca a II Conferencia Nacional LGBT"),
 ("E12","G3","2011-12","P","norma_ou_orgao","G3_Q4","criou a Política Nacional de Saúde Integral LGBT","G3","portaria do Ministro da Saude"),
 ("E13","G3","2014-09-01","P","governante","G3_Q2","criminalizar a homofobia","G3","fala de campanha da presidente candidata a reeleicao (nao ato de governo)"),
 ("E14","G4","2017","T3","governante","G4_Q5","zerou em 2017 os já escassos repasses","G4","repasses federais a programas LGBT zerados (Aos Fatos/UOL; Siga Brasil)"),
 ("E15","G4","2016","T3","governante","G4_Q8","sequer demonstra interesse em receber a comitiva","G4","presidente interino nao recebe comitiva LGBT (relato de ativista via imprensa)"),
 ("E16","G4","2017-11-01","T3?","norma_ou_orgao","G4_Q4","também não incluía a população LGBT","G4","rol do ministerio sem LGBT; sem linha de base nao e 'retirada' (T3 com ressalva; nao soma)"),
 ("E17","G5","2019-04-25","T1","governante","fala-2019-04-25/congressoemfoco","o Brasil não pode ser um país do mundo gay","G5","fala em cafe com jornalistas no Planalto; relato de segunda mao (Crusoe); transcricao oficial nao localizada"),
 ("E18","G5","2019-01-01","T3?","norma_ou_orgao","G5_Q10","retira a população LGBT da lista","G5","MP 870: texto igual ao de 2017 (T3 com ressalva; nao soma)"),
 ("E19","G5","2019-04-11","T3","norma_ou_orgao","G5_Q9","Decreto 9.759, que\s+anunciou a extinção","G5","Decreto 9.759 extingue colegiados, incluindo o CNCD/LGBT; Decreto 9.883 recria sem 'LGBT' (nota de ONGs LGBT)"),
 ("E20","G5","2019-08","T4","governante","G5_Q6","ordered funding be stopped for LGBT\+ films","G5","suspensao de verba/edital audiovisual com tema LGBT, apos fala do presidente (reverso judicial em 2019-10)"),
 ("E21","G5","2023-04 (relatorio do TCU sobre 2018-2021)","T3","norma_ou_orgao","G5_Q3","ficou sem a implementação de políticas públicas","G5","auditoria do TCU lida via imprensa: omissao; data do relatorio fora do mandato"),
 ("E22","G6","2023-04-06","P","norma_ou_orgao","G6_Q9","criou o Conselho Nacional dos Direitos das Pessoas","G6","Decreto 11.471 (CNLGBTQIA+)"),
 ("E23","G6","2024-12-13","T3","norma_ou_orgao","G6_Q4","O descaso do governo","G6","T3 fraco: OPINIAO/contagem declarada de veiculo de direita citando ativistas LGBT (sem departamento com equipe e verba); nao e dado oficial"),
 ("E24","G6","2026-09-07","NA","norma_ou_orgao","G6_Q3","perdeu força","G6","reclassificado T3->NA apos revisao: programa de campanha nao e suspensao, corte, extincao nem silencio documentado (CRITERIOS T3); listado, nao soma"),
]
rows = []
for (eid, g, data, tipo, ag, arq, anc, lido, jul) in E:
    if arq.startswith("fala-"):
        raw = f"{B}/{arq.split('/')[0]}/{arq.split('/')[1]}.raw"; txt = raw.replace(".raw", ".txt"); url = "ver fala-2019-04-25"; tf = "imprensa"
    else:
        r = dl[arq]; raw = f"{B}/brasil/{arq}.raw"; txt = f"{B}/brasil/{arq}.txt"; url = r["url"]; tf = r["tipo_fonte"]
    t = re.sub(r"\s+", " ", open(txt).read())
    m = re.search(anc.replace(r"\s+", " "), t)
    if not m:
        m = re.search(anc, t)
    trecho = t[max(0, m.start() - 120): m.end() + 180] if m else "ANCORA_NAO_ACHADA"
    rows.append([eid, g, data, tipo, ag, tf, url, trecho, raw, hashlib.sha256(open(raw, "rb").read()).hexdigest(), lido, jul])
with open(OUT + "/eventos_C18.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "governante_do_mandato", "data", "tipo", "agente", "tipo_fonte", "url", "trecho_verbatim", "arquivo", "sha256", "achado_na_leitura_de", "julgamento_meu"]); w.writerows(rows)
print(len(rows), sum(1 for r in rows if r[7] == "ANCORA_NAO_ACHADA"), [r[0] for r in rows if r[7] == "ANCORA_NAO_ACHADA"])
