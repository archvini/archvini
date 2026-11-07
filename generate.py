#!/usr/bin/env python3
"""Gera os SVGs pixel art do README de perfil do GitHub.
Rode: python3 generate.py  (cria a pasta assets/ e o README.md)
Edite os textos na seção CONTEUDO e rode de novo.
"""
import os
import unicodedata

# ---------------------------------------------------------------- fonte 5x7
FONT_SRC = """
A:01110/10001/10001/11111/10001/10001/10001
B:11110/10001/10001/11110/10001/10001/11110
C:01110/10001/10000/10000/10000/10001/01110
D:11110/10001/10001/10001/10001/10001/11110
E:11111/10000/10000/11110/10000/10000/11111
F:11111/10000/10000/11110/10000/10000/10000
G:01110/10001/10000/10111/10001/10001/01111
H:10001/10001/10001/11111/10001/10001/10001
I:01110/00100/00100/00100/00100/00100/01110
J:00111/00010/00010/00010/00010/10010/01100
K:10001/10010/10100/11000/10100/10010/10001
L:10000/10000/10000/10000/10000/10000/11111
M:10001/11011/10101/10101/10001/10001/10001
N:10001/11001/10101/10011/10001/10001/10001
O:01110/10001/10001/10001/10001/10001/01110
P:11110/10001/10001/11110/10000/10000/10000
Q:01110/10001/10001/10001/10101/10010/01101
R:11110/10001/10001/11110/10100/10010/10001
S:01111/10000/10000/01110/00001/00001/11110
T:11111/00100/00100/00100/00100/00100/00100
U:10001/10001/10001/10001/10001/10001/01110
V:10001/10001/10001/10001/10001/01010/00100
W:10001/10001/10001/10101/10101/11011/10001
X:10001/10001/01010/00100/01010/10001/10001
Y:10001/10001/01010/00100/00100/00100/00100
Z:11111/00001/00010/00100/01000/10000/11111
0:01110/10001/10011/10101/11001/10001/01110
1:00100/01100/00100/00100/00100/00100/01110
2:01110/10001/00001/00010/00100/01000/11111
3:11110/00001/00001/01110/00001/00001/11110
4:00010/00110/01010/10010/11111/00010/00010
5:11111/10000/11110/00001/00001/10001/01110
6:00110/01000/10000/11110/10001/10001/01110
7:11111/00001/00010/00100/01000/01000/01000
8:01110/10001/10001/01110/10001/10001/01110
9:01110/10001/10001/01111/00001/00010/01100
.:00000/00000/00000/00000/00000/01100/01100
,:00000/00000/00000/00000/01100/00100/01000
::00000/01100/01100/00000/01100/01100/00000
!:00100/00100/00100/00100/00100/00000/00100
-:00000/00000/00000/11111/00000/00000/00000
+:00000/00100/00100/11111/00100/00100/00000
/:00001/00001/00010/00100/01000/10000/10000
?:01110/10001/00001/00010/00100/00000/00100
_:00000/00000/00000/00000/00000/00000/11111
>:10000/01000/00100/00010/00100/01000/10000
 :00000/00000/00000/00000/00000/00000/00000
"""
FONT = {}
for line in FONT_SRC.strip("\n").split("\n"):
    ch, rows = line[0], line[2:]
    FONT[ch] = rows.split("/")

# ---------------------------------------------------------------- cores
BG = "#0a0e0d"
PANEL = "#101916"
LINE = "#1f2e28"
FG = "#e9efe9"
MUTED = "#9aa89f"
GREEN = "#22e07a"
ORANGE = "#d97757"
DARK = "#06130d"
CREAM = "#f1ece1"

# mascote: olhos são buracos; os pés verdes ficam meia célula abaixo das pernas
MASCOT = [
    ".########.",
    ".##.##.##.",
    "###.##.###",
    ".########.",
    "..#....#..",
]
FEET = ["..#....#.."]


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.upper()


def tw(s, sc):
    """largura em px de um texto (sem o espaço final)"""
    return len(norm(s)) * 6 * sc - sc


def text(s, x, y, sc, color):
    out = []
    for i, ch in enumerate(norm(s)):
        rows = FONT.get(ch, FONT[" "])
        gx = x + i * 6 * sc
        for r, row in enumerate(rows):
            c = 0
            while c < 5:
                if row[c] == "1":
                    st = c
                    while c < 5 and row[c] == "1":
                        c += 1
                    out.append(
                        f'<rect x="{gx + st * sc}" y="{y + r * sc}" '
                        f'width="{(c - st) * sc}" height="{sc}" fill="{color}"/>'
                    )
                else:
                    c += 1
    return "\n".join(out)


def sprite(pattern, x, y, sc, color):
    out = []
    for r, row in enumerate(pattern):
        c = 0
        while c < len(row):
            if row[c] == "#":
                st = c
                while c < len(row) and row[c] == "#":
                    c += 1
                out.append(
                    f'<rect x="{x + st * sc}" y="{y + r * sc}" '
                    f'width="{(c - st) * sc}" height="{sc}" fill="{color}"/>'
                )
            else:
                c += 1
    return "\n".join(out)


