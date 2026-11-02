Vou auditar o PDF contra o repositório, só com leitura local, e fechar as três perguntas na ordem pedida.O selo e os metadados já divergem da versão que o PDF declara. Vou conferir hashes, numeração e as remissões no arquivo.Sigo a auditoria só com leitura local: primeiro confiro o PDF e o selo contra os hashes declarados, depois as citações e o que o repositório ainda descreve como versão antiga.O selo e o PDF ainda não foram conferidos contra os arquivos. Vou calcular os hashes e cruzar citações e caminhos que o README ainda trata como versão antiga.Vou conferir nos arquivos os trechos que decidem o veredito, antes de fechar o parecer.# Parecer de pré-publicação — Grok 4.7 (grok-4.7)

## Vereditos

| Pergunta | Veredito | Por quê (1 linha) |
|---|---|---|
| 1. PDF pronto | pronto com ressalvas | Números centrais, apêndices B–M e a lista de 101 referências fecham entre si; ficam a Portaria e dois ponteiros herdados para a “seção 3.2”. |
| 2. Repositório atualizado | não | A face pública ainda cita o preprint 0.4.4 e a versão 0.1.0, e dois caminhos do README e do CHANGELOG não existem. |
| 3. DOI | pode depois de corrigir os bloqueantes | A rc1, neste estado, cunharia no Zenodo a versão 0.1.0, fechada, com resumo parado na v0.3. |

Limite desta leitura: o SHA-256 de `docs/paper/paper-final.pdf` não foi recalculado aqui, e `python3 -I make_provenance.py --verify` não foi reexecutado. A última evidência de selo fechado é o manifesto de 2026-10-31T22:11:25Z. Esta cópia não tem `.git`. O estado do GitHub e a resolução das URLs (ANTRA, GGB, CNV) ficam como não verificado. A conferência APA nos dois sentidos foi por amostra, não por extração de todas as citações.

## Bloqueantes

**GRO-P01.** A face que o Zenodo e o leitor citariam não é o PDF que está em `docs/paper/`.

- Local: `paper/v05/MANUSCRITO.md` (p. 49 do PDF); `paper/v05/referencias.md`, linha 59; `README.md`, linhas 31, 270 e 376–395; `CITATION.cff`, linhas 11–24; `codemeta.json`, linhas 6–7; `.zenodo.json`, linhas 3–15; `ROADMAP.md`, linha 18.
- Trecho literal: “repositório público do estudo, versão 1.0.0 (Flores, 2026)” e, no README, “O artigo (preprint, versão 0.4.4)” e “Artigo, versão 0.5 (em preparação; não lançada)”.
- Problema: o PDF e a entrada Flores (2026) anunciam o depósito 1.0.0. `CITATION.cff`, `codemeta.json` e `.zenodo.json` estão em `0.1.0`, com `date-released: 2026-10-23` e descrição que para em “Na v0.3”. O `.zenodo.json` traz `access_right: closed`. A tabela do README não nomeia `docs/paper/paper-final.pdf`. Etiquetar esta árvore cunharia um registro fechado, versão 0.1.0, com resumo da v0.3. O `ROADMAP.md` reserva a 1.0.0 para o commit imediatamente anterior ao release que cunha o DOI.
- Evidência: título, autor Carlos Ulisses Flores, ORCID `0000-0002-6034-7765` e afiliação Codex Hash Research Laboratory batem. A versão, a data e o resumo não batem. O PDF de fato está em `/private/var/folders/wx/_0vy9yl163lfvnp8pgtvq14m0000gn/T/tmpzidecybr/docs/paper/paper-final.pdf`.
- Correção proposta: no commit da rc1, antes da tag, apontar o README para `docs/paper/paper-final.pdf` e retirar “em preparação”; alinhar `CITATION.cff`, `codemeta.json` e `.zenodo.json` à 1.0.0 que o PDF já declara (ou voltar o PDF para 0.x até esse bump); `date-released` 2026-10-31; descrição que cubra esta versão; `access_right: open` nesse commit, como a nota do `.zenodo.json` já prevê.

**GRO-P02.** Dois caminhos citados na face pública não existem.

