# Redactions in this folder (v1.3.0)

One parliamentary speech excerpt was redacted in version 1.3.0. It reported a criminal allegation about a private person. The name had already been omitted, but the excerpt kept identifying details, and the transcript locator led back to the full text. The excerpt is not needed for any number in the study: the coding result of the item is unchanged (`FORA`, source `nenhuma`), and so is every aggregate computed from the 60 baseline items.

| File | Line | Field | Replaced by |
|---|---|---|---|
| `baseline_itens.jsonl` | 59 (item `4245c528…`) | `trecho`, `url` | `[trecho redigido na v1.3.0: …]`, `[localizador redigido na v1.3.0]` |
| `baseline_resultado_C27.csv` | 111-112 (item `1fd7c5167fbe`) | `trecho` | `[trecho redigido na v1.3.0: …]` |

SHA-256 of each file, from the record of the original run to this version:

| File | `SHA256SUMS.txt` (run record) | v1.2.0 | v1.3.0 |
|---|---|---|---|
| `baseline_itens.jsonl` | `917ebcd16ce315b4677a2abe7e369211fe187055479f1dc9078417d15dc3725b` | `9a2ca9d448573925e510283b701861a7427a01f6898b5eefde347b845f48bc94` | `f93b5dfb48ea64e0ea9678b1ac4aa468b37032309af2ecc866ee8a169d18445f` |
| `baseline_resultado_C27.csv` | `da413a0b578c36b506803632de1694ccae66663a2fbb1239a2c5022cc6a6a75b` | `92a1a6a175b6b1ac3db73d301cb8f5ca2ac40c6996c07201f962dd44155b3365` | `5979f6a474854b189f7b6d109c47d441eecc50b4461bcd0005510abb28ef0cec` |

`SHA256SUMS.txt` records the files as they stood when the study was run, and it is kept unchanged as that record. It is not a check on the distributed files: 12 of the files it lists were edited afterwards (the omission of the private person's name, before v1.2.0, and path and privacy cleanups), and 36 of them are not distributed. The criteria and addenda of this study (`CRITERIOS.md`, `ADENDO-*.md` and their recording times) still match it.

Em português: um trecho de discurso parlamentar com alegação criminal sobre pessoa privada foi redigido na v1.3.0 nos dois arquivos acima; o resultado da codificação e os agregados não mudam. `SHA256SUMS.txt` é o registro da execução original e fica como está.
