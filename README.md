<div align="center">
  <img src="opticparse_cover.png" alt="OpticParse Enterprise Banner" width="750"/>
  <h1>OpticParse Enterprise Developer Hub</h1>
  <p><strong>The Autonomous AI Vision Web Scraper, Continuous Threat Refinery & MCP Agent Protocol</strong></p>

  <p>
    <a href="https://opticparse.com"><img src="https://img.shields.io/badge/Website-opticparse.com-blue?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Live Website"></a>
    <a href="https://github.com/parastejpal987-cmyk/opticparse-public/stargazers"><img src="https://img.shields.io/github/stars/parastejpal987-cmyk/opticparse-public?style=for-the-badge&color=gold&logo=github" alt="GitHub Stars"></a>
    <a href="https://huggingface.co/spaces/paras9909/opticparse-universal-scraper"><img src="https://img.shields.io/badge/Hugging_Face-Live_Demo-yellow?style=for-the-badge&logo=huggingface&logoColor=white" alt="Hugging Face Demo"></a>
    <a href="https://pypi.org/project/opticparse-py/"><img src="https://img.shields.io/pypi/v/opticparse-py?style=for-the-badge&color=blue&logo=pypi&logoColor=white" alt="PyPI opticparse-py"></a>
    <a href="https://pypi.org/project/langchain-opticparse/"><img src="https://img.shields.io/pypi/v/langchain-opticparse?style=for-the-badge&color=green&logo=pypi&logoColor=white" alt="PyPI langchain-opticparse"></a>
    <a href="https://smithery.ai/server/@parastejpal987-cmyk/opticparse"><img src="https://img.shields.io/badge/Smithery_MCP-Indexed-orange?style=for-the-badge" alt="Smithery MCP"></a>
    <a href="https://github.com/marketplace/actions/phishvision-security-scanner"><img src="https://img.shields.io/badge/GitHub_Marketplace-v1.0.0_Verified-blueviolet?style=for-the-badge&logo=githubactions&logoColor=white" alt="Marketplace Action"></a>
    <a href="https://rapidapi.com/studio/"><img src="https://img.shields.io/badge/RapidAPI-5_Live_APIs-informational?style=for-the-badge&logo=rapid&logoColor=white" alt="RapidAPI"></a>
  </p>
  <p>
    <a href="https://github.com/sponsors/parastejpal987-cmyk"><img src="https://img.shields.io/badge/Sponsor_Web3-0xd458...DD27-ff69b4?style=flat&logo=ethereum&logoColor=white" alt="Web3 Sponsor"></a>
    <a href="https://github.com/parastejpal987-cmyk/opticparse-public/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
    <img src="https://img.shields.io/badge/Autonomous_x402-$0.05_USDC-purple" alt="x402 Paywall">
    <img src="https://img.shields.io/badge/Daily_Velocity-%2B1%2C250_Records%2F24h-blueviolet" alt="Velocity">
    <img src="https://img.shields.io/badge/MCP_Protocol-2024--11--05-orange" alt="MCP Protocol">
  </p>
</div>

> ⭐ **Support Open Source:** If you find OpticParse or PhishVision useful, please **give us a Star on GitHub**! It helps us maintain free edge scrapers and datasets for everyone.

---

## 📌 Overview

**OpticParse** is an edge-native, computer vision web scraper and continuous threat intelligence refinery. Operating **150 autonomous extraction pipelines** across **13 industries**, it auto-harvests **1,250+ verified intelligence records every 24 hours** at the global edge on Cloudflare Workers, R2, and D1.

Designed natively for the **Agent-to-Agent (A2A) Economy**, OpticParse provides direct **Model Context Protocol (MCP)** tools for Claude Desktop, Cursor, and autonomous AI agents to interact with structured web data without fragile CSS selector breakages.

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    OpticParse System Architecture                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│  │ 150 Scraping  │──▶│ Cloudflare   │──▶│ Cloudflare   │       │
│  │ Pipelines    │   │ Workers Edge │   │ D1 + R2 Lake │       │
│  └──────────────┘   └──────────────┘   └──────┬───────┘       │
│                                                │               │
│                    ┌───────────────────────────┼───────┐       │
│                    │        Distribution        │       │       │
│                    ▼              ▼             ▼       ▼       │
│            ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────┐  │
│            │ Kaggle   │  │ Hugging  │  │ RapidAPI │  │Ocean│  │
│            │ Hub      │  │ Face Hub │  │ Gateway  │  │ NFTs│  │
│            └──────────┘  └──────────┘  └──────────┘  └─────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Anthropic Model Context Protocol (MCP) Server for Agents │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 150-Pipeline Industry Coverage Matrix

| Industry Vertical | Active Pipelines | Core Extractions & Capabilities |
| :--- | :---: | :--- |
| **🛡️ Cybersecurity & Threat Intel** | **70** | Zero-day phishing kits, typosquats, crypto-drainers, brand impersonation |
| **🛒 E-Commerce & Retail Arbitrage** | **15** | Amazon undercut alerts, Shopify inventory snipers, price elasticity |
| **💼 B2B Growth & Lead Signals** | **45** | Executive hiring telemetry, YC startup surge, wage trends, SEC filings |
| **⚡ Finance, Crypto & DEX Arbitrage**| **20** | Liquidity pool spreads, token mint monitors, funding rate surveillance |
| **📊 TOTAL CORPUS** | **150** | **Continuous 15-minute harvesting (+1,250 records/24 hours)** |

---

## 🐍 Python & LangChain Quickstart (PyPI)

Install the official Python SDK or LangChain multi-agent toolkit:

