/**
 * @opticparse/agent-guard
 * Autonomous AI Agent Pre-Flight Safety Oracle & Visual Prompt Injection Firewall
 * Compatible with ElizaOS, Coinbase AgentKit, LangChain, Browserbase, and Stagehand.
 */
export interface AgentGuardConfig {
    endpoint?: string;
    apiKey?: string;
    treasuryEvm?: string;
    strictMode?: boolean;
}
export interface PreFlightCheckResult {
    safe: boolean;
    verdict: 'CLEAN_APPROVED' | 'DRAINER_DETECTED' | 'PROMPT_INJECTION_DETECTED' | 'MALICIOUS_CLOAK';
    threatScore: number;
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
export declare class AgentGuard {
    private endpoint;
    private apiKey;
    private treasuryEvm;
    private strictMode;
    constructor(config?: AgentGuardConfig);
    /**
     * Pre-Flight Execution Hook: Audits target dApp or URL before an agent signs a tx or submits forms.
     * Resolves in <1.2s via Cloudflare edge routing.
     */
    preFlightCheck(targetUrl: string, paymentTxHash?: string): Promise<PreFlightCheckResult>;
    /**
     * ToxicCanvas Sanitizer: Scans visual layout tokens for hidden adversarial prompt injection payloads.
     */
    sanitizeVisualTokens(tokens: string[]): CanvasSanitizeResult;
}
/**
 * Functional wrapper to execute an autonomous action with inline pre-flight audit.
 */
export declare function withAgentGuard<T>(targetUrl: string, action: () => Promise<T>, options?: AgentGuardConfig): Promise<T>;
export default AgentGuard;
