import argparse
import json
import os

def synthesize_report(results_path, output_dir):
    print(f"[Synthesizer] Reading diagnostic results from: {results_path}")
    
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "AUDIT_REPORT.md")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🛡️ PhishVision LLM Security Audit Report\n\n")
        
        vulnerabilities = data.get("vulnerabilities", [])
        if not vulnerabilities:
            f.write("✅ **No structural LLM integration risks detected.**\n")
            print(f"[Synthesizer] Report generated successfully at {report_path}")
            return
            
        f.write(f"⚠️ **Found {len(vulnerabilities)} Vulnerabilities**\n\n")
        
        for idx, vuln in enumerate(vulnerabilities, 1):
            f.write(f"## {idx}. {vuln['type']} ({vuln['severity']})\n")
            f.write(f"- **File:** `{vuln['file']}`\n")
            f.write(f"- **Description:** {vuln['description']}\n\n")
            
            f.write("### Recommended Remediation Patch\n")
            f.write("```diff\n")
            if "String Interpolation" in vuln["type"]:
                f.write("- prompt = f\"Hello {user_input}\"\n")
                f.write("+ prompt = PromptTemplate(template=\"Hello {user_input}\", input_variables=[\"user_input\"])\n")
            elif "Tool Execution" in vuln["type"]:
                f.write("- def my_tool(command: str):\n")
                f.write("-     execute(command)\n")
                f.write("+ from pydantic import BaseModel\n")
                f.write("+ class ToolArgs(BaseModel):\n")
                f.write("+     command: Literal['safe_command']\n")
                f.write("+ \n")
                f.write("+ def my_tool(args: ToolArgs):\n")
                f.write("+     execute(args.command)\n")
            f.write("```\n\n")
            
    print(f"[Synthesizer] Report generated successfully at {report_path}")

    # Output to GitHub Step Summary if running in GitHub Actions
    step_summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary_file:
        try:
            with open(report_path, "r", encoding="utf-8") as rf:
                report_content = rf.read()
            with open(step_summary_file, "a", encoding="utf-8") as wf:
                wf.write(report_content)
        except Exception as e:
            print(f"[Synthesizer] Could not write to GITHUB_STEP_SUMMARY: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Report Synthesizer")
    parser.add_argument("--input", required=True, help="Input audit results JSON file")
    parser.add_argument("--outdir", default="./audits", help="Output directory for reports")
    args = parser.parse_args()
    
    synthesize_report(args.input, args.outdir)
