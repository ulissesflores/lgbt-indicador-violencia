"""Lista os nomes de campo do cabecalho DBF (nao comprimido) dos microdados SIM DOBR (DATASUS). Uso: sim_campos.py <arquivo.dbc>"""
import struct,sys,hashlib
p=sys.argv[1]
b=open(p,'rb').read(65536)
hl=struct.unpack('<H',b[8:10])[0]
names=[]
i=32
while i<hl-1 and b[i]!=0x0D:
    names.append(b[i:i+11].split(b'\0')[0].decode('latin-1')); i+=32
print(p); print('sha256',hashlib.sha256(open(p,'rb').read()).hexdigest()); print(len(names),'campos'); print(' '.join(names))
print('contem ORIENT/IDENTG/GENERO/SEXUAL:',[n for n in names if any(k in n.upper() for k in ('ORIENT','IDENTG','GENER','SEXUAL','LGBT'))])
