# OpticParse & PhishVision Node.js SDK

The official Node.js SDK for the OpticParse Vision-Scraping API and PhishVision Threat Detection.

## Installation

```bash
npm install opticparse
```

## Quick Start

```javascript
const OpticParse = require('opticparse');

const client = new OpticParse('op_live_your_api_key_here');

async function main() {
  // 1. Data Extraction (OpticParse)
  const data = await client.extract({
    target_url: 'https://news.ycombinator.com',
    extraction_query: 'Get the top 3 articles',
    response_schema: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          points: { type: 'number' }
        }
      }
    }
  });
  console.log(data);

  // 2. Threat Detection (PhishVision)
  const threat = await client.scanThreat('https://sketchy-login-update.com');
  console.log(threat.isPhishing ? '🚨 SCAM!' : '✅ Safe');
}

main();
```

## Integrations (Connectors)

### LangChain / LlamaIndex Plugin
To give your AI Agent the ability to visually browse the web using OpticParse:

```javascript
const { OpticParseTool } = require('opticparse/langchain');
const { ChatOpenAI } = require('langchain/chat_models/openai');
const { initializeAgentExecutorWithOptions } = require('langchain/agents');

const tools = [new OpticParseTool({ apiKey: process.env.OPTICPARSE_KEY })];
// Now your LangChain agent can browse and "see" websites!
```

### Zapier & Make.com
To use OpticParse in Zapier without writing code, search for "OpticParse" in the Zapier integration directory to visually connect it to Google Sheets, Slack, and thousands of other apps.
