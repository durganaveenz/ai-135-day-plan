#!/usr/bin/env python3
import re
from pathlib import Path

HERE = Path(__file__).parent

header = """<!doctype html>
<html lang="te">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<title>135-Day AI Roadmap – తెలుగు వివరణలు – Phase 8</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#f7f8fb;--panel:#fff;--text:#1b2433;--muted:#5d6b82;--line:#e3e8f0;--accent:#4f46e5;--soft:#eceafd;--ok:#16a34a;--warn:#fff4e0;--warnb:#b45309;--code:#0f172a;--codet:#e2e8f0}
@media (prefers-color-scheme:dark){:root{--bg:#0e1320;--panel:#161d2e;--text:#e6ebf5;--muted:#93a1ba;--line:#26304a;--accent:#8b8cff;--soft:#232a52;--warn:#33270f;--warnb:#f5b04c}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.85 "Noto Sans Telugu",system-ui,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:24px 16px 80px}
h1{font-size:1.7rem;line-height:1.3;margin:0 0 6px}
.sub{color:var(--muted);margin:0 0 16px}
.tools{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 20px;position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:5}
.tools input{flex:1;min-width:200px;padding:10px 14px;border-radius:10px;border:1px solid var(--line);background:var(--panel);color:var(--text);font:inherit}
.tools button{padding:10px 14px;border-radius:10px;border:1px solid var(--line);background:var(--panel);color:var(--text);cursor:pointer;font:inherit}
.day{margin:28px 0 8px;font-size:1.25rem;color:var(--accent);border-bottom:2px solid var(--soft);padding-bottom:6px}
details{background:var(--panel);border:1px solid var(--line);border-radius:12px;margin:10px 0}
summary{cursor:pointer;padding:12px 16px;font-weight:700;list-style:none}
summary::-webkit-details-marker{display:none}
summary::before{content:"▸ ";color:var(--accent)}
details[open]>summary::before{content:"▾ "}
summary small{display:block;font-weight:400;color:var(--muted)}
.body{padding:0 18px 16px;border-top:1px solid var(--line)}
.body h4{margin:16px 0 4px;color:var(--accent);font-size:1rem}
.body p{margin:4px 0}
pre{background:var(--code);color:var(--codet);padding:12px 14px;border-radius:10px;overflow-x:auto;font:13.5px/1.6 ui-monospace,Menlo,Consolas,monospace;margin:8px 0}
.mistake{background:var(--warn);border-left:4px solid var(--warnb);padding:8px 12px;border-radius:8px;margin-top:12px}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.92em;background:var(--soft);padding:1px 5px;border-radius:5px}
.hide{display:none}
</style>
</head>
<body>
<div class="wrap">
<h1>135-Day AI Engineering Roadmap<br>తెలుగు వివరణలు – Phase 8 (Day 91–135)</h1>
<p class="sub"><a href="telugu-index.html">← అన్ని phases</a></p>
<p class="sub">ప్రతి topic కి: ఎందుకు అవసరం, సరళమైన వివరణ, ఉదాహరణ, సాధారణ తప్పులు. Technical పదాలు English లోనే ఉంటాయి.</p>
<div class="tools">
  <input id="q" type="search" placeholder="Search / వెతకండి…">
  <button id="all">అన్నీ తెరువు / మూసివేయి</button>
</div>

"""

footer = """
</div>
<script>
var q=document.getElementById('q'),ds=[].slice.call(document.querySelectorAll('details.t'));
q.addEventListener('input',function(){var v=q.value.toLowerCase().trim();ds.forEach(function(d){var m=!v||d.textContent.toLowerCase().indexOf(v)>-1;d.classList.toggle('hide',!m);if(v&&m)d.open=true;});});
var openAll=false;document.getElementById('all').addEventListener('click',function(){openAll=!openAll;ds.forEach(function(d){d.open=openAll;});});
</script>
</body>
</html>
"""

def main():
    body_parts = []
    missing = []
    total_topics = 0
    for day in range(91, 136):
        f = HERE / f"phase8_day{day}.html"
        if not f.exists():
            missing.append(day)
            continue
        content = f.read_text(encoding="utf-8").strip()
        topics = len(re.findall(r'<details class="t">', content))
        total_topics += topics
        body_parts.append(content)

    if missing:
        print(f"Cannot merge yet! Missing days: {missing}")
        return False

    out_file = HERE / "telugu-phase-8.html"
    full_html = header + "\n\n" + "\n\n".join(body_parts) + "\n" + footer
    out_file.write_text(full_html, encoding="utf-8")
    print(f"Successfully merged {len(body_parts)} days ({total_topics} topics) into {out_file.name}")
    print(f"File size: {out_file.stat().st_size:,} bytes")
    return True

if __name__ == "__main__":
    main()
