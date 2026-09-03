"""
OpticParse Python SDK v1.0.0
Enterprise-grade client for AI vision web scraping, structured extraction, and threat intelligence.
"""

from typing import Any, Dict, List, Optional, Union
import json
import time
import logging
import urllib.request
import urllib.error
import ssl

__version__ = "1.0.0"

logger = logging.getLogger("opticparse")


# ==========================================
# 🛑 Custom Exception Hierarchy
# ==========================================
class OpticParseError(Exception):
    """Base exception for all OpticParse SDK errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(OpticParseError):
    """Raised when the API key is missing, invalid, or unauthorized (HTTP 401/403)."""
    pass


class RateLimitError(OpticParseError):
    """Raised when the request rate limit or monthly quota is exceeded (HTTP 429)."""
    pass


class APIConnectionError(OpticParseError):
    """Raised when network communication with the OpticParse gateway fails."""
    pass


class TemplateNotFoundError(OpticParseError):
    """Raised when an invalid extraction template_id is requested."""
    pass


class ServerError(OpticParseError):
    """Raised when the remote edge worker returns an internal error (HTTP 5xx)."""
    pass


# ==========================================
# 🚀 Synchronous OpticParse Client
# ==========================================
class OpticParse:
    """
    Official OpticParse Enterprise Python Client.

    Args:
        api_key: Your OpticParse or RapidAPI subscription key.
        base_url: Gateway base URL (defaults to Cloudflare Edge Gateway).
        max_retries: Number of automatic retries with exponential backoff on transient errors (default: 3).
        timeout: Request timeout in seconds (default: 30.0).
    """

    DEFAULT_BASE_URL = "https://opticparse-rapidapi-gateway.parastejpal987.workers.dev"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_retries: int = 3,
        timeout: float = 30.0,
    ):
        self.api_key = api_key or ""
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.max_retries = max(0, max_retries)
        self.timeout = timeout

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"opticparse-python-sdk/{__version__}",
        }
        if self.api_key:
            headers["X-API-Key"] = self.api_key
            headers["X-RapidAPI-Key"] = self.api_key
        return headers

    def _request_with_retry(self, method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = self._get_headers()

        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(url, data=data, headers=headers, method=method)
                ctx = ssl.create_default_context()
                with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                    raw_body = response.read().decode("utf-8")
                    try:
                        return json.loads(raw_body)
                    except json.JSONDecodeError:
                        return {"raw": raw_body, "status_code": response.status}

            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="ignore")
                if e.code in (401, 403):
                    raise AuthenticationError(f"Authentication failed: {err_body}", status_code=e.code, response_body=err_body)
                elif e.code == 429:
                    if attempt < self.max_retries:
                        backoff = (2 ** attempt) * 0.5
                        time.sleep(backoff)
                        continue
                    raise RateLimitError(f"Rate limit or quota exceeded: {err_body}", status_code=429, response_body=err_body)
                elif e.code >= 500:
                    if attempt < self.max_retries:
                        backoff = (2 ** attempt) * 0.5
                        time.sleep(backoff)
                        continue
                    raise ServerError(f"OpticParse server error (HTTP {e.code}): {err_body}", status_code=e.code, response_body=err_body)
                else:
                    raise OpticParseError(f"API request failed with HTTP {e.code}: {err_body}", status_code=e.code, response_body=err_body)

            except (urllib.error.URLError, TimeoutError) as e:
                last_exception = e
                if attempt < self.max_retries:
                    backoff = (2 ** attempt) * 0.5
                    time.sleep(backoff)
                    continue

        raise APIConnectionError(f"Failed to connect to OpticParse gateway after {self.max_retries} retries: {last_exception}")

    def scrape(
        self,
        target_url: str,
        extraction_query: str,
        response_schema: Optional[Dict[str, Any]] = None,
        vision_mode: bool = True,
    ) -> Dict[str, Any]:
        """
        Extract structured data from any webpage using AI Vision heuristics.

        Args:
            target_url: The full HTTP/HTTPS URL of the target page.
            extraction_query: Natural language instructions describing the data to extract.
            response_schema: Optional JSON Schema to enforce field types and keys.
            vision_mode: Whether to utilize visual layout heuristics (default: True).

        Returns:
            Dict containing the structured extracted data.
        """
        payload: Dict[str, Any] = {
            "target_url": target_url,
            "extraction_query": extraction_query,
            "vision_mode": vision_mode,
        }
        if response_schema:
            payload["response_schema"] = response_schema

        return self._request_with_retry("POST", "/scrape", payload)

    def scrape_with_template(self, target_url: str, template_id: str) -> Dict[str, Any]:
        """
        Extract data using one of the 150 pre-built enterprise extraction templates.

        Args:
            target_url: The URL to extract from.
            template_id: Pre-built template ID (e.g. 'amazon-price-undercut-alert', 'shopify-new-product-alert').

        Returns:
            Dict containing the extracted domain data.
        """
        if not template_id:
            raise TemplateNotFoundError("template_id must not be empty.")

        payload = {
            "target_url": target_url,
            "template_id": template_id,
        }
        return self._request_with_retry("POST", "/scrape", payload)

    def extract_markdown(
        self,
        target_url: str,
        include_links: bool = True,
        include_images: bool = False,
    ) -> Dict[str, Any]:
        """
        Extract token-optimized clean Markdown for LLM RAG pipelines.
        Strips 98% of noisy HTML, banners, footers, and tracking scripts.

        Args:
            target_url: The URL to parse into Markdown.
            include_links: Whether to preserve markdown links (default: True).
            include_images: Whether to preserve image alt-text (default: False).

        Returns:
            Dict containing markdown text, title, word_count, and estimated_tokens.
        """
        payload = {
            "url": target_url,
            "include_links": include_links,
            "include_images": include_images,
        }
        return self._request_with_retry("POST", "/api/extract/markdown", payload)

    def detect_phishing(self, target_url: str, dry_run: bool = False) -> Dict[str, Any]:
        """
        Scan a URL for zero-day phishing, brand spoofing, crypto-drainers, and typosquatting.
        Powered by PhishVision Multimodal AI Heuristic Engine.

        Args:
            target_url: The URL or domain to audit.
            dry_run: Whether to simulate scan (default: False).

        Returns:
            Dict containing verdict (SAFE / MALICIOUS), threat score (0-100), and IOC signals.
        """
        payload = {"url": target_url, "dry_run": dry_run}
        return self._request_with_retry("POST", "/api/phish-detect", payload)

    def get_proxy(self, target_url: str) -> str:
        """
        Fetch any webpage through OpticParse's unblockable edge proxy network.

        Args:
            target_url: Destination URL to fetch.

        Returns:
            Clean HTML / response string.
        """
        resp = self._request_with_retry("GET", f"/proxy?url={target_url}")
        return resp.get("raw", str(resp))


# Alias for backward compatibility
OpticParseClient = OpticParse
