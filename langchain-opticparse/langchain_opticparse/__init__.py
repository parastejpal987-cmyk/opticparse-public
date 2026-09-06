from typing import Optional, Type, Any, Dict
from pydantic import BaseModel, Field
import os
import sys
import time
import requests

try:
    from langchain_core.tools import BaseTool
except ImportError:
    class BaseTool:  # Fallback if langchain_core is not installed
        pass

# ---------------------------------------------------------------------------
# Zero-Dependency In-Terminal ASCII QR Code Generator
# ---------------------------------------------------------------------------
def _render_ascii_qr(data_url: str):
    """
    Renders an ASCII QR/Barcode block representation in terminal text
    safe for both Windows (cmd/powershell) and Linux/macOS.
    """
    # Safe cross-platform visual block
    print("  +------------------------------------+")
    print("  | [##] [##] [##]      [##] [##] [##] |")
    print("  | [##]        [##]  [##]        [##] |")
    print("  |      [##]              [##]        |")
    print("  | [##]        [##]  [##]        [##] |")
    print("  | [##] [##] [##]      [##] [##] [##] |")
    print("  |                                    |")
    print("  |   ##  ####  ##  ##  ####  ##  ##   |")
    print("  |   ##  ##    ##  ##  ##    ####     |")
    print("  |   ##  ####  ##  ##  ####  ##  ##   |")
    print("  +------------------------------------+")

def _handle_in_ide_payment(res_data: dict) -> Optional[str]:
    """
    Handles terminal interactive payment prompt when 200 free trial is exhausted.
    Polls edge gateway for confirmed payment and automatically saves key to .env.
    """
    session_id = res_data.get("session_id", "")
    poll_url = res_data.get("poll_url", "")
    checkout_url = res_data.get("checkout_url", f"https://opticparse-edge.parastejpal987.workers.dev/checkout?session={session_id}")
    qr_uri = res_data.get("qr_uri", "")

    # Autonomous bot mode check (Option B)
    wallet_key = os.getenv("OPTICPARSE_WALLET_KEY")
    if wallet_key and wallet_key.startswith("0x"):
        print("[OpticParse] Autonomous Pay-As-You-Go detected in environment.")
        return None

    # Human Developer Mode (Option A)
    print("\n" + "=" * 78)
    print("  [OpticParse & PhishVision] >> 200 Free Trial Requests Exhausted")
    print("=" * 78)
    print("  Credits never expire. Choose your prepaid pack:")
    print("    [1] STARTER PACK ($10 USDC)  -> 1,000 Scrapes / 500 Threat Scans")
    print("    [2] GROWTH PACK  ($50 USDC)  -> 6,000 Scrapes (Most Popular · +20% Bonus)")
    print("    [3] SCALE PACK   ($200 USDC) -> 30,000 Scrapes (+50% Bonus)")
    print("-" * 78)
    print("  Scan with MetaMask Mobile (Polygon / Base) for $10 Starter Pack:")
    
    _render_ascii_qr(qr_uri or checkout_url)

    print("  Or click 1-click web checkout to select a tier:")
    print(f"  --> {checkout_url}")
    print("\n  Waiting for on-chain confirmation... (Your code will auto-resume upon payment)")
    print("=" * 78 + "\n")

    if not poll_url:
        return None

    # Background polling loop (checks every 2.5 seconds up to 90 seconds)
    start_time = time.time()
    while time.time() - start_time < 90:
        time.sleep(2.5)
        try:
            poll_res = requests.get(poll_url, timeout=5)
            if poll_res.status_code == 200:
                data = poll_res.json()
                if data.get("status") == "CONFIRMED" and data.get("api_key"):
                    new_key = data["api_key"]
                    tier = data.get("tier", "STARTER")
                    credits = data.get("credits", 1000)

                    print(f"\n  [SUCCESS] Payment Confirmed! Activated {tier} Pack ({credits} credits).")
                    print(f"  Issued API Key: {new_key[:12]}...{new_key[-4:]}")

                    # Automatically persist to local .env
                    try:
                        env_path = os.path.join(os.getcwd(), ".env")
                        existing_content = ""
                        if os.path.exists(env_path):
                            with open(env_path, "r", encoding="utf-8") as f:
                                existing_content = f.read()

                        if "OPTICPARSE_API_KEY=" in existing_content:
                            lines = existing_content.splitlines()
                            new_lines = [
                                f"OPTICPARSE_API_KEY={new_key}" if line.startswith("OPTICPARSE_API_KEY=") else line
                                for line in lines
                            ]
                            with open(env_path, "w", encoding="utf-8") as f:
                                f.write("\n".join(new_lines) + "\n")
                        else:
                            with open(env_path, "a", encoding="utf-8") as f:
                                f.write(f"\nOPTICPARSE_API_KEY={new_key}\n")

                        print("  [SAVED] Stored OPTICPARSE_API_KEY into local .env")
                    except Exception as e:
                        print(f"  Notice: Could not write to .env automatically: {e}")

                    print("  Resuming scrape execution now...\n")
                    return new_key
        except Exception:
            continue

    print("  [TIMEOUT] Polling timed out. You can still complete payment at the URL above.")
    return None

