"""Build the profile SVGs: a neofetch-style card and a text-glyph contribution grid.

Reads live numbers from the GitHub GraphQL API (needs GITHUB_TOKEN) and writes
assets/{card,grid}-{dark,light}.svg. Run daily by .github/workflows/build.yml.
"""
from __future__ import annotations

import json
import os
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USER = "Abh1shxkk"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"

MONO = "'JetBrains Mono','Cascadia Code','SF Mono',Consolas,Menlo,'DejaVu Sans Mono',monospace"

THEMES = {
    "dark": dict(bg="#0d1117", fg="#c9d1d9", mute="#6e7681", faint="#30363d", acc="#d29922"),
    "light": dict(bg="#ffffff", fg="#24292f", mute="#6e7781", faint="#d0d7de", acc="#9a6700"),
}

LOGO = [  # "AC" in a 5x7 pixel face
    ".###...####",
    "#...#.#....",
    "#...#.#....",
    "#####.#....",
    "#...#.#....",
    "#...#.#....",
    "#...#..####",
]

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, first: 100) {
      totalCount
      nodes { stargazerCount }
    }
    repositoriesContributedTo(contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount contributionLevel date } }
      }
    }
  }
}"""


def fetch() -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["user"]


def uptime(since: date, today: date) -> str:
    months = (today.year - since.year) * 12 + today.month - since.month - (today.day < since.day)
    y, m = divmod(months, 12)
    anchor = date(since.year + (since.month - 1 + months) // 12, (since.month - 1 + months) % 12 + 1, 1)
    d = (today - anchor.replace(day=min(since.day, 28))).days
    part = lambda n, w: f"{n} {w}{'' if n == 1 else 's'}"
    return ", ".join([part(y, "year"), part(m, "month"), part(d, "day")])


# ---------------------------------------------------------------------------- card

def card(t: dict, u: dict) -> str:
    stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])
    cal = u["contributionsCollection"]["contributionCalendar"]
    since = datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00")).date()
    today = datetime.now(timezone.utc).date()

    W = 54  # characters per info line, leaders included
    rows: list[tuple] = [
        ("title", "abhishek@meerut"),
        ("rule",),
        ("kv", "OS", "Windows 11, Ubuntu on the servers"),
        ("kv", "Uptime", uptime(since, today)),
        ("kv", "Host", "Subharti University, IT Dept"),
        ("kv", "Kernel", "Junior PHP Developer"),
        ("kv", "Previous", "Global Matrix Solution, 2025-26"),
        ("kv", "IDE", "VS Code"),
        ("gap",),
        ("kv", "Languages.Code", "PHP, TypeScript, JS, Python"),
        ("kv", "Languages.Stack", "Laravel, Node.js, Vue, React"),
        ("kv", "Languages.Real", "Hindi, English"),
        ("kv", "Infra", "Docker, cPanel, nginx, Postgres"),
        ("gap",),
        ("kv", "Now", "University ERP, 100+ college sites"),
        ("kv", "Shipped", "OPD Scan QC, OPD Scribe, ILMS"),
        ("kv", "Learning", "React + Laravel, deployments"),
        ("head", "Contact"),
        ("kv", "Email", "abhichauhan200504@gmail.com"),
        ("kv", "LinkedIn", "abhishek-chauhan-880496394"),
        ("kv", "X", "@abh1shxkk"),
        ("head", "GitHub Stats"),
        ("kv2", "Repos", f"{u['repositories']['totalCount']}", "Contributed", f"{u['repositoriesContributedTo']['totalCount']}"),
        ("kv2", "Contribs (1y)", f"{cal['totalContributions']:,}", "Stars", f"{stars}"),
        ("kv2", "Followers", f"{u['followers']['totalCount']}", "Since", since.strftime("%b %Y")),
    ]

    x0, y0, lh = 390, 40, 20
    lines = []
    for i, r in enumerate(rows):
        y = y0 + i * lh
        delay = f"animation-delay:{0.15 + i * 0.045:.3f}s"
        kind = r[0]
        if kind == "gap":
            continue
        if kind == "title":
            body = f'<tspan class="a">{escape(r[1])}</tspan>'
        elif kind == "rule":
            body = f'<tspan class="m">{"─" * W}</tspan>'
        elif kind == "head":
            label = f"─ {r[1]} "
            body = f'<tspan class="m">{escape(label + "─" * (W - len(label)))}</tspan>'
        elif kind == "kv":
            k, v = r[1], r[2]
            dots = "." * max(2, W - len(k) - len(v) - 4)
            body = (f'<tspan class="m">. </tspan><tspan class="k">{escape(k)}</tspan><tspan class="m">:</tspan><tspan class="d">{dots}</tspan><tspan> </tspan>'
                    f'<tspan class="v">{escape(v)}</tspan>')
        else:  # two pairs on one line, split by a bar
            k1, v1, k2, v2 = r[1:]
            half = 27
            d1 = "." * max(2, half - len(k1) - len(v1) - 4)
            d2 = "." * max(2, W - half - len(k2) - len(v2) - 5)
            body = (f'<tspan class="m">. </tspan><tspan class="k">{escape(k1)}</tspan><tspan class="m">:</tspan><tspan class="d">{d1}</tspan><tspan> </tspan>'
                    f'<tspan class="v">{escape(v1)}</tspan><tspan class="m"> | </tspan>'
                    f'<tspan class="k">{escape(k2)}</tspan><tspan class="m">:</tspan><tspan class="d">{d2}</tspan><tspan> </tspan><tspan class="v">{escape(v2)}</tspan>')
        lines.append(f'<text x="{x0}" y="{y}" class="ln" style="{delay}" xml:space="preserve">{body}</text>')

    last_y = y0 + (len(rows) - 1) * lh
    px, lx, ly = 20, 80, 160
    faint, acc = t["faint"], t["acc"]
    order = [(r, c) for r, row in enumerate(LOGO) for c, ch in enumerate(row) if ch == "#"]
    logo = "".join(
        f'<rect x="{lx + c * px + 3}" y="{ly + r * px + 3}" width="{px - 2}" height="{px - 2}" fill="{faint}"/>'
        for r, c in order)
    logo += "".join(
        f'<rect x="{lx + c * px}" y="{ly + r * px}" width="{px - 2}" height="{px - 2}" class="px" '
        f'style="animation-delay:{0.3 + ((r * 7 + c * 13) % 23) * 0.03:.2f}s" fill="{acc}"/>'
        for r, c in order)
    h = last_y + 40
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="985" height="{h}" viewBox="0 0 985 {h}" font-family="{MONO}" font-size="15" role="img" aria-label="abhishek@meerut: Junior PHP Developer at Subharti University, Laravel, Vue, Angular, React">
<style>
.k{{fill:{t['fg']}}} .d{{fill:{t['faint']}}} .v{{fill:{t['fg']}}} .m{{fill:{t['mute']}}} .a{{fill:{t['acc']};font-weight:700}}
.px{{opacity:0;animation:fade .25s ease-out forwards}}
@keyframes fade{{to{{opacity:1}}}}
.ln{{opacity:0;animation:on .01s steps(1) forwards}}
@keyframes on{{to{{opacity:1}}}}
.cur{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.ln,.px{{animation:none;opacity:1}}.cur{{animation:none}}}}
</style>
<rect width="985" height="{h}" rx="12" fill="{t['bg']}" stroke="{t['faint']}"/>
{logo}
<text x="80" y="330" class="m" font-size="13" xml:space="preserve">building useful things, daily</text>
{''.join(lines)}
<rect class="cur" x="{x0}" y="{last_y + 8}" width="9" height="16" fill="{t['acc']}"/>
</svg>"""


