#!/usr/bin/env python3
"""Build the public automotive security wiki as a static site.

Reads Markdown pages under wiki/, renders them with the retro-futurist
"field manual" design (web/site.css, web/site.js) and writes plain HTML
to the output directory (default: _site/). All links are relative, so
the output works from a GitHub Pages project path or any static host.

Usage: python3 scripts/build_site.py [--out _site]
Requires: PyYAML
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import posixpath
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
WEB = ROOT / "web"
REPO_URL = "https://github.com/hexsecs/automotive-security-wiki"

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500;600&display=swap\">"
)

MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def fmt_date(d: dt.date, long: bool = False) -> str:
    if long:
        return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    return f"{d.day:02d} {MONTHS[d.month - 1]}"


def to_date(v) -> dt.date | None:
    if isinstance(v, dt.date):
        return v
    if isinstance(v, str):
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})", v)
        if m:
            return dt.date(int(m[1]), int(m[2]), int(m[3]))
    return None


# --------------------------------------------------------------------------
# Page model
# --------------------------------------------------------------------------
@dataclass
class Page:
    src: Path
    rel: str  # path relative to wiki/, without .md, posix
    meta: dict
    body: str
    title: str = ""
    kind: str = ""
    date: dt.date | None = None
    url: str = ""  # output path relative to site root
    data: dict = field(default_factory=dict)

    @property
    def stem(self) -> str:
        return posixpath.basename(self.rel)


def parse_page(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            meta = yaml.safe_load(text[3:end]) or {}
            body = text[end + 4 :].lstrip("\n")
    rel = path.relative_to(WIKI).with_suffix("").as_posix()
    p = Page(src=path, rel=rel, meta=meta, body=body)
    p.kind = meta.get("type", "page")
    m = re.search(r"^# (.+)$", body, re.M)
    p.title = str(meta.get("title") or (m[1] if m else p.stem))
    p.date = to_date(meta.get("published")) or to_date(meta.get("created")) or to_date(p.stem)
    p.url = rel + ".html"
    if rel.endswith("/index") or rel == "index":
        p.url = rel + ".html"
    return p


class Site:
    def __init__(self):
        self.pages: dict[str, Page] = {}
        for path in sorted(WIKI.rglob("*.md")):
            p = parse_page(path)
            self.pages[p.rel] = p
        self.slugs: dict[str, Page] = {}
        for p in self.pages.values():
            if p.kind in ("concept", "entity", "source-record"):
                self.slugs[p.stem] = p
                short = re.sub(r"-\d{4}-\d{2}-\d{2}$", "", p.stem)
                self.slugs.setdefault(short, p)
        # Aliases: names that link inline to a note, organization or source record.
        self.alias_map: dict[str, Page] = {}
        for p in self.pages.values():
            if p.kind in ("concept", "entity", "source-record"):
                for a in p.meta.get("aliases") or []:
                    self.alias_map[esc(str(a))] = p
        names = sorted(self.alias_map, key=len, reverse=True)
        self.alias_re = (
            re.compile(r"(?<![\w-])(" + "|".join(re.escape(n) for n in names) + r")(?![\w-])")
            if names else None
        )
        self.briefings = sorted(
            (p for p in self.pages.values() if p.kind == "briefing"),
            key=lambda p: p.date,
            reverse=True,
        )
        self.concepts = sorted(
            (p for p in self.pages.values() if p.kind == "concept"), key=lambda p: p.title
        )
        self.entities = sorted(
            (p for p in self.pages.values() if p.kind == "entity"), key=lambda p: p.title
        )
        self.sources = sorted(
            (p for p in self.pages.values() if p.kind == "source-record"),
            key=lambda p: (p.date or dt.date.min),
            reverse=True,
        )
        for b in self.briefings:
            b.data.update(analyse_briefing(b))

    def resolve(self, target: str) -> Page | None:
        target = target.strip().removesuffix(".md")
        if target in self.pages:
            return self.pages[target]
        if target.startswith("wiki/") and target[5:] in self.pages:
            return self.pages[target[5:]]
        stem = posixpath.basename(target)
        return self.slugs.get(stem)


# --------------------------------------------------------------------------
# Briefing analysis
# --------------------------------------------------------------------------
FAMILY_CLASS = [
    ("vendor", "fam-advisory"),
    ("archive-controlled follow-up / vendor", "fam-advisory"),
    ("academic", "fam-research"),
    ("archive-controlled follow-up / academic", "fam-research"),
    ("threat", "fam-intel"),
    ("researcher", "fam-intel"),
    ("regulation", "fam-standards"),
    ("industry", "fam-standards"),
    ("patents", "fam-standards"),
    ("evidence", "fam-method"),
]


def family_class(heading: str) -> str:
    h = heading.lower()
    for key, cls in FAMILY_CLASS:
        if h.startswith(key):
            return cls
    return "fam-other"


def confidence_level(text: str) -> tuple[int, str]:
    t = (text or "").strip().lower()
    if t.startswith("high"):
        return 5, "High"
    if t.startswith("medium-high") or t.startswith("medium–high"):
        return 4, "Medium-high"
    if t.startswith("medium"):
        return 3, "Medium"
    if t.startswith("low-medium") or t.startswith("low–medium"):
        return 2, "Low-medium"
    if t.startswith("low"):
        return 1, "Low"
    return 0, "Unrated"


def strip_md(s: str) -> str:
    s = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"\^\[[^\]]+\]", "", s)
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def clip(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0].rstrip(",;:—-")
    return cut + "…"


def analyse_briefing(p: Page) -> dict:
    body = p.body
    headlines = re.findall(r"^- \*\*Headline:\*\*\s*(.+)$", body, re.M)
    sections = [
        h for h in re.findall(r"^## (.+)$", body, re.M)
        if h.strip().lower() not in {"bottom line", "sources", "source", "related pages", "question",
                                     "short answer", "evidence", "decision note", "assessment"}
    ]
    m = re.search(r"^\*\*Assessment:\*\*\s*(.+)$", body, re.M)
    assessment = m[1] if m else ""
    if not assessment:
        m = re.search(r"^## (?:Short answer|Assessment)\n+(.+?)(?:\n\n|\n##)", body, re.S | re.M)
        assessment = m[1] if m else ""
    if not assessment:
        m = re.search(r"^(?!#|\*\*|-|\s*$)(.+)$", body, re.M)
        assessment = m[1] if m else ""
    m = re.search(r"^## Bottom line\n+(.+?)(?:\n\n|\Z)", body, re.S | re.M)
    bottom = strip_md(m[1]) if m else ""
    bl_lead = ""
    m2 = re.match(r"\*\*(.+?)\*\*", m[1]) if m else None
    if m2:
        bl_lead = m2[1].rstrip(":")
    lead = headlines[0] if headlines else ""
    if not lead:
        lead = bl_lead or clip(strip_md(assessment), 90)
    level, label = confidence_level(str(p.meta.get("confidence", "")))
    families = []
    for s in sections:
        fam = s.split("/")[0].strip()
        if fam.lower().startswith("archive-controlled"):
            fam = "Follow-up"
        if fam not in families:
            families.append(fam)
    quiet = bool(re.search(r"\bno (?:new|fresh)\b", strip_md(assessment)[:160], re.I))
    return {
        "headlines": [strip_md(h) for h in headlines],
        "lead": strip_md(lead),
        "assessment": strip_md(assessment),
        "bottom": bottom,
        "bottom_lead": bl_lead,
        "sections": sections,
        "families": families,
        "conf_level": level,
        "conf_label": label,
        "quiet": quiet,
    }


# --------------------------------------------------------------------------
# Markdown rendering
# --------------------------------------------------------------------------
class Renderer:
    def __init__(self, site: Site, page: Page):
        self.site = site
        self.page = page
        self.cites: list[Page | str] = []
        self.linked: set[str] = set()  # targets already linked in the current section

    def new_section(self):
        self.linked = set()

    # link helpers ---------------------------------------------------------
    def href(self, target: Page) -> str:
        return relurl(self.page.url, target.url)

    def page_link(self, target: Page, label: str, cls: str = "") -> str:
        c = f' class="{cls}"' if cls else ""
        return f'<a href="{esc(self.href(target))}"{c}>{label}</a>'

    def cite(self, raw: str) -> str:
        out = []
        for part in [x.strip() for x in raw.split(",") if x.strip()]:
            stem = posixpath.basename(part).removesuffix(".md")
            target = self.site.slugs.get(stem) or self.site.slugs.get(
                re.sub(r"-\d{4}-\d{2}-\d{2}$", "", stem)
            )
            key = target or stem
            if key not in self.cites:
                self.cites.append(key)
            n = self.cites.index(key) + 1
            if target:
                out.append(
                    f'<a class="cite" href="{esc(self.href(target))}" title="{esc(target.title)}">S{n}</a>'
                )
            else:
                out.append(f'<span class="cite dead" title="Private capture: {esc(stem)}">S{n}</span>')
        return '<sup class="cites">' + "".join(out) + "</sup>"

    # inline ---------------------------------------------------------------
    def inline(self, text: str, auto: bool = True) -> str:
        stash: list[str] = []

        def keep(s: str) -> str:
            stash.append(s)
            return f"\x00{len(stash) - 1}\x00"

        text = re.sub(r"`([^`]+)`", lambda m: keep(f"<code>{esc(m[1])}</code>"), text)
        text = re.sub(r"\^\[([^\]]+)\]", lambda m: keep(self.cite(m[1])), text)

        def wiki(m):
            target, label = m[1], m[2]
            p = self.site.resolve(target)
            lab = esc(label or (p.title if p and p.kind == "concept" else target.replace("-", " ")))
            if p:
                self.linked.add(p.rel)
                return keep(self.page_link(p, lab, "wl"))
            return keep(f'<span class="wl dead" title="Not in the public edition">{lab}</span>')

        text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", wiki, text)

        def mdlink(m):
            label, url = m[1], m[2]
            if re.match(r"https?://", url):
                return keep(f'<a href="{esc(url)}" class="ext" rel="noopener">{self.inline(label)}</a>')
            p = self.resolve_rel(url)
            if p:
                lab = label
                if lab.strip().lower() in ("raw source", "source"):
                    lab = p.title
                return keep(self.page_link(p, self.inline(lab)))
            return keep(f"<span>{esc(label)}</span>")

        text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", mdlink, text)

        def bare(m):
            url = m[0]
            trail = ""
            while url and url[-1] in ".,;:)":
                trail = url[-1] + trail
                url = url[:-1]
            disp = re.sub(r"^https?://(www\.)?", "", url)
            if len(disp) > 48:
                disp = disp[:46] + "…"
            return keep(f'<a href="{esc(url)}" class="ext" rel="noopener">{esc(disp)}</a>') + trail

        text = re.sub(r"https?://[^\s<>\x00]+", bare, text)

        text = esc(text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", text)

        if auto and self.site.alias_re:
            def alias(m):
                p = self.site.alias_map[m[0]]
                if p is self.page or p.rel in self.linked:
                    return m[0]
                self.linked.add(p.rel)
                return keep(self.page_link(p, m[0], "xl"))

            text = self.site.alias_re.sub(alias, text)

        def slug(m):
            p = self.site.slugs.get(m[0])
            if p and p is not self.page:
                lab = p.title if p.kind == "concept" else m[0]
                self.linked.add(p.rel)
                return keep(self.page_link(p, esc(lab), "wl"))
            return m[0]

        text = re.sub(r"(?<![\w/.-])[a-z0-9]+(?:-[a-z0-9]+)+(?![\w/-])", slug, text)

        while "\x00" in text:
            text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m[1])], text)
        return text

    def resolve_rel(self, url: str) -> Page | None:
        url = url.split("#")[0]
        if not url.endswith(".md"):
            return None
        base = posixpath.dirname(self.page.rel)
        target = posixpath.normpath(posixpath.join(base, url))[:-3]
        return self.site.pages.get(target) or self.site.resolve(target)

    # blocks ---------------------------------------------------------------
    def blocks(self, md: str) -> list[tuple[str, object]]:
        out: list[tuple[str, object]] = []
        para: list[str] = []
        items: list[str] | None = None

        def flush():
            nonlocal para, items
            if para:
                out.append(("p", " ".join(para)))
                para = []
            if items is not None:
                out.append(("ul", items))
                items = None

        for line in md.splitlines():
            if not line.strip():
                flush()
                continue
            m = re.match(r"^(#{1,6})\s+(.+)$", line)
            if m:
                flush()
                out.append((f"h{len(m[1])}", m[2].strip()))
                continue
            if re.match(r"^\s*([-*_])\s*\1\s*\1\s*$", line):
                flush()
                out.append(("hr", None))
                continue
            m = re.match(r"^\s*[-*]\s+(.*)$", line)
            if m:
                if para:
                    out.append(("p", " ".join(para)))
                    para = []
                if items is None:
                    items = []
                items.append(m[1])
                continue
            if items is not None and line.startswith("  "):
                items[-1] += " " + line.strip()
                continue
            if items is not None:
                out.append(("ul", items))
                items = None
            para.append(line.strip())
        flush()
        return out

    def render_blocks(self, blocks, skip_h1=True) -> str:
        h = []
        for kind, val in blocks:
            if kind == "h1" and skip_h1:
                continue
            if kind.startswith("h"):
                lvl = int(kind[1])
                if lvl <= 2:
                    self.new_section()
                h.append(f"<h{lvl}>{self.inline(val, auto=False)}</h{lvl}>")
            elif kind == "p":
                h.append(f"<p>{self.inline(val)}</p>")
            elif kind == "ul":
                h.append("<ul>" + "".join(f"<li>{self.inline(i)}</li>" for i in val) + "</ul>")
            elif kind == "hr":
                h.append("<hr>")
        return "\n".join(h)

    def render(self, md: str) -> str:
        return self.render_blocks(self.blocks(md))

    def citations_html(self) -> str:
        if not self.cites:
            return ""
        rows = []
        for i, c in enumerate(self.cites, 1):
            if isinstance(c, Page):
                rows.append(
                    f'<li><span class="cn">S{i}</span>{self.page_link(c, esc(c.title))}</li>'
                )
            else:
                rows.append(
                    f'<li><span class="cn">S{i}</span><span class="muted">{esc(c)} '
                    "(private capture)</span></li>"
                )
        return '<ol class="citelist">' + "".join(rows) + "</ol>"


def relurl(from_url: str, to_url: str) -> str:
    base = posixpath.dirname(from_url) or "."
    return posixpath.relpath(to_url, base)


# --------------------------------------------------------------------------
# Components
# --------------------------------------------------------------------------
def meter(level: int, label: str, compact: bool = False) -> str:
    cells = "".join(f'<i class="{"on" if n <= level else ""}"></i>' for n in range(1, 6))
    cls = "meter compact" if compact else "meter"
    return (
        f'<span class="{cls}" role="img" aria-label="Confidence: {esc(label)}">'
        f'<span class="cells">{cells}</span><span class="mlabel">{esc(label)}</span></span>'
    )


def grille_mark(size: int = 40) -> str:
    dots = []
    for r in range(5):
        for c in range(5):
            cls = "hot" if (r, c) == (1, 3) else ""
            dots.append(f'<circle cx="{6 + c * 7}" cy="{6 + r * 7}" r="2.2" class="{cls}"/>')
    return (
        f'<svg class="grille" width="{size}" height="{size}" viewBox="0 0 40 40" aria-hidden="true">'
        f'<rect x="0.5" y="0.5" width="39" height="39" rx="7" class="g-frame"/>{"".join(dots)}</svg>'
    )


def plate_svg(site: Site, page: Page) -> tuple[str, str]:
    """Cutaway figure of a vehicle with numbered call-outs, plus its legend."""

    def link(target_rel: str) -> str:
        p = site.resolve(target_rel)
        return relurl(page.url, p.url) if p else "#"

    thermal = next((s for s in site.sources if "thermal" in s.stem), None)
    callouts = [
        (1, 300, 118, "GNSS receiver", "Position spoofing on V2X and fleet tracking",
         link("concepts/gnss-spoofing")),
        (2, 232, 150, "Telematics unit", "Cloud APIs, OTA, and the SDV perimeter",
         link("concepts/connected-vehicle-identity")),
        (3, 400, 176, "Infotainment", "Android Automotive platform advisories",
         link("concepts/android-automotive-os-security")),
        (4, 470, 236, "CAN backbone", "In-vehicle network and gateway policy",
         link("concepts/automotive-can")),
        (5, 262, 236, "Masquerading ECU", "Frame substitution that keeps timing intact",
         link("concepts/can-masquerade-attacks")),
        (6, 62, 168, "Charge port & EVSE", "OCPP backends and charger firmware",
         link("concepts/ev-charging-security")),
        (7, 604, 220, "Perception sensors", "Thermal and sensor-side attacks on ADAS",
         relurl(page.url, thermal.url) if thermal else "#"),
    ]
    num = []
    for n, x, y, label, _, href in callouts:
        num.append(
            f'<a href="{esc(href)}" class="callout" aria-label="{n}. {esc(label)}">'
            f'<circle cx="{x}" cy="{y}" r="11"/><text x="{x}" y="{y + 4}">{n}</text></a>'
        )
    svg = f"""
