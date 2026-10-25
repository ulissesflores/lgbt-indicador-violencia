"""SUPERADO em 2026-10-21 por triangulacao_pns_sinan.py (calcula tudo dos microdados, com IC da PNS); este arquivo tem insumos digitados à mão. Mantido só como histórico.
Sensibilidade da triangulação PNS x Sinan à não resposta de orientação sexual (campo 36) no Sinan.
Recorte: violência física, interpessoal, adultos 18+ (2023 e 2024). Entradas: contagens já calculadas (resumo.md): válidas, ignorado+branco, 'não se aplica', homo+bi.
Cenários para a parcela LGB+ entre as NÃO respondidas (ign+branco+NA): MCAR (= parcela observada), pior caso (0%), melhor caso (100%),
e intermediários plausíveis (LGB+ 2x e 0,5x a parcela observada entre não respondidas). Compara com o implícito da PNS (6,9%)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
dados={2023:dict(n=197779,ign=0.204,na=0.039,val=0.757,hb_val=0.0412),2024:dict(n=202416,ign=0.202,na=0.040,val=0.758,hb_val=0.0408)}
pns=0.0189*0.147/(0.0189*0.147+0.9811*0.0382)
L=["\n## Sensibilidade à não resposta de orientação (violência física, adultos, interpessoal)",f"PNS 2019 implícito: {pns*100:.2f}% LGB+ entre adultos com violência física em 12 m.",
   "| ano | cenário p/ não respondidas (24% das notificações) | parcela LGB+ total no Sinan | razão Sinan/PNS |","|---|---|---|---|"]
for y,d in dados.items():
    nr=d['ign']+d['na']; obs=d['hb_val']
    for nome,p_nr in [("MCAR: igual à observada",obs),("0,5x observada",obs*0.5),("2x observada",obs*2),("pior caso: 0%",0.0),("melhor caso: 100%",1.0),("iguala PNS: parcela necessária entre não respondidas",None)]:
        if p_nr is None:
            p_nr=(pns-d['val']*obs)/nr; nome=f"para igualar a PNS, não respondidas precisariam ter {p_nr*100:.1f}% LGB+"
        tot=d['val']*obs+nr*p_nr
        L.append(f"| {y} | {nome} | {tot*100:.2f}% | {tot/pns:.2f} |")
L.append("Leitura: sob MCAR o Sinan dá ~4,1% (razão 0,6 da PNS); para igualar a PNS, as 24% não respondidas precisariam ser ~15-16% LGB+ (quase 4x a parcela observada), o que é implausível como única explicação; a diferença residual é compatível com (a) não resposta diferencial moderada (LGB+ omitem mais a orientação no serviço de saúde) somada a (b) menor procura de serviço de saúde por LGB+ vitimizados e (c) diferença de instrumento (PNS = autorrelato em 12 m; Sinan = notificação do profissional). Em todos os cenários exceto o pior caso extremo, a parcela LGB+ fica entre 2x e 3,6x a prevalência populacional (1,89%): a direção da sobre-representação é robusta; a magnitude não é identificada entre 2x e 3,7x.")
open((REPO_ROOT + '/dados/sinan/resumo.md'),'a').write("\n".join(L)+"\n"); print("\n".join(L))
