"""
CrewAI Multi-Agent Recipe using langchain-opticparse
Demonstrates autonomous multi-agent reconnaissance and threat-proof web extraction.
"""
import os
from crewai import Agent, Crew, Process, Task
from langchain_opticparse import OpticParseTool, PhishVisionTool

# 1. Initialize Tools
api_key = os.getenv("OPTICPARSE_API_KEY", "op_live_dev")
scraper_tool = OpticParseTool(api_key=api_key)
scanner_tool = PhishVisionTool(api_key=api_key)

# 2. Define Autonomous Security Scout Agent
security_scout = Agent(
    role="Cybersecurity URL Inspector",
    goal="Ensure target URLs are safe before extraction, detecting zero-day phishing or wallet drainers",
    backstory="You are a senior security researcher analyzing unverified web domains for cyber risks.",
    tools=[scanner_tool],
    verbose=True
)

# 3. Define Multimodal Web Extraction Agent
data_extractor = Agent(
    role="Vision-Language Web Extractor",
    goal="Extract clean, structured product, pricing, and article data without breaking on CSS changes",
    backstory="You are an autonomous intelligence agent specializing in visual web layout parsing.",
    tools=[scraper_tool],
    verbose=True
)

# 4. Define Investigation Workflow
def create_web_investigation_crew(target_url: str):
    security_task = Task(
        description=f"Scan {target_url} for malicious signatures, credential harvesters, or brand impersonations.",
        expected_output="Security audit report containing verdict (SAFE or MALICIOUS) and threat score.",
        agent=security_scout
    )

    extraction_task = Task(
        description=f"If {target_url} is marked SAFE, extract key headlines, pricing, and main content summaries.",
        expected_output="Structured JSON or Markdown containing verified web extractions.",
        agent=data_extractor
    )

    crew = Crew(
        agents=[security_scout, data_extractor],
        tasks=[security_task, extraction_task],
        process=Process.sequential,
        verbose=True
    )
    return crew

if __name__ == "__main__":
    print(f"Initialized OpticParse CrewAI Recipe: {scraper_tool.name}, {scanner_tool.name}")
