# Real-Time Phishing & Visual Threat Detection (TypeScript/JavaScript Tutorial)

In modern web security, checking static URL reputation blacklists is no longer enough. Hackers spin up phishing domains in minutes, steal credentials, and shut them down before blacklists can flag them. 

In this tutorial, we will learn how to build a proactive, real-time threat detection scanner using **PhishVision**, an AI-powered security API that renders target web pages using Playwright, extracts script execution logs, and uses GPT-4o vision analysis to spot brand impersonation and hidden prompt injection payloads.

We will use the official **PhishVision JavaScript/TypeScript SDK client** to run scans, retrieve forensic verdicts, and download audit reports.

---

## The Concept: Multimodal Threat Intelligence

PhishVision doesn't just check domain ratings. Instead, it:
1. Launches a secure headless browser to navigate to the target URL.
2. Analyzes page redirect chains and records all network hops.
3. Performs inline script vulnerability checks to detect skimmers or credential keyloggers.
4. Queries domain registry details (RDAP WHOIS) to calculate registration age.
5. Captures a screenshot and evaluates visual impersonation anomalies (fake login forms, low-res logos) using vision AI.
6. Returns a structured JSON verdict and a downloadable forensic PDF report.

---

## Setup & Installation

Install the client package:

```bash
npm install opticparse-js
```

### Get Your API Key
Subscribe and retrieve your free-tier key on the [RapidAPI PhishVision Listing Page](https://rapidapi.com/parastejpal987cmyk/api/phishvision).

---

## Code Example: Scanning a Suspicious Login Link

Let's write a script to evaluate a suspicious website, inspect the visual verdict, and inspect the redirect hops.

```typescript
import { PhishVisionClient } from 'opticparse-js';

// Initialize the client with your RapidAPI Key
const client = new PhishVisionClient({
  apiKey: 'YOUR_RAPIDAPI_KEY_HERE',
  useRapidApi: true
});

async function analyzeUrl(targetUrl: string) {
  console.log(`Starting security analysis for: ${targetUrl}...`);

  try {
    const report = await client.detectPhishing({
      url: targetUrl
    });

    console.log('\n--- Forensic Verdict ---');
    console.log(`Verdict: ${report.verdict.toUpperCase()}`);
    console.log(`Confidence: ${report.confidence_score_percentage}%`);
    console.log(`Impersonated Brand: ${report.impersonated_brand || 'None'}`);
    console.log(`Threat Type: ${report.threat_type}`);
    
    if (report.visual_anomalies_detected.length > 0) {
      console.log('Visual Anomalies Found:', report.visual_anomalies_detected);
    }
    
    if (report.hidden_payload_detected) {
      console.log(`AI Agent Attack Vector Found: ${report.hidden_payload_detected}`);
    }

  } catch (error) {
    console.error('Forensic scan failed:', error);
  }
}

// Run a check on an example domain
analyzeUrl('https://suspicious-login-portal-microsoft.com');
```

### Sample JSON Verdict Output
If a malicious impersonation site is detected, PhishVision returns detailed structured metrics:

```json
{
  "verdict": "malicious",
  "confidence_score_percentage": 97,
  "impersonated_brand": "Microsoft",
  "threat_type": "brand_impersonation",
  "visual_anomalies_detected": [
    "Pixelated Microsoft logo",
    "Urgent password reset warning header",
    "Login form pointing to unverified external domain"
  ],
  "hidden_payload_detected": null,
  "domain_age_days": 4,
  "suspicious_scripts": ["obfuscated_eval_skimmer"],
  "redirect_hops": [
    "https://t.co/shortlink",
    "https://redirect-gateway.com",
    "https://suspicious-login-portal-microsoft.com"
  ]
}
```

---

## Downloading Forensic PDF Reports

To generate a PDF report showing the visual screenshot and security logs suitable for your security team, stream the report directly using the SDK:

```typescript
import * as fs from 'fs';

async function downloadReport(targetUrl: string) {
  console.log('Generating forensic audit PDF...');
  
  try {
    const pdfStream = await client.downloadForensicReport(targetUrl);
    const fileStream = fs.createWriteStream('phishvision_report.pdf');
    
    pdfStream.pipe(fileStream);
    
    fileStream.on('finish', () => {
      console.log('Forensic PDF report successfully saved as phishvision_report.pdf!');
    });
  } catch (error) {
    console.error('Failed to download PDF:', error);
  }
}

downloadReport('https://suspicious-login-portal-microsoft.com');
```

---

## Scheduled Monitoring (Slack/Discord Webhooks)

You can register dynamic watches to continuously monitor critical corporate brand pages on an hourly interval and send automatic alerts:

```typescript
async function createMonitor(brandUrl: string, slackWebhook: string) {
  const monitor = await client.createMonitor({
    url: brandUrl,
    webhook_url: slackWebhook,
    interval_minutes: 60 // Scan every hour
  });
  
  console.log(`Monitor registered successfully! ID: ${monitor.id}`);
}
```

---

## Conclusion

PhishVision bridges the gap between raw web scraping and automated visual threat intelligence. Try integrating it into your security monitoring stacks to safeguard your domains and guard your AI agents from prompt injection exploits.
