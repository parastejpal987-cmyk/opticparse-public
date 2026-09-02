<div align="center">
  <h1>⚡ OpticParse Developer Hub</h1>
  <p><strong>The Multimodal AI Web Scraper, Continuous Threat Refinery & MCP Agent Protocol</strong></p>

  <p>
    <a href="https://opticparse.com"><img src="https://img.shields.io/badge/Website-opticparse.com-blue?style=flat-square&logo=googlechrome&logoColor=white" alt="Live Website"></a>
    <a href="https://github.com/parastejpal987-cmyk/opticparse-public/actions/workflows/test.yml"><img src="https://img.shields.io/badge/Tests-Passing-brightgreen?style=flat-square&logo=githubactions&logoColor=white" alt="Tests"></a>
    <a href="https://www.kaggle.com/code/parastejpal/opticparse-full-system-benchmark"><img src="https://img.shields.io/badge/Kaggle_Audit-100%25_Verified-20BEFF?style=flat-square&logo=kaggle&logoColor=white" alt="Kaggle Benchmark"></a>
    <a href="https://huggingface.co/datasets/paras9909/opticparse-150-template-web-corpus"><img src="https://img.shields.io/badge/Hugging_Face-Master_Corpus-yellow?style=flat-square&logo=huggingface&logoColor=white" alt="Hugging Face Dataset"></a>
    <a href="https://pypi.org/project/opticparse-py/"><img src="https://img.shields.io/pypi/v/opticparse-py.svg?style=flat-square" alt="PyPI version"></a>
    <a href="https://github.com/parastejpal987-cmyk/opticparse-public/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License: MIT"></a>
  </p>
  <p>
    <a href="https://opticparse.com/api-docs.html"><b>📖 Live API Docs</b></a> •
    <a href="https://opticparse.com/threat-db/"><b>🛡️ Threat Intelligence DB</b></a> •
    <a href="TEMPLATES.md"><b>📚 150 Extraction Templates</b></a> •
    <a href="INSIGHTS.md"><b>📊 Live Insights</b></a> •
    <a href="https://rapidapi.com/studio/"><b>⚡ RapidAPI Hub</b></a>
  </p>
</div>

---

## ⚡ What is OpticParse?

**OpticParse** is a multimodal AI scraping, visual extraction, and security threat detection suite engineered for modern developers and autonomous AI agents. Unlike legacy scrapers that rely on fragile CSS selectors or break on Cloudflare Turnstile, OpticParse uses **Computer Vision heuristics, headless Playwright rendering, and multi-model routing** to extract clean, structured JSON from any webpage on Earth.

This repository contains the open-source client SDKs, Model Context Protocol (MCP) server, Chrome extensions, and developer tooling.

```
                     ┌──────────────────────────────────────────────┐
                     │           DEVELOPER INTEGRATIONS            │
                     │  • Python SDK (opticparse-py)                │
                     │  • MCP Server (Claude, Cursor, Windsurf)     │
                     │  • RapidAPI 5-Endpoint Gateway               │
                     │  • PhishVision Chrome Extension              │
                     └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │          CLOUDFLARE EDGE GATEWAY             │
                     │  • Global Anycast (285+ cities)              │
                     │  • 150 Pre-Built Extraction Templates        │
                     │  • Sub-second Semantic KV Cache              │
                     └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │          VISION & ENGINE CLUSTER             │
                     │  • Visual Heuristic Phishing Detection       │
                     │  • Dynamic JS & Anti-Bot Bypass              │
                     │  • Forensic Threat Report Synthesis          │
                     └──────────────────────────────────────────────┘
```

---

## 🚀 4 Ways to Integrate

Choose the workflow that fits your stack:

### 1. 🐍 Python SDK (`opticparse-py`)
Install the official Python client:
```bash
pip install opticparse-py
```

