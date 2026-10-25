"""grep por pagina em PDF (pdftotext por pagina, cache em memoria).
uso: python3 -I gp.py arquivo.pdf 'regex' [largura=220]
imprime: pag | trecho (whitespace normalizado)"""
import sys, re, subprocess
pdf, rx = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 220
n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
txt = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
for i, t in enumerate(txt[:n], 1):
    t = re.sub(r'\s+', ' ', t)
    for m in re.finditer(rx, t, re.I):
        s = max(0, m.start() - w // 2); print(f'p{i} | ...{t[s:m.end() + w // 2]}...')
