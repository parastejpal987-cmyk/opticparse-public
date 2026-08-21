<div align="center">
  <img src="opticparse_cover.png" alt="OpticParse Banner" width="700"/>
  <h1>OpticParse & PhishVision Developer Hub</h1>
  <p><strong>The Next-Generation AI Vision Web Scraper, Threat Intelligence & Autonomous Agent Tooling Suite</strong></p>

  <p>
    <a href="https://pypi.org/project/opticparse-py/"><img src="https://img.shields.io/pypi/v/opticparse-py.svg?color=blue&label=PyPI%20SDK" alt="PyPI version"></a>
    <a href="https://smithery.ai/server/@parastejpal987-cmyk/opticparse-public"><img src="https://img.shields.io/badge/Smithery-MCP%20Verified-blueviolet" alt="Smithery Verified"></a>
    <a href="https://glama.ai/mcp/servers"><img src="https://img.shields.io/badge/Glama-MCP%20Connector-orange" alt="Glama MCP"></a>
    <a href="https://rapidapi.com/hub"><img src="https://img.shields.io/badge/RapidAPI-Hub%20Collection-0052CC" alt="RapidAPI Hub"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
    <a href="https://opticparse.parastejpal987.workers.dev"><img src="https://img.shields.io/badge/Edge%20API-Global%20285%2B%20Colos-success" alt="Edge Network"></a>
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
                     │  • RapidAPI Collection                       │
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

#### Manual Claude Desktop / Cursor Config (`mcpServers`):
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

---

### 3. 🌐 REST API & RapidAPI Hub
For teams preferring REST / OpenAPI integration with unified billing:

* **Interactive Sandbox & RapidAPI Collection:** [OpticParse on RapidAPI Hub](https://rapidapi.com/hub)
* **Direct cURL Example:**
```bash
curl -X POST https://opticparse.parastejpal987.workers.dev/api/vision-scrape \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "target_url": "https://example.com",
    "extraction_query": "Extract the main heading, summary paragraph, and all navigation links"
  }'
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
| 🛡️ **PhishVision Threat Intel** | 50 | `typosquatting-auto-assassin`, `zero-day-phishing-kit-extractor`, `ransomware-leak-site-tracker` |
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

## 📊 Open Datasets & Ocean Protocol Integration

OpticParse continuously auto-feeds its AI knowledge base with verified multi-industry telemetry. Explore our open datasets:
* [Master 150-Template Feed Catalog](https://opticparse.parastejpal987.workers.dev/opticparse_master_150_template_catalog.csv)
* [PhishVision Threat Intelligence Feed](https://opticparse.parastejpal987.workers.dev/threat_intel_dataset.csv)
* [E-Commerce Pricing Feed](https://opticparse.parastejpal987.workers.dev/opticparse_ecommerce_and_retail.csv)
* [B2B Leads & Finance Feed](https://opticparse.parastejpal987.workers.dev/opticparse_b2b_and_finance.csv)

---

## 🤝 Community & Contributing

We welcome contributions to SDKs, MCP adapters, and extraction templates!
* Read our [CONTRIBUTING.md](CONTRIBUTING.md) to get started.
* Review our [SECURITY.md](SECURITY.md) for responsible disclosure.

---

## 📄 License
This project is open-sourced under the **[MIT License](LICENSE)**.
OpticParse & PhishVision are trademarks of the OpticParse Project.