```python
from opticparse import OpticParse

# Initialize with your API key
client = OpticParse(api_key="your_api_key_here")

# 1. Vision Scrape: Extract structured data from any webpage
data = client.scrape(
    target_url="https://news.ycombinator.com",
    extraction_query="Extract top 5 stories with title, url, points, and author as JSON"
)
print(data)

# 2. Template Scrape: Use any of our 150 pre-built enterprise templates
products = client.scrape_with_template(
    target_url="https://amazon.com/dp/B08N5WRWNW",
    template_id="amazon-price-undercut-alert"
)

# 3. PhishVision: Analyze URL for zero-day phishing, brand spoofing & malware
threat = client.detect_phishing("https://suspect-banking-login.com")
print(f"Verdict: {threat['verdict']} | Score: {threat['score']}/100")
```

---

### 2. 🤖 Model Context Protocol (MCP for AI Agents)
Connect **Claude Desktop**, **Cursor IDE**, **Windsurf**, or any MCP-compatible agent directly to the live web.

#### Install via Smithery:
```bash
npx @smithery/cli install @parastejpal987-cmyk/opticparse-public --client claude
```

#### Manual Claude Desktop / Cursor Config (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "opticparse": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "OPTICPARSE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Supported MCP Tools:**
* `opticparse_scrape`: Autonomous AI vision web scraping and schema enforcement.
* `phishvision_detect`: Real-time threat, brand impersonation, and JS skimmer analysis.
* `search_lessons`: Query indexed threat telemetry records.

---

### 3. 🌐 REST API & RapidAPI Hub
For teams preferring REST / OpenAPI integration with unified Pay-As-You-Go billing at `$0.008/request`:

* **Live Gateway Base URL:** `https://opticparse-rapidapi-gateway.parastejpal987.workers.dev`
* **Direct cURL Example:**
```bash
curl -X POST https://opticparse-rapidapi-gateway.parastejpal987.workers.dev/scrape \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "target_url": "https://example.com",
    "extraction_query": "Extract the main heading, summary paragraph, and all navigation links"
  }'
```

**Available Endpoints:**
1. `POST /scrape`: Autonomous AI vision scraper
2. `POST /api/extract/markdown`: Noise-stripped HTML-to-Markdown parser (RAG token-optimized)
3. `POST /api/agent/interact`: Interactive browser action sequence engine (click, type, scroll)
4. `WSS /ws/threat-stream`: Real-time 24/7 zero-day WebSocket security stream
5. `POST /poison`: Streaming adversarial anti-scraping tag injector
6. `GET /proxy?url=...`: Global unblockable fetcher proxy
7. `GET /sentiment`: Real-time threat & telemetry database feed

---

### 4. 📄 Clean Markdown & RAG Parser (Token-Optimized)
AI engineers building LLM chatbots and retrieval pipelines can strip noisy headers, footers, cookie banners, and navigation menus with one API call:

```bash
curl -X POST https://opticparse-api.onrender.com/api/extract/markdown \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "url": "https://example.com/article",
    "include_images": false,
    "include_links": true
  }'
```

Returns clean Markdown with token estimation and word count.

---

### 5. 🤖 Interactive "Browser-Use" Agent Actions
Instruct our Playwright vision engine to click buttons, fill forms, and paginate dynamically before extracting the final result:

```bash
curl -X POST https://opticparse-api.onrender.com/api/agent/interact \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "target_url": "https://example.com/search",
    "actions": [
      {"action": "type", "selector": "#search-bar", "text": "AI research papers"},
      {"action": "click", "selector": "#submit-btn"},
      {"action": "wait", "delay_ms": 1000}
    ],
    "final_query": "Extract search result titles and authors"
  }'
```

---

### 6. ⚡ Live Zero-Day WebSocket Threat Feed
Subscribe to real-time broadcasts of newly discovered crypto drainers, typosquatting domains, and credential harvesters:

```python
import asyncio
import websockets
import json

async def stream_threats():
    async with websockets.connect("wss://opticparse-api.onrender.com/ws/threat-stream") as ws:
        print("Connected to PhishVision Live Sentinel Stream...")
        while True:
            alert = await ws.recv()
            print("Threat Alert:", json.loads(alert))

asyncio.run(stream_threats())
```

---

### 4. 🧩 Chrome Extensions
* **PhishVision Sentinel**: Real-time visual threat detector that protects users against zero-day phishing, credential harvesters, and malicious redirects.
* **BYOB Extractor**: Local DOM & screenshot capture extension for extracting data using your own authenticated session.

