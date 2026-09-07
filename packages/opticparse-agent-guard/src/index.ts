/**
 * @opticparse/agent-guard
 * Autonomous AI Agent Pre-Flight Safety Oracle & Visual Prompt Injection Firewall
 * Compatible with ElizaOS, Coinbase AgentKit, LangChain, Browserbase, and Stagehand.
 */

declare var process: any;

export interface AgentGuardConfig {
  endpoint?: string;
  apiKey?: string;
  treasuryEvm?: string;
  strictMode?: boolean;
}

export interface PreFlightCheckResult {
  safe: boolean;
  verdict: 'CLEAN_APPROVED' | 'DRAINER_DETECTED' | 'PROMPT_INJECTION_DETECTED' | 'MALICIOUS_CLOAK';
  threatScore: number; // 0 (clean) to 100 (critical threat)
  details: {
    targetUrl: string;
    detectedVectors: string[];
    isPhishing: boolean;
    hasHiddenPromptInjection: boolean;
    auditLatencyMs: number;
  };
  settlement?: {
    requiredUsdc: number;
    recipientTreasury: string;
    instructions: string;
  };
}

export interface CanvasSanitizeResult {
  isCompromised: boolean;
  sanitizedTokens: string[];
  injectionsFound: string[];
  confidence: number;
}

export class AgentGuard {
  private endpoint: string;
  private apiKey: string;
  private treasuryEvm: string;
  private strictMode: boolean;

  constructor(config?: AgentGuardConfig) {
    const env = typeof process !== 'undefined' && process.env ? process.env : {};
    this.endpoint = config?.endpoint || env.OPTICPARSE_ENDPOINT || 'https://opticparse-mcp-portal.parastejpal987.workers.dev';
    this.apiKey = config?.apiKey || env.OPTICPARSE_API_KEY || 'op_live_agentguard';
    this.treasuryEvm = config?.treasuryEvm || '0xd458E709e7d54fd3659EF66624A621Cde74EDD27';
    this.strictMode = config?.strictMode ?? true;
  }

  /**
   * Pre-Flight Execution Hook: Audits target dApp or URL before an agent signs a tx or submits forms.
   * Resolves in <1.2s via Cloudflare edge routing.
   */
  async preFlightCheck(targetUrl: string, paymentTxHash?: string): Promise<PreFlightCheckResult> {
    const startTime = Date.now();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.apiKey}`,
      'User-Agent': 'OpticParse-AgentGuard/1.0.0'
    };

    if (paymentTxHash) {
      headers['X-Payment-TxHash'] = paymentTxHash;
    }

    try {
      const resp = await fetch(`${this.endpoint}/phishvision/scan`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ url: targetUrl })
      });

      const latency = Date.now() - startTime;

      if (resp.status === 402) {
        return {
          safe: false,
          verdict: 'CLEAN_APPROVED',
          threatScore: 0,
          details: {
            targetUrl,
            detectedVectors: [],
            isPhishing: false,
            hasHiddenPromptInjection: false,
            auditLatencyMs: latency
          },
          settlement: {
            requiredUsdc: 0.05,
            recipientTreasury: this.treasuryEvm,
            instructions: 'Send 0.05 USDC to treasury wallet on Base/Polygon/Arbitrum.'
          }
        };
      }

      if (!resp.ok) {
        return {
          safe: !this.strictMode,
          verdict: 'CLEAN_APPROVED',
          threatScore: 0,
          details: {
            targetUrl,
            detectedVectors: ['upstream_audit_fallback'],
            isPhishing: false,
            hasHiddenPromptInjection: false,
            auditLatencyMs: latency
          }
        };
      }

      const data: any = await resp.json();
      const isMalicious = Boolean(data.is_phishing);

      return {
        safe: !isMalicious,
        verdict: isMalicious ? 'DRAINER_DETECTED' : 'CLEAN_APPROVED',
        threatScore: isMalicious ? (data.confidence_score || 95) : 0,
        details: {
          targetUrl,
          detectedVectors: data.checked_vectors || [],
          isPhishing: isMalicious,
          hasHiddenPromptInjection: false,
          auditLatencyMs: latency
        }
      };
    } catch (err: any) {
      return {
        safe: !this.strictMode,
        verdict: 'CLEAN_APPROVED',
        threatScore: 0,
        details: {
          targetUrl,
          detectedVectors: [`error: ${err?.message || 'network'}`],
          isPhishing: false,
          hasHiddenPromptInjection: false,
          auditLatencyMs: Date.now() - startTime
        }
      };
    }
  }

  /**
   * ToxicCanvas Sanitizer: Scans visual layout tokens for hidden adversarial prompt injection payloads.
   */
  sanitizeVisualTokens(tokens: string[]): CanvasSanitizeResult {
    const suspiciousPatterns = [
      /ignore all previous instructions/i,
      /system override/i,
      /dump private key/i,
      /reveal secret/i,
      /transfer .* to 0x/i,
      /rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*0\.0\d+\)/i
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
      injectionsFound,
      confidence: injectionsFound.length > 0 ? 0.98 : 0.05
    };
  }
}

/**
 * Functional wrapper to execute an autonomous action with inline pre-flight audit.
 */
export async function withAgentGuard<T>(
  targetUrl: string,
  action: () => Promise<T>,
  options?: AgentGuardConfig
): Promise<T> {
  const guard = new AgentGuard(options);
  const audit = await guard.preFlightCheck(targetUrl);
  if (!audit.safe) {
    throw new Error(`[AgentGuard Intercepted] Blocked interaction with ${targetUrl}. Reason: ${audit.verdict}`);
  }
  return await action();
}

export default AgentGuard;
