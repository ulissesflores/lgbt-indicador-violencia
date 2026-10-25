# Frente L (v0.3, 2026-10-24): lacunas de literatura e verificação externa

**Achado que muda conclusão:** a §3.3 diz que "gays morrem mais" é "não sustentada como frase geral"; o texto integral contradiz a forma. O ONS (dado oficial, Censo 2021 ligado a óbitos) dá razão de mortalidade por todas as causas LGB+/heterossexual de 1,31 (1,28-1,33) na Inglaterra e País de Gales, 2021-2024 (`L-fontes/ons-mortalidade-2026/tabelas.xlsx`, Table_5 linha 7), e Zachry et al. (2025), já citado como se fosse só negativo, conclui "Although mixed, findings suggest elevated mortality" (14 de 43 estudos com apoio pleno, 28 parcial, 1 nenhum). Para **homicídio**, nenhuma fonte lida tem razão populacional por orientação; Brasil segue sem estimativa. Proposta: `L-SECAO-3-3-PROPOSTA.md`.

## Contagem (lido / pedido)

| item | lido/pedido | nota |
|---|---|---|
| L1 fontes | 11/11 | ONS mortalidade (+xlsx), ONS suicídio (+xlsx, só o boletim lido), ONS expectativa, McKetta 2024, Erlangsen 2023, Luis 2026, McLellan 2026 + correção, Halliwell 2024, Zachry 2025 (arquivo já no projeto), Lum-Price-Banks 2013, HRDAG 2013 |
| L1 quartil | 7/7 periódicos | PLOS ONE, Epidemiol Serv Saúde ("conferir categoria"), Violence Against Women, American Statistician: tabelas locais. **JAMA e JAMA Netw Open não estavam nas tabelas locais**; conferidos Q1 2023-2025 nas páginas do Scimago salvas em `L-fontes/scimago-jama/` (via Firecrawl, não Chrome real). As linhas 6, 7 e 9 do ledger dizem `nao_verificado`; as linhas 23-24 registram o Q1. Recomendo à coordenadora appendar as duas linhas em `fontes/scimago/` (não escrevi lá) |
| L2 verificações | 3/3 | (a) procede, (b) procede, (c) procede em parte (ver abaixo) |
| L3 Disque 100 | 4/4 períodos com cabeçalho; 3/4 com arquivo inteiro | 2024-2026 só amostra de 2 MiB (arquivos de 0,94 a 1,93 GB) |
| L4 rascunho §3.3 | 1/1 | com tabela número x trecho x arquivo x página |
| Ledger | 30 linhas | `L-ledger/sources.jsonl`, só por `emit_sources.py`; linha 25 corrige o DOI de Luis (sem `.pt` dá 404) |

## Para a frente R (L2, trecho verbatim e página)

- **(a) Guia de Vigilância em Saúde, vol. 3, 6ª ed. revisada (2024), p. 1222 (PDF p. 211): PROCEDE.** "A violência comunitária ou extrafamiliar contra homens adultos (20 a 59 anos) não será objeto de notificação, exceto nas condições de vulnerabilidade já mencionadas", que incluem "população LGBT". Mesma página: notificam-se "violências homofóbicas contra mulheres e homens em todas as idades". Arquivo `L-fontes/guia-vigilancia-v3/gvs-v3-6ed.pdf`.
- **(b) Manual da Declaração de Óbito (MS, 2022), p. 10 e p. 30: PROCEDE.** "A versão atualmente em uso da DO foi atualizada, pela última vez, em 2014, e é composta por 59 variáveis distribuídas em 9 blocos". Busca por "orientação sexual", "identidade de gênero" e "nome social" no manual: 0 ocorrências. Arquivo `L-fontes/manual-do/manual-do-ms-2022.pdf`. Redação segura: "o formulário tem 59 variáveis; o arquivo do SIM, 87 campos; nenhum dos dois tem orientação ou identidade".
- **(c) IBGE, PNS 2019, orientação sexual autoidentificada, p. 7 e nota 1 da p. 10: PROCEDE EM PARTE.** "visou apenas a captação da orientação sexual das pessoas de 18 anos ou mais de idade, não havendo, naquele momento, coleta a respeito da identidade de gênero"; nota 1: "foi realizada a captação do sexo biológico dos indivíduos". Que pessoas trans **não foram excluídas** o documento não diz; é inferência do desenho (p. 6: morador de 18+ "selecionado, aleatoriamente", sem filtro por identidade). Arquivo `L-fontes/ibge-pns2019/liv101934.pdf`.

## O que muda no paper (linhas do `paper/paper.md` do repo; não editei)

