#!/usr/bin/env python3
"""Gera ideologia_mapeamento.md (regras + tabelas derivadas dos CSVs). Rodar depois de build_ideologia.py."""
import csv, collections, json, os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = list(csv.DictReader(open(f"{H}/ideologia_ondas_observadas.csv")))
d = collections.defaultdict(dict)
for r in O: d[r['linhagem']][(r['fonte'], r['onda'])] = float(r['escore'])
cols = [('BRC', '2018'), ('BRC', '2022'), ('BLS', '2009'), ('BLS', '2013'), ('BLS', '2017'), ('BLS', '2021'), ('PREPPS_LR', '2018'), ('CHES_LRGEN', '2020'),
        ('VPARTY_ECON', '2010'), ('VPARTY_ECON', '2014'), ('VPARTY_ECON', '2018'), ('VPARTY_LGBT', '2010'), ('VPARTY_LGBT', '2014'), ('VPARTY_LGBT', '2018'), ('GPS_ECON', '2019')]
hdr = ['BRC 2018', 'BRC 2022', 'BLS 2009', 'BLS 2013', 'BLS 2017', 'BLS 2021', 'PREPPS 2018 (1-20)', 'CHES-LA 2020', 'V-Party econ 2010', 'V-Party econ 2014', 'V-Party econ 2018', 'V-Party LGBT 2010', 'V-Party LGBT 2014', 'V-Party LGBT 2018', 'GPS econ 2019']
order = ['PSOL', 'PT', 'PCdoB', 'PDT', 'PSB', 'REDE', 'PV', 'CID', 'MDB', 'PSDB', 'PSD', 'PODE', 'AVANTE', 'SD', 'PROS', 'PMN', 'PHS', 'PTB', 'PP', 'REP', 'PL', 'DEM', 'PSL', 'UNIAO', 'NOVO', 'PSC']
tab = ['| linhagem | ' + ' | '.join(hdr) + ' |', '|---|' + '---|' * len(hdr)]
for l in order:
    tab.append(f'| {l} | ' + ' | '.join((f'{d[l][c]:.2f}' + ('*' if any(k == c for k in [(r["fonte"], r["onda"]) for r in O if r["linhagem"] == l and "FUSAO" in r["nota"]]) else '')) if c in d[l] else '' for c in cols) + ' |')
C = list(csv.DictReader(open(f"{H}/ideologia_correlacoes.csv")))
def rows(f, sub, maxlag=99):
    out = ['| par | defasagem (anos) | n | Spearman | IC95% aprox. | Pearson |', '|---|---|---|---|---|---|']
    for r in C:
        if r['subconjunto'].startswith(sub) and f(r) and int(r['defasagem_anos']) <= maxlag:
            out.append(f"| {r['fonteA']} {r['ondaA']} x {r['fonteB']} {r['ondaB']} | {r['defasagem_anos']} | {r['n']} | {r['spearman']} | {r['spearman_ic95_aprox']} | {r['pearson']} |")
    return '\n'.join(out)
LR = {'BRC', 'BLS', 'PREPPS_LR', 'CHES_LRGEN'}
glr = lambda r: r['fonteA'] in LR and r['fonteB'] in LR
imp = json.load(open(f"{H}/impacto_painel_resumo.json"))

