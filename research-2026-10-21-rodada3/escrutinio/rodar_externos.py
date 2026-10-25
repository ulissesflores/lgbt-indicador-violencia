"""Escrutínio adversarial por assinaturas (custo zero): codex (gpt-6-astra), grok, agy (gemini-4-argon-high). Cada revisor recebe o MESMO pacote e um papel diferente.
FERRAMENTA DO AUTOR (não re-executável no clone): chama CLIs de modelos de linguagem pela assinatura do autor; defina GROK_BIN, AGY_BIN (e codex no PATH) com o caminho do executável. As saídas gravadas no repositório são as da execução original.
Rodar: python3 -I rodar_externos.py   Saídas: revisao_<modelo>.md + revisao_<modelo>.hora.txt. Nada é enviado além do pacote (sem nomes de vítimas, sem credenciais)."""
import os as _os
import pathlib as _pl

REPO_ROOT = _os.environ.get("REPO_ROOT") or str(_pl.Path(__file__).resolve().parents[2])  # raiz configurável
import subprocess, os, tempfile, shutil, datetime, hashlib, sys
from concurrent.futures import ThreadPoolExecutor
D = (REPO_ROOT + "/research-2026-10-21-rodada3/escrutinio")
PACOTE = open(f"{D}/PACOTE-ESCRUTINIO.md", encoding="utf-8").read()
FORMATO = """FORMATO OBRIGATÓRIO (PT-BR, sem preâmbulo):
Liste no máximo 12 ATAQUES, do mais grave ao menos grave. Para cada um:
### A<n> [severidade 1-5] <título curto>
- Trecho atacado (literal, curto, com a seção §):
- Por que é grave (o argumento do revisor hostil, o mais forte possível):
- Resposta/correção que o autor pode dar (texto proposto, que NÃO invente fonte nem número):
- Evidência que faltaria para fechar o ataque:
Depois: '## O que o dossiê acerta (steel-man)': até 6 pontos onde o dossiê resiste ao ataque mais forte.
Depois: '## Frases que eu cortaria ou reescreveria' (até 8, citando literal).
Regras: não use a web; não invente referência; se não souber, diga 'não sei'; ataque o ARGUMENTO e a EVIDÊNCIA apresentados, não o tema."""
CONTEXTO = """Você é revisor de um dossiê de pesquisa acadêmica brasileira (violência contra mulheres, negros e pessoas LGBT+; indicadores, GGB, governos, falsas alegações) que será submetido a revisão por pares e atacado por bancadas políticas de DIREITA e de ESQUERDA. O autor quer a versão mais difícil de refutar. Abaixo, um extrato do dossiê. Regras do autor: só dado público; nada de pesquisa de campo; frequência de uma afirmação mede circulação, não verdade; 'não sei' é resposta válida."""
PAPEIS = {
 "codex": "PAPEL: revisor Q1 de métodos quantitativos (amostragem complexa, poder, econometria de painel/TWFE, captura-recaptura, padronização por idade, projeção, inferência causal, múltiplas comparações). Procure: erro de método, inferência além do dado, intervalos mal interpretados, 'nulo' tratado como 'ausência de efeito', pareamentos sem ajuste, contagens usadas como taxas, comparação entre fontes não independentes.",
 "grok": "PAPEL: DOIS revisores hostis, em duas seções separadas. (1) 'Crítico de DIREITA': tenta mostrar que o dossiê exagera a vitimização LGBT, é leniente com dados de ONG, usa linguagem enviesada ou esconde o que desfavorece a narrativa de perseguição estatal. (2) 'Crítico de ESQUERDA': tenta mostrar que o dossiê minimiza a violência, trata testes sem poder como 'não há efeito', desqualifica o GGB por pedantismo metodológico, ignora a subnotificação estrutural ou usa a régua de países ricos. Em cada seção: no máximo 6 ataques no formato pedido, sem poupar ninguém.",
 "agy": "PAPEL: auditor de FONTES e de ESCOPO. Procure: afirmação mais forte que a fonte permite, número sem fonte no extrato, linguagem causal sem desenho, generalização de um estudo (país/ano/amostra) para o Brasil, citação de abstract tratada como leitura, incoerência interna entre seções, uso de 'independente' onde há dependência, e onde o texto afirma 'não existe/ninguém' sem espaço de busca enumerado.",
}
def hora(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def prompt(papel): return f"{CONTEXTO}\n\n{PAPEIS[papel]}\n\n{FORMATO}\n\n=== EXTRATO DO DOSSIÊ ===\n{PACOTE}"
def run(papel):
    t0 = hora(); wd = tempfile.mkdtemp(prefix="escrut_")
    try:
        if papel == "codex":
            ch = tempfile.mkdtemp(prefix="codexhome_")
            shutil.copy(os.path.expanduser("~/.codex/auth.json"), ch)
            r = subprocess.run(["/opt/homebrew/bin/codex", "exec", "-m", "gpt-6-astra", "--skip-git-repo-check", "-C", wd, "-"], input=prompt(papel), capture_output=True, text=True, timeout=1500, env=dict(os.environ, CODEX_HOME=ch))
            shutil.rmtree(ch, ignore_errors=True)
        elif papel == "grok":
            r = subprocess.run([_os.environ.get("GROK_BIN", "grok"), "-p", prompt(papel)], capture_output=True, text=True, timeout=1500, cwd=wd)
        else:
            r = subprocess.run([_os.environ.get("AGY_BIN", "agy"), "-p", prompt(papel), "--model", "gemini-4-argon-high"], capture_output=True, text=True, timeout=1500, cwd=wd)
        out = r.stdout if r.stdout.strip() else r.stderr
        rc = r.returncode
    except Exception as e:
        out, rc = f"ERRO: {e}", -1
    shutil.rmtree(wd, ignore_errors=True)
    open(f"{D}/revisao_{papel}.md", "w", encoding="utf-8").write(f"<!-- {papel} rc={rc} início {t0} fim {hora()} pacote sha256 {hashlib.sha256(PACOTE.encode()).hexdigest()[:16]} -->\n{out}\n")
    return papel, rc, len(out)
if __name__ == "__main__":
    with ThreadPoolExecutor(3) as ex:
        for res in ex.map(run, ["codex", "grok", "agy"]): print(res, flush=True)