```bash
# Core Python SDK (OpticParse AI Scraper + PhishVision)
pip install opticparse-py

# LangChain & CrewAI Tool Integration
pip install langchain-opticparse
```

### Python Agent Usage:
```python
from opticparse import OpticParse

client = OpticParse(api_key="YOUR_API_KEY")

# 1. Clean Markdown Extraction for LLM RAG pipelines
res = client.extract_markdown("https://news.ycombinator.com")
print(res["markdown"])

# 2. Autonomous Zero-Day Threat Inspection
safety = client.detect_phishing("https://suspicious-dapp-claim.xyz")
print(f"Verdict: {safety['verdict']} | Threat Score: {safety['threat_score']}/100")
```

---

## 🤖 Model Context Protocol (MCP) Integration

Connect **Claude Desktop, Cursor IDE, or AutoGen** directly to OpticParse in 1 click:

### 1. Install via Smithery
```bash
npx -y @smithery/cli install @parastejpal987-cmyk/opticparse --client claude
```

### 2. Manual Configuration (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "opticparse": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "OPTICPARSE_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### 🛠️ Exposed AI Agent Tools:
* `opticparse_scrape`: Vision-based structured data extraction from any web URL.
* `phishvision_detect`: Real-time phishing and brand impersonation heuristic scanner.
* `search_lessons`: Query indexed threat telemetry records.

---

## 📦 Master Public Datasets (Hugging Face & Kaggle)

All master datasets are public, verified, and streamable in **Apache Parquet & CSV format**:

| Dataset Name | Records | Format | Direct Access |
| :--- | :---: | :---: | :--- |
| **Master 150-Template Catalog** | `150` | `CSV / Parquet` | [Hugging Face](https://huggingface.co/datasets/paras9909/opticparse-150-template-web-corpus) / [Kaggle](https://www.kaggle.com/datasets/parastejpal/opticparse-150-template-web-corpus) |
| **PhishVision Threat Intelligence** | `70` | `CSV / Parquet` | [Hugging Face](https://huggingface.co/datasets/paras9909/opticparse-150-template-web-corpus) / [Kaggle](https://www.kaggle.com/datasets/parastejpal/opticparse-150-template-web-corpus) |
| **E-Commerce & Retail Arbitrage** | `15` | `CSV / Parquet` | [Hugging Face](https://huggingface.co/datasets/paras9909/opticparse-150-template-web-corpus) / [Kaggle](https://www.kaggle.com/datasets/parastejpal/opticparse-150-template-web-corpus) |
| **B2B Growth & Financial Signals** | `45` | `CSV / Parquet` | [Hugging Face](https://huggingface.co/datasets/paras9909/opticparse-150-template-web-corpus) / [Kaggle](https://www.kaggle.com/datasets/parastejpal/opticparse-150-template-web-corpus) |

### 💻 Load in Python (1-Line Quickstart):
```python
import pandas as pd

# Load master threat intelligence dataset
df_threat = pd.read_csv("https://opticparse.com/threat_intel_dataset.csv")
print(f"Loaded {len(df_threat)} live threat vectors")
print(df_threat.head())
```

---

## ⚡ Commercial RapidAPI Gateway

Pay-As-You-Go developer access with **sub-350ms global edge latency** at `$0.008/request`:

1. **`01-ai-web-scraper`**: Autonomous AI vision web scraper
2. **`02-dom-poisoner`**: Streaming adversarial anti-scraping tag injector
3. **`03-edge-proxy`**: Global unblockable fetcher proxy
4. **`04-rate-limit-bypasser`**: Residential edge IP rotator
5. **`05-realtime-sentiment`**: Live threat & telemetry database feed

👉 **Target Gateway URL:** `https://opticparse-rapidapi-gateway.parastejpal987.workers.dev`

---

## 🦊 Autonomous AI Agent Micropayments (HTTP 402 Machine Paywall)

For autonomous bots, multi-agent frameworks (ElizaOS, AutoGPT, CrewAI), and automated scrapers with no human in the loop, OpticParse supports **instant on-chain settlement**:

* **Price**: `$0.05 USDC` per request
* **Supported Chains**: **Polygon**, **Base**, **Arbitrum**
* **Treasury Address**: `0xd458E709e7d54fd3659EF66624A621Cde74EDD27`

### 🤖 1-Line Autonomous Agent Request:
```bash
curl -X POST https://opticparse-edge.parastejpal987.workers.dev/api/edge/scrape \
  -H "X-Payment-TxHash: <YOUR_CONFIRMED_USDC_TX_HASH>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://news.ycombinator.com"}'
```
*No account creation, no credit card, and zero KYC required.* Every verified on-chain transfer is verified cryptographically via global RPC nodes and grants immediate edge execution.

---

## 🛡️ Interactive Threat DB Directory (21 Brands)

Explore live brand safety evaluations and visual impersonation checks:
* [Google Threat Dossier](https://opticparse.com/threat-db/google.com.html)
* [PayPal Threat Dossier](https://opticparse.com/threat-db/paypal.com.html)
* [Binance Threat Dossier](https://opticparse.com/threat-db/binance.com.html)
* [Coinbase Threat Dossier](https://opticparse.com/threat-db/coinbase.com.html)
* [Amazon Threat Dossier](https://opticparse.com/threat-db/amazon.com.html)
* [Full Directory Index](https://opticparse.com/threat-db/)

---

## 🤝 Open Source & Licensing

OpticParse developer tools, client SDKs, and MCP servers are proudly released under the **MIT License**.

* **Author:** Paras Tejpal ([@parastejpal](https://github.com/parastejpal987-cmyk))
* **Official Website:** [https://opticparse.com](https://opticparse.com)