<svg class="plate-svg" viewBox="0 0 660 360" role="img" aria-labelledby="plate-t">
  <title id="plate-t">Cutaway drawing of a car showing seven numbered points where attacks enter the vehicle</title>
  <defs>
    <pattern id="halftone" width="5" height="5" patternUnits="userSpaceOnUse">
      <circle cx="2.5" cy="2.5" r="1.05" class="ht"/>
    </pattern>
    <clipPath id="bodyclip"><path d="M80,280 L76,240 Q78,222 100,216 L190,200 Q220,162 280,156 L340,154 Q370,156 412,196 L520,206 Q560,212 570,230 L574,274 Q574,280 566,280 L516,280 A46,46 0 0 0 424,280 L216,280 A46,46 0 0 0 124,280 Z"/></clipPath>
  </defs>
  <g class="grid">
    {''.join(f'<line x1="{x}" y1="20" x2="{x}" y2="330"/>' for x in range(40, 660, 40))}
    {''.join(f'<line x1="20" y1="{y}" x2="640" y2="{y}"/>' for y in range(40, 340, 40))}
  </g>
  <!-- sky signals -->
  <g class="sat"><rect x="560" y="34" width="22" height="12"/><line x1="548" y1="40" x2="594" y2="40"/></g>
  <path class="sig" d="M566,48 L304,148"/>
  <path class="sig spoof" d="M70,40 Q180,70 296,148"/>
  <text class="tiny" x="74" y="34">SPOOFED L1 · 1575.42 MHz</text>
  <text class="tiny" x="470" y="28">GNSS SV</text>
  <!-- charger -->
  <g class="evse"><rect x="18" y="196" width="30" height="88" rx="3"/><rect x="24" y="206" width="18" height="12" class="screen"/>
  <path class="cable" d="M46,250 C70,252 76,236 92,236"/></g>
  <text class="tiny" x="14" y="302">EVSE · OCPP 1.6J</text>
  <!-- body -->
  <ellipse class="shadow" cx="326" cy="318" rx="270" ry="10"/>
  <path class="body" d="M80,280 L76,240 Q78,222 100,216 L190,200 Q220,162 280,156 L340,154 Q370,156 412,196 L520,206 Q560,212 570,230 L574,274 Q574,280 566,280 L516,280 A46,46 0 0 0 424,280 L216,280 A46,46 0 0 0 124,280 Z"/>
  <rect clip-path="url(#bodyclip)" x="60" y="236" width="540" height="60" fill="url(#halftone)"/>
  <path class="glass" d="M202,198 Q228,168 278,164 L318,163 L318,196 Z"/>
  <path class="glass" d="M328,163 L340,163 Q362,166 395,196 L328,196 Z"/>
  <path class="trim" d="M100,222 L566,230"/>
  <path class="trim" d="M323,200 L323,276"/>
  <path class="fin" d="M292,155 L300,143 L312,155 Z"/>
  <!-- cutaway network -->
  <path class="bus" d="M112,252 L548,256"/>
  <path class="bus thin" d="M240,252 L240,196 M400,254 L400,204 M300,253 L300,160"/>
  {''.join(f'<rect class="ecu" x="{x - 6}" y="{y - 6}" width="12" height="12"/>' for x, y in [(150,252),(240,252),(330,253),(400,254),(470,255),(530,256)])}
  <rect class="ecu" x="226" y="186" width="28" height="14"/>
  <rect class="ecu" x="386" y="196" width="26" height="10"/>
  <g class="rogue"><circle cx="300" cy="253" r="16"/><circle cx="300" cy="253" r="26"/><rect x="294" y="247" width="12" height="12"/></g>
  <circle class="port" cx="96" cy="236" r="6"/>
  <path class="radar" d="M574,246 L650,214 L650,280 Z"/>
  <!-- wheels -->
  {''.join(f'<g class="wheel"><circle cx="{cx}" cy="282" r="34"/><circle cx="{cx}" cy="282" r="13" class="hub"/></g>' for cx in (170, 470))}
  <line class="ground" x1="20" y1="317" x2="640" y2="317"/>
  <!-- dimension line -->
  <g class="dim"><line x1="76" y1="338" x2="574" y2="338"/><line x1="76" y1="332" x2="76" y2="344"/><line x1="574" y1="332" x2="574" y2="344"/>
  <text x="325" y="352">4.62 m · OVERALL LENGTH</text></g>
  {''.join(num)}
