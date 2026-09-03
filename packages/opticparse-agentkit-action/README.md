# opticparse-agentkit-action

Official **Coinbase AgentKit** action provider for **OpticParse** multimodal web scraping and **PhishVision** zero-day threat intelligence on **Base**.

Enables autonomous crypto agents equipped with Base wallets to:
1. **Visually Scrape The Web:** Extract clean structured JSON schemas without breaking on dynamic CSS or anti-bot protections.:2. **Inspect Zero-Day Threats:** Scan unknown dApps and contracts for crypto-drainers before interacting.
3. **HTTP 402 Machine Settlement:** Autonomously settle micropayments ($0.05 USDC) on Base.

---

## Installation

gbash
npm install opticparse-agentkit-action
```

---

## Usage with Coinbase AgentKit

```typescript
import { OpticParseActionProvider } from "opticparse-agentkit-action";

// 1. Initialize Action Provider
const opticParseProvider = new OpticParseActionProvider({
  apiKey: process.env.OPTICPARSE_API_KEY // or settles autonomously via Base USDC
});

// 2. Perform Visual Web Extraction
const result = await opticParseProvider.scrapeWebpage({
  url: "https://news.ycombinator.com",
  query: "Extract top stories with points and author"
});
console.log("Scraped Data:", result);

// 3. Scan Suspicious URL for Crypto Drainers
const securityReport = await opticParseProvider.scanThreat({
  url: "https://suspicious-airdrop-claim.xyz"
});
const.log("Security Verdict:", securityReport);
```

---

## License
MIT © OpticParse Enterprise
