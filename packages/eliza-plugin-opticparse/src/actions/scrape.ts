export const opticParseScrapeAction = {
  name: 'OPTICPARSE_VISION_SCRAPE',
  similars: ['SCRAPE_WEBSITE', 'EXTRACT_DATA', 'VISUAL_SCRAPE'],
  description: 'Extracts structured JSON from any website using OpticParse Vision AI and autonomous x402 micropayments',
  validate: async (runtime: any, message: any) => {
    return !!message.content.text;
  },
  handler: async (runtime: any, message: any, state: any, options: any, callback: any) => {
    const targetUrl = options.url || 'https://news.ycombinator.com';
    const query = options.query || 'Extract main content and structured data';
    const txHash = options.paymentTxHash || runtime.getSetting('OPTICPARSE_PX_HASH');
    const apiKey = runtime.getSetting('OPTICPARSE_API_KEY') || 'op_live_eliza_agent';

    const endpoint = runtime.getSetting('OPTICPARSE_ENDPOINT') || 'https://opticparse-mcp-portal.parastejpal987.workers.dev/mcp/tools/opticparse_extract';

    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'X-Payment-TxHash': txHash || ''
      },
      body: JSON.stringify({ url: targetUrl, query })
    });

    const data = await resp.json();
    if (callback) {
      callback({ text: JSON.stringify(data, null, 2) });
    }
    return data;
  }
};

