import json
import logging
import os
import sys
from typing import Any

# Disable logging to stdout as stdout is reserved for JSON-RPC messages
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mcp_server")

def send_response(response: dict[str, Any]):
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()

def handle_request(req: dict[str, Any]):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        logger.info("Initializing MCP Server")
        send_response({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": "opticparse-mcp",
                    "version": "1.0.0"
                }
            }
        })
    elif method == "tools/list":
        logger.info("Listing tools")
        send_response({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "opticparse_scrape",
                        "description": "Extract structured, token-optimized data from any live web page using AI Multimodal Vision. Bypasses Cloudflare Turnstile, anti-bot mechanisms, and dynamic JavaScript rendering without brittle CSS selectors. Perfect for LLM context windows and RAG pipelines.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "target_url": {
                                    "type": "string",
                                    "description": "The fully-qualified HTTP/HTTPS URL of the webpage to scrape and extract content from."
                                },
                                "extraction_query": {
                                    "type": "string",
                                    "description": "Natural language instructions specifying what data fields, tables, or text to extract from the webpage."
                                },
                                "response_schema": {
                                    "type": "object",
                                    "description": "Optional JSON Schema definition to enforce a strict structured output format on the extracted result."
                                }
                            },
                            "required": ["target_url", "extraction_query"]
                        }
                    },
                    {
                        "name": "phishvision_detect",
                        "description": "Audit and inspect any URL for real-time zero-day phishing campaigns, smart contract wallet drainers, credential harvesting kits, and brand impersonation attacks using visual layout heuristics in under 1.6 seconds.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "description": "The target domain or fully qualified URL to audit for security threats, drainers, and malicious vectors."
                                }
                            },
                            "required": ["url"]
                        }
                    }
                ]
            }
        })
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        logger.info(f"Calling tool: {tool_name}")
        
        api_key = os.getenv("OPTICPARSE_API_KEY", "")
        if not api_key:
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32001, "message": "OPTICPARSE_API_KEY env var is not set. Set it in your MCP config."}
            })
            return

        from opticparse import OpticParse
        client = OpticParse(api_key=api_key)

        try:
            if tool_name == "opticparse_scrape":
                target_url = arguments.get("target_url")
                query = arguments.get("extraction_query")
                schema = arguments.get("response_schema")
                res = client.scrape(target_url, query, schema)
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(res, indent=2)}
                        ]
                    }
                })
            elif tool_name == "phishvision_detect":
                url = arguments.get("url")
                res = client.detect_phishing(url)
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(res, indent=2)}
                        ]
                    }
                })
            else:
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool not found: {tool_name}"}
                })
        except Exception as e:  # noqa: BLE001
            logger.error(f"Tool execution failed: {e}")
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "isError": True,
                    "content": [
                        {"type": "text", "text": f"Error during execution: {e!s}"}
                    ]
                }
            })
    elif method == "resources/list":
        logger.info("Listing resources")
        send_response({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "resources": [
                    {
                        "uri": "opticparse://capabilities",
                        "name": "OpticParse & PhishVision Capabilities",
                        "mimeType": "application/json",
                        "description": "Live status and supported extraction models and threat heuristics"
                    }
                ]
            }
        })
    elif method == "resources/read":
        uri = params.get("uri", "")
        logger.info(f"Reading resource: {uri}")
        if uri == "opticparse://capabilities":
            data = {
                "engine": "OpticParse Vision Multimodal",
                "security": "PhishVision 0-Day Heuristics",
                "supported_formats": ["json", "markdown", "raw_tokens"],
                "anti_bot_bypass": ["cloudflare_turnstile", "datadome", "kasada"]
            }
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": json.dumps(data)
                        }
                    ]
                }
            })
        else:
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Invalid resource URI: {uri}"}
            })
    else:
        if req_id is not None:
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            })

def main():
    # Add local SDK source directory to python path
    sys.path.append(os.path.join(os.path.dirname(__file__), "opticparse-py", "src"))
    
    logger.info("Starting MCP stdio loop...")
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            req = json.loads(line)
            handle_request(req)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Error in stdio loop: {e}")

if __name__ == "__main__":
    main()
