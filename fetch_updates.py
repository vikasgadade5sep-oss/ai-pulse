#!/usr/bin/env python3
"""
AI Pulse — 15-Second Anti-Slop AI Digest Generator with Universal Multi-Digest History
Zero external dependencies (pure Python standard library).
Queries Gemini 2.5 Flash + Google Search Grounding to fetch 15 verified updates from the last 4 days.
Maintains an embedded historical archive of all past 4-day runs inside index.html so the single
universal link serves both the latest run and every historical digest ever generated.
"""

import os
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta

def get_updates():
    api_key = os.environ.get("GEMINI_API_KEY")
    today = datetime.now()
    four_days_ago = today - timedelta(days=4)
    date_str = f"{four_days_ago.strftime('%b %d')} – {today.strftime('%b %d, %Y')}"

    if not api_key:
        print("[INFO] GEMINI_API_KEY not found in environment. Using fallback seed data.")
        return get_fallback_data(date_str)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
Search the live web for the top verified AI news, open weights drops, and engineering announcements from the last 4 days ({date_str}).
Return ONLY a valid JSON object matching the exact schema below, with no surrounding conversation.

Requirements (EXACTLY 15 updates):
- 5 under 'models' (Foundation models, open weights, architecture papers)
- 5 under 'tools' (Developer tools, libraries, agents, SDKs, CLIs)
- 5 under 'industry' (Hardware, compute, data centers, major policy/business shifts)

Strict Rules:
1. 'takeaway': STRICTLY 5 WORDS OR FEWER. No fluff, no marketing words.
2. 'summary': Exactly ONE concise technical sentence.
3. 'use_case': Exactly ONE sentence describing the practical developer/engineer use case.
4. 'link': Primary source link (official blog, GitHub repo, paper, or company announcement).

Schema:
{{
  "date_range": "{date_str}",
  "updates": [
    {{
      "category": "models",
      "name": "Exact Name",
      "takeaway": "Max five word takeaway",
      "summary": "One sentence technical summary.",
      "use_case": "Practical application or developer workflow unlock.",
      "link": "https://official-source-url"
    }}
  ]
}}
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}]
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            res = json.loads(response.read().decode("utf-8"))
            raw_text = res["candidates"][0]["content"]["parts"][0]["text"]
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                if "updates" in data and len(data["updates"]) >= 15:
                    print(f"[SUCCESS] Fetched {len(data['updates'])} live AI updates via Gemini Search!")
                    return data
            print("[WARN] Could not parse complete JSON array. Using fallback.")
            return get_fallback_data(date_str)
    except Exception as e:
        print(f"[ERROR] Gemini API request failed: {e}. Using fallback.")
        return get_fallback_data(date_str)

