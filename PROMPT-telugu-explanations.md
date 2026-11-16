# Prompt: Telugu explanations for every topic

Paste this into Claude Code, run from the `ai-135-day-plan` folder.

```text
My 135-day AI engineering roadmap website is in this folder (index.html, built by build.py from ~/Downloads/notes.html).
Right now it only lists topic names. I need a clear explanation for EVERY topic, in Telugu, so I don't have to search outside.

TASK
For each topic (every bullet/list item under each Day), write an explanation with this exact structure:

1. Topic name (English, exactly as in my document) + Telugu name/meaning in brackets
2. ఎందుకు అవసరం? (Why do we need this?): 2-3 simple sentences, real-world reason
3. సరళమైన వివరణ (Simple explanation): explain from basics, as if to a backend developer with 15 years of PHP/Laravel/MySQL experience. Compare with PHP/Laravel equivalents wherever possible.
4. ఉదాహరణ (Example): a small, concrete example. Use real runnable code (Python) for coding topics, or a real-life analogy/scenario for concept topics. Add the Telugu explanation of the example line by line.
5. సాధారణ తప్పులు (Common mistake): 1 line, only where relevant.

LANGUAGE RULES
- Explanation text in Telugu script (conversational, easy to understand, not heavy literary Telugu).
- Keep technical terms in English (e.g., embedding, token, vector database, Kubernetes) and explain them in Telugu the first time they appear.
- Code, commands and variable names stay in English.

QUALITY RULES
- Be technically accurate. If unsure about a detail, say so rather than guessing.
- No filler. Short, clear, example-driven.
- Do not change or remove my original topics. Explanations are added on top.

HOW TO WORK (the content is large, so do it in batches)
1. FIRST do a sample only: Day 1 (all topics). Show it to me in the website so I can approve the style before continuing.
2. After I approve, generate the remaining days in batches of 5 days (one phase at a time). Run independent batches in parallel with subagents if possible.
3. Store explanations as data files (e.g. data/day-001.json ... day-135.json), one entry per topic, keyed by Day number + topic text. Do not hard-code them into index.html.
4. Update build.py / app.js so that:
   - every topic bullet gets a small "తెలుగులో వివరణ" button; clicking it expands the explanation under that topic
   - a "Expand all explanations" toggle exists per day
   - the existing search also searches the Telugu explanations
   - code examples are shown in a formatted code block with a Copy button
   - the Telugu font renders properly (use Noto Sans Telugu from Google Fonts)
   - topics with no explanation yet show nothing extra, and the page still works
5. Keep existing features working (progress checkboxes, search, dark mode, mobile layout).
6. At the end, list which days are done and which are pending, and verify in the browser preview that Telugu text displays correctly and the buttons work.
```

## Tips
- Start with the Day 1 sample, then say "continue Phase 1" and so on.
- If answers feel too long or too short, tell it before the full run, such as "shorter" or "add more code".
- To get a plain printable file as well, add: "Also generate a single PDF/HTML per phase with all Telugu explanations."