- L27 e L61: "A declaração de óbito tem 87 campos" está errado (87 é o arquivo do SIM; o formulário tem 59). L27, L61, L189, L310, L376: "não sustentada como frase geral" / "parcial" vira "sustentada para mortalidade geral em populações definidas fora do Brasil; não universal; sem razão populacional de homicídio; não testável no Brasil". "Não testável no Brasil" continua certo.
- L187-189: substituir pela proposta. Novas referências: ONS 2025, 2026a, 2026b; McKetta 2024 (distinto do McKetta 2026 já citado); Erlangsen 2023; Luis 2026; McLellan 2026 + correção; Halliwell 2024; MS 2022.
- §3.4 (não reescrita): o intervalo 175-198 de Chapman precisa de ressalva. Lum, Price & Banks (2013, The American Statistician 67(4), p. 192): "This homogeneity assumption is usually wrong" e os registros dão "only a lower bound on the true count" (só se o pareamento for perfeito); HRDAG (2013): estratificar reduz a heterogeneidade de captura. Arquivos `L-fontes/lum-price-banks-2013/duke.pdf`, `L-fontes/hrdag-2013/hrdag.html`.
- Luis et al. (2026): o resumo diz "36.452 casos ..., dos quais 563 (42,5%)", mas os 42,5% são dos 1.325 óbitos pareados (Tabela 1, p. 5). As "causas violentas" incluem intenção indeterminada. A citação de "1.057 homicídios" na introdução é da ANTRA, não achado do estudo.

## L3: Disque 100 (só cabeçalhos e unidade; nada analisado)

- Acesso: catálogo e arquivos sem cadastro, sem aceite e sem cookie (`curl` puro: 302 para `dadosabertos.mdh.gov.br`, 200/206). 23 arquivos de microdados: anuais 2011-2019 (57 a 252 MB), semestrais 2020-2026 (103 MB a 1,93 GB), 3º trimestre de 2026 (940 MB), mais os balanços 2011-2019 (CSV agregados).
- 2011-2019 (35 colunas; `disque100-2011.csv` inteiro, 99.949 linhas): tem `vitima_identidade_genero` e `vitima_orientacao_sexual`, mas os campos misturam categorias: em 2011 a coluna de identidade traz "Heterossexual" e "Gay"; na amostra de 2019 ela traz quase só valores de orientação. Não há identificador de denúncia, então a unidade não dá para identificar sem dicionário.
- 1º semestre de 2020 (`disque100-primeiro-semestre-2020.csv` inteiro, 103.376.976 bytes, sha256 `aed18437…d2bb`): terceiro formato, com 34 colunas; a chave `hash_par_vitima_suspeito` sugere que a linha é o par vítima-suspeito; há uma única coluna `orientacao_sexual`, sem dizer de quem, e `Gênero_da_vítima`. Três formatos em 15 anos exigem harmonização antes de qualquer série.
- 2º semestre de 2023 a 2026 (62 colunas, com `hash`, `sl_quantidade_vitimas`, `Gênero_da_vítima`, `Orientação_sexual_da_vítima`, `Motivação`, `violacao`): o `hash` se repete até 33 vezes em cerca de 3 mil linhas, então a linha **parece** ser violação × vítima e o `hash` parece ser a denúncia. Pessoas trans aparecem na coluna de **orientação** ("PESSOA TRANS.TRANSEXUAL"); não há coluna própria de identidade de gênero.
- Balanço 2011-2019 população LGBT: tabela "Perfil das Vítimas - Identidade de gênero" com Gay, Lésbica, Bissexual, Heterossexual, Travesti e Transexual juntos. A unidade declarada é a vítima.

## O que não foi possível ler, e por quê

- Chrome real indisponível (extensão desconectada). JAMA Network e Scimago foram lidos via Firecrawl, o degrau 2 da casa; o texto integral de McLellan saiu em markdown, não em PDF.
- Suplementos (eTables) de McKetta 2024, Erlangsen 2023 e McLellan 2026 não lidos. A página final dos dois artigos do JAMA não foi verificada.
- Disque 100: arquivos inteiros de 2019 (192 MB), 2º sem. 2023 (1,03 GB), 1º sem. 2024 (1,22 GB) e 3º tri. 2026 (0,94 GB) não baixados; ficaram amostras de 2 MiB, e o sha256 é o da amostra. Inteiros: 2011 (sha256 `fd6d3bdf…bd11`) e 1º sem. 2020.
- Coortes do ASTRA C6 (Austrália PMC12914191, Taiwan PMC12556306, Suécia PMC13453480): **lidas** pelo HTML do PMC e registradas no ledger, mas sem quartil (Lancet Reg Health West Pac; eClinicalMedicine) e fora desta §3.3. As três acham excesso de mortalidade geral em pessoas trans identificadas por registro (Taiwan: some na comparação entre irmãos, salvo suicídio). Próxima onda: conferir quartil e decidir se entram.

## Fila de PDFs pendentes (sem pedir a ninguém)

1. PDF da editora de McKetta et al. 2024 e de Erlangsen et al. 2023, só para a página final (JAMA, Cloudflare; Chrome real).
2. Quartil SJR de The Lancet Regional Health: Western Pacific e de eClinicalMedicine (Scimago pelo Chrome real).
3. Dicionário de dados do Disque 100 (unidade de contagem), se publicado no dados.gov.br.