</svg>"""
    legend = "".join(
        f'<li><a href="{esc(href)}"><span class="lnum">{n}</span><span><strong>{esc(label)}</strong>'
        f"<small>{esc(desc)}</small></span></a></li>"
        for n, _, _, label, desc, href in callouts
    )
    return svg, legend


def dial_svg(site: Site, page: Page, selected: Page | None = None) -> str:
    """Braun-style tuning scale: one tick per day, a station per briefing."""
    bs = sorted(site.briefings, key=lambda b: b.date)
    start, end = bs[0].date, bs[-1].date
    days = (end - start).days
    x0, x1 = 34, 966
    sx = lambda d: x0 + (d - start).days * (x1 - x0) / max(days, 1)
    ticks, labels, stations = [], [], []
    for i in range(days + 1):
        d = start + dt.timedelta(days=i)
        x = sx(d)
        major = d.weekday() == 0
        ticks.append(f'<line x1="{x:.1f}" y1="{70 if major else 78}" x2="{x:.1f}" y2="92" class="{"maj" if major else ""}"/>')
        if major or (i == 0 and (7 - d.weekday()) % 7 > 3):
            labels.append(f'<text x="{x:.1f}" y="112">{fmt_date(d)}</text>')
    sel = selected or bs[-1]
    for b in bs:
        x = sx(b.date)
        lvl = b.data["conf_level"]
        cls = "st" + (" quiet" if b.data["quiet"] else "") + (" sel" if b is sel else "")
        h = 18 + lvl * 7
        stations.append(
            f'<a href="{esc(relurl(page.url, b.url))}" class="{cls}" data-date="{fmt_date(b.date, True)}"'
            f' data-lead="{esc(b.data["lead"])}" data-conf="{esc(b.data["conf_label"])}">'
            f'<title>{fmt_date(b.date, True)} · {esc(b.data["lead"])}</title>'
            f'<rect x="{x - 7:.1f}" y="12" width="14" height="86" class="hit"/>'
            f'<rect x="{x - 2.5:.1f}" y="{66 - h}" width="5" height="{h}" class="bar"/></a>'
        )
    nx = sx(sel.date)
    return f"""
