"""Deriva a FONTE DE PUBLICACAO (markdown com estilos da casa) a partir do paper
canonico, por edicao de idioma. O pipeline do laboratorio exporta essa fonte para
DOCX/PDF (`build_export.sh`), e `validate_canon.py --lang <x>` e o juiz.

Contrato "bolo vs cozinha": o canonico fica no laboratorio, com marcador de numero
(`<!-- num:... -->`) e caminho relativo de figura; o artefato PUBLICO leva capa Codex
Hash, legenda visivel de figura/tabela e bibliografia em paragrafo com recuo deslocado.

Enxuto de proposito (escada da casa): o precedente `operating-point-dominance` mantem
a lista de referencias APA7 DUPLICADA dentro do script — uma segunda fonte de verdade
para o mesmo dado. Aqui a bibliografia sai do proprio canonico: os itens `- ` da secao
de referencias viram paragrafos do estilo Bibliography, sem reescrita manual.

Uso: python3 tools/make_export.py --lang pt-BR [--parte tudo|principal|anexos]
Saida: build/paper-export.md (tudo ou principal) ou build/anexos-export.md (anexos); figuras
referenciadas a partir de paper/, via --resource-path.

v0.3 (P2a): o MESMO canonico gera dois PDFs. O marcador `<!-- parte:anexos -->` do paper.md
separa o artigo principal (capa .. Apendices) dos anexos (Anexo A .. ultimo anexo). Texto novo
inserido em qualquer lado do marcador entra no PDF certo sem mexer nesta ferramenta.
Adaptado de um artigo anterior do laboratório (repositório privado).
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # paper/
PAPER = ROOT
LOGO = "tools/assets/codex-hash-lockup-stacked@2x.png"  # copia do logo da casa

PARTE = "<!-- parte:anexos -->"
LINHA_ANEXOS = "Anexos A a F (PDF de anexos do artigo)"  # linha extra da capa dos anexos; o titulo nao muda

SPACER = '\n```{=openxml}\n<w:p><w:pPr><w:spacing w:after="1100"/></w:pPr></w:p>\n```\n'

LANGS = {
    "pt-BR": {
        "src": "paper.md", "out": "build/paper-export.md",
        "cut": "## Resumo", "refs": "## Referências",
        "fig": "Figura", "tab": "Tabela", "data": "Data: 24 de outubro de 2026",
        "fim_refs": "## Apêndice A",
    },
    "en": {
        "src": "paper-final-en.md", "out": "paper-export-en.md",
        "cut": "## Abstract", "refs": "## References",
        "fig": "Figure", "tab": "Table", "data": "Date: September 4, 2026",
        "fim_refs": "## Appendix A",
    },
}


def capa(titulo: str, subtitulo: str, data: str, linha_extra: str = "") -> str:
    # alt text obrigatorio: sem ele o pandoc escreve o CAMINHO da imagem no `descr` do
    # DOCX, e o canon reprova caminho de sistema no pacote publicado.
    extra = f'\n::: {{custom-style="CoverInfo"}}\n**{linha_extra}**\n:::\n' if linha_extra else ""
    return f"""::: {{custom-style="FigureImage"}}
![Codex Hash Research Laboratory]({LOGO}){{width=5.2cm}}
:::
{SPACER}
::: {{custom-style="CoverTitle"}}
{titulo}
:::

::: {{custom-style="CoverSubtitle"}}
{subtitulo}
:::
{extra}{SPACER}
::: {{custom-style="CoverInfo"}}
**Carlos Ulisses Flores**
:::

::: {{custom-style="CoverInfo"}}
Codex Hash Research Laboratory
:::

::: {{custom-style="CoverSmall"}}
ORCID: 0000-0002-6034-7765
:::
{SPACER}
::: {{custom-style="CoverInfo"}}
{data}
:::

