"""Generate the animated SVG assets for the GitHub profile README (dark + light)."""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Ubuntu, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, 'SF Mono', Menlo, monospace"

THEMES = {
    "dark": dict(bg1="#0d1117", bg2="#111826", panel="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8b949e", dot="#21262d", a1="#7c5cff", a2="#22d3ee", a3="#34d399",
                 kw="#ff7b72", st="#a5d6ff", fn="#d2a8ff", chip="#1f2630", chipt="#c9d1d9"),
    "light": dict(bg1="#ffffff", bg2="#f4f6fb", panel="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", dot="#e3e8ef", a1="#6d4aff", a2="#0891b2", a3="#059669",
                  kw="#cf222e", st="#0a3069", fn="#8250df", chip="#eef1f5", chipt="#24292f"),
}

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def header(t: dict) -> str:
    roles = [
        "Laravel &amp; PHP backend developer",
        "building dashboards, APIs &amp; AI tools",
        "React · FastAPI · Docker in production",
    ]
    # Each role types in, holds, then fades; the three share one 12s loop.
    role_svg = []
    for i, r in enumerate(roles):
        role_svg.append(f"""
    <g class="role r{i}">
      <clipPath id="c{i}"><rect class="typer t{i}" x="64" y="186" width="0" height="34"/></clipPath>
      <text x="64" y="211" class="mono role-text" clip-path="url(#c{i})"><tspan fill="{t['a3']}">❯</tspan> {r}</text>
    </g>""")
    code = [
        [("const ", "kw"), ("dev", "fn"), (" = {", "tx")],
        [("  name: ", "tx"), ("'Abhishek Chauhan'", "st"), (",", "tx")],
        [("  stack: [", "tx"), ("'Laravel'", "st"), (", ", "tx"), ("'React'", "st"), ("],", "tx")],
        [("  ships: ", "tx"), ("'to production'", "st"), (",", "tx")],
        [("  based: ", "tx"), ("'Meerut, IN'", "st")],
        [("};", "tx")],
    ]
    code_svg = []
    for n, line in enumerate(code):
        spans = "".join(f'<tspan class="{c}">{escape(s)}</tspan>' for s, c in line)
        code_svg.append(
            f'<text x="800" y="{128 + n * 24}" class="mono code ln" xml:space="preserve" style="animation-delay:{0.6 + n * 0.25:.2f}s">'
            f'<tspan class="lnum">{n + 1}</tspan>  {spans}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="Hi, I'm Abhishek Chauhan — Laravel and backend developer">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/>
    </linearGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
      <stop offset="0" stop-color="{t['a1']}"/><stop offset="0.5" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a1']}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="{t['dot']}"/>
      <animateTransform attributeName="patternTransform" type="translate" values="0 0;24 24" dur="8s" repeatCount="indefinite"/>
    </pattern>
    <radialGradient id="orbA"><stop offset="0" stop-color="{t['a1']}" stop-opacity=".35"/><stop offset="1" stop-color="{t['a1']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="orbB"><stop offset="0" stop-color="{t['a2']}" stop-opacity=".28"/><stop offset="1" stop-color="{t['a2']}" stop-opacity="0"/></radialGradient>
    <clipPath id="frame"><rect width="1200" height="300" rx="20"/></clipPath>
  </defs>
  <style>
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .hello{{font-size:22px;fill:{t['muted']};font-weight:500}}
    .big{{font-size:52px;font-weight:800;letter-spacing:-1.5px}}
    .role-text{{font-size:21px;fill:{t['text']}}}
    .pill{{font-size:14px;fill:{t['text']};font-weight:600}}
    .code{{font-size:15px}} .kw{{fill:{t['kw']}}} .st{{fill:{t['st']}}} .fn{{fill:{t['fn']}}} .tx{{fill:{t['text']}}} .lnum{{fill:{t['muted']};opacity:.6}}
    .rise{{opacity:0;animation:rise .8s cubic-bezier(.2,.8,.2,1) forwards}}
    .d1{{animation-delay:.1s}} .d2{{animation-delay:.3s}} .d3{{animation-delay:.5s}} .d4{{animation-delay:.4s}}
    @keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
    .wave{{transform-box:fill-box;transform-origin:70% 80%;animation:wave 2.6s ease-in-out 1s infinite}}
    @keyframes wave{{0%,60%,100%{{transform:rotate(0)}}10%,30%{{transform:rotate(16deg)}}20%,40%{{transform:rotate(-8deg)}}50%{{transform:rotate(10deg)}}}}
    .role{{opacity:0;animation:roleFade 12s infinite}}
    .r1{{animation-delay:4s}} .r2{{animation-delay:8s}}
    @keyframes roleFade{{0%{{opacity:1}}30%{{opacity:1}}33.3%{{opacity:0}}100%{{opacity:0}}}}
    .typer{{animation:type 12s steps(42,end) infinite}}
    .t1{{animation-delay:4s}} .t2{{animation-delay:8s}}
    @keyframes type{{0%{{width:0}}12%{{width:560px}}100%{{width:560px}}}}
    .caret{{animation:blink 1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
    @keyframes pulse{{0%{{transform:scale(1);opacity:.7}}100%{{transform:scale(3.2);opacity:0}}}}
    .floatA{{animation:floatA 14s ease-in-out infinite}} .floatB{{animation:floatB 18s ease-in-out infinite}}
    @keyframes floatA{{50%{{transform:translate(60px,30px)}}}} @keyframes floatB{{50%{{transform:translate(-70px,-20px)}}}}
    .ln{{opacity:0;animation:rise .5s ease-out forwards}}
    .win{{opacity:0;animation:rise .9s cubic-bezier(.2,.8,.2,1) .3s forwards}}
    {REDUCED}
  </style>
  <g clip-path="url(#frame)">
    <rect width="1200" height="300" fill="url(#bg)"/>
    <rect width="1200" height="300" fill="url(#dots)"/>
    <circle class="floatA" cx="180" cy="40" r="260" fill="url(#orbA)"/>
    <circle class="floatB" cx="1050" cy="280" r="280" fill="url(#orbB)"/>
  </g>
  <rect x=".5" y=".5" width="1199" height="299" rx="20" fill="none" stroke="{t['border']}"/>

  <g class="rise d1">
    <rect x="64" y="40" width="262" height="32" rx="16" fill="{t['panel']}" stroke="{t['border']}"/>
    <circle class="pulse" cx="84" cy="56" r="5" fill="{t['a3']}"/>
    <circle cx="84" cy="56" r="5" fill="{t['a3']}"/>
    <text x="98" y="61" class="sans pill">Open to interesting projects</text>
  </g>
  <text x="64" y="112" class="sans hello rise d2">Hi there, I'm</text>
  <g class="rise d3">
    <text x="62" y="166" class="sans big" fill="url(#name)">Abhishek Chauhan</text>
    <text x="530" y="160" font-size="42" class="wave">👋</text>
  </g>
  {''.join(role_svg)}
  <rect class="caret" x="64" y="236" width="0" height="0"/>
  <text x="64" y="262" class="sans rise d4" font-size="15" fill="{t['muted']}">Full-stack web developer · Global Matrix Solution · Meerut, India</text>

  <g class="win">
    <rect x="772" y="60" width="368" height="200" rx="14" fill="{t['panel']}" stroke="{t['border']}"/>
    <circle cx="796" cy="82" r="5.5" fill="#ff5f57"/><circle cx="814" cy="82" r="5.5" fill="#febc2e"/><circle cx="832" cy="82" r="5.5" fill="#28c840"/>
    <text x="1120" y="87" text-anchor="end" class="mono" font-size="12" fill="{t['muted']}">dev.ts</text>
    <line x1="772" y1="100" x2="1140" y2="100" stroke="{t['border']}"/>
    {''.join(code_svg)}
    <rect class="caret" x="836" y="236" width="9" height="18" fill="{t['a2']}" style="opacity:1"/>
  </g>
</svg>"""


def divider(t: dict) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="24" viewBox="0 0 1200 24" aria-hidden="true">
  <defs>
    <linearGradient id="g" x1="0" x2="1">
      <stop offset="0" stop-color="{t['a1']}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{t['a2']}"/>
      <stop offset="1" stop-color="{t['a1']}" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <style>{REDUCED}</style>
  <rect x="0" y="11" width="1200" height="1.5" fill="{t['border']}"/>
  <rect x="0" y="10.5" width="1200" height="2.5" rx="1" fill="url(#g)"/>
  <circle cx="600" cy="12" r="4" fill="{t['a2']}">
    <animate attributeName="r" values="3;5;3" dur="2.5s" repeatCount="indefinite"/>
  </circle>
</svg>"""


def wrap(text: str, width: int) -> list[str]:
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur]


def card(t: dict, title: str, kind: str, desc: str, chips: list[str], status: str, accent: str) -> str:
    desc_svg = "".join(
        f'<text x="32" y="{104 + i * 24}" class="sans desc">{escape(l)}</text>' for i, l in enumerate(wrap(desc, 60)))
    x, chip_svg = 32, []
    for c in chips:
        w = 16 + len(c) * 8
        chip_svg.append(f'<rect x="{x}" y="186" width="{w}" height="26" rx="13" fill="{t["chip"]}" stroke="{t["border"]}"/>'
                        f'<text x="{x + w / 2}" y="203.5" text-anchor="middle" class="mono chip">{escape(c)}</text>')
        x += w + 8
    live = status.lower().startswith("live")
    dot = t["a3"] if live else t["muted"]
    sw = 34 + round(len(status) * 8.4)
    arrow = (f'<g class="arrow"><path d="M512 34 l12 0 l0 12 M524 34 l-14 14" fill="none" stroke="{t["muted"]}" '
             'stroke-width="2" stroke-linecap="round"/></g>') if live else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="560" height="240" viewBox="0 0 560 240" role="img" aria-label="{escape(title)}: {escape(desc)}">
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{t['a2']}"/>
    </linearGradient>
    <radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  </defs>
  <style>
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .title{{font-size:24px;font-weight:700;fill:{t['text']};letter-spacing:-.3px}}
    .kind{{font-size:12px;font-weight:600;fill:{accent};letter-spacing:1.6px}}
    .desc{{font-size:15.5px;fill:{t['muted']}}}
    .chip{{font-size:12px;fill:{t['chipt']}}}
    .stat{{font-size:11.5px;font-weight:700;letter-spacing:1px;fill:{t['text']}}}
    .in{{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) forwards}}
    .i2{{animation-delay:.15s}} .i3{{animation-delay:.3s}} .i4{{animation-delay:.45s}}
    @keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
    .trace{{stroke-dasharray:1580;stroke-dashoffset:1580;animation:trace 2.2s cubic-bezier(.6,0,.2,1) .1s forwards}}
    @keyframes trace{{to{{stroke-dashoffset:0}}}}
    .arrow{{animation:nudge 2.4s ease-in-out infinite}}
    @keyframes nudge{{0%,70%,100%{{transform:none}}80%{{transform:translate(3px,-3px)}}}}
    .pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
    @keyframes pulse{{0%{{transform:scale(1);opacity:.7}}100%{{transform:scale(3);opacity:0}}}}
    .breathe{{animation:breathe 6s ease-in-out infinite}}
    @keyframes breathe{{50%{{opacity:.55}}}}
    {REDUCED}
  </style>
  <rect x="1" y="1" width="558" height="238" rx="18" fill="{t['panel']}" stroke="{t['border']}"/>
  <rect class="breathe" x="1" y="1" width="558" height="238" rx="18" fill="url(#glow)"/>
  <rect class="trace" x="1" y="1" width="558" height="238" rx="18" fill="none" stroke="url(#edge)" stroke-width="1.6"/>
  <text x="32" y="44" class="sans kind in">{escape(kind.upper())}</text>
  <text x="32" y="76" class="sans title in i2">{escape(title)}</text>
  <g class="in i2">
    <rect x="{528 - sw - 36}" y="28" width="{sw}" height="24" rx="12" fill="{t['chip']}" stroke="{t['border']}"/>
    {'<circle class="pulse" cx="' + str(528 - sw - 24) + '" cy="40" r="4" fill="' + dot + '"/>' if live else ''}
    <circle cx="{528 - sw - 24}" cy="40" r="4" fill="{dot}"/>
    <text x="{528 - sw - 14}" y="44.5" class="mono stat">{escape(status.upper())}</text>
  </g>
  {arrow}
  <g class="in i3">{desc_svg}</g>
  <g class="in i4">{''.join(chip_svg)}</g>
</svg>"""


PROJECTS = [
    ("opd-scan", "OPD Scan QC", "Healthcare · Computer vision",
     "Quality control for scanned hospital records: OpenCV page checks, AI handwriting & diagnosis transcription, human review.",
     ["FastAPI", "React", "OpenCV", "Expo"], "live", "#7c5cff"),
    ("opd-scribe", "OPD Scribe", "Healthcare · Speech AI",
     "AI scribe that turns doctor–patient consultations in Indian languages into transcripts, summaries and SOAP notes.",
     ["Node.js", "Speech-to-text", "LLMs"], "in production", "#f472b6"),
    ("ilms", "ILMS", "Legal tech · Workflow",
     "Institutional legal management: matters, notices, litigation, contracts and RTI, with live AI co-drafting.",
     ["TypeScript", "React", "AI assist"], "in production", "#f59e0b"),
    ("medi", "Medi BillSuite", "ERP · Pharma distribution",
     "Pharma distribution ERP with GST invoicing, batch & expiry tracking, sales hierarchy and 50+ reports.",
     ["Laravel", "MySQL", "Tailwind"], "live", "#22c55e"),
]

for name, t in THEMES.items():
    (out / f"header-{name}.svg").write_text(header(t), encoding="utf-8")
    (out / f"divider-{name}.svg").write_text(divider(t), encoding="utf-8")
    for slug, title, kind, desc, chips, status, accent in PROJECTS:
        (out / f"card-{slug}-{name}.svg").write_text(card(t, title, kind, desc, chips, status, accent), encoding="utf-8")
print(sorted(p.name for p in out.iterdir()))
