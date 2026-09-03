from typing import Optional, Type, Any, Dict
from pydantic import BaseModel, Field
import os
import requests

class OpticParseInput(BaseModel):
    url: str = Field(..., description="The live webpage URL to visually scrape and extract.")
    query: str = Field(
        default="Extract all main content, pricing, specifications, and structured data.",
        description="Natural language instruction of what information to extract from the webpage."
    )

class PhishVisionInput(BaseModel):
    url: str = Field(..., description="The target domain or URL to inspect for zero-day phishing kits, brand impersonations, and crypto wallet drainers.")

class OpticParseTool:
    """
    OpticParse Autonomous Multimodal Vision Web Scraper Tool for LangChain & CrewAI.
    Visually parses live websites via Cloudflare Edge AI & Playwright without fragile CSS selectors.
    """
    name: str = "opticparse_vision_scrape"
    description: str = (
        "A stealth multimodal visual web scraper. Use this tool when you need to extract structured data, "
        "pricing, articles, or real-time information from any webpage without breaking on layout changes or anti-bot challenges."
    )
    args_schema: Type[BaseModel] = OpticParseInput

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPTICPARSE_API_KEY", "op_live_langchain_agent")
        self.endpoint = endpoint or os.getenv("OPTICPARSE_ENDPOINT", "https://opticparse-mcp-portal.parastejpal987.workers.dev")

    def _run(self, url: str, query: str = "Extract structured data.") -> Dict[str, Any]:
        target_endpoint = f"{self.endpoint}/mcp/tools/opticparse_extract"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "LangChain-OpticParse/1.0"
        }
        payload = {"url": url, "query": query}
        try:
            res = requests.post(target_endpoint, json=payload, headers=headers, timeout=30)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            return {"status": "error", "message": f"OpticParse scrape failed: {str(e)}"}

    async def _arun(self, url: str, query: str = "Extract structured data.") -> Dict[str, Any]:
        return self._run(url=url, query=query)


class PhishVisionTool:
    """
    PhishVision Zero-Day Cybersecurity & Crypto Drainer Scanner Tool for LangChain & CrewAI.
    """
    name: str = "phishvision_threat_detect"
    description: str = (
        "A real-time zero-day cybersecurity threat scanner. Use this tool before visiting, clicking, or interacting "
        "with unknown domains, Web3 crypto dApps, or suspicious links to detect wallet-drainers and credential harvesting kits."
    )
    args_schema: Type[BaseModel] = PhishVisionInput

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPTICPARSE_API_KEY", "op_live_langchain_agent")
        self.endpoint = endpoint or os.getenv("OPTICPARSE_ENDPOINT", "https://opticparse-mcp-portal.parastejpal987.workers.dev")

    def _run(self, url: str) -> Dict[str, Any]:
        target_endpoint = f"{self.endpoint}/phishvision/scan"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "LangChain-PhishVision/1.0"
        }
        payload = {"url": url}
        try:
            res = requests.post(target_endpoint, json=payload, headers=headers, timeout=15)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            return {"status": "error", "message": f"PhishVision detection failed: {str(e)}"}

    async def _arun(self, url: str) -> Dict[str, Any]:
        return self._run(url=url)