<svg class="dial-svg" viewBox="0 0 1000 124" role="group" aria-label="Briefings by date; taller marks are higher-confidence issues">
  <rect x="1" y="1" width="998" height="122" rx="10" class="face"/>
  <g class="ticks">{''.join(ticks)}</g>
  <g class="lbl">{''.join(labels)}</g>
  <g class="stations">{''.join(stations)}</g>
  <line x1="{nx:.1f}" y1="8" x2="{nx:.1f}" y2="98" class="needle"/>
  <circle cx="{nx:.1f}" cy="8" r="4" class="needle-cap"/>
</svg>"""


def masthead(page: Page, site: Site, active: str) -> str:
    root = relurl(page.url, "index.html")
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{esc(relurl(page.url, href))}"{cur}>{label}</a>'
    latest = site.briefings[0]
    return f"""
<header class="mast">
  <div class="shell mast-in">
    <a class="brand" href="{esc(root)}">{grille_mark()}<span><span class="eyebrow">Field notes · open archive</span>
    <span class="wordmark">Automotive Security Research</span></span></a>
    <nav class="nav" aria-label="Sections">
      {nav("briefings/automotive/index.html", "Briefings", "briefings")}
      {nav("concepts/index.html", "Notes", "concepts")}
      {nav("sources/index.html", "Sources", "sources")}
      {nav("method.html", "Method", "method")}
      <a href="{REPO_URL}" class="ext" rel="noopener">GitHub</a>
    </nav>
    <div class="mast-meta">
      <span>Vol. 1 · No. {len(site.briefings):02d}</span>
      <span>Updated {fmt_date(latest.date, True)}</span>
      <button class="theme-switch" type="button" id="theme-switch" aria-label="Switch colour theme">
        <span class="sw-track"><span class="sw-knob"></span></span><span class="sw-label">Light</span>
      </button>
    </div>
  </div>
</header>"""


def footer(page: Page) -> str:
    return f"""
<footer class="foot"><div class="shell foot-in">
  <span>{grille_mark(28)}</span>
  <span>Built for readers who check the footnotes.</span>
  <span>Source records are metadata-only. Text licensed CC BY 4.0.</span>
  <a href="{REPO_URL}" class="ext" rel="noopener">hexsecs / automotive-security-wiki</a>
</div></footer>"""


def document(page: Page, site: Site, title: str, body: str, active: str, description: str,
             fragment: bool = False) -> str:
    css = esc(relurl(page.url, "assets/site.css"))
    js = esc(relurl(page.url, "assets/site.js"))
    head = (
        f"<title>{esc(title)}</title>\n"
        '<meta name="claude:viewport-fit-sides" content="cover">\n'
        f'<meta name="description" content="{esc(description)}">\n'
        f"{FONT_LINK}\n"
        f'<link rel="stylesheet" href="{css}">\n'
    )
    inner = (
        f"{masthead(page, site, active)}\n<main id=\"main\">{body}</main>\n{footer(page)}\n"
        f'<script src="{js}"></script>'
    )
    if fragment:
        return head + inner + "\n"
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head
        + "<script>try{var t=localStorage.getItem('asr-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>\n"
        + "</head>\n<body>\n<a class=\"skip\" href=\"#main\">Skip to content</a>\n"
        + inner
        + "\n</body>\n</html>\n"
    )


def briefing_card(site: Site, page: Page, b: Page, cls: str = "") -> str:
    d = b.data
    fams = "".join(f'<span class="chip {family_class(f)}">{esc(f)}</span>' for f in d["families"][:3])
    return f"""
