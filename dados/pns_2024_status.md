# PNS 2024/2025: status e orientação sexual

Verificado em 2026-10-11. Resultado: **não existe PNS 2024 nem PNS 2025**. Não consegui checar o questionário, então a pergunta Y008 fica sem resposta.

| Item | Situação | Evidência | Estado |
|---|---|---|---|
| PNS 2019 | Última edição concluída; coleta até fev/2020 (segundo a busca), divulgação de resultados em 2021 | Busca em `ibge.gov.br`/`agenciadenoticias` (WebSearch, 2026-10-11) | Snippet, não abri a página de origem |
| PNS 2024 | Não encontrada. A pesquisa que foi a campo em 2024 foi a PeNSE (escolares) | Busca em `ibge.gov.br` (mesma consulta); não há URL oficial de PNS 2024 | Verificado só pela busca |
| PNS 2026 (3ª edição) | Coleta iniciada, data citada: 08/07/2026 | Snippet de notícia do IBGE, sem URL legível no resultado | **Não verificado**: não consegui abrir a notícia |
| Pergunta de orientação sexual (Y008 do módulo PNS 2019) | Não verificada no questionário PNS 2026 | Sem acesso ao questionário | **Não verificado** |

## Bloqueio de acesso ao IBGE

- `https://www.ibge.gov.br/estatisticas/sociais/saude/10586-pesquisa-nacional-de-saude.html` respondeu HTTP 403 ao curl (com e sem User-Agent de navegador) e ao WebFetch.
- A API de agregados `servicodados.ibge.gov.br/api/v3/agregados` respondeu 200, mas a busca por nome não retornou nenhuma entrada de PNS (`fontes/p2-f8-dados-uf/pns/ibge_agregados_pns.json`).

## Próxima ação

Abrir a página oficial da PNS 2026 no Chrome real logado (`claude-in-chrome`), ler o estágio e o questionário e conferir a Y008. Não usei navegador nesta rodada.
