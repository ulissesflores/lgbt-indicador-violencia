# Dicionário harmonizado do Disque 100 (3 formatos, 2011-2026)

Rótulo a rótulo, com a classe aplicada e os períodos em que aparece: `saidas/dicionario_rotulos.csv` (775 rótulos dos 23 arquivos; o selo cobriu os 17 primeiros e o adendo 2 do pré-registro estendeu aos 23, com as mesmas regras). Regras: `scripts/d100_comum.py` (seladas em `PREREGISTRO-D100.sha256`).

| campo harmonizado | A 2011-2019 (35 col.) | B 2020S1 (34 col.) | C 2020S2-2026T3 (62 col.) | comparável entre formatos? |
|---|---|---|---|---|
| chave | nenhuma | `hash_par_vitima_suspeito` (par vítima-suspeito) | `hash` (denúncia; 32 hex até 2022S1, 64 hex depois) | não: hashes não ligam formatos |
| unidade da linha | vítima x suspeito de um atendimento (sem chave) | par vítima-suspeito | violação x vítima x suspeito dentro da denúncia | não |
| data | `data_atendimento` | `Data_da_denúncia` | `Data_de_cadastro` (dd/mm/aaaa ou ISO) | sim (dia) |
| UF | `vitima_uf` (UF da vítima) | `UF` | `UF` (do fato/denúncia); também `UF_da_vítima` | parcial (A é UF da vítima) |
| grupo / módulo | `grupo_violacao` = "LGBT" | `Grupo_vulnerável` = "Violência Contra População LGBTQIA+" | `Grupo_vulnerável` = "VIOLÊNCIA CONTRA POPULAÇÃO LGBTQIA+" (por linha; varia dentro do hash em 14-18% desde 2022S2) | quase: único indicador 2011-2026 |
| orientação da vítima | `vitima_orientacao_sexual`: Homossexual, Bissexual, Heterossexual, Não informado | `orientacao_sexual` (sujeito não documentado): GAY, LÉSBICA, HOMOSSEXUAL, BISSEXUAL, TRANSEXUAL, TRAVESTI, NULL (sem hétero) | `Orientação_sexual_da_vítima`: 2020S2-2022S1 ASSEXUAL, BISSEXUAL, HOMOSSEXUAL, PANSEXUAL, OUTRO, N/D; desde 2022S2 HOMOSSEXUAL.GAY/LÉSBICA, BISSEXUAL, PESSOA TRANS.TRANSEXUAL/TRANSGÊNERO/TRAVESTI, NÃO, NÃO INFORMADO, OUTRO, NULL | NÃO |
| identidade de gênero da vítima | `vitima_identidade_genero`: Travesti, Transexual, Feminina, Masculina, e também Gay, Lésbica, Bissexual, Heterossexual (orientação no campo de identidade) | não existe | não existe (trans aparece na coluna de orientação) | NÃO |
| sexo/gênero da vítima | `vitima_sexo`: Feminino, Masculino, Não informado | `Gênero_da_vítima`: FEMININO, MASCULINO, LGBTQIA+, N/D | `Gênero_da_vítima` (`Sexo_` em 2024S2, `Genero_` em 2025S1): FEMININO, MASCULINO, INTERSEXO, NI, NÃO INFORMADO, NÃO SE APLICA, NULL | parcial |
| sexo/gênero do suspeito | `suspeito_pf_sexo` | `Gênero_do_suspeito` (inclui "LGBT") | `Gênero_do_suspeito` | parcial |
| motivação | não existe | `motivacoes` (multivalorada): "EM RAZÃO DE ORIENTAÇÃO SEXUAL/IDEOLOGIA DE GÊNERO" | `Motivação`: "EM RAZÃO DE ORIENTAÇÃO SEXUAL/ IDEOLOGIA DE GÊNERO" (até 2022S1), "MOTIVAÇÃO.EM RAZÃO DE ORIENTAÇÃO SEXUAL" (desde 2022S2; às vezes várias unidas por vírgula) | não (A sem campo; rótulo muda) |
| violação | `violacoes` multivalorada (ex.: "DISCRIMINAÇÃO.POR ORIENTAÇÃO SEXUAL") | `violacoes` multivalorada (`violencia_*.X`) | `violacao`, uma por linha (`INTEGRIDADE>PSÍQUICA>...`) | só no nível macro (tabela no CSV) |
| nº de vítimas | não existe | não existe | `sl_quantidade_vitimas` (10-100 em 2020S2-2022S1: não interpretável; 1-7 desde 2022S2) | não |

Faltantes, sempre separados: `ausente` (NULL, vazio), `nao_informado` (N/D, NA, NI, não informado, não sabe/soube, atendimento interrompido), `nao_se_aplica`; zero só quando a categoria existe no formato.

Pessoa única: NÃO há chave pública de pessoa em nenhum formato; o total de vítimas únicas não é calculável.