<article class="card {cls}">
  <a href="{esc(relurl(page.url, b.url))}" class="card-link">
    <div class="card-top"><span class="date">{fmt_date(b.date, True)}</span>{meter(d["conf_level"], d["conf_label"], True)}</div>
    <h3>{esc(d["lead"])}</h3>
    <p>{esc(clip(d["assessment"], 190))}</p>
    <div class="chips">{fams}</div>
  </a>
</article>"""


def source_items(site: Site, r: "Renderer", page: Page) -> list[str]:
    """Sidebar list items for a page's frontmatter sources (paths or URLs)."""
    by_url = {str(x.meta.get("source_url", "")).rstrip("/"): x for x in site.sources}
    items = []
    for s in page.meta.get("sources") or []:
        if isinstance(s, dict):
            ref = s.get("path") or s.get("url") or ""
        else:
            ref = str(s)
        p = by_url.get(ref.rstrip("/")) if ref.startswith("http") else site.resolve(ref)
        if p:
            items.append(f'<li>{r.page_link(p, esc(p.title))}<small>{esc(p.meta.get("source_type", ""))} · '
                         f'{esc(p.meta.get("published", ""))} · {esc(p.meta.get("status", ""))}</small></li>')
        elif ref.startswith("http"):
            disp = re.sub(r"^https?://(www\.)?", "", ref)
            items.append(f'<li><a class="ext" href="{esc(ref)}" rel="noopener">{esc(clip(disp, 60))}</a><small>external · no public record</small></li>')
    return items


# --------------------------------------------------------------------------
# Page builders
# --------------------------------------------------------------------------
def build_home(site: Site, fragment=False) -> str:
    page = Page(src=WIKI / "index.md", rel="index", meta={}, body="", url="index.html")
    latest = site.briefings[0]
    svg, legend = plate_svg(site, page)
    lead_story = next((b for b in site.briefings if not b.data["quiet"]), latest)
    grid = [b for b in site.briefings if b is not lead_story][:6]

    signals = []
    for b in site.briefings[:8]:
        for h in b.data["headlines"][:1]:
            signals.append(
                f'<li><a href="{esc(relurl(page.url, b.url))}"><span class="date">{fmt_date(b.date)}</span>'
                f'<span>{esc(clip(h, 120))}</span></a></li>'
            )

    conf_counts = {}
    for b in site.briefings:
        conf_counts[b.data["conf_label"]] = conf_counts.get(b.data["conf_label"], 0) + 1
    total = len(site.briefings)
    conf_bar = "".join(
        f'<span class="seg lv{lvl}" style="flex:{conf_counts.get(lab, 0)}" title="{lab}: {conf_counts.get(lab, 0)}"></span>'
        for lvl, lab in [(5, "High"), (4, "Medium-high"), (3, "Medium")]
        if conf_counts.get(lab)
    )
    conf_key = "".join(
        f'<li><span class="sw lv{lvl}"></span>{lab}<b>{conf_counts.get(lab, 0)}</b></li>'
        for lvl, lab in [(5, "High"), (4, "Medium-high"), (3, "Medium")]
        if conf_counts.get(lab)
    )
    src_types = {}
    for s in site.sources:
        k = s.meta.get("source_type", "other")
        src_types[k] = src_types.get(k, 0) + 1
    captured = sum(1 for s in site.sources if s.meta.get("status") == "captured")

    notes = "".join(
        f"""<a class="note" href="{esc(relurl(page.url, c.url))}">
  <span class="eyebrow">Note {i:02d} · {len(c.meta.get('sources') or [])} sources</span>
  <strong>{esc(c.title)}</strong>
  <span>{esc(clip(strip_md(str(c.meta.get('summary', ''))), 120))}</span></a>"""
        for i, c in enumerate(site.concepts, 1)
    )

    ld = lead_story.data
    body = f"""
<section class="cover">
  <div class="shell cover-in">
    <div class="cover-copy">
      <div class="issue-strip"><span>Issue {len(site.briefings):02d}</span><span>{fmt_date(latest.date, True)}</span><span>{len(site.sources)} source records</span></div>
      <h1 class="display">Security research,<br><em>filed for action.</em></h1>
      <p class="lede">A source-grounded archive of automotive cybersecurity research: vehicle networks, charging infrastructure, software-defined vehicles, and the systems that quietly connect them.</p>
      <div class="actions">
        <a class="btn primary" href="{esc(relurl(page.url, latest.url))}">Read the latest briefing</a>
        <a class="btn" href="briefings/automotive/index.html">Browse the archive</a>
      </div>
    </div>
    <figure class="plate">
      <figcaption class="plate-head"><span>Plate 1</span><span>Attack surface, cutaway</span></figcaption>
      <div class="plate-art">{svg}</div>
      <ol class="plate-legend">{legend}</ol>
    </figure>
  </div>
</section>

<section class="band dial-band">
  <div class="shell">
    <div class="sectionhead"><h2>Briefing receiver</h2><span>{fmt_date(site.briefings[-1].date, True)} – {fmt_date(latest.date, True)} · bar height = evidence confidence</span></div>
    <div class="dial">
      <div class="dial-scroll">{dial_svg(site, page)}</div>
      <div class="readout" aria-live="polite"><span class="r-date">{fmt_date(latest.date, True)}</span><span class="r-lead">{esc(latest.data["lead"])}</span><span class="r-conf">{esc(latest.data["conf_label"])}</span></div>
    </div>
  </div>
</section>

<section class="shell feature">
  <div class="sectionhead"><h2>Cover story</h2><span>Most recent issue with new primary-source signal</span></div>
  <a class="story" href="{esc(relurl(page.url, lead_story.url))}">
    <div class="story-meta">
      <span class="date big">{lead_story.date.day:02d}<small>{MONTHS[lead_story.date.month - 1]} {lead_story.date.year}</small></span>
      {meter(ld["conf_level"], ld["conf_label"])}
      <div class="chips">{''.join(f'<span class="chip {family_class(f)}">{esc(f)}</span>' for f in ld["families"])}</div>
    </div>
    <div class="story-body">
      <h3>{esc(ld["lead"])}</h3>
      <p>{esc(clip(ld["assessment"], 420))}</p>
      {f'<p class="bottomline"><b>Bottom line.</b> {esc(clip(ld["bottom"], 260))}</p>' if ld["bottom"] else ""}
      <span class="more">Read the briefing</span>
    </div>
  </a>
</section>

<section class="shell">
  <div class="sectionhead"><h2>Recent issues</h2><a href="briefings/automotive/index.html">All {total} briefings</a></div>
  <div class="cards">{''.join(briefing_card(site, page, b) for b in grid)}</div>
</section>

<section class="shell lower">
  <div class="panel signals">
    <h2 class="panel-h">Signal board</h2>
    <ol class="signal-list">{''.join(signals)}</ol>
  </div>
  <div class="panel posture">
    <h2 class="panel-h">Evidence posture</h2>
    <p class="eyebrow">Confidence describes evidence strength, not exploit severity</p>
    <div class="stack">{conf_bar}</div>
    <ul class="stack-key">{conf_key}</ul>
    <dl class="readings">
      <div><dt>Briefings</dt><dd>{total}</dd></div>
      <div><dt>Source records</dt><dd>{len(site.sources)}</dd></div>
      <div><dt>Captured privately</dt><dd>{captured}</dd></div>
      <div><dt>Papers / articles</dt><dd>{src_types.get('paper', 0)} / {src_types.get('article', 0)}</dd></div>
    </dl>
    <a class="textlink" href="method.html">How the archive is kept</a>
  </div>
</section>

<section class="shell">
  <div class="sectionhead"><h2>Durable notes</h2><a href="concepts/index.html">Concept index</a></div>
  <div class="notes">{notes}</div>
</section>
"""
    return document(page, site, "Automotive Security Research", body, "home",
                    "Source-grounded automotive cybersecurity briefings, notes and citation records.",
                    fragment)


