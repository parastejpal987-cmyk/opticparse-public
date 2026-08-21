import sys
import json
import logging
import os
from typing import Dict, Any

# Disable logging to stdout as stdout is reserved for JSON-RPC messages
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mcp_server")

def send_response(response: Dict[str, Any]):
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()

def handle_request(req: Dict[str, Any]):
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
                    "tools": {}
                },
                "serverInfo": {
                    "name": "opticparse-mcp",
                    "version": "0.1.0"
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
                        "description": "Extract structured data from a web page using AI Vision scraping.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "target_url": {"type": "string", "description": "The URL of the webpage to scrape."},
                                "extraction_query": {"type": "string", "description": "Instructions for what information to extract from the webpage."},
                                "response_schema": {"type": "object", "description": "Optional JSON schema to enforce on the extracted data."}
                            },
                            "required": ["target_url", "extraction_query"]
                        }
                    },
                    {
                        "name": "phishvision_detect",
                        "description": "Scan a URL to detect phishing threat indicators and impersonations.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string", "description": "The URL to inspect for threats."}
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
        api_key = os.getenv("OPTICPARSE_API_KEY")
        if not api_key:
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32602,
                    "message": "Missing OPTICPARSE_API_KEY environment variable. Please set OPTICPARSE_API_KEY or obtain a key at https://opticparse.com"
                }
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
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "isError": True,
                    "content": [
                        {"type": "text", "text": f"Error during execution: {str(e)}"}
                    ]
                }
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
        except Exception as e:
            logger.error(f"Error in stdio loop: {e}")

if __name__ == "__main__":
    main()