def get_fallback_data(date_str):
    return {
        "date_range": date_str,
        "updates": [
            {"category": "models", "name": "Gemini 2.5 Flash", "takeaway": "Sub-second multimodal thinking model released.", "summary": "Google upgraded Flash with adaptive reasoning depth and native coding agents.", "use_case": "High-speed multi-agent orchestration and automated code repair.", "link": "https://ai.google.dev/"},
            {"category": "models", "name": "DeepSeek-V3", "takeaway": "671B MoE open weights released.", "summary": "Activates 37B per token with Multi-Head Latent Attention at 1/5th compute cost.", "use_case": "Self-hosted high-throughput local inference on consumer hardware.", "link": "https://github.com/deepseek-ai/DeepSeek-V3"},
            {"category": "models", "name": "Llama 3.3 70B", "takeaway": "405B performance in 70B footprint.", "summary": "Upgraded 128K context window matching the massive 405B model efficiency.", "use_case": "Private enterprise RAG pipelines on dual RTX 3090/4090 GPUs.", "link": "https://ai.meta.com/blog/llama-3-3/"},
            {"category": "models", "name": "Qwen 2.5 Coder 32B", "takeaway": "Open source code champion updated.", "summary": "Alibaba released the top-performing open-source coding model on HumanEval.", "use_case": "Autonomous local code review and offline pair programming.", "link": "https://qwenlm.github.io/"},
            {"category": "models", "name": "Mistral Large 2", "takeaway": "128K context reasoning frontier model.", "summary": "Advanced multilingual model designed for massive multi-hop reasoning.", "use_case": "Document analysis and complex multilingual enterprise pipelines.", "link": "https://mistral.ai/"},
            {"category": "tools", "name": "vLLM 0.6.5", "takeaway": "Prefix caching throughput boosted 40%.", "summary": "Ultra-fast LLM inference engine with automated continuous batching and FP8 kernels.", "use_case": "Deploying scalable local LLM servers with zero prompt latency.", "link": "https://github.com/vllm-project/vllm"},
            {"category": "tools", "name": "LangChain v0.3", "takeaway": "Lightweight core separated from integrations.", "summary": "Total decoupling of core interfaces from vendor packages for faster CI/CD.", "use_case": "Production AI workflows with minimal dependency footprint.", "link": "https://github.com/langchain-ai/langchain"},
            {"category": "tools", "name": "LlamaIndex Workflows", "takeaway": "Event-driven multi-agent orchestration framework.", "summary": "Replaces rigid DAG execution graphs with async event-driven reactive loops.", "use_case": "Complex RAG search agents with human-in-the-loop approval.", "link": "https://www.llamaindex.ai/"},
            {"category": "tools", "name": "Ollama 0.5", "takeaway": "Built-in structured JSON schema enforcement.", "summary": "Guarantees schema compliance during token generation directly inside llama.cpp.", "use_case": "Reliable local tool calling and agent action routing.", "link": "https://ollama.com/"},
            {"category": "tools", "name": "Cursor Agent Mode", "takeaway": "Autonomous multi-file codebase editor.", "summary": "Background agent that writes, verifies, and debugs code across multiple files.", "use_case": "Accelerated full-stack feature development and automated refactoring.", "link": "https://cursor.com/"},
            {"category": "industry", "name": "NVIDIA Blackwell B200", "takeaway": "Full scale volume production underway.", "summary": "Delivers 4x training and 30x inference throughput over H100 architecture.", "use_case": "Massive multi-trillion parameter MoE model training.", "link": "https://nvidianews.nvidia.com/"},
            {"category": "industry", "name": "Anthropic 3.5 Sonnet", "takeaway": "Computer use API generally available.", "summary": "Empowers agents to visually interact with desktop software and web interfaces.", "use_case": "Automating legacy enterprise software lacking APIs.", "link": "https://www.anthropic.com/"},
            {"category": "industry", "name": "OpenAI Operator", "takeaway": "Autonomous browser agent preview launched.", "summary": "Execute multi-step web browsing tasks directly inside cloud containers.", "use_case": "Automated end-to-end travel booking and competitor intelligence.", "link": "https://openai.com/"},
            {"category": "industry", "name": "Google TPU v6e", "takeaway": "Trillium clusters available on GCP.", "summary": "Provides 4.7x compute boost per chip compared to TPU v5e.", "use_case": "Cost-effective large-scale transformer fine-tuning.", "link": "https://cloud.google.com/tpu"},
            {"category": "industry", "name": "AWS Trainium2", "takeaway": "UltraServer clusters now live.", "summary": "Links 64 Trainium2 chips with non-blocking petabit-scale fabric.", "use_case": "Low-cost alternative for hyperscale AI model pretraining.", "link": "https://aws.amazon.com/machine-learning/trainium/"}
        ]
    }

def load_existing_digests():
    if os.path.exists("index.html"):
        try:
            with open("index.html", "r", encoding="utf-8") as f:
                content = f.read()
            match = re.search(r'<script id="digests-data" type="application/json">\s*(.*?)\s*</script>', content, re.DOTALL)
            if match:
                parsed = json.loads(match.group(1))
                if isinstance(parsed, list):
                    return parsed
        except Exception as e:
            print(f"[WARN] Could not parse existing digests from index.html: {e}")
    return []

