<!-- Transcrito de https://gemini.google.com/app/abfc7be101195042 (4 Argon, Thinking High), 2026-10-31, por get_page_text.
A mensagem digitada chegou truncada no início ("ório anexo (repo-lgbt-indicador.zip)..."), mas o pedido completo foi o arquivo
anexo argon.prompt.pub1.txt (= argon.prompt.navegador.txt), que o modelo leu. Marcadores de citação vazios do app ("()",
"``", "[cite: 31]") foram mantidos como vieram. -->

# Parecer de pré-publicação — Gemini 4 Argon (gemini-4-argon-high)

## Vereditos

| Pergunta | Veredito | Por quê (1 linha) |
|---|---|---|
| 1. PDF pronto | não pronto | Há 3 falhas internas no PDF: promessa não cumprida na p. 30 (QUADRO-E2.md ficou fora do Apêndice E), contradição e autorreferência no Apêndice H (p. 144–147) e remissão em branco (Apêndice ) na p. 46. |
| 2. Repositório atualizado | com ressalvas | A árvore do .zip tem os diretórios de dados, scripts, paper/v05/ e runs/20261031T221125Z/, mas a Tabela M1 do PDF aponta para paper/build/juiz/* (inexistente no .zip) e omite paper/v05/; o conteúdo interno dos fluxos Deflate do .zip fica como não verificado. |
| 3. DOI | pode depois de corrigir os bloqueantes | Corrigidos os 4 bloqueantes (ARG-P01 a ARG-P04) no manuscrito/apêndices e regerado o PDF e seus hashes, a v1.0.0-rc1 pode ser publicada para disparar o DOI no Zenodo. |

## Bloqueantes

### ARG-P01 — Promessa de dados não cumprida no PDF (Quadro E2 ausente do Apêndice E e arquivo paper/v05/QUADRO-E2.md órfão no repositório)
- Local: PDF, p. 30 (seção 3.4) e p. 95–105 (Apêndice E); repositório paper/v05/QUADRO-E2.md.
- Trecho literal curto: "Os números dessas coortes estão no Apêndice E." (p. 30).
- Problema: A seção 3.4 menciona três coortes de pessoas trans identificadas por registro na Austrália (Saxby et al., 2026), em Taiwan (Hsu et al., 2025) e na Suécia (Clark et al., 2026) e afirma que os números dessas coortes estão no Apêndice E. Contudo, o Apêndice E do PDF (p. 95–105) não contém nenhuma estimativa numérica dessas três coortes — nem na Tabela E1 (p. 97), nem na Figura E1 (p. 98), nem no texto da p. 99. Na árvore do repositório consta o arquivo separado paper/v05/QUADRO-E2.md, que não foi integrado ao Apêndice E na montagem do PDF final.
- Evidência verificável: No PDF, p. 30, lê-se "Três coortes de pessoas trans identificadas por registro, na Austrália, em Taiwan e na Suécia, também acham excesso de mortalidade geral (Clark et al., 2026; Hsu et al., 2025; Saxby et al., 2026). Em Taiwan, porém, o excesso some na comparação entre irmãos, salvo para suicídio. Os números dessas coortes estão no Apêndice E." No Apêndice E, p. 99, lê-se apenas que as três coortes "também encontram excesso de mortalidade geral, que em Taiwan desaparece na comparação entre irmãos, salvo para suicídio; os periódicos não tiveram o quartil conferido, e as três ficam fora do veredito", saltando da Tabela E1 (p. 97) para a Tabela E2 (p. 102). No índice do arquivo .zip, o arquivo paper/v05/QUADRO-E2.md aparece avulso em paper/v05/.
- Correção proposta: Incluir o conteúdo de paper/v05/QUADRO-E2.md no Apêndice E (em paper/v05/MATERIAL-COMPLEMENTAR.md e em paper/tools/monta_fonte_v05.py) antes de gerar o PDF, ou remover da p. 30 a frase "Os números dessas coortes estão no Apêndice E.".

### ARG-P02 — Caminhos inexistentes (paper/build/juiz/*) e omissão da estrutura paper/v05/ na Tabela M1 do Apêndice M
- Local: PDF, p. 162–163 (Apêndice M, Tabela M1); árvore de arquivos de repo-lgbt-indicador.zip.
- Trecho literal curto: "paper/AUDIT.md e paper/build/juiz/rodada-v4-3-* e rodada-v4-4-* (...) paper/build/juiz/rodada-v4-5" e "paper/paper.md" (p. 162–163).
- Problema: A Tabela M1 promete caminhos que não existem no repositório publicado ou que refletem apenas a estrutura da v0.4.x: na linha referente à seção 2.6 (Revisão adversarial), aponta para paper/build/juiz/rodada-v4-3-*, rodada-v4-4-* e paper/build/juiz/rodada-v4-5, caminhos que não existem no .zip publicado, e omite paper/v05/revisao/r5/ a r8/, onde estão os pareceres e matrizes dos três modelos prometidos na seção 2.6 (p. 12). Na linha Texto-fonte do artigo, aponta apenas para paper/paper.md e omite paper/v05/MANUSCRITO.md, MATERIAL-COMPLEMENTAR.md, referencias.md, mapa-apendices.json e os scripts de figuras *_v05.py. Nas linhas de PNS e GGB, lista apenas Tabelas C1 a C5 (o Apêndice C vai até C11) e Tabelas F1 e F2 (o Apêndice F vai até F4 e usa research-2026-10-30-contraponto/).
- Evidência verificável: Confronto da Tabela M1 (p. 162–163) com a listagem de arquivos de repo-lgbt-indicador.zip: não há diretório paper/build/ no .zip, ao passo que paper/v05/MANUSCRITO.md, MATERIAL-COMPLEMENTAR.md, paper/v05/revisao/r5/ a r8/ e research-2026-10-30-contraponto/ estão presentes no .zip e ausentes da Tabela M1.
- Correção proposta: Atualizar a Tabela M1 para: (a) incluir paper/v05/ como texto-fonte da versão publicada; (b) substituir paper/build/juiz/rodada-v4-* por paper/v05/revisao/r5/ a r8/ (ou exportar os laudos antigos para um caminho versionado); (c) atualizar a cobertura para Tabelas C1 a C11, Tabelas F1 a F4 e research-2026-10-30-contraponto/.

### ARG-P03 — Contradição interna e tripla autorremissão (Apêndice H) dentro do próprio Apêndice H
- Local: PDF, p. 144, 146 e 147 (Apêndice H).
- Trecho literal curto: "sem instrumento normativo lido (Tabela H1)" (p. 144) vs. "O ato é a Portaria nº 1.576, do Ministério da Cidadania, de 20 de agosto de 2019. O texto suspende por 180 dias o edital inteiro..." (p. 147).
- Problema: O Apêndice H concatena o texto herdado da v0.4.4 (p. 144–146) com a subseção "Leitura dos atos por período de governo" (p. 147), produzindo dois erros de montagem: na p. 144 a ordem de agosto de 2019 foi noticiada "sem instrumento normativo lido (Tabela H1)" e a nota da Tabela H1 (p. 146) repete que as fontes são de imprensa; na p. 147, afirma-se "um ato oficial hostil, ambos em 2019. O ato é a Portaria nº 1.576 ... não menciona conteúdo LGBT". O texto da p. 147 cita (Apêndice H) três vezes, resíduo de quando a subseção integrava o corpo do artigo.
- Evidência verificável: PDF, p. 144, p. 146 e p. 147.
- Correção proposta: Remover as três autorremissões (Apêndice H) da p. 147 (substituindo por (Tabela H1) onde cabível) e conciliar a redação entre as p. 144/146 e a p. 147 (esclarecendo que nas 60 consultas originais a fonte recuperada foi a notícia de imprensa, e que a Portaria nº 1.576/2019 foi identificada de forma complementar).

### ARG-P04 — Remissão truncada (Apêndice ) na seção 5 (Limitações)
- Local: PDF, p. 46 (seção 5, final do 4º parágrafo).
- Trecho literal curto: "nenhum desses trabalhos decide uma conclusão do quadro (Apêndice )." (p. 46).
- Problema: A letra do apêndice foi omitida na remissão.
- Evidência verificável: PDF, p. 46, linha 13.
- Correção proposta: Inserir a letra correspondente: (Apêndice B e Apêndice E) ou (Apêndice E).

## Não bloqueantes

### ARG-N01 — Número de sensibilidade do Disque 100 (39 denúncias) remete ao Apêndice D, mas não consta no texto do Apêndice D
- Local: PDF, p. 22 (seção 3.2) e p. 93–94 (Apêndice D).
- Trecho: "exigir que todas as linhas sejam do módulo LGBT reduz 2025 a 39 denúncias (MDHC, 2026; Apêndice D)."
- Problema: o Apêndice D apresenta só o total de 9.346 denúncias e não menciona o 39.
- Correção proposta: acrescentar no Apêndice D que a regra estrita reduz 2025 de 9.346 para 39 denúncias.

### ARG-N02 — Coexistência de remissões com numeração da v0.4.4 e da v0.5 nos Apêndices D, F e M
- Local: PDF, p. 92, p. 113 e p. 162–163.
- Trecho: "cerca de 3,01 milhões pelo peso calibrado da PNS de 2019 (seção 3.1)" (p. 113) e "seção 6" vs. "seção 2.6" (Tabela M1).
- Problema: (a) p. 113 remete à seção 3.1 para 3,01 milhões, que está no Apêndice C; (b) a p. 92 usa "seção 6 do artigo" no sentido novo, e a Tabela M1 usa "seção 6" no sentido antigo (Reprodutibilidade) ao lado de "seção 2.6", que só existe na v0.5.
- Correção proposta: p. 113 -> (Apêndice C); atualizar a coluna "Seção, tabela ou figura" da Tabela M1 para a v0.5.

### ARG-N03 — Saída bruta de script (agressor_risco_pns2019.md) colada sem acabamento editorial no Apêndice C
- Local: PDF, p. 83–87.
- Trecho: "Reprodução de seguro_pns2019.md (6 fatias, tolerância 0,01 p.p.): divergências = 0." e "(publicado: 2,82; 2,16 a 3,68)" na Tabela C8.
- Problema: linha de asserção de teste, caixa alta em "AJUSTADA", anotação de conferência interna na célula da Tabela C8 e abreviações de código (het, n = 85913) nas subseções 5 e 7.
- Correção proposta: dar acabamento editorial às subseções 1 a 7 do Apêndice C.

### ARG-N04 — Detalhes tipográficos e de APA 7
- Local: PDF, p. 20, 33, 39, 50, 60, 64 e 160.
- Trechos: "4,79 (2,58 8,90)" (p. 20); "nesse material" (p. 33); "/lei/115380.htm" (p. 50); "UNAMI & OHCHR. (2015)" (p. 64); "(OSCE/ODIHR, 2025)" (p. 160).
- Problema: falta "a" no intervalo da Tabela 3; resíduos "nesse material" / "no mesmo material"; URL da Lei 15.380 com "1" no lugar de "l"; espaço na quebra da URL de ONS (2025); sigla no autor de UNAMI & OHCHR; (OSCE/ODIHR, 2025) diverge da entrada "Office for Democratic Institutions and Human Rights. (2025)".
- Correção proposta: corrigir cada item.

### ARG-N05 — Truncamento em ADENDO-2.hora.txt, arquivo legado paper_v0.1.md e conteúdo Deflate do .zip não verificado
- Local: repo-lgbt-indicador.zip: research-2026-10-21-rodada3/escrutinio/simetria/ADENDO-2.hora.txt, paper/figures/fontes/paper_v0.1.md e arquivos comprimidos.
- Problema: ADENDO-2.hora.txt conteria só "3202"; o rascunho paper_v0.1.md permanece; o texto dos arquivos comprimidos por Deflate (README, CHANGELOG, CITATION.cff, codemeta, .zenodo, REPRODUCIBILITY, paper/v05/*, PAPER-SHA256, hash-chain, provenance, manifesto, test_numeros_v05.py) e os hashes ficam não verificados.
- Correção proposta: antes da rc1, rodar pytest, make_provenance.py --verify e auditar_publicacao.py, atualizar PAPER-SHA256 com o PDF corrigido e uniformizar a versão 1.0.0 em README, CHANGELOG, CITATION.cff, codemeta.json e .zenodo.json; DOI só depois da rc1.

## O que está bom
- Coerência numérica rigorosa entre Resumo, Abstract, corpo, tabelas, figuras e apêndices (85.913 + 849 + 1.769 = 88.531; 796 + 758 = 1.554; 2.260 + 726 + 66 + 60 = 3.112; 130 + 39 + 5 + 5 = 179; fatias exclusivas somam 100,0% na Tabela 3; funil do GGB 160 -> 106 -> 88 -> 73 -> 50).
- Correspondência 1:1 entre citações e a lista única de referências em APA 7: as 101 obras estão citadas, em ordem alfabética, com marcação das leituras só por resumo e das citações secundárias.
- Nenhum rótulo "MC" no PDF; tabelas A1 a M1 e figuras C1 a K1 numeradas por letra de apêndice.
- Transparência sobre desvios e análises pós-dados (Tabelas B3 e B4, com carimbos UTC iguais aos arquivos .hora.txt).
- Simetria analítica e disciplina causal nos quatro níveis (N1 a N4).