def build_briefing(site: Site, b: Page) -> str:
    r = Renderer(site, b)
    d = b.data
    idx = site.briefings.index(b)
    newer = site.briefings[idx - 1] if idx > 0 else None
    older = site.briefings[idx + 1] if idx + 1 < len(site.briefings) else None

    blocks = r.blocks(b.body)
    intro, sections, cur = [], [], None
    for kind, val in blocks:
        if kind == "h1":
            continue
        if kind == "h2":
            cur = {"title": val, "blocks": []}
            sections.append(cur)
        elif cur is None:
            intro.append((kind, val))
        else:
            cur["blocks"].append((kind, val))

    intro_html = []
    for kind, val in intro:
        m = re.match(r"^\*\*(Window|Assessment):\*\*\s*(.+)$", val) if kind == "p" else None
        if m and m[1] == "Window":
            continue
        if m:
            intro_html.append(f'<p class="standfirst">{r.inline(m[2])}</p>')
        else:
            intro_html.append(r.render_blocks([(kind, val)]))
    window = re.search(r"^\*\*Window:\*\*\s*(.+)$", b.body, re.M)

    sec_html = []
    fig = 0
    for s in sections:
        r.new_section()
        title = s["title"]
        low = title.lower()
        if low == "bottom line":
            sec_html.append(f'<section class="bottom-box"><h2>Bottom line</h2>{r.render_blocks(s["blocks"])}</section>')
            continue
        items = s["blocks"][0][1] if s["blocks"] and s["blocks"][0][0] == "ul" else None
        is_spec = items and all(re.match(r"^\*\*[^*]+:\*\*", i) for i in items)
        if is_spec:
            fig += 1
            fam, _, topic = title.partition(" / ")
            rows, headline, conf = [], "", ""
            for it in items:
                m = re.match(r"^\*\*([^*]+):\*\*\s*(.*)$", it)
                key, val = m[1], m[2]
                if key == "Headline":
                    headline = val
                    continue
                if key == "Confidence":
                    conf = val
                if key == "Lens":
                    chips = "".join(f'<span class="chip plain">{esc(x.strip())}</span>' for x in re.split(r"[;,]", val) if x.strip())
                    rows.append(f"<div><dt>{esc(key)}</dt><dd><div class=\"chips\">{chips}</div></dd></div>")
                    continue
                wide = key in ("Why it matters", "Decision note", "Confidence")
                rows.append(f'<div class="{"wide" if wide else ""}"><dt>{esc(key)}</dt><dd>{r.inline(val)}</dd></div>')
            lvl, lab = confidence_level(conf)
            rest = r.render_blocks(s["blocks"][1:])
            sec_html.append(f"""
<section class="spec {family_class(title)}">
  <header class="spec-head"><span class="fig">Fig. {fig}</span><span class="fam">{esc(fam)}</span><span class="topic">{esc(topic)}</span>{meter(lvl, lab, True) if lvl else ""}</header>
  {f'<h2 class="spec-title">{r.inline(headline, auto=False)}</h2>' if headline else f'<h2 class="spec-title">{esc(title)}</h2>'}
  <dl class="spec-rows">{''.join(rows)}</dl>
  {rest}
</section>""")
        else:
            sec_html.append(f'<section class="prose-sec"><h2>{r.inline(title, auto=False)}</h2>{r.render_blocks(s["blocks"])}</section>')

    srcs = source_items(site, r, b)
    pager = '<nav class="pager" aria-label="Adjacent issues">'
    pager += (f'<a href="{esc(relurl(b.url, older.url))}" class="prev"><small>Previous issue</small>{fmt_date(older.date, True)}</a>' if older else "<span></span>")
    pager += (f'<a href="{esc(relurl(b.url, newer.url))}" class="next"><small>Next issue</small>{fmt_date(newer.date, True)}</a>' if newer else "<span></span>")
    pager += "</nav>"

    tags = "".join(f'<span class="chip plain">{esc(t)}</span>' for t in b.meta.get("tags") or [])
    body = f"""
<div class="shell crumbs"><a href="{esc(relurl(b.url, 'index.html'))}">Home</a> / <a href="{esc(relurl(b.url, 'briefings/automotive/index.html'))}">Briefings</a> / {b.date.isoformat()}</div>
<header class="shell doc-head">
  <div class="datecol"><span class="date big">{b.date.day:02d}<small>{MONTHS[b.date.month - 1]} {b.date.year}</small></span></div>
  <div class="doc-title">
    <p class="eyebrow">Automotive cybersecurity briefing · Issue {len(site.briefings) - idx:02d}</p>
    <h1>{esc(d["lead"])}</h1>
    <div class="doc-meta">{meter(d["conf_level"], d["conf_label"])}<span>{esc(window[1]) if window else ""}</span></div>
  </div>
</header>
<div class="shell doc-grid">
  <article class="doc prose">
    {''.join(intro_html)}
    {''.join(sec_html)}
    {('<section class="prose-sec"><h2>Citations</h2>' + r.citations_html() + '</section>') if r.cites else ''}
  </article>
  <aside class="side">
    <div class="side-box"><h2>Sources cited</h2><ul class="srclist">{''.join(srcs) or '<li class="muted">None listed</li>'}</ul></div>
    <div class="side-box"><h2>Filed under</h2><div class="chips">{tags}</div></div>
    <div class="side-box"><h2>Record</h2><dl class="kv"><div><dt>Depth</dt><dd>{esc(b.meta.get('depth', '—'))}</dd></div><div><dt>Contested</dt><dd>{'Yes' if b.meta.get('contested') else 'No'}</dd></div><div><dt>Snapshot</dt><dd>Immutable</dd></div></dl>
    <a class="textlink" href="{REPO_URL}/blob/main/wiki/{esc(b.rel)}.md" rel="noopener">View source Markdown</a></div>
  </aside>
</div>
<div class="shell">{pager}</div>
"""
    return document(b, site, f"Briefing {b.date.isoformat()}", body, "briefings",
                    clip(d["assessment"], 155))