md = f"""# Mapeamento de partidos, regras de alocação por ano e correlações entre fontes

Gerado por `scripts/gerar_mapeamento_md.py` a partir de `ideologia_partidos_ano.csv`, `ideologia_ondas_observadas.csv` e `ideologia_correlacoes.csv` (que vêm de `scripts/build_ideologia.py`, só stdlib, `python3.14 -I`). Entradas e sha256 em `raw/SHA256SUMS.txt`. Data: 2026-10-21.

## 1. Vocabulário

- **linhagem**: identificador estável do partido através de renomeações (ex.: `MDB` cobre PMDB até 2017 e MDB depois). A coluna `partido` do CSV traz o rótulo vigente no ano; `ideologia_aliases.csv` traduz qualquer rótulo que aparece nos CSV de governadores (inclusive rótulos obsoletos, como `PMDB` em 2019-2022 no CSV "wiki") para a linhagem.
- **onda**: ano de coleta da fonte. **tipo** = `onda` quando o ano do CSV coincide com a onda; `alocado` quando o escore da onda foi atribuído a outro ano pela regra da seção 3 (`dist_anos` = distância). `existia_no_ano` = 0 quando o rótulo não existia legalmente naquele ano (o escore é emprestado de onda/sucessor; decida se usa).
- **escore_direita** = escore na orientação "maior = mais à direita/conservador" (o escore LGBT do V-Party tem o sinal invertido porque o original é "maior = mais apoio"). **escore_0_10** só existe quando a escala tem limites teóricos (BRC, BLS, PREPPS, CHES, GPS); o V-Party é IRT sem limites e fica em branco.

## 2. Regras de sucessão (decisões, com a fonte de cada uma)

| caso | regra aplicada | fonte da regra / estado |
|---|---|---|
| Renomeação pura (PMDB→MDB 2018; PPS→Cidadania 2019; PR→PL 2019; PRB→Republicanos 2019; PTN→Podemos 2016; PP→Progressistas→PP; PTdoB→Avante; PTC→Agir; PEN→Patriota) | mesma linhagem, escore inalterado | Apêndice A de Zucco & Power (`raw` do projeto, appendix.pdf p. 2-3) confirma MDB (PMDB 1981-2017), CID (2019), PL (nome original reassumido em 2019), PODE (2016), REP (PRB até 2019). Datas de PP, PTdoB, PTC, PEN: ⚠️ não verificadas em fonte lida (fila) |
| **Fusão** que cria partido novo: DEM+PSL → União Brasil (2022) | escore = média **ponderada por cadeiras eleitas em 2018**: DEM 5,7% e PSL 10,1% (V-Party v2 `v2paseatshare`) = pesos 0,361 / 0,639. Onde a fonte já avaliou o União (BRC 2022), usa-se o escore direto | Zucco & Power fazem o mesmo (Apêndice A, p. 4: "0.66 ... average between the positions of the DEM (0.43) and the PSL (0.8), weighted by each party's size at the time of the merger"); meu cálculo dá 0,67 para o BLS 2021. **Bolognesi et al. 2025 (p. 13)** usam média aritmética simples; a diferença no BRC 2018 é 8,34 (simples) vs 8,28 (ponderada) |
| **Fusão** PTB+Patriota → PRD (2023) | média aritmética simples (cadeiras de 2022 não obtidas); só aparece onde as duas existem na onda (BRC 2018, 2022). Nenhum governador do PRD no painel | Bolognesi et al. 2025, nota 13. Registro TSE 09/11/2023 só por Wikipédia (não primária) |
| **Incorporação** (o absorvido some; o absorvedor mantém identidade): PPL→PCdoB, PRP→Patriota, PHS→Podemos, PSC→Podemos (2023), PROS→Solidariedade (2023) | o absorvedor **mantém o próprio escore**; o absorvido não entra em média. Se a onda não traz o absorvido (ex.: BRC 2022 não tem PHS), usa-se o escore do sucessor, marcado `FALLBACK sucessor` em `nota_mapeamento` | PPL→PCdoB: Bolognesi et al. 2025, p. 14 (valores do PPL "simplesmente não tiveram seus valores ideológicos mobilizados"). PROS: Apêndice A de Z&P ("Absorbed by Solidariedade (SD) in October 2022 and formally dissolved in February 2023"). Demais datas ⚠️ não verificadas (TSE bloqueia automação; fila) |
| DEM e PSL em 2021 quando a onda é BRC 2022 (que só tem União) | fallback: escore do União Brasil (8,49) | decisão minha; efeito: DEM 8,57→8,49; PSL 8,11→8,49 |
| Federações (Brasil da Esperança 2022: PT+PCdoB+PV; PSOL+Rede; PSDB+Cidadania) | **nenhum ajuste**: cada partido mantém o escore avaliado | os autores do BRC documentam "contágio" do âncora da federação (p. 19-20): PV 5,29→4,12, Rede 4,77→3,69, Cidadania 4,93→6,17 na onda 2022 refletem o parceiro, não mudança programática. Irrelevante para governadores (nenhum desses 3 tem governador no painel) |

### Divergência com a Tabela 1 de Bolognesi et al. 2025 (achado)

A coluna 2018 da Tabela 1 do artigo de 2025 **não é a média bruta de 2018**: ela usa média aritmética nas incorporações, ao contrário do que o texto diz na p. 14. Conferido contra `df_experts.csv` (recomputado, 519 respondentes de 2018): PCdoB 4,60 na tabela vs 1,920 no dado (= (1,92 + 7,27 do PPL)/2 = 4,59); Podemos 7,10 vs 7,243 (= (7,243 + PHS 6,959)/2 = 7,10); Patriota 8,08 vs 8,551 (= (8,551 + PRP 7,595)/2 = 8,07). As outras 28 linhas conferem na 2ª casa decimal, e os NR (não respostas) das 3 linhas também são médias dos dois partidos. Consequência: a "dilatação do PCdoB para a esquerda" (4,60→1,78) descrita na p. 19 é artefato da regra de média; com o dado bruto o PCdoB vai de 1,92 a 1,78. O painel F8 usa a Tabela 1 de **Bolognesi, Ribeiro & Codato 2023** (Dados), que é a média bruta, então não foi afetado. Os escores 2018 deste CSV são brutos.

## 3. Regras de alocação onda → ano (2010-2024)

| fonte | regra | observação |
|---|---|---|
| BRC | anos ≤ 2020 → onda jul/2018; anos ≥ 2021 → onda jul/2022 | só duas ondas; 2012-2017 são retroprojeção de 1 a 6 anos; os autores dizem (p. 10) que não pretendem a classificação "viaje no tempo" |
| BLS | por legislatura do Congresso: 2010 → onda 2009; 2011-2014 → 2013; 2015-2018 → 2017; 2019-2022 → 2021; 2023-2024 → 2021 **extrapolado** (BLS10, 2025, não publicado) | ondas de legisladores; refletem alinhamento governo/oposição da época |
| V-Party | mandato da eleição: eleição t vale t..t+3 (2010→2010-13; 2014→2014-17; 2018→2018-21); 2022+ sem cobertura | v2 termina na eleição de 2018 |
| PREPPS, CHES-LA, GPS | janela de ±2 anos em torno da onda (2018, 2020, 2019) | ondas únicas |

## 4. Escores observados (por onda; sem alocação)

`*` = escore derivado por regra de fusão (não avaliado pela fonte). Escalas: BRC/CHES/GPS 0-10; BLS ≈ −1..+1; PREPPS 1-20; V-Party IRT (econ: maior = direita; LGBT: maior = mais apoio a igualdade LGBT, sinal **original**).

""" + '\n'.join(tab) + f"""

Partidos com escore só no BRC: Avante, PMN, PHS, PMB, PRTB, DC, PCO, PSTU, PCB (e UP, só 2022). O BLS não cobre PHS, PMN, Avante e não tem PROS na onda 2013 (por isso 3 UF-anos do painel ficam sem escore BLS: PROS na variante wiki, PMN na tse). V-Party v2 cobre só ~11 partidos por eleição (os que passaram de ~5% dos votos) e não tem PSOL, PCdoB, Rede, Novo, Podemos, Avante.

## 5. Validação convergente

### 5.1 Esquerda-direita geral, pares de ondas com defasagem até 4 anos, todos os partidos em comum (Spearman; IC de Fisher aproximado, impreciso com n pequeno)

{rows(glr, 'todos', 4)}

### 5.2 Os mesmos pares **sem o bloco de esquerda** (PT, PSB, PDT, PCdoB, PSOL, PV, Rede e radicais): discriminação dentro do centro-direita

{rows(glr, 'sem', 4)}

**Leitura.** As correlações do conjunto completo (0,87-0,99) são dominadas pela separação esquerda x resto, que todas as fontes enxergam. Dentro do centro-direita (MDB, PSDB, PSD, Podemos, PTB, PP, DEM, PL, Republicanos, Novo...) o acordo cai para 0,5-0,88 e é instável: BLS 2017 x BLS 2021 dá 0,65 (n=13), BRC 2018 x CHES-LA 2020 dá 0,50 (n=8). No BRC 2018, MDB (7,02), PSDB (7,11) e PSD (7,09) ficam a 0,1 ponto entre si, na ordem de grandeza do erro-padrão da média (DP ≈ 1,7 / raiz(480) ≈ 0,08). **Ordenar governadores dentro da direita é frágil; o contraste que as fontes sustentam é esquerda x resto.** BRC e PREPPS não são independentes (ambos são surveys de cientistas políticos brasileiros; sobreposição de respondentes plausível, não verificada); BLS e V-Party são independentes dos dois.

### 5.3 Correlação por ano-calendário (escores alocados; `ideologia_correlacoes_por_ano.csv`, 250 linhas)

Exemplo, BRC x BLS (n = partidos em comum): 2012 ρ=0,969 (n=14); 2016 0,941 (20); 2018 0,941 (20); 2019-2020 0,865 (20); 2021-2024 0,934 (18). BRC x CHES-LA 2018-2020: 0,80 (11). BRC x PREPPS 2016-2020: 0,968 (17).

### 5.4 V-Party: esquerda-direita econômica x apoio LGBT (mesmo partido, mesma eleição)

Spearman 0,83 (2010, n=9), 0,86 (2014, n=11), 0,91 (2018, n=11). A dimensão LGBT se separa do eixo econômico em casos específicos: em 2018, Republicanos (PRB) tem o pior escore LGBT (−2,70) e PSL −2,25, enquanto o PP (mais à direita no econômico do que o PRB) tem −0,97; PSDB (+0,48) e MDB (+0,72) ficam do lado "apoia" apesar de estarem à direita do PT/PSB na escala econômica.

## 6. Impacto sobre o painel F8 (recomputado por outro caminho; painel NÃO alterado)

Réplica do escore "atual" do painel (escore 2018 de Bolognesi 2023 para todos os anos): {imp[0]['replica_atual_ok']} UF-anos idênticos ao `painel_uf_ano.csv` (variante wiki) e {imp[1]['replica_atual_ok']} (variante tse).

| variante de partido | UF-anos | Pearson atual x BRC por período | Spearman | UF-anos que mudam > 0,5 ponto | > 1 ponto | Pearson atual x BLS | Spearman |
|---|---|---|---|---|---|---|---|
| wiki | {imp[0]['uf_anos']} | {imp[0]['pearson_atual_vs_BRCper']} | {imp[0]['spearman_atual_vs_BRCper']} | {imp[0]['mudam_gt_0_5']} | {imp[0]['mudam_gt_1']} | {imp[0]['pearson_atual_vs_BLS']} | {imp[0]['spearman_atual_vs_BLS']} |
| tse | {imp[1]['uf_anos']} | {imp[1]['pearson_atual_vs_BRCper']} | {imp[1]['spearman_atual_vs_BRCper']} | {imp[1]['mudam_gt_0_5']} | {imp[1]['mudam_gt_1']} | {imp[1]['pearson_atual_vs_BLS']} | {imp[1]['spearman_atual_vs_BLS']} |

Os UF-anos que mais mudam são 2022-2024 sob PL (7,78→8,80), Republicanos (7,78→8,33) e Novo (8,13→8,67), mais RS-2022 na variante tse (PSDB|PTB, PTB 6,10→7,72). O TWFE reestimado com cada variante está em `sensibilidade_twfe.md`: todos os coeficientes continuam com IC95% cruzando zero.

### Rótulos obsoletos nos CSV de governadores (achado lateral)

No CSV "wiki" (`dados/governadores_uf_2011_2026.csv`) há rótulos que não existiam no ano: `PSC` para Cláudio Castro (RJ) 2023-2026 (PSC foi incorporado ao Podemos em 2023 e ele foi eleito em 2022 pelo PL; o CSV "tse" traz PL a partir de 2023), `PMDB` 2019-2022 (renomeado MDB em 2018) e `PSL` 2023-2024 (RO, RR). Resolvidos via `ideologia_aliases.csv` + fallback de sucessor; efeito numérico pequeno, mas o escore usado por esses UF-anos no painel atual é o do rótulo velho.

## 7. Não obtido

MARPOR (site inacessível daqui), ondas PREPPS 2006/07-2015, BLS10 (2025), texto principal de Zucco & Power 2024, datas oficiais do TSE: ver `fila-aquisicao.jsonl`.
"""
open(f"{H}/ideologia_mapeamento.md", "w").write(md); print(len(md))
