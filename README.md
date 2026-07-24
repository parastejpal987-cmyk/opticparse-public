<div align="center">
  <img src="opticparse_cover.png" alt="OpticParse Logo" width="600"/>
  <h1>OpticParse Developer Hub</h1>
  <p><strong>The Next-Generation AI Web Scraper & Threat Detection Engine</strong></p>

  <a href="https://pypi.org/project/opticparse-py/"><img src="https://img.shields.io/pypi/v/opticparse-py.svg" alt="PyPI version"></a>
  <a href="https://github.com/parastejpal987-cmyk/opticparse-public/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://opticparse-api.onrender.com/"><img src="https://img.shields.io/badge/API-Live-brightgreen" alt="API Status"></a>
</div>

## What is OpticParse?
OpticParse is a suite of developer tools that connects AI agents and backend systems to the live web. It uses Playwright, custom residential proxy routing (BYOP), and fallback LLM vision heuristics to extract structured data from any website, bypassing the toughest bot protections. 

This repository contains all the open-source developer tools, extensions, and integration logic for the OpticParse API.

## 🚀 Features
- **opticparse-py**: Official Python SDK for instant integration.
- **MCP Server**: Connect Claude Desktop or Cursor IDE directly to the live web via Model Context Protocol.
- **PhishVision Sentinel**: A lightweight Chrome extension for instant zero-day phishing detection using visual AI heuristics.
- **BYOB Extractor**: A Chrome extension that lets you use your own browser to extract data, completely evading Cloudflare and Datadome.

---

## ⚡ Quick Start (Python SDK)

To get started, you will need a free API key. [Get your API Key here](https://opticparse-api.onrender.com/).

```bash
pip install opticparse-py
```

```python
from opticparse import OpticParseClient

client = OpticParseClient(api_key="your_api_key_here")

# 1. Vision Scrape (Extracts JSON directly from screen pixels)
data = client.scrape(
    target_url="https://example.com", 
    extraction_query="Extract all product names and prices as JSON",
    vision_mode=True
)
print(data)

# 2. PhishVision Threat Detection (Hybrid Heuristic + LLM Analysis)
threat = client.detect_phishing("https://google.com")
print(f"Threat Level: {threat.verdict} (Score: {threat.score})")
```

## 🔌 Model Context Protocol (MCP)

Allow your AI coding assistants (like Cursor or Claude) to browse the web autonomously. 
Add this to your MCP configuration file:

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

---

## 🤝 Contributing
We welcome community contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on submitting pull requests, requesting features, and setting up the local development environment.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
```
