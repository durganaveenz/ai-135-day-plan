# Telugu Explanations Generation Guide

## Topic Structure
For every single topic, follow this exact HTML format:
```html
<details class="t"><summary>N. [Topic Name in English]<small>[Telugu meaning / summary]</small></summary><div class="body">
<h4>ఎందుకు అవసరం?</h4>
<p>[2-3 simple sentences, real-world reason why this is needed]</p>
<h4>సరళమైన వివరణ</h4>
<p>[Explanation from basics for a backend developer with 15 years PHP/Laravel/MySQL experience; compare with PHP/Laravel equivalents wherever possible]</p>
<h4>ఉదాహరణ</h4>
<pre>[Runnable Python code with Telugu comments or concrete scenario. Always escape < as &lt; and > as &gt;]</pre>
<div class="mistake"><b>సాధారణ తప్పు:</b> [1 line common mistake]</div>
</div></details>
```

## Language Rules
- Explanations in simple conversational Telugu script.
- Technical terms stay in English (agent, state, node, edge, checkpoint, tool, router, MCP, etc.) and explained in Telugu the first time.
- Code, commands, variable names stay in English.

## Quality Rules
- Modern LangChain (0.2+) and LangGraph (0.1+) syntax (`@tool`, `StateGraph`, `START`, `END`, `MemorySaver`, etc.).
- Modern MCP concepts (JSON-RPC 2.0, resources, tools, prompts, sampling).
- Accurate, no hallucinated library methods.
- Compare with PHP/Laravel:
  - Agent state vs Laravel session/Redis state
  - LangChain tools vs Laravel action classes/service methods
  - StateGraph vs Laravel workflow / state machine (e.g. spatie/laravel-model-states)
  - MCP server vs Laravel API endpoint / microservice
  - Agent memory vs Laravel cache / MySQL conversation history
  - HITL (Human-in-the-loop) vs Laravel approval workflow / admin review gate
- Do not change, merge or skip any topic. Number topics starting at 1 for each day.

## Chunking & Output
Because each day has 40–65 topics, DO NOT try to write an entire day in one tool call if it exceeds limits.
Write each day to `phase5_day<NUM>.html`.
Start with `<h2 class="day">Day <NUM>: <Title></h2>`.
Append topics in batches of 15–20 topics using `write_file(Append=True)`.
Validate after each day with:
`python3 validate_day.py <NUM> phase5_day<NUM>.html`
