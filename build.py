#!/usr/bin/env python3
"""Convert the 135-day plan notes (plain text) into a static website.

Usage: python3 build.py /path/to/notes.html
Writes index.html, style.css, app.js next to this script.
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
src = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "Downloads/notes.html")
lines = src.read_text(encoding="utf-8").splitlines()

PHASE_RE = re.compile(r"^Phase (\d+) — (?!.*\(Days)(.+)$")
DAYS_RE = re.compile(r"^Days? (\d+)\s*[–-]\s*(\d+)$")
NUM_RE = re.compile(r"^(\d{1,3})\.\s+(.{3,110})$")
LABEL_RE = re.compile(
    r"^(Objective|Practical(?: implementation| exercise| project)?|Expected outcome|"
    r"Final deliverable|Phase \d+ (?:practical project|capstone)|Capstone|Next|Practical project)\s*:\s*(.*)$"
)
NOISE_RE = re.compile(r"^(\d+|\d+/\d+)$")
DOMAIN_RE = re.compile(r"^[a-z0-9.-]+\.(com|ai|io|org|net|github\.io)$", re.I)
SECTION_RE = re.compile(r"^(Section \d+ — .+|Final supplementary topics — .+|Phase \d+ completion — .+)$")


def esc(s):
    return html.escape(s, quote=False)


# ---------- parse ----------
phases = []  # each: dict(num,title,days,sub,intro[],sections[])
cur_phase = None
cur_sec = None
skip = True  # skip chat preamble until first phase
pending_table = []


def nodes():
    return cur_sec["nodes"] if cur_sec else cur_phase["intro"]


def new_phase(num, title, key=None):
    global cur_phase, cur_sec
    cur_phase = dict(num=num, title=title, days="", sub="", intro=[], sections=[], key=key or f"p{num}", start=0, end=0, last=0)
    if num == 8:
        cur_phase.update(days="Days 91–135", start=91, end=135, last=90)
    cur_sec = None
    phases.append(cur_phase)


def new_section(title, kind="topic"):
    global cur_sec
    cur_sec = dict(title=title, kind=kind, nodes=[])
    cur_phase["sections"].append(cur_sec)


def add_li(text, checkbox=False):
    ns = nodes()
    if ns and ns[-1]["t"] == "ul" and ns[-1]["cb"] == checkbox:
        ns[-1]["items"].append(text)
    else:
        ns.append(dict(t="ul", items=[text], cb=checkbox))


def flush_table():
    global pending_table
    if pending_table:
        nodes().append(dict(t="table", rows=[r.split("\t") for r in pending_table]))
        pending_table = []


for idx, raw in enumerate(lines):
    line = raw.strip()
    if not line:
        flush_table()
        continue
    if "\t" in line:
        if not skip or cur_phase:
            pending_table.append(line)
        continue
    flush_table()

    m = PHASE_RE.match(line)
    if m:
        skip = False
        new_phase(int(m.group(1)), m.group(2).strip())
        continue
    if cur_phase is None:
        continue
    # phase-8 style "Additional 30-day curriculum · Days 91–120"
    if "Additional 30-day curriculum" in line and not cur_phase["sub"]:
        cur_phase["sub"] = line
        continue
    m = DAYS_RE.match(line)
    if m:
        if not cur_phase["days"]:
            cur_phase["days"] = f"Days {m.group(1)}–{m.group(2)}"
            cur_phase["start"], cur_phase["end"] = int(m.group(1)), int(m.group(2))
            cur_phase["last"] = int(m.group(1)) - 1
        continue
    if skip:
        continue
    if NOISE_RE.match(line) or DOMAIN_RE.match(line) or ", man" in line or line.startswith("Perfect, man"):
        continue
    if re.match(r"^Phase \d+ self-assessment$", line):
        continue
    if re.match(r"^Phase \d+ completion checklist$", line):
        new_section("Completion checklist", "checklist")
        continue
    if line == "Final master roadmap" and cur_phase["num"] == 8:
        new_section("Appendix: roadmap summary, optional topics and final notes", "appendix")
        continue
    if SECTION_RE.match(line):
        new_section(line, "divider")
        continue
    if line.startswith("[ ] "):
        add_li(line[4:].strip(), checkbox=True)
        continue
    m = LABEL_RE.match(line)
    if m:
        label, rest = m.group(1), m.group(2)
        if label == "Next":
            nodes().append(dict(t="callout", label="Next", text=rest))
            skip = True  # chat preamble of the following phase follows
            continue
        full = re.match(r"^([^:]+):", line).group(1)
        nodes().append(dict(t="callout", label=full, text=rest))
        continue
    m = NUM_RE.match(line)
    if m and not re.search(r"[.:;?!]$", m.group(2)):
        n, title = int(m.group(1)), m.group(2).strip()
        if n == cur_phase["last"] + 1 and cur_phase["start"] <= n <= cur_phase["end"]:
            cur_phase["last"] = n
            new_section(f"Day {n}: {title}", "day")
        else:
            nodes().append(dict(t="h4", text=f"{n}. {title}"))
        continue
    if line.startswith("- "):
        add_li(line[2:].strip())
        continue
    if m:  # numbered item ending in punctuation -> list item
        add_li(f"{m.group(1)}. {m.group(2)}")
        continue
    words = len(line.split())
    if line.endswith(".") and len(line) <= 95 and words < 13 and cur_sec:
        add_li(line)
        continue
    if len(line) <= 70 and not re.search(r"[.,:;!?]$", line) and words <= 9:
        nodes().append(dict(t="h4", text=line))
        continue
    nodes().append(dict(t="p", text=line))

flush_table()

# ---------- render ----------
def render_nodes(ns, pid, sid):
    out = []
    for i, n in enumerate(ns):
        t = n["t"]
        if t == "h4":
            out.append(f"<h4>{esc(n['text'])}</h4>")
        elif t == "p":
            out.append(f"<p>{esc(n['text'])}</p>")
        elif t == "callout":
            cls = re.sub(r"[^a-z]+", "-", n["label"].lower()).strip("-")
            out.append(
                f'<div class="callout {cls}"><strong>{esc(n["label"])}</strong>'
                f'{(": " + esc(n["text"])) if n["text"] else ""}</div>'
            )
        elif t == "ul":
            if n["cb"]:
                items = "".join(
                    f'<li><label><input type="checkbox" data-id="{pid}-{sid}-{i}-{k}"> <span>{esc(x)}</span></label></li>'
                    for k, x in enumerate(n["items"])
                )
                out.append(f'<ul class="checklist">{items}</ul>')
            else:
                out.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in n["items"]) + "</ul>")
        elif t == "table":
            rows = n["rows"]
            head = "".join(f"<th>{esc(c)}</th>" for c in rows[0])
            body = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
    return "\n".join(out)


def phase_html(p):
    pid = p["key"]
    parts = [
        f'<section class="phase" id="{pid}" data-phase="{p["num"]}" hidden>',
        f'<header class="phase-head"><span class="eyebrow">Phase {p["num"]}'
        f'{(" · " + esc(p["days"])) if p["days"] else ""}</span><h2>{esc(p["title"])}</h2>',
        f'{("<p class=sub>" + esc(p["sub"]) + "</p>") if p["sub"] else ""}</header>',
        render_nodes(p["intro"], pid, "i"),
    ]
    for s_i, s in enumerate(p["sections"]):
        sid = f"s{s_i}"
        if s["kind"] == "divider":
            parts.append(f'<h3 class="divider">{esc(s["title"])}</h3>')
            parts.append(render_nodes(s["nodes"], pid, sid))
            continue
        done = "" if s["kind"] in ("checklist", "appendix") else (
            f'<label class="done" title="Mark as done"><input type="checkbox" class="sec-done" data-id="{pid}-{sid}-done"> Done</label>'
        )
        open_attr = " open" if s["kind"] == "checklist" else ""
        parts.append(
            f'<details class="topic {s["kind"]}"{open_attr} data-sec="{pid}-{sid}">'
            f'<summary><span class="t">{esc(s["title"])}</span>{done}</summary>'
            f'<div class="body">{render_nodes(s["nodes"], pid, sid)}</div></details>'
        )
    parts.append("</section>")
    return "\n".join(parts)


def sec_count(p):
    return sum(1 for s in p["sections"] if s["kind"] in ("topic", "day"))


# merge a trailing "Wrap-up" if the final phase contains the final roadmap (kept inside phase 8 sections)
total_topics = sum(sec_count(p) for p in phases)
nav = []
cards = []
for p in phases:
    label = f'Phase {p["num"]}'
    nav.append(
        f'<a href="#{p["key"]}" data-nav="{p["key"]}"><span class="n">{p["num"]}</span>'
        f'<span class="l"><b>{esc(p["title"].split(":")[0])}</b><small>{esc(p["days"])}</small>'
        f'<i class="bar"><i data-bar="{p["key"]}"></i></i></span></a>'
    )
    cards.append(
        f'<a class="card" href="#{p["key"]}"><span class="eyebrow">{label} · {esc(p["days"])}</span>'
        f'<h3>{esc(p["title"])}</h3><span class="meta">{sec_count(p)} topics</span>'
        f'<i class="bar"><i data-bar="{p["key"]}"></i></i></a>'
    )

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<title>135-Day AI Engineering Roadmap</title>
<meta name="description" content="A 135-day, 8-phase AI engineering curriculum: Python, ML, LLMs, RAG, agents, production AI and enterprise architecture.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<button class="menu-btn" id="menuBtn" aria-label="Toggle menu">☰</button>
<aside id="sidebar">
  <a class="brand" href="#home">135-Day AI<br>Engineering Roadmap</a>
  <div class="overall"><div class="bar big"><i data-bar="all"></i></div><small id="overallText">0% complete</small></div>
  <nav>{''.join(nav)}</nav>
  <button id="themeBtn" class="theme">Toggle theme</button>
</aside>
<main>
  <div class="searchbar"><input id="search" type="search" placeholder="Search all topics (e.g. RAG, Kubernetes, LangGraph)…" aria-label="Search"><span id="searchInfo"></span></div>
  <section id="home" class="home">
    <div class="hero">
      <span class="eyebrow">8 phases · 135 days</span>
      <h1>From Python backend engineer to AI solution architect</h1>
      <p>A complete roadmap covering Python, machine learning, generative AI, RAG, agentic systems, production AI, cloud and enterprise architecture. Tick topics off as you finish them; progress is saved in your browser.</p>
    </div>
    <div class="cards">{''.join(cards)}</div>
  </section>
  {''.join(phase_html(p) for p in phases)}
</main>
<script>window.TOTAL_TOPICS={total_topics};</script>
<script src="app.js"></script>
</body>
</html>
"""
(HERE / "index.html").write_text(page, encoding="utf-8")
print(f"phases={len(phases)} topics={total_topics}")
for p in phases:
    kinds = {}
    for s in p["sections"]:
        kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
    n_h4 = sum(1 for s in p["sections"] for n in s["nodes"] if n["t"] == "h4") + sum(1 for n in p["intro"] if n["t"] == "h4")
    print(p["num"], p["title"][:50], p["days"], kinds, "h4:", n_h4)
