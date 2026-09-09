"""
OpticParse Autonomous Agent Payment & Perception Demonstration
Simulates an autonomous AI agent or physical robotic node performing an
HTTP-402 micro-payment on Base/Polygon to obtain sanitized, injection-free web data.
"""

import hashlib
import json
import time


def simulate_autonomous_loop():
    print("=" * 70)
    print("OPTICPARSE AUTONOMOUS PERCEPTION & PAYMENT DEMO")
    print("=" * 70)

    # 1. Agent discovers service via Google A2A Agent Card
    print("\n[Step 1: Agent Discovery via A2A Standard]")
    manifest_url = "https://opticparse.com/.well-known/agent.json"
    print(f"Reading Agent Card from {manifest_url}...")
    sample_manifest = {
        "name": "OpticParse Autonomous Perception Node",
        "payment": {
            "protocol": "HTTP-402",
            "currency": "USDC",
            "networks": ["base", "polygon"],
            "treasury_address": "0xd458E709e7d54fd3659EF66624A621Cde74EDD27",
            "cost_per_call": 0.01,
        },
        "capabilities": ["toxic_canvas_sanitization", "anti_bot_bypass"],
    }
    print(f"-> Discovered: {sample_manifest['name']}")
    print(
        f"-> Treasury: {sample_manifest['payment']['treasury_address']} (Network: Base)"
    )
    print(f"-> Price: {sample_manifest['payment']['cost_per_call']} USDC")

    # 2. Agent simulates calling without API key -> HTTP 402
    print("\n[Step 2: Autonomous Invoicing (HTTP 402)]")
    target_url = "https://example.com/pricing"
    print(f"Agent requests scrape for: {target_url} (No API key)")
    invoice_header = {
        "status": 402,
        "detail": "Payment Required",
        "x-payment-address": "0xd458E709e7d54fd3659EF66624A621Cde74EDD27",
        "x-payment-network": "base",
        "x-payment-amount": "0.01 USDC",
    }
    print(f"<- Server returns HTTP 402: {invoice_header}")

    # 3. Agent signs and broadcasts 0.01 USDC micro-payment on Base
    print("\n[Step 3: Autonomous On-Chain Settlement]")
    simulated_tx = "0x" + hashlib.sha256(str(time.time()).encode()).hexdigest()
    print(f"Agent signs transaction on Base...")
    print(f"-> Broadcasted TxHash: {simulated_tx}")
    print(
        "-> Sent 0.01 USDC to treasury 0xd458E709e7d54fd3659EF66624A621Cde74EDD27"
    )

    # 4. OpticParse verifies and returns sanitized data + shield headers
    print("\n[Step 4: Perception Stream & Security Shield Released]")
    response = {
        "status": "success",
        "headers": {
            "X-OpticParse-Shield": "VERIFIED-CLEAN",
            "X-OpticParse-Injections-Neutralized": "0",
            "X-OpticParse-Freshness": "realtime",
            "X-OpticParse-Discovery": "https://opticparse.com/.well-known/agent.json",
        },
        "data": {
            "url": target_url,
            "markdown": "# Example Pricing\n\n- Starter: $10/mo\n- Pro: $29/mo",
            "toxic_canvas": {
                "status": "CLEAN",
                "adversarial_elements_stripped": 0,
            },
        },
        "receipt": {
            "tx_hash": simulated_tx,
            "amount_paid": "0.01 USDC",
            "treasury": "0xd458E709e7d54fd3659EF66624A621Cde74EDD27",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
    }
    print(json.dumps(response, indent=2))
    print("\n" + "=" * 70)
    print("DEMO COMPLETE: Autonomous Loop Succeeded with Zero Human Intervention")
    print("=" * 70)


if __name__ == "__main__":
    simulate_autonomous_loop()
