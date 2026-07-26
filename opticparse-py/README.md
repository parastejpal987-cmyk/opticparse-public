# OpticParse & PhishVision

Two production-ready AI APIs.

## Products
- **OpticParse** — Vision-based web scraper
- **PhishVision** — Visual phishing detection

## Live URLs
- Landing page: https://opticparse.com
- Dashboard: https://dashboard.opticparse.com
- Support: support@opticparse.com

## Tech Stack
- Python/FastAPI (OpticParse backend)
- Node.js/Express (PhishVision backend)
- Supabase (auth + database)
- Playwright + Browserless.io
- Cloudflare (hosting + CDN)
- Render Singapore (API servers)

## Developer Tools
- **Python SDK:** `pip install opticparse-py` (See `opticparse-py/` directory)
- **MCP Server:** Hook directly into Claude Desktop or Cursor (See `mcp_server.py`)
- **Browser Extensions:** BYOB Extractor & PhishVision Sentinel included in the repo.

## API Endpoints
- OpticParse: https://opticparse-api.onrender.com
- PhishVision: https://opticparse-api.onrender.com/api/phish-detect (Proxied)
