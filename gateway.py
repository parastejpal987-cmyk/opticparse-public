"""
OpticParse & PhishVision Developer Gateway Proxy
Official open-source client gateway stub for connecting self-hosted AI agent swarms
to the OpticParse Multimodal Vision & Threat Intelligence Engine.
"""
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel, Field
import httpx
import os

app = FastAPI(
    title="OpticParse Public Client Gateway",
    description="Developer Gateway proxy for OpticParse Vision Web Scraping & PhishVision 0-Day Threat Sentinel",
    version="1.2.0"
)

OPTICPARSE_API_BASE = os.getenv("OPTICPARSE_API_BASE", "https://opticparse-api.onrender.com")

class ScrapeRequest(BaseModel):
    target_url: str = Field(..., description="Target webpage URL to scrape")
    extraction_query: str = Field(..., description="Natural language query or JSON schema instructions")
    response_schema: dict | None = Field(default=None, description="Optional target JSON schema")

class ThreatScanRequest(BaseModel):
    url: str = Field(..., description="Suspicious URL to analyze for zero-day phishing or wallet drainers")

@app.get("/")
async def gateway_status():
    return {
        "service": "OpticParse & PhishVision Public Gateway",
        "version": "1.2.0",
        "status": "online",
        "upstream_host": OPTICPARSE_API_BASE,
        "docs": "https://opticparse.com"
    }

@app.post("/api/gateway/scrape")
async def gateway_scrape(req: ScrapeRequest, request: Request):
    api_key = request.headers.get("Authorization") or os.getenv("OPTICPARSE_API_KEY", "")
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            resp = await client.post(
                f"{OPTICPARSE_API_BASE}/api/vision-scrape",
                json=req.dict(),
                headers=headers
            )
            return resp.json()
        except httpx.HTTPError as err:
            raise HTTPException(status_code=502, detail=f"Upstream OpticParse error: {err}")

@app.post("/api/gateway/scan-threat")
async def gateway_scan(req: ThreatScanRequest, request: Request):
    api_key = request.headers.get("Authorization") or os.getenv("OPTICPARSE_API_KEY", "")
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(
                f"{OPTICPARSE_API_BASE}/api/phishvision/scan",
                json=req.dict(),
                headers=headers
            )
            return resp.json()
        except httpx.HTTPError as err:
            raise HTTPException(status_code=502, detail=f"Upstream PhishVision error: {err}")
