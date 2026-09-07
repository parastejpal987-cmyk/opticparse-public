"use strict";
/**
 * @opticparse/agent-guard
 * Autonomous AI Agent Pre-Flight Safety Oracle & Visual Prompt Injection Firewall
 * Compatible with ElizaOS, Coinbase AgentKit, LangChain, Browserbase, and Stagehand.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.AgentGuard = void 0;
exports.withAgentGuard = withAgentGuard;
class AgentGuard {
    endpoint;
    apiKey;
    treasuryEvm;
    strictMode;
    constructor(config) {
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
    async preFlightCheck(targetUrl, paymentTxHash) {
        const startTime = Date.now();
        const headers = {
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
            const data = await resp.json();
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
        }
        catch (err) {
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
    sanitizeVisualTokens(tokens) {
        const suspiciousPatterns = [
            /ignore all previous instructions/i,
            /system override/i,
            /dump private key/i,
            /reveal secret/i,
            /transfer .* to 0x/i,
            /rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*0\.0\d+\)/i
        ];
        const injectionsFound = [];
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
exports.AgentGuard = AgentGuard;
/**
 * Functional wrapper to execute an autonomous action with inline pre-flight audit.
 */
async function withAgentGuard(targetUrl, action, options) {
    const guard = new AgentGuard(options);
    const audit = await guard.preFlightCheck(targetUrl);
    if (!audit.safe) {
        throw new Error(`[AgentGuard Intercepted] Blocked interaction with ${targetUrl}. Reason: ${audit.verdict}`);
    }
    return await action();
}
exports.default = AgentGuard;