- Local: `README.md`, linha 271; `CHANGELOG.md`, linhas 36–38 e 111; `paper/build/`.
- Trecho literal: “`dados/lihs-checagem-ggb2016.META.md`” e “`paper/build/v05/paper-v05.pdf`, gerado pelo Microsoft Word (169 páginas”.
- Problema: na raiz não há `dados/lihs-checagem-ggb2016.META.md`. O metadado da planilha da Liga Humanista Secular do Brasil está em `research-2026-10-30-contraponto/dados/lihs-checagem-ggb2016.META.md` (o `paper/v05/README.md`, linha 34, aponta o caminho certo). `paper/build/` só tem `v04/paper-v04.pdf` e `juiz/`. O bullet de 169 páginas e MC1–MC12 descreve um PDF que esta árvore não entrega. O bullet anterior do mesmo CHANGELOG, linhas 19–32, descreve corretamente `docs/paper/paper-final` e os Apêndices B–M.
- Evidência: listagem de `paper/build/` e leitura do arquivo em `research-2026-10-30-contraponto/dados/lihs-checagem-ggb2016.META.md`.
- Correção proposta: trocar os dois atalhos pelo caminho longo; apagar ou reescrever o bullet do `paper-v05.pdf` de 169 páginas.

**GRO-P03.** O selo registrado não é um commit publicável como rc1.

- Local: `runs/20261031T221125Z/manifest.json`, linhas 5–10; `REPRODUCIBILITY.md`, linhas 24–26.
- Trecho literal: `"commit": "0601c65e13280dcc6c82c5468997930517dedad0"`, `"working_tree_dirty": true`, e “O primeiro commit público (`0601c65`) não contém o artigo”.
- Problema: o manifesto prova que `make_provenance.py --verify` passou em 2026-10-31T22:11:25Z, com 768 arquivos e `chain_hash` `2aac3f60c497966c10cef173e892600084554dbf72d4f70ef8a0a4104163ced9`. O mesmo manifesto grava árvore suja sobre um commit que, pelo próprio `REPRODUCIBILITY.md`, não contém o artigo. Cunhar a rc1 nesse commit depositaria outra coisa. Esta cópia não tem `.git`; se o GitHub já tem um commit posterior, não verificado.
- Evidência: o mesmo `chain_hash` e 768 arquivos em `output/hash-chain.md` (linha 3) e `output/provenance.json` (`n_arquivos`: 768). `scripts/registra_run.py` só grava o manifesto depois de o `--verify` sair 0.
- Correção proposta: não etiquetar `0601c65`. Novo commit da árvore já corrigida (GRO-P01 e GRO-P02), com `python3 -I make_provenance.py --verify` verde nesse commit, e só então a tag `v1.0.0-rc1`.

## Não bloqueantes

**GRO-N01.** O Apêndice H se contradiz sobre o ato de agosto de 2019.

- Local: PDF, cerca das pp. 144 e 147; `paper/v05/MATERIAL-COMPLEMENTAR.md`, linhas 1095 e 1118.
- Trecho literal: “sem instrumento normativo lido (Tabela H1)” e, adiante, “O ato é a Portaria nº 1.576, do Ministério da Cidadania, de 20 de agosto de 2019.”
- Problema: o primeiro parágrafo diz que o ato hostil não teve instrumento lido. O segundo nomeia a portaria, diz que o texto não menciona LGBT e que o caráter hostil vem de falas, da imprensa e de liminar, e fecha com “(Apêndice H)”, remissão circular. A Portaria não está em `paper/v05/referencias.md`. A conclusão da busca (nenhuma perseguição estatal nas 60 consultas) permanece.
- Evidência: as duas frases no mesmo arquivo; busca por `1.576` em `paper/v05/` só acha essas linhas do material complementar.
- Correção proposta: uma frase só. Se a portaria foi lida, citar o instrumento na lista e dizer que o texto não nomeia LGBT. Pode entrar na remontagem do PDF que recebe o DOI.

**GRO-N02.** Dois ponteiros herdados caem na seção errada deste PDF.

- Local: PDF, cerca das pp. 70 e 101; `paper/v05/MATERIAL-COMPLEMENTAR.md`, linhas 38 e 493.
- Trecho literal: “A seção 3.2 apresenta o veredito sob as duas regras” e “controle positivo do argumento da seção 3.2”.
- Problema: neste PDF a seção 3.2 é denúncias, boletins e fichas. O veredito de mortalidade e o controle por sexo e raça estão na seção 3.4 e no Apêndice E. A Tabela B1 avisa que o texto herdado usa a numeração da v0.4.4, mas as duas frases leem-se como ponteiro deste artigo.
- Evidência: as linhas acima, contra o sumário da seção 3 no manuscrito.
- Correção proposta: trocar por “seção 3.4” e “Apêndice E”. Mesma remontagem do PDF.

**GRO-N03.** O comentário do selo da v0.5 conta 767 arquivos; os arquivos de máquina contam 768.

- Local: `paper/PAPER-SHA256.txt`, linha 9; `output/hash-chain.md`, linha 3; manifesto, linha 10.
- Trecho literal: “Selo do repositório: 2aac3f60…ced9 (767 arquivos)”.
- Problema: o hash é o mesmo. A contagem do comentário está uma unidade abaixo da cadeia, do `provenance.json` e do manifesto. O cabeçalho do mesmo arquivo ainda se intitula “versão 0.4.4” e conserva o selo antigo de 724 arquivos, o que é histórico legítimo se o bloco da v0.5 ficar inequívoco.
- Evidência: comparação dos três registros do mesmo `chain_hash`. O SHA-256 declarado do PDF (`5b17d4a5…de71a1`, 163 páginas, 2.898.219 bytes) não foi conferido contra o arquivo em disco: não verificado.
- Correção proposta: 768 no comentário. Não bloqueia a rc1.

**GRO-N04.** O teste da v0.5 trava um subconjunto, e o README arredonda dois números do PDF.

- Local: `tests/test_numeros_v05.py`, linhas 183–195 (fim do arquivo); `paper/v05/README.md`, linhas 5–6; `README.md`, linha 21; `CHANGELOG.md`, linhas 115–117.
- Trecho literal: “`tests/test_numeros_v05.py` trava os números novos da v0.5” e, no README, “LGBTfobia em 0,5%” e “42-44%”.
- Problema: o teste trava a tabulação da LiHS (347 casos), as variações de homicídio por governo, a fatia indeterminada de 18,0% (2018) e 30,1% (2024) e a coabitação de 29,49% e 62,39%. O CHANGELOG descreve esse alcance com precisão. O README da pasta v0.5 promete mais. No PDF, a falta de motivo no Sinan é 42,5% a 44,5%, e a LGBTfobia, 0,4% a 0,5%.
- Evidência: o arquivo de teste termina no teste de coabitação. Os intervalos do PDF estão na seção 3.2.
- Correção proposta: no README da v0.5, repetir o alcance que o CHANGELOG já escreve; no README raiz, usar 42,5% a 44,5% e 0,4% a 0,5%.

**GRO-N05.** A frase sobre a Transgender Europe não tem entrada na lista.

- Local: PDF, Apêndice F; `paper/v05/MATERIAL-COMPLEMENTAR.md`, linha 724.
- Trecho literal: “Transgender Europe, que declara não conseguir estimar o número real”.
- Problema: TGEU aparece no glossário (Apêndice A) e não como referência. No repositório, o apoio é paráfrase secundária em `research-2026-10-30-contraponto/frente-B-internacional.md`, não a página da organização.
- Evidência: a frase na linha 724; ausência de entrada TGEU em `referencias.md` (101 entradas, linhas ímpares de 1 a 201, de Asal, 2013, a Zucco e Power, 2023).
- Correção proposta: citar a página da organização, ou atribuir a frase à fonte secundária que o repositório de fato guardou.

**GRO-N06.** Um rótulo antigo sobrevive no README da pasta, não no PDF.

- Local: `paper/v05/README.md`, linha 32.
- Trecho literal: “nota da Tabela MC5.C1”.
- Problema: o mapa em `paper/v05/mapa-apendices.json` manda esse rótulo para a Tabela F4. O corpo de `MATERIAL-COMPLEMENTAR.md` não conserva “MC” nem “Material Complementar”.
- Evidência: a linha 32 contra o mapa e o corpo do apêndice.
- Correção proposta: “nota da Tabela F4”.

## O que está bom

- Título, autor, ORCID e afiliação Codex Hash Research Laboratory coincidem no PDF, em `CITATION.cff`, em `codemeta.json` e em `.zenodo.json`.
- As contas centrais do PDF fecham entre si: 14,70/3,82 dá a razão bruta 3,84; 50/160 é 31,3%; 73/88 é 83,0%; 257/1.122 é 22,9%; 291/1.013 é 28,7%; Dilma, Temer, Bolsonaro e Lula dão +11,1%, −4,2%, −21,0% e −10,6%; o fluxo da amostra é 88.531 = 85.913 + 849 + 1.769.
- Os apêndices B–M e as remissões do corpo (Apêndice C, F, H, J, K, M; seções 3.1 a 3.7; Tabelas 1–6 e Figuras 1–8) apontam para o que o PDF contém. A frase do identificador permanente, na disponibilidade de dados, é a frase certa para antes do DOI.
- A planilha nominal da LiHS não é distribuída, e `tests/test_numeros_v05.py` trava o SHA-256 `0dc25783…179d5ad`.
- O `chain_hash` `2aac3f60…ced9` é o mesmo em `paper/PAPER-SHA256.txt`, `output/hash-chain.md`, `output/provenance.json` e no manifesto. O artigo fica fora do selo de propósito, porque cita a cadeia.

Depois do DOI, e só depois: colocar o identificador em `README.md`, `CITATION.cff`, `codemeta.json`, `CHANGELOG.md` e no texto; refazer o PDF; release final `v1.0.0`. GRO-N01 e GRO-N02 cabem nessa remontagem. Convém corrigi-los antes da rc1 se o PDF da rc1 for o que o Zenodo arquiva. Nada pendente nesta auditoria.