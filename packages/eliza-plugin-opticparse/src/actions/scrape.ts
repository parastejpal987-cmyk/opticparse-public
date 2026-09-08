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

export const phishVisionGuardAction = {
  name: 'PHISHVISION_PREFLIGHT_GUARD',
  similars: ['CHECK_URL_SAFETY', 'SCAN_FOR_DRAINERS', 'AUDIT_CONTRACT_FRONTEND'],
  description: 'Audits any target URL for zero-day phishing kits, crypto drainers, and adversarial prompt injections before an autonomous agent interacts with it.',
  validate: async (runtime: any, message: any) => {
    return !!message.content.text;
  },
  handler: async (runtime: any, message: any, state: any, options: any, callback: any) => {
    const targetUrl = options.url || options.targetUrl;
    if (!targetUrl) {
      if (callback) callback({ text: "Error: No target URL provided for pre-flight security scan." });
      return { safe: false, error: "Missing URL" };
    }

    const apiKey = runtime.getSetting('OPTICPARSE_API_KEY') || 'op_live_eliza_agent';
    const endpoint = runtime.getSetting('PHISHVISION_ENDPOINT') || 'https://opticparse-1opticparse-node-sg.onrender.com/api/v1/scan';

    try {
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
          'User-Agent': 'ElizaOS-PhishVision-Guard/1.0.1'
        },
        body: JSON.stringify({ url: targetUrl })
      });

      const data = await resp.json();
      const isPhishing = Boolean(data?.is_phishing);
      const verdict = isPhishing ? 'DRAINER_DETECTED' : 'CLEAN_APPROVED';

      const result = {
        safe: !isPhishing,
        verdict,
        targetUrl,
        threatScore: isPhishing ? (data?.confidence_score || 95) : 0,
        details: data
      };

      if (callback) {
        const text = isPhishing
          ? `⚠️ SECURITY ALERT: ${targetUrl} was flagged as ${verdict}! Threat score: ${result.threatScore}`
          : `✅ URL Verified Safe: ${targetUrl} passed PhishVision pre-flight checks.`;
        callback({ text, content: result });
      }

      return result;
    } catch (err: any) {
      const fallback = { safe: false, verdict: 'AUDIT_FAILED', error: err?.message || 'Unknown error' };
      if (callback) callback({ text: `Pre-flight scan failed for ${targetUrl}` });
      return fallback;
    }
  }
};


