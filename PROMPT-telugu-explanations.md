# Prompt: Telugu explanations in a separate document

Paste this into Claude Code, run from the `ai-135-day-plan` folder.

```text
In this folder I have:
- notes.html source: ~/Downloads/notes.html (my 135-day AI engineering syllabus, topics only)
- telugu-explanations.html (a finished sample for Day 1). Use it as the exact style, structure and design template.

TASK
Create the Telugu explanation document for the remaining days (Day 2 to Day 135) in the SAME style as Day 1, as separate files. Do NOT modify index.html, build.py, app.js or style.css.

For EVERY topic (every bullet under each Day in my notes), write:
1. Topic name (English, exactly as in my document) + Telugu meaning below it
2. ఎందుకు అవసరం? (Why we need it): 2-3 simple sentences, real-world reason
3. సరళమైన వివరణ (Simple explanation): from basics, for a backend developer with 15 years of PHP/Laravel/MySQL experience; compare with PHP/Laravel equivalents wherever possible
4. ఉదాహరణ (Example): small concrete example, real runnable code for coding topics (with Telugu comments), or a real-life scenario for concept topics
5. సాధారణ తప్పు (Common mistake): 1 line, only where relevant

LANGUAGE RULES
- Explanations in simple conversational Telugu script. Technical terms stay in English (embedding, token, Kubernetes...), explained in Telugu the first time they appear.
- Code, commands and variable names stay in English.

QUALITY RULES
- Technically accurate. If unsure about a detail, say so instead of guessing. Check current library/API names before using them (LangChain, LangGraph, MCP, etc. change often).
- Short, clear, example-driven. No filler.
- Do not change, merge or skip my original topics.

HOW TO WORK
- One HTML file per phase: telugu-phase-1.html ... telugu-phase-8.html (same design as the Day 1 sample, with search and expand-all), plus telugu-index.html linking to all phases.
- Work phase by phase. For each phase, split the days across parallel subagents (about 5 days each), then merge and check the results.
- After each phase, open it in the browser preview, verify the Telugu renders and the code blocks look right, and tell me which days are done.
- Start with Phase 1 (finish Days 2-10) and wait for my OK before starting Phase 2.
```

## Tips
- Say "continue Phase 2" and so on after you review each phase.
- Want it shorter or more detailed? Say so before the full run.
- Want one printable PDF per phase? Add: "Also export each phase file to PDF."
