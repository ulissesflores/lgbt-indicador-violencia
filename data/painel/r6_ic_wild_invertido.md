# R6 — IC95% por inversão do teste wild-cluster bootstrap-t (painel de governadores; adendo v0.3, 2026-10-24)

Forma pré-registrada em `R6-PREREGISTRO-FORMA.md` (sha256 `c6f07e2c0391c11745e75569dc79137647409034ece8e43675928bff9e7698bf`, hora em `R6-PREREGISTRO-FORMA.sha256`). B = 9999, semente 20261024, Rademacher por UF, H0 imposta em cada valor testado; t(0,975; 26) = 2.0555 calculado numericamente. Modelo e dados idênticos ao painel principal (b e EP conferidos com `c02_indet_resultados.csv`). Os números antigos (IC normal) continuam publicados; este adendo só acrescenta.

Troca de 5 pontos de ideologia (por exemplo PT -> DEM ou PL), variação na taxa registrada, em %:

| grupo | b (EP) | normal b ± 1,96 EP (publicado) | wild-cluster invertido | t(26) | p(0) da grade / p wild publicado | inclui 0 |
|---|---|---|---|---|---|---|
| total | +0.00090 (0.01208) | -10,8 a +13,1 | -12,3 a +12,4 | -11,3 a +13,7 | 0.945 / 0.943 | sim |
| homens | +0.00052 (0.01253) | -11,3 a +13,4 | -12,9 a +12,8 | -11,9 a +14,0 | 0.968 / 0.970 | sim |
| mulheres | -0.00067 (0.01052) | -10,1 a +10,5 | -12,3 a +10,5 | -10,5 a +11,0 | 0.946 / 0.951 | sim |
| negros | -0.00705 (0.01456) | -16,3 a +11,3 | -18,2 a +9,9 | -16,9 a +12,1 | 0.659 / 0.661 | sim |
| nao_negros | -0.00160 (0.01712) | -16,1 a +17,3 | -18,2 a +17,0 | -16,8 a +18,3 | 0.920 / 0.911 | sim |
| arma | +0.00087 (0.01846) | -16,2 a +20,4 | -19,5 a +19,7 | -16,9 a +21,4 | 0.963 / 0.970 | sim |

- Conjunto de aceitação contíguo na grade de ±6 EP (481 pontos) em todos os desfechos: sim.
- Veredito pela regra pré-registrada: todos os 6 intervalos invertidos contêm 0; o veredito publicado (não distinguível de zero) fica.
- Leitura: o intervalo invertido reflete os 27 clusters; o normal (CR1) é o publicado. Nenhum deles é limite causal garantido: são intervalos da associação condicionais ao modelo (efeitos fixos de UF e ano, ideologia BRC por período).
