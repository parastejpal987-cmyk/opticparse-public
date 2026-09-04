"""
OpticParse Command-Line Interface (CLI).
Provides instant command-line extraction, zero-day threat scanning, and repository links.
"""

import sys
import os
import argparse
import json
from .client import OpticParse, __version__

STAR_BANNER = (
    "\n\033[93m⭐ Enjoying OpticParse? Star us on GitHub:\033[0m "
    "\033[94mhttps://github.com/parastejpal987-cmyk/opticparse-public\033[0m\n"
)


def main():
    parser = argparse.ArgumentParser(
        prog="opticparse",
        description="OpticParse Autonomous Vision Web Scraper & PhishVision CLI.",
        epilog="Star our GitHub repo: https://github.com/parastejpal987-cmyk/opticparse-public"
    )
    parser.add_argument("-v", "--version", action="version", version=f"opticparse-py v{__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: extract
    extract_parser = subparsers.add_parser("extract", help="Extract clean Markdown or structured data from any URL")
    extract_parser.add_argument("url", help="Target URL to scrape")
    extract_parser.add_argument("--key", help="OpticParse API Key (or set OPTICPARSE_API_KEY env var)")

    # Command: scan
    scan_parser = subparsers.add_parser("scan", help="Scan a URL for phishing, brand impersonation, or crypto drainers")
    scan_parser.add_argument("url", help="Target URL or domain to audit")
    scan_parser.add_argument("--key", help="OpticParse API Key (or set OPTICPARSE_API_KEY env var)")

    # Command: star
    subparsers.add_parser("star", help="Open or show the OpticParse GitHub repository")

    args = parser.parse_args()

    if not args.command or args.command == "star":
        print(f"OpticParse Enterprise SDK v{__version__}")
        print(STAR_BANNER)
        return

    api_key = getattr(args, "key", None) or os.getenv("OPTICPARSE_API_KEY", "op_live_cli_user")
    client = OpticParse(api_key=api_key)

    if args.command == "extract":
        print(f"[*] Extracting Markdown from: {args.url} ...")
        try:
            res = client.extract_markdown(args.url)
            print(res.get("markdown", str(res)))
        except Exception as e:
            print(f"[!] Extraction error: {e}", file=sys.stderr)
        finally:
            print(STAR_BANNER)

    elif args.command == "scan":
        print(f"[*] Scanning URL for threats: {args.url} ...")
        try:
            res = client.detect_phishing(args.url)
            print(json.dumps(res, indent=2))
        except Exception as e:
            print(f"[!] Scan error: {e}", file=sys.stderr)
        finally:
            print(STAR_BANNER)


if __name__ == "__main__":
    main()