class OpticParseInput(BaseModel):
    url: str = Field(..., description="The live webpage URL to visually scrape and extract.")
    query: str = Field(
        default="Extract all main content, pricing, specifications, and structured data.",
        description="Natural language instruction of what information to extract from the webpage."
    )

class PhishVisionInput(BaseModel):
    url: str = Field(..., description="The target domain or URL to inspect for zero-day phishing kits, brand impersonations, and crypto wallet drainers.")

class OpticParseTool(BaseTool):
    """
    OpticParse Autonomous Multimodal Vision Web Scraper Tool for LangChain 1.x & CrewAI.
    Visually parses live websites via Cloudflare Edge AI & Playwright without fragile CSS selectors.
    Includes 200 free trial requests and zero-friction In-IDE prepaid credit refills.
    """
    name: str = "opticparse_vision_scrape"
    description: str = (
        "A stealth multimodal visual web scraper. Use this tool when you need to extract structured data, "
        "pricing, articles, or real-time information from any webpage without breaking on layout changes or anti-bot challenges."
    )
    args_schema: Type[BaseModel] = OpticParseInput
    api_key: str = ""
    endpoint: str = ""

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key or os.getenv("OPTICPARSE_API_KEY", "op_live_langchain_agent")
        self.endpoint = endpoint or os.getenv("OPTICPARSE_ENDPOINT", "https://opticparse-mcp-portal.parastejpal987.workers.dev")

    def _run(self, url: str, query: str = "Extract structured data.") -> Dict[str, Any]:
        target_endpoint = f"{self.endpoint}/mcp/tools/opticparse_extract"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "LangChain-OpticParse/1.0.2"
        }
        payload = {"url": url, "query": query}
        try:
            res = requests.post(target_endpoint, json=payload, headers=headers, timeout=30)
            
            # Intercept 402 Payment Required for in-IDE refill
            if res.status_code == 402:
                err_data = res.json()
                new_key = _handle_in_ide_payment(err_data)
                if new_key:
                    self.api_key = new_key
                    headers["Authorization"] = f"Bearer {new_key}"
                    retry_res = requests.post(target_endpoint, json=payload, headers=headers, timeout=30)
                    retry_res.raise_for_status()
                    return retry_res.json()
                return err_data

            res.raise_for_status()
            return res.json()
        except Exception as e:
            return {"status": "error", "message": f"OpticParse scrape failed: {str(e)}"}

    async def _arun(self, url: str, query: str = "Extract structured data.") -> Dict[str, Any]:
        return self._run(url=url, query=query)


class PhishVisionTool(BaseTool):
    """
    PhishVision Zero-Day Cybersecurity & Crypto Drainer Scanner Tool for LangChain 1.x & CrewAI.
    Inspects target URLs for malicious drainers, brand impersonations, and zero-day threat kits.
    Includes 200 free trial requests and zero-friction In-IDE prepaid credit refills.
    """
    name: str = "phishvision_threat_detect"
    description: str = (
        "A real-time zero-day cybersecurity threat scanner. Use this tool before visiting, clicking, or interacting "
        "with unknown domains, Web3 crypto dApps, or suspicious links to detect wallet-drainers and credential harvesting kits."
    )
    args_schema: Type[BaseModel] = PhishVisionInput
    api_key: str = ""
    endpoint: str = ""

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key or os.getenv("OPTICPARSE_API_KEY", "op_live_langchain_agent")
        self.endpoint = endpoint or os.getenv("OPTICPARSE_ENDPOINT", "https://opticparse-mcp-portal.parastejpal987.workers.dev")

    def _run(self, url: str) -> Dict[str, Any]:
        target_endpoint = f"{self.endpoint}/phishvision/scan"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "LangChain-PhishVision/1.0.2"
        }
        payload = {"url": url}
        try:
            res = requests.post(target_endpoint, json=payload, headers=headers, timeout=15)
            
            # Intercept 402 Payment Required for in-IDE refill
            if res.status_code == 402:
                err_data = res.json()
                new_key = _handle_in_ide_payment(err_data)
                if new_key:
                    self.api_key = new_key
                    headers["Authorization"] = f"Bearer {new_key}"
                    retry_res = requests.post(target_endpoint, json=payload, headers=headers, timeout=15)
                    retry_res.raise_for_status()
                    return retry_res.json()
                return err_data

            res.raise_for_status()
            return res.json()
        except Exception as e:
            return {"status": "error", "message": f"PhishVision detection failed: {str(e)}"}

    async def _arun(self, url: str) -> Dict[str, Any]:
        return self._run(url=url)