def mascot(x, y, sc):
    """sc deve ser par; altura total = 6.5 * sc, largura = 10 * sc"""
    return (
        sprite(MASCOT, x, y, sc, ORANGE)
        + "\n"
        + sprite(FEET, x, y + 5 * sc + sc // 2, sc, GREEN)
    )


def rich(segs, y, sc, cx):
    """linha centralizada; segs = [(texto, None|'green'|'orange')]"""
    total = sum(len(norm(t)) * 6 * sc + (4 * sc if k else 0) for t, k in segs) - sc
    x = int(round(cx - total / 2))
    out = []
    for t, k in segs:
        w = len(norm(t)) * 6 * sc
        if k:
            col = GREEN if k == "green" else ORANGE
            out.append(
                f'<rect x="{x}" y="{y - 2 * sc}" width="{w - sc + 4 * sc}" '
                f'height="{11 * sc}" fill="{col}"/>'
            )
            out.append(text(t, x + 2 * sc, y, sc, DARK))
            x += w + 4 * sc
        else:
            out.append(text(t, x, y, sc, FG))
            x += w
    return "\n".join(out)


def svg(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" shape-rendering="crispEdges">\n{body}\n</svg>\n'
    )


def panel(w, h):
    return (
        f'<rect width="{w}" height="{h}" fill="{BG}"/>'
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="{PANEL}" '
        f'stroke="{LINE}" stroke-width="2"/>'
    )


def dashes(x0, x1, y, color=LINE):
    out, x = [], x0
    while x + 40 <= x1:
        out.append(f'<rect x="{x}" y="{y}" width="40" height="4" fill="{color}"/>')
        x += 48
    return "\n".join(out)


# ---------------------------------------------------------------- peças
def banner(name, sub1, segs2, tagline, badge):
    W, H = 830, 380
    b = [panel(W, H)]
    # badge "FEITO!" + mascote
    bw = tw(badge, 2) + 24
    b.append(f'<rect x="{W - 112 - bw}" y="40" width="{bw}" height="30" fill="{CREAM}"/>')
    b.append(text(badge, W - 112 - bw + 12, 51, 2, DARK))
    b.append(mascot(W - 96, 36, 4))
    # nome
    sc = 7
    b.append(text(name, int(round((W - tw(name, sc)) / 2)), 100, sc, FG))
    # subtítulos
    sc = 3
    b.append(text(sub1, int(round((W - tw(sub1, sc)) / 2)), 185, sc, FG))
    b.append(rich(segs2, 230, sc, W / 2))
    # chão pontilhado + mascote andando
    b.append(dashes(48, W - 48, 330))
    b.append(
        '<g><animateTransform attributeName="transform" type="translate" '
        'values="48 0;742 0;48 0" dur="9s" repeatCount="indefinite"/>'
        + mascot(0, 302, 4)
        + "</g>"
    )
    b.append(text(tagline, int(round((W - tw(tagline, 2)) / 2)), 346, 2, MUTED))
    return svg(W, H, "\n".join(b))


def section(title):
    W, H = 830, 72
    b = [panel(W, H)]
    b.append(f'<rect x="28" y="28" width="16" height="16" fill="{GREEN}"/>')
    b.append(text(title, 64, 25, 3, FG))
    return svg(W, H, "\n".join(b))


def card(title, tag, lines, tag_color=GREEN):
    W = 830
    H = 28 + 35 + 26 + len(lines) * 22 - 8 + 30
    b = [panel(W, H)]
    b.append(text(title, 32, 28, 5, FG))
    tx = 32 + tw(title, 5) + 24
    tgw = tw(tag, 2) + 24
    b.append(f'<rect x="{tx}" y="30" width="{tgw}" height="30" fill="{tag_color}"/>')
    b.append(text(tag, tx + 12, 41, 2, DARK))
    y = 28 + 35 + 26
    for ln in lines:
        b.append(text(ln, 32, y, 2, MUTED))
        y += 22
    return svg(W, H, "\n".join(b))


def chips(rows):
    W = 830
    H = 24 + len(rows) * 45 + (len(rows) - 1) * 14 + 24
    b = [panel(W, H)]
    y = 24
    for row in rows:
        widths = [tw(t, 3) + 36 for t, _ in row]
        total = sum(widths) + 14 * (len(row) - 1)
        x = int(round((W - total) / 2))
        for (t, col), w in zip(row, widths):
            b.append(
                f'<rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="43" '
                f'fill="{BG}" stroke="{col}" stroke-width="2"/>'
            )
            b.append(text(t, x + 18, y + 12, 3, FG))
            x += w + 14
        y += 45 + 14
    return svg(W, H, "\n".join(b))


def button(label, color=GREEN):
    w, h = tw(label, 3) + 52, 52
    b = [
        f'<rect width="{w}" height="{h}" fill="{color}"/>',
        text(label, 26, 15, 3, DARK),
    ]
    return svg(w, h, "\n".join(b))


def mascot_panel():
    W, H = 830, 108
    b = []
    b.append(
        "<g>"
        '<animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/>'
        + mascot(int(W / 2 - 40), 20, 8)
        + "</g>"
    )
    return svg(W, H, "\n".join(b))


# ================================================================ CONTEUDO
# (acentos são removidos automaticamente: a fonte pixel só tem A-Z e 0-9)
NOME = "Vinicius"
SUB1 = "Desenvolvedor Full Stack em formação."
SUB2 = [("Aprendendo na prática.", None), (".", None)]
TAGLINE = "React / Node / MySQL / IA"

CARDS = {
    "card-sobre": ("Quem sou eu", "em evolução", [
        "Cursando Desenvolvedor Full Stack na Geração Tech.",
        "Prática em HTML, CSS, JS e React. Indo pro backend.",
        "Aprendo construindo: um projeto de cada vez.",
    ]),
    "card-ia": ("App com IA", "em breve", [
        "App com IA feito com TypeScript e Python.",
    ]),
    "card-senhas": ("Gerador de senhas", "no ar", [
        "Feito com JavaScript.",
    ]),
    "card-atividades": ("Lista de atividades", "no ar", [
        "Lista de tarefas em JavaScript para organizar suas atividades.",
        "Anote o que fazer no dia a dia e não esqueça nenhuma tarefa.",
    ]),
}

STACK = [
    [("HTML", GREEN), ("CSS", GREEN), ("JS", GREEN), ("React", GREEN), ("Node", GREEN)],
    [("MySQL", GREEN), ("Git", GREEN), ("Insomnia", GREEN)],
]

README = """<!-- Troque SEU_USUARIO e SEU_LINKEDIN. Para mudar textos, edite generate.py e rode de novo. -->

<div align="center">
  <img src="assets/banner.svg" alt="Vinícius — Desenvolvedor Full Stack em formação" />
</div>

<br/>

<div align="center">
  <img src="assets/section-sobre.svg" alt="Sobre mim" />
  <img src="assets/card-sobre.svg" alt="Quem sou eu" />
</div>

<br/>

<div align="center">
  <img src="assets/section-build.svg" alt="O que estou construindo" />
  <a href="https://github.com/archvini/app"><img src="assets/card-ia.svg" alt="App com IA" /></a>
  <a href="https://github.com/archvini/gerador-senhas-aleatorias"><img src="assets/card-senhas.svg" alt="Gerador de senhas" /></a>
  <a href="https://github.com/archvini/focusflow-task-manager"><img src="assets/card-atividades.svg" alt="Lista de atividades" /></a>
</div>

<br/>

<div align="center">
  <img src="assets/section-stack.svg" alt="Stack" />
  <img src="assets/stack.svg" alt="HTML, CSS, JS, React, Node, MySQL, Git, Insomnia" />
</div>

<br/>

<div align="center">
  <img src="assets/section-contato.svg" alt="Contato" />
  <a href="https://www.linkedin.com/in/viniciusdevfllstk/"><img src="assets/btn-linkedin.svg" alt="LinkedIn" /></a>
  &nbsp;
  <a href="https://github.com/archvini"><img src="assets/btn-github.svg" alt="GitHub" /></a>
  &nbsp;
  <a href="mailto:marcosviniciuspessoa5@gmail.com"><img src="assets/btn-email.svg" alt="E-mail" /></a>
</div>

<br/>

<table align="center" bgcolor="#101916" border="1" bordercolor="#1f2e28" cellpadding="12" cellspacing="0">
    <tr>
        <td align="center">
            <img src="assets/thanks.svg" alt="Mascote pixel art" width="830" />
            <p align="center">
                <img src="https://github-readme-mwendwa.vercel.app/api/top-langs/?username=archvini&layout=compact&count_private=true&theme=blue-green&title_color=00b3ff" alt="Linguagens mais usadas" />
            </p>
            <p align="center">
                <img src="https://streak-stats.demolab.com/?user=archvini&count_private=true&theme=blue-green&title_color=00b3ff" alt="Sequência de contribuições no GitHub" />
            </p>
            <p align="center">
                <a href="https://github.com/stats-organization/github-stats-extended"><img src="https://github-stats-extended.vercel.app/api?username=archvini" alt="Estatísticas do GitHub" /></a>
            </p>
        </td>
    </tr>
</table>
"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "assets")
    os.makedirs(out, exist_ok=True)

    def save(name, content):
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(content)

    save("banner.svg", banner(NOME, SUB1, SUB2, TAGLINE, "olá"))
    save("section-sobre.svg", section("Sobre mim"))
    save("section-build.svg", section("O que estou construindo"))
    save("section-stack.svg", section("Stack"))
    save("section-contato.svg", section("Contato"))
    for fname, (t, tag, lines) in CARDS.items():
        save(fname + ".svg", card(t, tag, lines))
    save("stack.svg", chips(STACK))
    save("btn-linkedin.svg", button("LinkedIn"))
    save("btn-github.svg", button("GitHub"))
    save("btn-email.svg", button("E-mail", ORANGE))
    save("thanks.svg", mascot_panel())

    with open(os.path.join(here, "README.md"), "w", encoding="utf-8") as f:
        f.write(README)
    print("ok:", len(os.listdir(out)), "svgs em", out)


if __name__ == "__main__":
    main()