def build_briefing_index(site: Site) -> str:
    page = site.pages["briefings/automotive/index"]
    rows = []
    month = None
    for b in site.briefings:
        m = (b.date.year, b.date.month)
        if m != month:
            month = m
            n = sum(1 for x in site.briefings if (x.date.year, x.date.month) == m)
            rows.append(f'<li class="month"><span>{MONTHS[m[1] - 1]} {m[0]}</span><span>{n} issues</span></li>')
        d = b.data
        fams = "".join(f'<span class="chip {family_class(f)}">{esc(f)}</span>' for f in d["families"][:4])
        rows.append(f"""<li class="row" data-conf="{d['conf_level']}" data-quiet="{'1' if d['quiet'] else '0'}">
  <a href="{esc(relurl(page.url, b.url))}">
    <span class="date">{b.date.strftime('%a').upper()} {fmt_date(b.date)}</span>
    <span class="row-main"><strong>{esc(d['lead'])}</strong><small>{esc(clip(d['assessment'], 170))}</small><span class="chips">{fams}</span></span>
    {meter(d['conf_level'], d['conf_label'], True)}
  </a></li>""")
    body = f"""
<div class="shell crumbs"><a href="../../index.html">Home</a> / Briefings</div>
<header class="shell page-head">
  <p class="eyebrow">Dated · immutable · source-grounded</p>
  <h1 class="display sm">Briefing archive</h1>
  <p class="lede">Each issue covers a seven-day window and is kept as written. Confidence labels describe the strength of the evidence, not the severity of a vulnerability.</p>
</header>
<section class="shell">
  <div class="dial"><div class="dial-scroll">{dial_svg(site, page)}</div>
  <div class="readout" aria-live="polite"><span class="r-date">{fmt_date(site.briefings[0].date, True)}</span><span class="r-lead">{esc(site.briefings[0].data['lead'])}</span><span class="r-conf">{esc(site.briefings[0].data['conf_label'])}</span></div></div>
  <div class="controls" role="group" aria-label="Filter briefings">
    <span class="eyebrow">Filter</span>
    <button type="button" class="rocker" id="f-signal" aria-pressed="false"><span class="led"></span>New signal only</button>
    <button type="button" class="rocker" id="f-conf" aria-pressed="false"><span class="led"></span>Medium-high and above</button>
    <span class="count" id="f-count">{len(site.briefings)} shown</span>
  </div>
  <ol class="archive" id="archive">{''.join(rows)}</ol>
</section>"""
    return document(page, site, "Briefing Archive", body, "briefings",
                    "Every dated automotive cybersecurity briefing in the public archive.")


def build_concept(site: Site, c: Page) -> str:
    r = Renderer(site, c)
    content = r.render(c.body)
    srcs = source_items(site, r, c)
    mentions = [b for b in site.briefings if c.stem in b.body or b.rel in c.body]
    ment = "".join(f'<li><a href="{esc(relurl(c.url, b.url))}">{fmt_date(b.date, True)}</a><small>{esc(clip(b.data["lead"], 70))}</small></li>' for b in mentions[:8])
    lvl, lab = confidence_level(str(c.meta.get("confidence", "")))
    body = f"""
<div class="shell crumbs"><a href="{esc(relurl(c.url, 'index.html'))}">Home</a> / <a href="{esc(relurl(c.url, 'concepts/index.html'))}">Notes</a> / {esc(c.title)}</div>
<header class="shell page-head">
  <p class="eyebrow">{'Organization profile' if c.kind == 'entity' else 'Durable research note'} · updated {esc(c.meta.get('updated', ''))}</p>
  <h1 class="display sm">{esc(c.title)}</h1>
  <div class="doc-meta">{meter(lvl, lab)}<span>{len(c.meta.get('sources') or [])} linked sources</span></div>
</header>
<div class="shell doc-grid">
  <article class="doc prose">{content}
  {('<section class="prose-sec"><h2>Citations</h2>' + r.citations_html() + '</section>') if r.cites else ''}</article>
  <aside class="side">
    <div class="side-box"><h2>Source records</h2><ul class="srclist">{''.join(srcs) or '<li class="muted">None</li>'}</ul></div>
    {f'<div class="side-box"><h2>Mentioned in briefings</h2><ul class="srclist">{ment}</ul></div>' if ment else ''}
  </aside>
</div>"""
    return document(c, site, c.title, body, "concepts", clip(strip_md(str(c.meta.get("summary", ""))), 155))


def build_concept_index(site: Site) -> str:
    page = Page(src=WIKI, rel="concepts/index", meta={}, body="", url="concepts/index.html")
    notes = "".join(
        f"""<a class="note" href="{esc(relurl(page.url, c.url))}">
  <span class="eyebrow">Note {i:02d} · updated {esc(c.meta.get('updated', ''))}</span>
  <strong>{esc(c.title)}</strong>
  <span>{esc(strip_md(str(c.meta.get('summary', ''))))}</span></a>"""
        for i, c in enumerate(site.concepts, 1)
    )
    orgs = "".join(
        f"""<a class="note" href="{esc(relurl(page.url, e.url))}">
  <span class="eyebrow">{esc(str(e.meta.get('entity_kind', 'organization')).replace('-', ' '))} · {len(e.meta.get('sources') or [])} sources</span>
  <strong>{esc(e.title)}</strong>
  <span>{esc(clip(strip_md(str(e.meta.get('summary', ''))), 140))}</span></a>"""
        for e in site.entities
    )
    body = f"""
<div class="shell crumbs"><a href="../index.html">Home</a> / Notes</div>
<header class="shell page-head"><p class="eyebrow">Durable notes</p><h1 class="display sm">Concept index</h1>
<p class="lede">Longer-lived notes that briefings link back to. They change as evidence accumulates; briefings do not.</p></header>
<section class="shell"><div class="notes wide">{notes}</div></section>
<section class="shell"><div class="sectionhead"><h2>Organizations</h2><span>Sources that recur across briefings</span></div>
<div class="notes">{orgs}</div></section>"""
    return document(page, site, "Concept Notes", body, "concepts", "Durable automotive security research notes.")