# ---------------------------------------------------------------------------- grid

DOT = {"NONE": (1.5, 1), "FIRST_QUARTILE": (2.6, .55), "SECOND_QUARTILE": (3.6, .7), "THIRD_QUARTILE": (4.6, .85), "FOURTH_QUARTILE": (5.6, 1)}


def grid(t: dict, u: dict) -> str:
    cal = u["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    cw, ch, gx, gy = 16, 16, 44, 46
    cells, months, last_month = [], [], None
    for wi, wk in enumerate(weeks):
        for d in wk["contributionDays"]:
            dt = date.fromisoformat(d["date"])
            row = (dt.weekday() + 1) % 7  # Sunday first, like GitHub
            r_, op = DOT[d["contributionLevel"]]
            fill = t["faint"] if d["contributionLevel"] == "NONE" else t["fg"]
            cells.append(f'<circle cx="{gx + wi * cw + 4}" cy="{gy + row * ch - 5}" r="{r_}" fill="{fill}" opacity="{op}"/>')
            if row == 0 or wi == 0:
                if dt.month != last_month and dt.day <= 7:
                    months.append(f'<text x="{gx + wi * cw}" y="{gy - 20}" class="lbl">{dt.strftime("%b").lower()}</text>')
                last_month = dt.month if dt.day <= 7 else last_month

    # The snake walks the grid column by column, down then up, like a plough.
    pts = []
    for wi in range(len(weeks)):
        rows = range(7) if wi % 2 == 0 else range(6, -1, -1)
        for r in rows:
            pts.append((gx + wi * cw + 4, gy + r * ch - 5))
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    dur = len(pts) * 0.07
    seg = 0.07
    snake = []
    for i in range(6):
        op = 1 - i * 0.15
        snake.append(f'<circle r="{5.6 - i * 0.5:.1f}" fill="{t["acc"]}" opacity="{op:.2f}">'
                     f'<animateMotion dur="{dur:.1f}s" repeatCount="indefinite" begin="-{(i * seg) + 0.001:.3f}s" '
                     f'calcMode="linear" path="{path}"/></circle>')
    snake.reverse()

    width = gx + len(weeks) * cw + 20
    days = "".join(f'<text x="8" y="{gy + r * ch}" class="lbl">{n}</text>' for r, n in ((1, "mon"), (3, "wed"), (5, "fri")))
    legend_y = gy + 7 * ch + 16
    total = f"{cal['totalContributions']:,} contributions in the last year"
    legend = "".join(
        f'<circle cx="{width - 124 + i * 16}" cy="{legend_y - 4}" r="{r_}" fill="{t["faint"] if i == 0 else t["fg"]}" opacity="{op}"/>'
        for i, (r_, op) in enumerate(DOT.values()))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{legend_y + 14}" viewBox="0 0 {width} {legend_y + 14}" font-family="{MONO}" role="img" aria-label="{total}">
<style>
.g{{fill:{t['fg']};font-size:15px}} .z{{fill:{t['faint']};font-size:15px}} .lbl{{fill:{t['mute']};font-size:11px}}
@media (prefers-reduced-motion:reduce){{.snake{{display:none}}}}
</style>
<rect width="{width}" height="{legend_y + 14}" rx="12" fill="{t['bg']}" stroke="{t['faint']}"/>
{''.join(months)}{days}
{''.join(cells)}
<g class="snake">{''.join(snake)}</g>
<text x="{gx}" y="{legend_y}" class="lbl">{escape(total)}</text>
<text x="{width - 140}" y="{legend_y}" class="lbl" text-anchor="end">less</text>{legend}<text x="{width - 20}" y="{legend_y}" class="lbl" text-anchor="end">more</text>
</svg>"""


def main() -> None:
    u = fetch()
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"card-{name}.svg").write_text(card(t, u), encoding="utf-8")
        (OUT / f"grid-{name}.svg").write_text(grid(t, u), encoding="utf-8")
    print("built", sorted(p.name for p in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
