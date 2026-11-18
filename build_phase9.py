#!/usr/bin/env python3
"""Build telugu-phase-9.html from phase9_data modules."""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Module definitions
MODULES_INFO = [
    (136, "Advanced Distributed Systems", "కన్సెన్సస్, డిస్ట్రిబ్యూటెడ్ ట్రాన్సాక్షన్స్, వెక్టర్ క్లాక్స్, CRDTs & లీనియరైజబిలిటీ", "module1"),
    (137, "Advanced Microservices & Architecture Patterns", "సెల్-బేస్డ్, బల్క్‌హెడ్, సర్వీస్ మెష్, సాగా, అవుట్‌బాక్స్ & CDC", "module2"),
    (138, "Advanced Database Internals", "MVCC, WAL, LSM Trees, B+ Trees, బఫర్ పూల్, SSI & ఆన్‌లైన్ మైగ్రేషన్", "module3"),
    (139, "Advanced Performance Engineering", "టెయిల్ లాటెన్సీ, క్యూయింగ్ థియరీ, బ్యాక్‌ప్రెషర్, జీరో-కాపీ & NUMA", "module4"),
    (140, "Advanced Security Architecture", "జీరో ట్రస్ట్, OAuth 2.1, DPoP, mTLS, SPIFFE, Zanzibar & ఎన్వలప్ ఎన్‌క్రిప్షన్", "module5"),
    (141, "Advanced Reliability Engineering", "SLO/SLA, ఎర్రర్ బడ్జెట్స్, మల్టీ-రీజియన్, ఖోస్ ఇంజనీరింగ్ & బ్రౌన్‌అవుట్", "module6"),
    (142, "Advanced Messaging & Streaming", "Exactly-Once, కన్స్యూమర్ రీబ్యాలెన్సింగ్, వాటర్‌మార్క్స్, కప్పా ఆర్కిటెక్చర్ & కాంపాక్టెడ్ టాపిక్స్", "module7"),
    (143, "Advanced Cloud-Native Architecture", "కుబెర్‌నెటిస్ ఆపరేటర్స్, CRDs, eBPF, కంటైనర్ రన్‌టైమ్, GitOps & ప్లాట్‌ఫామ్ ఇంజనీరింగ్", "module8"),
    (144, "Advanced AI / LLM System Architecture", "RAG, గ్రాఫ్‌రాగ్, ఏజెంటిక్ వర్క్‌ఫ్లోస్, MCP, సెమాంటిక్ క్యాషింగ్, vLLM & AI గేట్‌వే", "module9"),
    (145, "Principal Engineer-Level Concepts", "ADRs, ఫిట్‌నెస్ ఫంక్షన్స్, DDD, టీమ్ టోపోలాజీస్, కాన్వేస్ లా, FinOps & డిస్ట్రిబ్యూటెడ్ ఓనర్‌షిప్", "module10"),
]

def load_all_modules():
    all_days = []
    global_idx = 1
    total_topics_count = 0
    
    for day_num, title, te_summary, mod_name in MODULES_INFO:
        mod = __import__(f'phase9_data.{mod_name}', fromlist=['topics'])
        topics = mod.topics
        total_topics_count += len(topics)
        
        day_topics = []
        for local_idx, t in enumerate(topics, 1):
            day_topics.append({
                "global_idx": global_idx,
                "local_idx": local_idx,
                "title": t["title"],
                "subtitle": t["subtitle"],
                "why": t["why"],
                "explanation": t["explanation"],
                "example": t["example"],
                "mistake": t["mistake"],
            })
            global_idx += 1
            
        all_days.append({
            "day": day_num,
            "title": title,
            "te_summary": te_summary,
            "topics": day_topics
        })
    return all_days, total_topics_count