---

## 📚 150 Pre-Built Extraction Templates

OpticParse includes **150 production-grade extraction templates** across 13 industries, ready to invoke without writing custom parsers:

| Category | Templates | Sample Templates |
| :--- | :--- | :--- |
| 🛒 **E-Commerce & Retail** | 15 | `amazon-price-undercut-alert`, `shopify-new-product-alert`, `flipkart-flash-sale-auto-cart` |
| 🏢 **Real Estate** | 10 | `zillow-rent-estimate-aggregator`, `airbnb-pricing-spy`, `foreclosure-auction-monitor` |
| 💼 **B2B & Lead Gen** | 15 | `product-hunt-maker-extractor`, `hiring-signal-aggregator`, `yc-founder-scraper` |
| 📊 **Finance & Crypto** | 10 | `crypto-exchange-arbitrage`, `dex-liquidity-pool-watcher`, `sec-10k-filing-summarizer` |
| 🛡️ **PhishVision Threat Intel** | 70 | `typosquatting-auto-assassin`, `zero-day-phishing-kit-extractor`, `ransomware-leak-site-tracker` |
| 🧑‍💻 **Developer Operations** | 10 | `npm-package-vulnerability-alert`, `cve-zero-day-radar`, `docker-hub-vulnerability-alert` |

👉 **[View the Complete 150-Template Catalog in TEMPLATES.md](TEMPLATES.md)**

---

## 🛡️ PhishVision GitHub Action

Add automated prompt injection and URL threat auditing to your CI/CD workflow:

```yaml
name: Security Audit Pipeline
on: [push, pull_request]

jobs:
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run PhishVision Audit
        uses: parastejpal987-cmyk/opticparse-public@main
        with:
          target_dir: '.'
          output_dir: './audits'
```

---

## 📊 Master Datasets & Verified Benchmark

OpticParse continuously auto-feeds its AI knowledge base with verified multi-industry telemetry (+1,250 records/24 hours). Explore our open datasets and benchmarks:

* 🏆 **Kaggle 100% Verified Benchmark:** [Kaggle Full System Benchmark](https://www.kaggle.com/code/parastejpal/opticparse-full-system-benchmark)
* 🤗 **Hugging Face Master Corpus:** [Hugging Face Dataset Hub](https://huggingface.co/datasets/paras9909/opticparse-150-template-web-corpus) (Apache Parquet streaming supported)
* 📁 **Live CSV Direct Feeds:**
  * [Master 150-Template Feed Catalog](https://opticparse.com/opticparse_master_150_template_catalog.csv)
  * [PhishVision Threat Intelligence Feed](https://opticparse.com/threat_intel_dataset.csv)
  * [E-Commerce Pricing Feed](https://opticparse.com/opticparse_ecommerce_and_retail.csv)
  * [B2B Leads & Finance Feed](https://opticparse.com/opticparse_b2b_and_finance.csv)

---

## 🛡️ Interactive Threat DB Directory (21 Brands)

Explore real-time visual safety evaluations and impersonation forensics:
* [Google Threat Dossier](https://opticparse.com/threat-db/google.com.html) • [PayPal Threat Dossier](https://opticparse.com/threat-db/paypal.com.html) • [Binance Threat Dossier](https://opticparse.com/threat-db/binance.com.html) • [Coinbase Threat Dossier](https://opticparse.com/threat-db/coinbase.com.html)
* 👉 **[Full Threat DB Directory Index](https://opticparse.com/threat-db/)**

---

## 🤝 Community & Contributing

We welcome contributions to SDKs, MCP adapters, and extraction templates!
* Read our [CONTRIBUTING.md](CONTRIBUTING.md) to get started.
* Review our [SECURITY.md](SECURITY.md) for responsible disclosure.
* Track development milestones in [INSIGHTS.md](INSIGHTS.md) and [ROADMAP.md](ROADMAP.md).

---

## 📄 License
This project is open-sourced under the **[MIT License](LICENSE)**.
OpticParse & PhishVision are trademarks of the OpticParse Project.
