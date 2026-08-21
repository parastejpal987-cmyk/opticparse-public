import httpx
from typing import Optional, Dict, Any

class OpticParse:
    def __init__(self, api_key: str, base_url: str = "https://opticparse.parastejpal987.workers.dev"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(
            headers={
                "X-API-Key": self.api_key,
                "Content-Type": "application/json",
                "User-Agent": "OpticParse-Python-SDK/0.2.0"
            },
            timeout=120.0
        )

    def scrape(self, target_url: str, extraction_query: str, response_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract structured data from a webpage using AI Vision scraping.
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

    def scrape_with_template(self, target_url: str, template_id: str) -> Dict[str, Any]:
        """
        Extract structured data using one of the 150 pre-built enterprise templates.
        """
        payload = {
            "target_url": target_url,
            "template_id": template_id
        }
        r = self.client.post(f"{self.base_url}/api/vision-scrape", json=payload)
        r.raise_for_status()
        return r.json()

    def detect_phishing(self, url: str) -> Dict[str, Any]:
        """
        Analyze a webpage for phishing threat markers, brand impersonation, and JS skimmers.
        """
        payload = {"url": url}
        r = self.client.post(f"{self.base_url}/api/phish-detect", json=payload)
        r.raise_for_status()
        return r.json()

    def get_phishing_report(self, url: str) -> bytes:
        """
        Get the binary content of the forensic PDF threat report.
        """
        r = self.client.get(f"{self.base_url}/api/phish-report", params={"url": url})
        r.raise_for_status()
        return r.content