def render_html():
    days_data, total_topics = load_all_modules()
    
    # Read the head & CSS & scripts from phase 8 as clean template
    p8_text = (ROOT / 'telugu-phase-8.html').read_text(encoding='utf-8')
    
    # Extract head (before body)
    head_part = p8_text[:p8_text.find('<body>')]
    # Update title
    head_part = head_part.replace('Phase 8', 'Phase 9 (Principal Engineer & Advanced Architecture)')
    
    # Build Top Nav & Modal Header
    body_header = f"""<body>
<!-- Sticky Top Navigation Bar -->
<div class="top-nav">
  <div class="top-nav-wrap">
    <div class="nav-left">
      <a href="telugu-index.html" class="nav-back-link" title="అన్ని phases ఇండెక్స్ డాష్‌బోర్డ్‌కి వెళ్లండి">←</a>
      <span class="nav-phase-badge">Phase 9</span>
      <span class="nav-days-text">Days 136–145 · {total_topics} Topics</span>
    </div>
    
    <div class="nav-center">
      <div class="nav-search-box">
        <span class="nav-search-icon">🔍</span>
        <input id="q" type="search" placeholder="ఈ Phase లోని topics వెతకండి… (/ key)" autocomplete="off">
      </div>
    </div>
    
    <div class="nav-right">
      <button id="nav-prof-btn" class="nav-prof-pill" title="చదువుతున్న వ్యక్తిని మార్చండి">
        <span id="nav-prof-avatar" class="prof-avatar">👨‍💻</span>
        <span id="nav-prof-name">Naveen</span>
        <span class="prof-arrow">▾</span>
      </button>

      <button id="nav-popup-btn" class="nav-popup-pill" title="సెట్టింగ్స్ & ప్రోగ్రెస్ మెనూ తెరవండి">
        <span class="pill-dot"></span>
        <span id="nav-status-counts">0 / {total_topics}</span>
        <span id="nav-status-pct" style="color:var(--ok);font-weight:700">0%</span>
        <span class="pill-arrow">⚙️</span>
      </button>
    </div>
  </div>
</div>

<div class="wrap">

<!-- Header Popup Modal -->
<div id="header-modal" class="modal-overlay hide">
  <div class="modal-card">
    <div class="modal-header">
      <div>
        <h3 class="modal-title">Phase 9: Principal Engineer & Advanced Systems Architecture</h3>
        <span class="modal-phase-meta">Day 136–145 · మొత్తం {total_topics} టాపిక్స్</span>
      </div>
      <button id="close-modal-btn" class="modal-close-btn" title="మూసివేయి (Esc)">✕</button>
    </div>
    
    <div class="modal-body">
      <!-- 0. User Profile Selection Card -->
      <div class="modal-section user-section">
        <div class="modal-section-head">చదువుతున్న వ్యక్తి (Active Learner Profile):</div>
        <div class="user-toggle-wrap">
          <button class="user-btn active" data-user="naveen">
            <span class="user-avatar">👨‍💻</span>
            <div class="user-btn-info">
              <span class="user-name">Naveen</span>
              <span id="user-naveen-summary" class="user-summary">0% పూర్తయింది</span>
            </div>
          </button>
          <button class="user-btn" data-user="durga">
            <span class="user-avatar">👩‍💻</span>
            <div class="user-btn-info">
              <span class="user-name">Durga</span>
              <span id="user-durga-summary" class="user-summary">0% పూర్తయింది</span>
            </div>
          </button>
        </div>
      </div>

      <!-- 1. Progress Overview Card -->
      <div class="modal-section progress-card">
        <div class="progress-card-top">
          <span class="prog-card-title">అభ్యసన పురోగతి (Progress)</span>
          <span id="prog-pct" class="prog-card-pct">0% పూర్తయింది</span>
        </div>
        <div class="progress-wrap">
          <div id="prog-bar" class="progress-bar"></div>
        </div>
        <div class="progress-meta">
          <span id="prog-ratio">0 / {total_topics} టాపిక్స్ పూర్తయ్యాయి</span>
          <span id="prog-breakdown">⏳ 0 చదువుతున్నారు · 📦 0 ఆర్కైవ్</span>
        </div>
      </div>

      <!-- 2. Filter Tabs -->
      <div class="modal-section">
        <div class="modal-section-head">టాపిక్స్ ఫిల్టర్ చేయండి (Filter by Status):</div>
        <div class="tabs">
          <button class="tab-btn active" data-tab="all">
            అన్నీ (All) <span class="tab-badge" id="cnt-all">0</span>
          </button>
          <button class="tab-btn" data-tab="start">
            ప్రారంభించు (Start) <span class="tab-badge" id="cnt-start">0</span>
          </button>
          <button class="tab-btn" data-tab="progress">
            చదువుతున్నా (In Progress) ⏳ <span class="tab-badge" id="cnt-progress">0</span>
          </button>
          <button class="tab-btn" data-tab="done">
            పూర్తయింది (Completed) ✅ <span class="tab-badge" id="cnt-done">0</span>
          </button>
          <button class="tab-btn" data-tab="archive">
            ఆర్కైవ్ (Archive) 📦 <span class="tab-badge" id="cnt-archive">0</span>
          </button>
        </div>
      </div>

      <!-- Backup & Multi-Browser Sync -->
      <div class="modal-section backup-section">
        <div class="modal-section-head">వేరే బ్రౌజర్‌లో వాడుకోవడానికి (Backup & Sync):</div>
        <div class="backup-btns-row">
          <button id="export-backup-btn" class="backup-btn" title="మీ మొత్తం నోట్స్ మరియు ప్రోగ్రెస్ ఫైల్ డౌన్‌లోడ్ చేసుకోండి">
            <span>📥</span> బ్యాకప్ డౌన్‌లోడ్ (Export)
          </button>
          <label class="backup-btn" style="margin:0;cursor:pointer" title="డౌన్‌లోడ్ చేసుకున్న బ్యాకప్ ఫైల్ ఇక్కడ అప్‌లోడ్ చేయండి">
            <span>📤</span> బ్యాకప్ లోడ్ (Import)
            <input id="import-backup-input" type="file" accept=".json" style="display:none">
          </label>
        </div>
      </div>

      <!-- 3. Page Controls -->
      <div class="modal-section">
        <div class="modal-section-head">పేజీ నియంత్రణలు (Page Controls):</div>
        <div class="modal-actions-row">
          <button id="all" class="modal-action-btn">
            <span>📂</span> అన్నీ తెరువు / మూసివేయి
          </button>
          
          <div class="font-ctrl-wrap">
            <span class="font-ctrl-label">ఫాంట్ సైజ్:</span>
            <div class="font-ctrls">
              <button id="font-dec" title="చిన్న ఫాంట్">A-</button>
              <button id="font-reset" title="సాధారణ ఫాంట్">A</button>
              <button id="font-inc" title="పెద్ద ఫాంట్">A+</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal-footer">
      <a href="telugu-index.html" class="modal-index-link">← అన్ని phases ఇండెక్స్ డాష్‌బోర్డ్</a>
      <button id="done-modal-btn" class="modal-done-btn">పూర్తయింది (Done)</button>
    </div>
  </div>
</div>

<div class="page-title-bar">
  <h1>135-Day AI Engineering Roadmap<br>Phase 9: Principal Engineer & Advanced Systems Architecture</h1>
  <p class="sub">డిస్ట్రిబ్యూటెడ్ సిస్టమ్స్, అడ్వాన్స్‌డ్ మైక్రోసర్వీసెస్, డేటాబేస్ ఇంటర్నల్స్, పర్ఫార్మెన్స్, సెక్యూరిటీ, రిలయబిలిటీ, స్ట్రీమింగ్, క్లౌడ్-నేటివ్, AI/LLM ఆర్కిటెక్చర్ & ప్రిన్సిపల్ ఇంజనీరింగ్ నిర్ణయాలు.</p>
</div>
"""

    body_content = []
    
    for d in days_data:
        day_num = d["day"]
        day_title = d["title"]
        topics = d["topics"]
        
        day_html = [
            f'<details class="day-sec" data-day="{day_num}">',
            '  <summary class="day-summary">',
            '    <div class="day-title-wrap">',
            '      <span class="day-chevron">▸</span>',
            f'      <span class="day-heading-text">Day {day_num}: {day_title} ({d["te_summary"]})</span>',
            '    </div>',
            '    <div class="day-badge-wrap">',
            f'      <span class="day-progress-badge" id="day-badge-{day_num}">0/{len(topics)}</span>',
            '    </div>',
            '  </summary>',
            '  <div class="day-body">'
        ]
        
        for t in topics:
            g_idx = t["global_idx"]
            l_idx = t["local_idx"]
            title_escaped = html.escape(t["title"])
            subtitle_escaped = html.escape(t["subtitle"])
            why_text = html.escape(t["why"]).replace('\n', '<br>')
            exp_text = html.escape(t["explanation"]).replace('\n', '<br>')
            example_code = html.escape(t["example"])
            mistake_text = html.escape(t["mistake"])
            
            topic_block = f"""    <span class="global-search-anchor" id="global-topic-9-{g_idx}"></span><details class="t" id="p9-t{g_idx}"><summary>{l_idx}. {title_escaped}<small>{subtitle_escaped}</small></summary><div class="body">
<h4>ఎందుకు అవసరం?</h4>
<p>{why_text}</p>
<h4>సరళమైన వివరణ</h4>
<p>{exp_text}</p>
<h4>ఉదాహరణ</h4>
<pre>{example_code}</pre>
<div class="mistake"><b>సాధారణ తప్పు:</b> {mistake_text}</div>
</div></details>"""
            day_html.append(topic_block)
            
        day_html.append('  </div>\n</details>')
        body_content.append('\n'.join(day_html))

    # JavaScript part
    # Extract the JS from phase 8 and update PHASE_NUM = 9
    js_start_idx = p8_text.find('<script>')
    js_part = p8_text[js_start_idx:]
    
    # In js_part, update:
    js_part = js_part.replace('var PHASE_NUM = 8;', 'var PHASE_NUM = 9;')
    # Update navigation in JS:
    # Phase 9 previous is Phase 8!
    # Phase 9 is the last phase (no phase 10 yet)
    js_part = js_part.replace('PHASE_NUM < 8', 'PHASE_NUM < 9')
    js_part = js_part.replace('Phase 8', 'Phase 9')
    
    full_html = head_part + body_header + '\n\n'.join(body_content) + '\n</div>\n' + js_part
    return full_html

def main():
    print("Building telugu-phase-9.html...")
    content = render_html()
    out_file = ROOT / 'telugu-phase-9.html'
    out_file.write_text(content, encoding='utf-8')
    print(f"✅ Generated {out_file.name} successfully! Size: {out_file.stat().st_size:,} bytes")

if __name__ == '__main__':
    main()
