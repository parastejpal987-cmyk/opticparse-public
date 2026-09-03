# 🦜️🔗 langchain-opticparse

Official **LangChain** and **CrewAI** ecosystem integration for **OpticParse** and **PhishVision**.

Enables AI agents to:
1. **Visually Scrape Live Webpages (`OpticParseTool`):** Extract clean, structured JSON using multimodal vision without fragile CSS selectors.
2. **Scan Zero-Day Cyber Threats (`PhishVisionTool`):** Inspect unknown domains for crypto wallet-drainers and brand impersonation kits before interacting.

---

## 📦 Installation

```bash
pip install langchain-opticparse
```

---

## 🚀 Usage with LangChain (1.x+)

`langchain-opticparse` provides standard `BaseTool` instances compatible with modern LangChain 1.x agent executors, LangGraph, and Tool Calling LLMs:

### Modern Tool Calling Agent (LangChain 1.x)

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_opticparse import OpticParseTool, PhishVisionTool

# 1. Initialize OpticParse and PhishVision tools
tools = [
    OpticParseTool(),
    PhishVisionTool()
]

# 2. Bind tools to any modern Tool-Calling model
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# 3. Direct Tool Invocation Example
scraper = OpticParseTool()
clean_data = scraper.invoke({
    "url": "https://news.ycombinator.com",
    "query": "Extract top stories with points and author"
})
print("Extracted Data:", clean_data)

# 4. Threat Inspection Example
scanner = PhishVisionTool()
security_report = scanner.invoke({
    "url": "https://suspicious-dapp-claim.xyz"
})
print("Threat Report:", security_report)
```

---

## 👥 Usage with CrewAI

```python
from crewai import Agent, Task, Crew
from langchain_opticparse import OpticParseTool

vision_scraper = OpticParseTool()

market_researcher = Agent(
    role='Senior Market Intelligence Analyst',
    goal='Extract and synthesize competitor pricing deltas in real-time',
    backstory='An expert automated web researcher powered by OpticParse Vision AI.',
    tools=[vision_scraper],
    verbose=True
)
```

---

## 📄 License
MIT © OpticParse Enterprise
