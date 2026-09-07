/**
 * Coinbase AgentKit Action Provider for OpticParse & PhishVision
 * Enables autonomous on-chain agents on Base to perform visual web scraping,
 * zero-day threat detection, and pre-flight transaction audits via HTTP 402 / USDC settlement.
 */

declare var process: any;

export interface OpticParseScrapeParams {
  url: string;
  query?: string;
  paymentTxHash?: string;
}

export interface PhishVisionScanParams {
  url: string;
  paymentTxHash?: string;
}

export interface PreFlightCheckParams {
  url: string;
  strictMode?: boolean;
  paymentTxHash?: string;
}

export interface PaymentRequiredResponse {
  status: 'payment_required';
  code: 402;
  required_amount_usdc: number;
  recipient_treasury: string;
  accepted_chains: string[];
  checkout_url: string;
  poll_url?: string;
  remaining_free_requests: number;
  instructions: string;
}

export interface PreFlightAuditResult {
  safe: boolean;
  verdict: 'CLEAN_APPROVED' | 'DRAINER_DETECTED' | 'PROMPT_INJECTION_DETECTED' | 'MALICIOUS_CLOAK';
  threatScore: number;
  details: {
    targetUrl: string;
    detectedVectors: string[];
    isPhishing: boolean;
    auditLatencyMs: number;
  };
  paymentInfo?: PaymentRequiredResponse;
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
   * Includes automatic 200 free trial and on-chain Base settlement instructions.
   */
  async scrapeWebpage(args: OpticParseScrapeParams): Promise<any> {
    const targetUrl = args.url;
    const query = args.query || 'Extract structured data, pricing, and main content';
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.apiKey}`,
      'User-Agent': 'Coinbase-AgentKit-OpticParse/1.0.1'
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
      let details: any = {};
      try {
        details = await response.json();
      } catch {
        // ignore
      }

      const paymentInfo: PaymentRequiredResponse = {
        status: 'payment_required',
        code: 402,
        required_amount_usdc: 0.05,
        recipient_treasury: this.treasuryEvm,
        accepted_chains: ['base', 'polygon', 'arbitrum'],
        checkout_url: details.checkout_url || 'https://opticparse-edge.parastejpal987.workers.dev/checkout',
        poll_url: details.poll_url,
        remaining_free_requests: details.remaining_free_requests ?? 0,
        instructions: 'Autonomous Agent: Transfer 0.05 USDC on Base to recipient_treasury and pass paymentTxHash. Human: Open checkout_url to activate prepaid tier pack.'
      };
      return paymentInfo;
    }

    return await response.json();
  }

  /**
   * Inspects a URL for malicious crypto drainers, zero-day phishing kits, or brand impersonations.
   */
  async scanThreat(args: PhishVisionScanParams): Promise<any> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.apiKey}`,
      'User-Agent': 'Coinbase-AgentKit-OpticParse/1.0.1'
    };

    if (args.paymentTxHash) {
      headers['X-Payment-TxHash'] = args.paymentTxHash;
    }

    const scanEndpoint = this.endpoint + '/phishvision/scan';
    const response = await fetch(scanEndpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify({ url: args.url })
    });

    if (response.status === 402) {
      let details: any = {};
      try {
        details = await response.json();
      } catch {
        // ignore
      }

      const paymentInfo: PaymentRequiredResponse = {
        status: 'payment_required',
        code: 402,
        required_amount_usdc: 0.05,
        recipient_treasury: this.treasuryEvm,
        accepted_chains: ['base', 'polygon', 'arbitrum'],
        checkout_url: details.checkout_url || 'https://opticparse-edge.parastejpal987.workers.dev/checkout',
        poll_url: details.poll_url,
        remaining_free_requests: details.remaining_free_requests ?? 0,
        instructions: 'Transfer 0.05 USDC on Base or complete checkout at checkout_url.'
      };
      return paymentInfo;
    }

    return await response.json();
  }

  /**
   * Pre-Flight Execution Oracle: Intercepts autonomous agent interactions before signing on-chain transactions.
   * Audits smart contract frontends, drainer scripts, and visual prompt injections in <1.2s.
   */
  async preFlightCheck(args: PreFlightCheckParams): Promise<PreFlightAuditResult> {
    const startTime = Date.now();
    const result = await this.scanThreat({ url: args.url, paymentTxHash: args.paymentTxHash });

    if (result && result.status === 'payment_required') {
      return {
        safe: false,
        verdict: 'CLEAN_APPROVED',
        threatScore: 0,
        details: {
          targetUrl: args.url,
          detectedVectors: [],
          isPhishing: false,
          auditLatencyMs: Date.now() - startTime
        },
        paymentInfo: result
      };
    }

    const isPhish = Boolean(result?.is_phishing);
    return {
      safe: !isPhish,
      verdict: isPhish ? 'DRAINER_DETECTED' : 'CLEAN_APPROVED',
      threatScore: isPhish ? (result?.confidence_score || 95) : 0,
      details: {
        targetUrl: args.url,
        detectedVectors: result?.checked_vectors || [],
        isPhishing: isPhish,
        auditLatencyMs: Date.now() - startTime
      }
    };
  }

  /**
   * ToxicCanvas Sanitizer: Scans visual layout tokens for hidden adversarial prompt injections.
   */
  sanitizeVisualTokens(tokens: string[]): { isCompromised: boolean; sanitizedTokens: string[]; injectionsFound: string[] } {
    const suspiciousPatterns = [
      /ignore all previous instructions/i,
      /system override/i,
      /dump private key/i,
      /reveal secret/i,
      /transfer .* to 0x/i
    ];

    const injectionsFound: string[] = [];
    const sanitizedTokens = tokens.filter(tok => {
      const match = suspiciousPatterns.some(pat => pat.test(tok));
      if (match) {
        injectionsFound.push(tok);
        return false;
      }
      return true;
    });

    return {
      isCompromised: injectionsFound.length > 0,
      sanitizedTokens,
      injectionsFound
    };
  }
}

/**
 * Inline functional guard to wrap autonomous agent actions with automated pre-flight security.
 */
export async function withAgentGuard<T>(
  targetUrl: string,
  action: () => Promise<T>,
  provider?: OpticParseActionProvider
): Promise<T> {
  const p = provider || new OpticParseActionProvider();
  const check = await p.preFlightCheck({ url: targetUrl });
  if (!check.safe) {
    throw new Error(`[OpticParse Pre-Flight Guard Intercepted] Blocked interaction with ${targetUrl}. Verdict: ${check.verdict}`);
  }
  return await action();
}

export default OpticParseActionProvider;