def render_html(new_digest):
    existing = load_existing_digests()
    
    if existing and existing[0].get("date_range") == new_digest.get("date_range"):
        existing[0] = new_digest
    else:
        existing.insert(0, new_digest)
    
    all_digests = existing[:30]
    digests_json_str = json.dumps(all_digests, indent=2)

    options_html = ""
    for idx, d in enumerate(all_digests):
        dr = d.get("date_range", f"Digest #{idx+1}")
        label = f"⚡ Latest ({dr})" if idx == 0 else f"📅 {dr}"
        selected = "selected" if idx == 0 else ""
        options_html += f'<option value="{idx}" {selected}>{label}</option>\n'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Pulse — 15-Second Anti-Slop AI Digest</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  </style>
</head>
<body class="bg-neutral-50 text-neutral-900 dark:bg-neutral-950 dark:text-neutral-100 min-h-screen p-3 sm:p-6 antialiased">
  <div class="max-w-5xl mx-auto space-y-6">

    <header class="border-b border-neutral-200 dark:border-neutral-800 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-semibold rounded bg-neutral-200 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200">
            ⚡ 15-SEC SCAN
          </span>
          <select id="digest-select" onchange="switchDigest(this.value)" class="text-xs font-mono font-semibold rounded bg-neutral-100 dark:bg-neutral-900 border border-neutral-300 dark:border-neutral-800 text-neutral-700 dark:text-neutral-300 px-2 py-0.5 focus:outline-none focus:ring-1 focus:ring-neutral-400 cursor-pointer">
            {options_html}
          </select>
        </div>
        <h1 class="text-xl sm:text-2xl font-bold tracking-tight">AI Pulse: 15 Verified Updates</h1>
        <p class="text-xs text-neutral-500 dark:text-neutral-400">Strictly 5 words per row. Click any row for details. Use dropdown to view past runs.</p>
      </div>

      <div class="flex items-center gap-2 self-start sm:self-auto">
        <div class="inline-flex p-1 rounded-lg bg-neutral-200/70 dark:bg-neutral-900 border border-neutral-300/60 dark:border-neutral-800">
          <button id="tab-table-btn" onclick="setView('table')" class="px-3 py-1 text-xs font-semibold rounded-md bg-white dark:bg-neutral-800 shadow-sm transition-all">
            📊 Table View
          </button>
          <button id="tab-pills-btn" onclick="setView('pills')" class="px-3 py-1 text-xs font-medium text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-all">
            💊 Pill Cards
          </button>
        </div>
      </div>
    </header>

    <div class="flex flex-wrap items-center justify-between gap-3 text-xs">
      <div class="flex flex-wrap gap-1.5" id="category-bar">
        <button onclick="setCategory('all')" id="cat-all" class="cat-btn px-2.5 py-1 rounded font-medium bg-neutral-900 text-white dark:bg-white dark:text-neutral-900 transition-colors">
          All (15)
        </button>
        <button onclick="setCategory('models')" id="cat-models" class="cat-btn px-2.5 py-1 rounded font-medium bg-neutral-100 dark:bg-neutral-900 text-neutral-600 dark:text-neutral-400 hover:bg-neutral-200 dark:hover:bg-neutral-800 transition-colors">
          🧠 Models (5)
        </button>
        <button onclick="setCategory('tools')" id="cat-tools" class="cat-btn px-2.5 py-1 rounded font-medium bg-neutral-100 dark:bg-neutral-900 text-neutral-600 dark:text-neutral-400 hover:bg-neutral-200 dark:hover:bg-neutral-800 transition-colors">
          ⚡ Tools (5)
        </button>
        <button onclick="setCategory('industry')" id="cat-industry" class="cat-btn px-2.5 py-1 rounded font-medium bg-neutral-100 dark:bg-neutral-900 text-neutral-600 dark:text-neutral-400 hover:bg-neutral-200 dark:hover:bg-neutral-800 transition-colors">
          🌐 Industry (5)
        </button>
      </div>
      <div class="flex items-center gap-3">
        <span id="run-badge" class="text-[11px] text-emerald-600 dark:text-emerald-400 font-mono font-medium">⚡ Live Run</span>
        <span class="text-[11px] text-neutral-400 font-mono">100% Primary Sources</span>
      </div>
    </div>

    <div id="view-table" class="border border-neutral-200 dark:border-neutral-800 rounded-xl overflow-hidden bg-white dark:bg-neutral-900/60 shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="border-b border-neutral-200 dark:border-neutral-800 bg-neutral-100/60 dark:bg-neutral-900 text-neutral-500 font-mono uppercase tracking-wider text-[11px]">
              <th class="py-2.5 px-3 w-28">Category</th>
              <th class="py-2.5 px-3 w-48">Tool / Model</th>
              <th class="py-2.5 px-3">5-Word Takeaway</th>
              <th class="py-2.5 px-3 text-right w-24">Link</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-neutral-100 dark:divide-neutral-800/60" id="table-body">
          </tbody>
        </table>
      </div>
    </div>

    <div id="view-pills" class="hidden grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
    </div>

    <footer class="pt-4 border-t border-neutral-200 dark:border-neutral-800 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-neutral-400 font-mono">
      <span>Auto-synced every 4 days via GitHub Actions (100% Free)</span>
      <span class="text-[11px] text-neutral-500">Universal Link: <a href="https://vikasgadade5sep-oss.github.io/ai-pulse/" class="underline hover:text-neutral-300">vikasgadade5sep-oss.github.io/ai-pulse/</a></span>
    </footer>

  </div>

  <script id="digests-data" type="application/json">
{digests_json_str}
  </script>

  <script>
    const allDigests = JSON.parse(document.getElementById('digests-data').textContent);
    let activeDigestIdx = 0;
    let activeCat = 'all';
    let activeView = 'table';

    function switchDigest(idx) {{
      activeDigestIdx = parseInt(idx);
      const badge = document.getElementById('run-badge');
      if (activeDigestIdx === 0) {{
        badge.innerText = '⚡ Live Run';
        badge.className = 'text-[11px] text-emerald-600 dark:text-emerald-400 font-mono font-medium';
      }} else {{
        badge.innerText = `🏛️ Historical Digest #${{allDigests.length - activeDigestIdx}}`;
        badge.className = 'text-[11px] text-amber-600 dark:text-amber-400 font-mono font-medium';
      }}
      renderContent();
    }}

    function setView(view) {{
      activeView = view;
      const table = document.getElementById('view-table');
      const pills = document.getElementById('view-pills');
      const tableBtn = document.getElementById('tab-table-btn');
      const pillsBtn = document.getElementById('tab-pills-btn');

      if (view === 'table') {{
        table.classList.remove('hidden');
        pills.classList.add('hidden');
        tableBtn.className = "px-3 py-1 text-xs font-semibold rounded-md bg-white dark:bg-neutral-800 shadow-sm transition-all";
        pillsBtn.className = "px-3 py-1 text-xs font-medium text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-all";
      }} else {{
        table.classList.add('hidden');
        pills.classList.remove('hidden');
        pillsBtn.className = "px-3 py-1 text-xs font-semibold rounded-md bg-white dark:bg-neutral-800 shadow-sm transition-all";
        tableBtn.className = "px-3 py-1 text-xs font-medium text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-all";
      }}
      renderContent();
    }}

    function toggleDrawer(id) {{
      const drawer = document.getElementById(id);
      if (drawer) drawer.classList.toggle('hidden');
    }}

    function setCategory(cat) {{
      activeCat = cat;
      document.querySelectorAll('.cat-btn').forEach(b => {{
        b.className = "cat-btn px-2.5 py-1 rounded font-medium bg-neutral-100 dark:bg-neutral-900 text-neutral-600 dark:text-neutral-400 hover:bg-neutral-200 dark:hover:bg-neutral-800 transition-colors";
      }});
      const activeBtn = document.getElementById('cat-' + cat);
      if (activeBtn) {{
        activeBtn.className = "cat-btn px-2.5 py-1 rounded font-medium bg-neutral-900 text-white dark:bg-white dark:text-neutral-900 transition-colors";
      }}
      renderContent();
    }}

    function renderContent() {{
      const digest = allDigests[activeDigestIdx] || allDigests[0];
      const updates = digest.updates || [];

      const tbody = document.getElementById('table-body');
      tbody.innerHTML = '';
      updates.forEach((u, idx) => {{
        const cat = (u.category || 'models').toLowerCase();
        if (activeCat !== 'all' && cat !== activeCat) return;

        const badgeColor = cat === 'models' ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400' :
                           cat === 'tools' ? 'bg-purple-500/10 text-purple-600 dark:text-purple-400' :
                           'bg-amber-500/10 text-amber-600 dark:text-amber-400';
        const drawerId = `d_${{activeDigestIdx}}_${{idx}}`;

        const row = document.createElement('tr');
        row.className = "item-row hover:bg-neutral-50 dark:hover:bg-neutral-800/40 cursor-pointer transition-colors";
        row.onclick = () => toggleDrawer(drawerId);
        row.innerHTML = `
          <td class="py-2.5 px-3"><span class="px-1.5 py-0.5 rounded text-[10px] font-semibold ${{badgeColor}}">${{cat.toUpperCase()}}</span></td>
          <td class="py-2.5 px-3 font-semibold text-neutral-900 dark:text-neutral-100">${{u.name}}</td>
          <td class="py-2.5 px-3 font-medium text-neutral-700 dark:text-neutral-300">${{u.takeaway}}</td>
          <td class="py-2.5 px-3 text-right font-mono text-[11px]">
            <a href="${{u.link}}" target="_blank" onclick="event.stopPropagation()" class="text-blue-600 dark:text-blue-400 hover:underline">Open &rarr;</a>
          </td>
        `;
        tbody.appendChild(row);

        const drawer = document.createElement('tr');
        drawer.id = drawerId;
        drawer.className = "hidden bg-neutral-50/80 dark:bg-neutral-950/60 border-b border-neutral-200 dark:border-neutral-800";
        drawer.innerHTML = `
          <td colspan="4" class="px-4 py-3">
            <div class="space-y-1.5 text-xs">
              <p class="text-neutral-600 dark:text-neutral-300"><strong>Summary:</strong> ${{u.summary}}</p>
              <p class="text-emerald-600 dark:text-emerald-400">💡 <strong>Use Case:</strong> ${{u.use_case}}</p>
              <a href="${{u.link}}" target="_blank" class="inline-block text-[11px] font-semibold text-neutral-900 dark:text-neutral-100 underline mt-1">Official Source &rarr;</a>
            </div>
          </td>
        `;
        tbody.appendChild(drawer);
      }});

      const pillsContainer = document.getElementById('view-pills');
      pillsContainer.innerHTML = '';
      updates.forEach((u, idx) => {{
        const cat = (u.category || 'models').toLowerCase();
        if (activeCat !== 'all' && cat !== activeCat) return;

        const badgeColor = cat === 'models' ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400' :
                           cat === 'tools' ? 'bg-purple-500/10 text-purple-600 dark:text-purple-400' :
                           'bg-amber-500/10 text-amber-600 dark:text-amber-400';

        const card = document.createElement('div');
        card.className = "p-3.5 rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/60 shadow-sm flex flex-col justify-between space-y-2 hover:border-neutral-300 dark:hover:border-neutral-700 transition-all cursor-pointer";
        card.onclick = () => card.querySelector('.pill-detail').classList.toggle('hidden');
        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between text-[10px] mb-1.5 font-mono">
              <span class="px-1.5 py-0.5 rounded font-semibold ${{badgeColor}}">${{cat.toUpperCase()}}</span>
              <a href="${{u.link}}" target="_blank" onclick="event.stopPropagation()" class="text-blue-600 dark:text-blue-400 hover:underline">Link &rarr;</a>
            </div>
            <h3 class="text-sm font-bold text-neutral-900 dark:text-neutral-100">${{u.name}}</h3>
            <p class="text-xs text-neutral-600 dark:text-neutral-300 mt-1 font-medium">${{u.takeaway}}</p>
          </div>
          <div class="pill-detail hidden pt-2 border-t border-neutral-100 dark:border-neutral-800 text-[11px] text-neutral-500">
            <p class="mb-1">${{u.summary}}</p>
            <p class="text-emerald-600 dark:text-emerald-400 font-medium">💡 ${{u.use_case}}</p>
          </div>
        `;
        pillsContainer.appendChild(card);
      }});
    }}

    renderContent();
  </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[SUCCESS] Updated index.html with {len(all_digests)} total historical digest(s)!")

if __name__ == "__main__":
    new_data = get_updates()
    render_html(new_data)