"""


def _titulo_e_subtitulo(texto: str) -> tuple[str, str]:
    """Capa a partir do H1 do canonico, partido no dois-pontos.

    Nada de titulo novo: o subtitulo da capa e a segunda metade do titulo que o autor
    escolheu no portao P2 — inventar linha de capa seria conteudo que ninguem aprovou.
    """
    h1 = re.search(r"^# (.+)$", texto, re.M)
    if not h1:
        raise SystemExit("[FATAL] paper canonico sem titulo H1")
    titulo = h1.group(1).strip()
    # v0.2: subtitulo explicito no front-matter (o titulo ditado pelo autor nao tem dois-pontos)
    sub = re.search(r'^subtitle:\s*"(.+)"\s*$', texto, re.M)
    if sub:
        return titulo, sub.group(1).strip()
    if ":" not in titulo:
        return titulo, ""
    a, b = titulo.split(":", 1)
    return a.strip(), b.strip().capitalize() if b.strip()[:1].islower() else b.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=sorted(LANGS), default="pt-BR")
    ap.add_argument("--parte", choices=("tudo", "principal", "anexos"), default="tudo")
    a = ap.parse_args()
    L, parte = LANGS[a.lang], a.parte
    src = PAPER / L["src"]
    out = PAPER / ("build/anexos-export.md" if parte == "anexos" else L["out"])
    t = src.read_text(encoding="utf-8")

    titulo, subtitulo = _titulo_e_subtitulo(t)

    # 1) capa no lugar do bloco de cabecalho (frontmatter + H1 + linha de autoria)
    corte = t.find(L["cut"])
    if corte == -1:
        raise SystemExit(f"[FATAL] secao de corte ausente: {L['cut']!r}")
    # v0.3: um so marcador de parte; sem ele, "principal" e "anexos" nao tem como existir
    if parte != "tudo" and t.count(PARTE) != 1:
        raise SystemExit(f"[FATAL] o canonico precisa de exatamente um {PARTE!r} (achados: {t.count(PARTE)})")
    m = t.find(PARTE)
    if parte == "principal":
        t = capa(titulo, subtitulo, L["data"]) + t[corte:m]
    elif parte == "anexos":
        # a quebra de página que abre o Anexo A no documento inteiro sobra aqui: a capa já fecha a página
        # e o fix_docx_tables põe pageBreakBefore em cada "Anexo X —" (senão nasce uma página em branco)
        resto = re.sub(r"^\s*<!-- quebra-de-pagina -->\s*", "", t[m + len(PARTE):])
        t = capa(titulo, subtitulo, L["data"], LINHA_ANEXOS) + resto
    else:
        t = capa(titulo, subtitulo, L["data"]) + t[corte:]
    t = t.replace(PARTE, "")

    # 2) marcador de numero e do laboratorio, nao do artefato publicado
    t = re.sub(r"<!--\s*num:[^>]*-->\s*", "", t)
    # v0.2: quebra de página explícita (o quadro de respostas abre página própria)
    t = t.replace("<!-- quebra-de-pagina -->",
                  '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```')
    t = re.sub(r"<!--\s*anexo-a:(inicio|fim)\s*-->\s*", "", t)
    # caminho longo em código inline não quebrava linha e abria buracos no texto justificado:
    # espaço de largura zero depois de "/" e "_" dá ponto de quebra (só no artefato publicado)
    t = re.sub(r"`([^`\n]{25,})`", lambda m: "`" + re.sub(r"([/_])", "\\1\u200b", m.group(1)) + "`", t)
    # hash hexadecimal longo (sem / nem _) em código inline: ponto de quebra a cada 16 dígitos
    t = re.sub(r"`([0-9a-f]{40,})`", lambda m: "`" + "\u200b".join(m.group(1)[i:i + 16] for i in range(0, len(m.group(1)), 16)) + "`", t)

    # 3) figura: `![Figura N — legenda](caminho)` -> rotulo + titulo + imagem (ordem APA)
    # figura alta não cabe na página junto da legenda (o LibreOffice joga a imagem para a
    # página seguinte e deixa a legenda sozinha): altura limitada a ALTURA_MAX polegadas.
    def _tamanho(caminho: str, legenda: str) -> str:
        from PIL import Image
        with Image.open(ROOT / caminho) as im:
            w, h = im.size
        largura = 6.5  # largura útil do modelo da casa, em polegadas
        # v0.3 (P2a): a altura máxima era fixa (5,6 in) e encolhia as figuras altas para 3,4-4,7 in de
        # largura, com a letra de dentro ilegível no PDF. Agora a figura alta ocupa a página: 9 in úteis
        # menos rótulo, legenda (cerca de 105 caracteres por linha de 11 pt, 0,25 in cada) e espaçamento,
        # com folga, para a imagem nunca ser empurrada para longe da legenda.
        linhas = -(-len(legenda) // 100)
        ALTURA_MAX = round(9.0 - 0.9 - 0.25 * linhas, 2)
        return "width=100%" if largura * h / w <= ALTURA_MAX else f"height={ALTURA_MAX}in"
    def figura(m: re.Match) -> str:
        num, legenda, caminho = m.group(1), m.group(2).strip().rstrip("."), m.group(3)
        return ('::: {custom-style="CaptionLabel"}\n' + f"{L['fig']} {num}" + "\n:::\n\n"
                '::: {custom-style="CaptionText"}\n' + legenda + "\n:::\n\n"
                '::: {custom-style="FigureImage"}\n'
                f"![{L['fig']} {num}]({caminho}){{{_tamanho(caminho, legenda)}}}" + "\n:::")
    t, n_fig = re.subn(rf"!\[{L['fig']} (\d+) — (.+?)\]\(([^)]+)\)", figura, t)

    # 4) tabela: `**Tabela N — titulo**` -> mesmo par de estilos
    def tabela(m: re.Match) -> str:
        return ('::: {custom-style="CaptionLabel"}\n' + f"{L['tab']} {m.group(1)}" + "\n:::\n\n"
                '::: {custom-style="CaptionText"}\n' + m.group(2).strip().rstrip(".") + "\n:::")
    t, n_tab = re.subn(rf"\*\*{L['tab']} (\d+) — (.+?)\*\*", tabela, t)

    # 5) bibliografia: itens `- ` viram paragrafos do estilo Bibliography (recuo
    #    deslocado, sem marcador de lista — exigencia do canon: `no_bullets`)
    if parte == "anexos":  # os anexos citam as Referencias do artigo principal; nao ha lista aqui
        out.write_text(t, encoding="utf-8")
        print(f"[OK] {out} (anexos: {n_fig} figuras, {n_tab} tabelas)")
        return
    ini, fim = t.rfind(L["refs"]), t.find(L["fim_refs"])
    if ini == -1 or fim <= ini:
        raise SystemExit(f"[FATAL] secao de referencias nao delimitada ({L['refs']} .. {L['fim_refs']})")
    zona = t[ini:fim]
    # o item comeca na linha `- ` e vai ate a proxima (ou ate o fim da zona): serve tanto
    # para a lista com linha em branco entre entradas quanto para a lista compacta.
    itens, resto, atual = [], [], None
    for linha in zona.splitlines():
        if linha.startswith("- "):
            if atual is not None:
                itens.append(atual)
            atual = linha[2:].strip()
        elif atual is not None and linha.strip() and not linha.startswith(("#", ">")):
            atual += " " + linha.strip()          # continuacao do mesmo item
        elif linha.strip() and not linha.startswith(L["refs"]):
            if atual is not None:
                itens.append(atual)
                atual = None
            resto.append(linha)  # nota de proveniencia etc.: preservada apos a lista
    if atual is not None:
        itens.append(atual)
    if not itens:
        raise SystemExit("[FATAL] nenhuma referencia em item de lista no canonico")
    t = (t[:ini] + f"{L['refs']}\n\n" + '::: {custom-style="Bibliography"}\n'
         + "\n\n".join(itens) + "\n:::\n\n"
         + ("\n".join(resto) + "\n\n" if resto else "") + t[fim:])

    out.write_text(t, encoding="utf-8")
    print(f"[OK] {out} ({len(itens)} referencias, {n_fig} figuras, {n_tab} tabelas)")


if __name__ == "__main__":
    main()
