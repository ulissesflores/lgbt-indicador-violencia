"""O artigo é UM documento: corpo, Referências e Apêndices A a D no mesmo paper.md (um PDF só).

Trava: (1) o Apêndice A (tabelas completas) é idêntico ao gerado por tools/make_anexos.py dos arquivos do
repositório, e só rótulos mudam em relação ao arquivo de origem (nenhum número é digitado); (2) as tabelas novas
da v0.3 estão no Apêndice A; (3) a ordem do documento é Resumo, Abstract, seções 1 a 7, Referências e Apêndices A, B,
C e D, sem marcador de segunda parte nem remissão a "anexo" ou a outro PDF; (4) a numeração APA: Tabelas 1 a N do
corpo e Tabelas A1..An, B1.., C1.., D1.. de cada apêndice, sem buraco nem repetição, cada uma dentro do seu apêndice;
Figuras 1 a N na ordem, cada arquivo de figura uma vez; (5) toda remissão a Tabela ou Figura aponta para um elemento
que existe; (6) controle negativo: um número trocado no Apêndice A reprova a conferência (e a mesma cópia sem a
troca passa). Uso: pytest ou python3 -I tests/test_anexo.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
GERADOR = PAPER / "tools" / "make_anexos.py"
INI, FIM = "<!-- apendice-a:inicio -->", "<!-- apendice-a:fim -->"
NOVAS_V03 = ["c08_cenarios_marginais.csv", "r6_ic_wild_invertido.csv", "c10_e1_federal.csv", "c10_e2_resumo.csv",
             "c09_d1_resultados.csv", "c09_d2_resultados.csv", "r7_parlamento_sensibilidade.csv"]


def _texto() -> str:
    return (PAPER / "paper.md").read_text(encoding="utf-8")


def _gerador(paper_dir: Path, opcao: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", str(paper_dir / "tools" / "make_anexos.py"), opcao],
                          capture_output=True, text=True)


def _secoes(texto: str) -> list[tuple[str, int]]:
    """Títulos de nível 1 (## ...) com a posição no texto."""
    return [(m.group(1).strip(), m.start()) for m in re.finditer(r"^## (.+)$", texto, flags=re.M)]


def test_apendice_a_identico_ao_gerado():
    """make_anexos.py --conferir devolve 0."""
    r = _gerador(PAPER, "--conferir")
    assert r.returncode == 0, r.stdout + r.stderr


def test_apendice_a_so_muda_rotulo():
    """make_anexos.py --provar: célula a célula, só rótulos (mapa ROTULOS) e setas entre anos mudam."""
    r = _gerador(PAPER, "--provar")
    assert r.returncode == 0, r.stdout + r.stderr


def test_apendice_a_traz_as_tabelas_da_v03():
    """Cada arquivo novo da v0.3 aparece como fonte de uma tabela do Apêndice A."""
    texto = _texto()
    bloco = texto[texto.index(INI):texto.index(FIM)]
    for nome in NOVAS_V03:
        assert nome in bloco, nome


def test_um_documento_com_apendices_a_a_d():
    """Ordem dos títulos de nível 1 e nenhuma segunda parte, anexo ou remissão a outro PDF."""
    texto = _texto()
    tit = [t for t, _ in _secoes(texto)]
    esperado_inicio = ["Resumo", "Abstract", "1. Introdução", "2. Método", "3. Resultados", "4. Discussão",
                       "5. Ameaças à validade", "6. Reprodutibilidade", "7. Conclusão", "Referências"]
    assert tit[:len(esperado_inicio)] == esperado_inicio, tit
    apend = tit[len(esperado_inicio):]
    assert [a.split(" — ")[0] for a in apend] == ["Apêndice A", "Apêndice B", "Apêndice C", "Apêndice D"], apend
    assert texto.count(INI) == 1 and texto.count(FIM) == 1
    assert texto.index(INI) > dict(_secoes(texto))[apend[0]]                       # o bloco gerado fica dentro do Apêndice A
    assert "<!-- parte:" not in texto and "anexo-a:" not in texto
    for proibido in (r"PDF de anexos", r"artigo principal", r"\bAnexos? [A-F]\b", r"^## Anexo"):
        assert not re.search(proibido, texto, flags=re.M), proibido


def test_numeracao_das_tabelas_apa():
    """Corpo: Tabela 1..N em ordem. Apêndices: A1..An, B1.., C1.., D1.., cada uma dentro do seu apêndice."""
    texto = _texto()
    sec = _secoes(texto)
    inicio_apend = next(p for t, p in sec if t.startswith("Apêndice A"))
    rotulos = [(m.group(1), m.start()) for m in re.finditer(r"^\*\*Tabela ([A-D]?\d+)\*\*\s*$", texto, flags=re.M)]
    corpo = [int(r) for r, p in rotulos if p < inicio_apend]
    assert corpo == list(range(1, len(corpo) + 1)), corpo
    assert all(p > inicio_apend for r, p in rotulos if not r.isdigit())
    for letra in "ABCD":
        ini = next(p for t, p in sec if t.startswith(f"Apêndice {letra}"))
        fim = next((p for t, p in sec if p > ini), len(texto))
        dentro = [r for r, p in rotulos if ini < p < fim]
        assert dentro == [f"{letra}{i}" for i in range(1, len(dentro) + 1)] and dentro, (letra, dentro)
    # rótulo APA: linha do número, linha em branco, título em itálico
    for m in re.finditer(r"^\*\*Tabela [A-D]?\d+\*\*\s*\n\n(.+)$", texto, flags=re.M):
        assert re.fullmatch(r"\*[^*].*\*", m.group(1).strip()), m.group(1)[:60]


def test_numeracao_das_figuras():
    """Figura 1..N em ordem, cada arquivo uma vez, rótulo igual ao texto alternativo e Nota logo abaixo."""
    texto = _texto()
    nums = [int(n) for n in re.findall(r"^\*\*Figura (\d+)\*\*\s*$", texto, flags=re.M)]
    assert nums == list(range(1, len(nums) + 1)), nums
    imgs = re.findall(r"^!\[Figura (\d+)\]\(figures/([\w.]+\.png)\)\s*$", texto, flags=re.M)
    assert [int(n) for n, _ in imgs] == nums
    arquivos = [a for _, a in imgs]
    assert len(set(arquivos)) == len(arquivos) and all((PAPER / "figures" / a).exists() for a in arquivos)
    for m in re.finditer(r"^!\[Figura \d+\]\(figures/[\w.]+\.png\)\s*\n\n(.+)$", texto, flags=re.M):
        assert m.group(1).startswith("*Nota.*") and "Fonte:" in m.group(1), m.group(1)[:60]


def test_remissoes_apontam_para_elementos_existentes():
    """Toda 'Tabela X' / 'Figura N' citada no texto existe como elemento rotulado."""
    texto = _texto()
    tabs = set(re.findall(r"^\*\*Tabela ([A-D]?\d+)\*\*\s*$", texto, flags=re.M))
    figs = set(re.findall(r"^\*\*Figura (\d+)\*\*\s*$", texto, flags=re.M))
    citadas_t = set(re.findall(r"(?<!\*\*)Tabelas? ([A-D]?\d{1,2})\b", texto))   # 3+ dígitos = tabela do SIDRA (ex.: 9514)
    citadas_f = set(re.findall(r"(?<!\*\*)Figuras? (\d+)\b", texto))
    assert citadas_t <= tabs, sorted(citadas_t - tabs)
    assert citadas_f <= figs, sorted(citadas_f - figs)


def test_controle_negativo_numero_alterado_reprova():
    """Numa cópia do artigo com um valor do Apêndice A trocado, a conferência falha; sem a troca, passa."""
    texto = _texto()
    a = texto.index(INI)
    alvo = "| 2,82 [2,16; 3,68] |"
    assert texto.find(alvo, a) > 0
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "paper"
        (copia / "tools").mkdir(parents=True)
        shutil.copy2(GERADOR, copia / "tools" / "make_anexos.py")
        i = texto.index(alvo, a)
        (copia / "paper.md").write_text(texto[:i] + "| 2,83 [2,16; 3,68] |" + texto[i + len(alvo):], encoding="utf-8")
        # o gerador lê os dados a partir de REPO = paper/.. : a cópia precisa ver os mesmos dados
        for d in ("dados", "docs", "research-2026-10-21-rodada3"):
            (Path(tmp) / d).symlink_to(PAPER.parent / d)
        (copia / "figures").symlink_to(PAPER / "figures")
        r = _gerador(copia, "--conferir")
        (copia / "paper.md").write_text(texto, encoding="utf-8")
        r_ok = _gerador(copia, "--conferir")
    assert r.returncode == 1 and "[FAIL] Apêndice A diverge" in r.stdout, r.stdout + r.stderr
    assert r_ok.returncode == 0, r_ok.stdout + r_ok.stderr



# ------------------------------------------------------------------ texto VIGENTE x arquivos de dados (v0.4.1, A2-15 do segundo exame)
REPO = PAPER.parent


def _csv(rel: str) -> list[dict]:
    import csv
    with open(REPO / rel, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _br(x: float, casas: int = 1) -> str:
    from decimal import ROUND_HALF_UP, Decimal
    return f"{Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP):.{casas}f}".replace(".", ",")


def test_texto_vigente_queda_de_2019_e_placebo():
    """Nota da Figura 20 e seção 3.7: a quebra de 2019 exclui zero e o placebo de 2018 também (c09_d1_resultados.csv)."""
    r = next(x for x in _csv("dados/presidencia/c09_d1_resultados.csv") if x["serie"] == "Brasil" and x["desfecho"] == "agressao" and x["quebra"] == "2019")
    lo, hi, p = float(r["pct_lo"]), float(r["pct_hi"]), float(r["p"])
    assert hi < 0 and float(r["placebo_pct_hi"]) < 0                                  # os dois intervalos excluem zero
    t = " ".join(_texto().split())
    frase = f"A queda de 2019 é distinguível de zero (-{_br(-float(r['pct']))}%; IC95% -{_br(-lo)}% a -{_br(-hi)}%; p = {_br(p, 3)})"
    assert frase in t, frase
    assert "o resultado é \"não distinguível de zero, com poder baixo\"" not in t      # a frase antiga da v0.4 saiu


def test_texto_vigente_ggb_estrito_e_captura_recaptura():
    """Seção 3.4: 50 de 160 (40 com correspondência estrita) e a faixa de Chapman pela regra de pareamento."""
    import json
    cod = _csv("research-2026-10-21-rodada3/F3-ggb/dados/codificacao_A.csv")
    ver = [x for x in cod if x["fonte"] == "R" and x["corresp"] in ("S", "P") and x["morte"] == "S" and x["lgbt"] == "S"]
    estrito = sum(x["corresp"] == "S" for x in ver)
    assert (len(cod), len(ver), estrito) == (160, 50, 40)
    t = " ".join(_texto().split())
    assert f"fração é de {estrito} em {len(cod)} ({_br(100 * estrito / len(cod))}%)" in t
    sens = json.loads((REPO / "research-2026-10-21-rodada3/F3-ggb/dados/captura_recaptura_sensibilidade.json").read_text(encoding="utf-8"))
    ch = [s["chapman"] for s in sens]
    cob = [100 * s["cob_ggb"] for s in sens]
    assert f"o total vai de {_br(min(ch), 0)} a {_br(max(ch), 0)} e a parcela, de {_br(min(cob), 0)}% a {_br(max(cob), 0)}%" in t


def test_texto_vigente_faltante_do_sinan():
    """Seções 3.5 e 4.4: faltante efetivo 2023-2025 arredondado meio para cima sobre as contagens (42% a 44%, não 45%)."""
    br_ = {int(r["ano"]): 100 * (int(r["m_ign_branco"]) + int(r["m_nao_se_aplica"])) / int(r["n_interpessoal"])
           for r in _csv("dados/sinan/serie_campo55_uf_ano.csv") if r["uf"] == "BR"}
    lo, hi = min(br_[a] for a in (2023, 2024, 2025)), max(br_[a] for a in (2023, 2024, 2025))
    t = _texto()
    assert f"{_br(lo, 0)}% a {_br(hi, 0)}% de 2023 a 2025" in t and f"faltante efetivo de {_br(lo, 0)}% a {_br(hi, 0)}%" in t
    assert "42% a 45%" not in t


def test_texto_vigente_parlamento_e_resumo():
    """Resumo: duas regras na mortalidade, 1 de 49 (0 de 49 na codificação original) contra 2 de 38; p de Fisher do arquivo r7."""
    r7 = {x["codificacao_F2"]: x for x in _csv("research-2026-10-21-rodada3/escrutinio/simetria/r7_parlamento_sensibilidade.csv")}
    p1 = float(next(v["p_fisher"] for k, v in r7.items() if "literal" in k))
    p0 = float(next(v["p_fisher"] for k, v in r7.items() if "aplicada" in k))
    t = _texto()
    resumo = t.split("## Resumo", 1)[1].split("## Abstract", 1)[0]
    assert "\"sustentada\" pela regra complementar" in resumo and "\"parcial\" pela pré-registrada" in resumo
    assert "1 de 49" in resumo and "0 de 49" in resumo and "2 de 38" in resumo
    assert "agentes estaduais e locais ficaram fora da busca" in resumo
    assert f"p = {_br(p1, 2)}" in t and f"p = {_br(p0, 2)}" in t


if __name__ == "__main__":
    ok = 0
    testes = [(k, f) for k, f in sorted(globals().items()) if k.startswith("test_") and callable(f)]
    for nome, fn in testes:
        try:
            fn()
            ok += 1
            print(f"PASS {nome}")
        except AssertionError as e:
            print(f"FAIL {nome}: {e}")
    print(f"{ok}/{len(testes)} passaram")
    raise SystemExit(0 if ok == len(testes) else 1)
