# @elizaos/plugin-opticparse

Official **ElizaOS** plugin for **OpticParse Autonomous Multimodal Vision AI Scraping** & **x402 On-Chain Micropayments**.

Allows autonomous AI agents and bots to visually scrape JavaScript-heavy, anti-bot-protected webpages without fragile CSS selectors, settling payments directly via on-chain USDC or API keys.

---

## 🚀 Capabilities

- **`OPTICPARSE_VISION_SCRAPE` Action:** Extracts structured JSON data from any URL using multimodal computer vision.
- **`x402` Machine-to-Machine Settlement:** Allows autonomous agents to pay $0.05 USDC per scrape directly via Base, Polygon, or Arbitrum with zero human intervention.

---

## 📦 Installation

```bash
npm install opticparse-eliza-plugin
# or
pnpm add opticparse-eliza-plugin
```

---

## 🤖 Usage in Character Configuration

Add the plugin directly to your Eliza character file (`character.json`):

```json
{
  "name": "WebScout",
  "plugins": ["opticparse-eliza-plugin"],
  "settings": {
    "secrets": {
      "OPTICPARSE_API_KEY": "op_live_your_key_here"
    }
  }
}
```

### Direct TypeScript Usage:

```typescript
import { opticParsePlugin } from "opticparse-eliza-plugin";

const agent = new AgentRuntime({
  plugins: [opticParsePlugin],
  // ...other runtime configs
});
```

---

## 📄 License
MIT © OpticParse Enterprise
