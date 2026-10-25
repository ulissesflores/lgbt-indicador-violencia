# Roadmap

Próxima versão honesta, por ordem:

1. **Colab de replicação** (`colab/replication.ipynb`): rodar a Trilha 1 sem instalar nada, conferir `make_provenance.py --verify`,
   `scripts/inventario_publico.py --check` e os testes, e mostrar os números centrais (inclusive C09 e C10) lidos dos CSV.
2. **CI no GitHub** (Linux, Python 3.12 e 3.13): exercida a partir do commit inicial; acompanhar diferenças de última casa decimal entre
   bibliotecas matemáticas.
3. **Trilha 2 completa no CI semanal**: SIM, Sinan e PNS baixados e re-agregados (hoje só a aquisição e o hash foram testados para SIM e Sinan).
4. **Registro externo com carimbo de tempo (OSF)** dos pré-registros ainda confirmatórios (painel de governos, projeção 2026-2030); o hash
   prova conteúdo, não anterioridade (`REPRODUCIBILITY.md`).
5. **Disque 100**: derivados, dicionário harmonizado entre os três formatos e pré-registro em `dados/disque100/`, com teste
   `tests/test_disque100.py` (unidade de contagem, duplicatas, quebras de série e períodos parciais).
6. **Índice de afirmações** (`manifest/CLAIMS.csv`): cada afirmação central ligada a população, período, arquivo, teste e limitação.
7. **Escrutínio externo do repositório**: reprodução do zero em máquina limpa e revisão por pessoa de fora; achados viram issues.
8. **Figuras dos dados (não só do artigo) como código**, como `paper/figures/make_figures.py`.
9. **Artigo derivado do repositório**: entra num commit posterior, citando a URL e o `chain_hash` daqui, com o sha256 do PDF em `paper/PAPER-SHA256.txt` (fora do selo).
10. **Versão 1.0.0** só imediatamente antes do primeiro release que cunha o DOI.
