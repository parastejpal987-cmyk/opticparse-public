import httpx
from typing import Optional, Dict, Any

class OpticParse:
    def __init__(self, api_key: str, base_url: str = "https://opticparse-api.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(
            headers={
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            },
            timeout=120.0
        )

    def scrape(self, target_url: str, extraction_query: str, response_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract structured data from a webpage using AI Vision.
        """
        payload = {
            "target_url": target_url,
            "extraction_query": extraction_query
        }
        if response_schema:
            payload["response_schema"] = response_schema
            
        r = self.client.post(f"{self.base_url}/api/vision-scrape", json=payload)
        r.raise_for_status()
        return r.json()

    def detect_phishing(self, url: str) -> Dict[str, Any]:
        """
        Analyze a webpage for phishing threat markers.
        """
        payload = {"url": url}
        r = self.client.post(f"{self.base_url}/api/phish-detect", json=payload)
        r.raise_for_status()
        return r.json()

    def get_phishing_report(self, url: str) -> bytes:
        """
        Get the binary content of the forensic PDF report.
        """
        r = self.client.get(f"{self.base_url}/api/phish-report", params={"url": url})
        r.raise_for_status()
        return r.content
