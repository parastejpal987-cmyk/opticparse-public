/**
 * Coinbase AgentKit Action Provider for OpticParse
 * Enables autonomous on-chain agents on Base to perform visual web scraping
 * and zero-day threat detection via HTTP 402 / USDC settlement.
 */

declare var process: any;

export interface OpticParseScrapeParams {
  url: string;
  query?: string;
  paymentTxHash?: string;
}

export interface PhishVisionScanParams {
  url: string;
}

export class OpticParseActionProvider {
  private endpoint: string;
  private apiKey: string;
  private treasuryEvm: string;

  constructor(options?: { endpoint?: string; apiKey?: string; treasuryEvm?: string }) {
    const env = typeof process !== 'undefined' && process.env ? process.env : {};
    this.endpoint = options?.endpoint || env.OPTICPARSE_ENDPOINT || 'https://opticparse-mcp-portal.parastejpal987.workers.dev';
    this.apiKey = options?.apiKey || env.OPTICPARSE_API_KEY || 'op_live_agentkit';
    this.treasuryEvm = options?.treasuryEvm || '0xd458E709e7d54fd3659EF66624A621Cde74EDD27';
  }

  /**
   * Scrapes structured JSON from any URL without breaking on CSS changes or anti-bot checks.
   */
  async scrapeWebpage(args: OpticParseScrapeParams): Promise<any> {
    const targetUrl = args.url;
    const query = args.query || 'Extract structured data, pricing, and main content';
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.apiKey}`,
      'User-Agent': 'Coinbase-AgentKit-OpticParse/1.0'
    };

    if (args.paymentTxHash) {
      headers['X-Payment-TxHash'] = args.paymentTxHash;
    }

    const targetEndpoint = this.endpoint + '/mcp/tools/opticparse_extract';
    const response = await fetch(targetEndpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify({ url: targetUrl, query })
    });

    if (response.status === 402) {
      return {
        status: 'payment_required',
        code: 402,
        required_amount_usdc: 0.05,
        recipient_treasury: this.treasuryEvm,
        accepted_chain: 'base',
        instructions: 'Transfer 0.05 USDC on Base to recipient_treasury and pass paymentTxHash in parameters.'
      };
    }

    return await response.json();
  }

  /**
   * Inspects a URL for malicious crypto drainers, zero-day phishing kits, or brand impersonations.
   */
  async scanThreat(args: PhishVisionScanParams): Promise<any> {
    const scanEndpoint = this.endpoint + '/phishvision/scan';
    const response = await fetch(scanEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({ url: args.url })
    });

    return await response.json();
  }
}

export default OpticParseActionProvider;