def build_source(site: Site, s: Page) -> str:
    r = Renderer(site, s)
    url = s.meta.get("source_url", "")
    cited_in = [b for b in site.briefings if s.stem in b.body] + [c for c in site.concepts if s.stem in str(c.meta.get("sources"))]
    cited = "".join(f'<li><a href="{esc(relurl(s.url, p.url))}">{esc(p.title)}</a></li>' for p in cited_in)
    body = f"""
<div class="shell crumbs"><a href="../index.html">Home</a> / <a href="index.html">Sources</a> / record</div>
<section class="shell">
  <article class="catalog-card">
    <div class="cc-top"><span>Source record</span><span>{esc(s.meta.get('source_type', 'source')).upper()}</span><span>{esc(s.meta.get('published', ''))}</span></div>
    <h1>{esc(s.title)}</h1>
    <dl class="kv cc">
      <div><dt>Canonical URL</dt><dd>{f'<a class="ext" href="{esc(url)}" rel="noopener">{esc(url)}</a>' if url else '—'}</dd></div>
      <div><dt>Published</dt><dd>{esc(s.meta.get('published', '—'))}</dd></div>
      <div><dt>Evidence status</dt><dd><code>{esc(s.meta.get('status', '—'))}</code></dd></div>
      <div><dt>Public record</dt><dd>{esc(s.meta.get('public_record', '—'))}</dd></div>
    </dl>
    <p class="muted">This is a public citation record. The full source capture is intentionally not republished here.</p>
    <div class="cc-hole" aria-hidden="true"></div>
  </article>
  {f'<div class="side-box narrow"><h2>Cited by</h2><ul class="srclist">{cited}</ul></div>' if cited else ''}
</section>"""
    return document(s, site, clip(s.title, 60), body, "sources", f"Citation record: {s.title}")


def build_source_index(site: Site) -> str:
    page = site.pages["sources/index"]
    types = sorted({s.meta.get("source_type", "other") for s in site.sources})
    rows = "".join(
        f"""<tr data-type="{esc(s.meta.get('source_type', 'other'))}">
<td class="num">{esc(s.meta.get('published', ''))}</td>
<td><a href="{esc(relurl(page.url, s.url))}">{esc(s.title)}</a></td>
<td><span class="chip plain">{esc(s.meta.get('source_type', ''))}</span></td>
<td><code>{esc(s.meta.get('status', ''))}</code></td></tr>"""
        for s in site.sources
    )
    btns = "".join(f'<button type="button" class="rocker src-f" data-type="{esc(t)}" aria-pressed="false"><span class="led"></span>{esc(t.title())}s</button>' for t in types)
    body = f"""
<div class="shell crumbs"><a href="../index.html">Home</a> / Sources</div>
<header class="shell page-head"><p class="eyebrow">Metadata-only · canonical URLs</p><h1 class="display sm">Source records</h1>
<p class="lede">These records preserve citation metadata and canonical URLs. Full captures stay in the private wiki so source text is not republished.</p></header>
<section class="shell">
  <div class="controls" role="group" aria-label="Filter by source type"><span class="eyebrow">Type</span>{btns}<span class="count" id="s-count">{len(site.sources)} records</span></div>
  <div class="table-wrap"><table class="ledger"><thead><tr><th>Published</th><th>Title</th><th>Type</th><th>Status</th></tr></thead><tbody id="src-rows">{rows}</tbody></table></div>
</section>"""
    return document(page, site, "Source Records", body, "sources", "Public metadata-only citation records.")


def build_method(site: Site) -> str:
    page = Page(src=ROOT / "SCHEMA.md", rel="method", meta={}, body="", url="method.html")
    r = Renderer(site, page)
    schema = r.render((ROOT / "SCHEMA.md").read_text(encoding="utf-8"))
    scale = "".join(
        f'<li>{meter(l, lab)}<span>{desc}</span></li>'
        for l, lab, desc in [
            (5, "High", "Primary record checked directly: advisory, feed, paper or filing."),
            (4, "Medium-high", "Primary source verified; practical exposure or replication not established."),
            (3, "Medium", "Author-reported or proprietary data; deployment conclusions remain open."),
        ]
    )
    body = f"""
<div class="shell crumbs"><a href="index.html">Home</a> / Method</div>
<header class="shell page-head"><p class="eyebrow">Operating manual</p><h1 class="display sm">How the archive is kept</h1>
<p class="lede">The rules every page in this edition follows, and how to read the confidence scale.</p></header>
<div class="shell doc-grid">
  <article class="doc prose">
    <section class="prose-sec"><h2>Confidence scale</h2><ul class="scale">{scale}</ul>
    <p>Confidence is not severity. A high-confidence briefing can describe a low-impact finding, and a medium-confidence one can describe a serious claim that still needs reproduction.</p></section>
    <section class="prose-sec"><h2>Publication boundary</h2>
    <p>This repository publishes the automotive cybersecurity subset of a larger private research wiki. It excludes unrelated research, operational notes, credentials, compatibility pages and full raw source captures. Source records keep provenance without republishing article or paper text.</p></section>
    <section class="prose-sec">{schema}</section>
  </article>
  <aside class="side"><div class="side-box"><h2>Edition</h2><dl class="kv">
    <div><dt>Format</dt><dd>Open Shelf {esc(yaml.safe_load((ROOT / 'kb.yaml').read_text())['openshelf'])}</dd></div>
    <div><dt>Licence</dt><dd>CC BY 4.0</dd></div>
    <div><dt>Briefings</dt><dd>{len(site.briefings)}</dd></div>
    <div><dt>Notes</dt><dd>{len(site.concepts)}</dd></div>
    <div><dt>Sources</dt><dd>{len(site.sources)}</dd></div></dl></div></aside>
</div>"""
    return document(page, site, "Archive Method", body, "method", "How the automotive security archive is kept.")


# --------------------------------------------------------------------------
def write(out: Path, url: str, content: str):
    path = out / url
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "_site"))
    ap.add_argument("--fragment-home", action="store_true",
                    help="also write index.fragment.html (home page without document skeleton)")
    args = ap.parse_args()
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    site = Site()
    write(out, "index.html", build_home(site))
    if args.fragment_home:
        write(out, "index.fragment.html", build_home(site, fragment=True))
    for b in site.briefings:
        write(out, b.url, build_briefing(site, b))
    write(out, "briefings/automotive/index.html", build_briefing_index(site))
    write(out, "briefings/index.html", '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=automotive/index.html"><title>Briefings</title><a href="automotive/index.html">Briefing archive</a>')
    for c in site.concepts + site.entities:
        write(out, c.url, build_concept(site, c))
    write(out, "concepts/index.html", build_concept_index(site))
    for s in site.sources:
        write(out, s.url, build_source(site, s))
    write(out, "sources/index.html", build_source_index(site))
    write(out, "method.html", build_method(site))
    (out / "assets").mkdir(parents=True, exist_ok=True)
    for f in ("site.css", "site.js"):
        shutil.copy(WEB / f, out / "assets" / f)
    (out / ".nojekyll").write_text("")
    n = sum(1 for _ in out.rglob("*.html"))
    print(f"Built {n} pages into {out}")


if __name__ == "__main__":
    main()
