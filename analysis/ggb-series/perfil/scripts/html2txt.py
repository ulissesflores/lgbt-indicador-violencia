"""html -> texto do <main>/article (stdlib). uso: python3 -I html2txt.py in.html [out.txt]"""
import sys, re, html
h = open(sys.argv[1], encoding='utf8', errors='replace').read()
h = re.sub(r'(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>', ' ', h)
m = re.search(r'(?is)<main.*?</main>', h) or re.search(r'(?is)<article.*?</article>', h)
b = m.group(0) if m else h
b = re.sub(r'(?i)<br\s*/?>|</(p|div|h\d|li|tr|section)>', '\n', b)
b = re.sub(r'(?s)<[^>]+>', ' ', b)
b = html.unescape(b)
b = re.sub(r'[ \t\xa0]+', ' ', b)
b = re.sub(r'\n\s*\n+', '\n', b).strip()
out = sys.argv[2] if len(sys.argv) > 2 else None
(open(out, 'w', encoding='utf8').write(b) if out else print(b))
