import pytest
import sys
import os

def test_opticparse_py_import():
    """Verify opticparse-py SDK imports cleanly."""
    sys.path.insert(0, os.path.abspath("opticparse-py/src"))
    import opticparse
    from opticparse import OpticParse
    client = OpticParse(api_key="test_key")
    assert client.api_key == "test_key"
    assert hasattr(client, "extract_markdown")
    assert hasattr(client, "detect_phishing")

def test_langchain_opticparse_import():
    """Verify langchain-opticparse BaseTool integration imports cleanly."""
    sys.path.insert(0, os.path.abspath("langchain-opticparse"))
    import langchain_opticparse
    from langchain_opticparse import OpticParseTool, PhishVisionTool
    tool = OpticParseTool(api_key="test_key")
    phish = PhishVisionTool(api_key="test_key")
    assert tool.name == "opticparse_vision_scrape"
    assert phish.name == "phishvision_threat_detect"

def test_llama_index_opticparse_import():
    """Verify llama-index-tools-opticparse ToolSpec imports cleanly."""
    sys.path.insert(0, os.path.abspath("llama-index-tools-opticparse"))
    from llama_index.tools.opticparse import OpticParseToolSpec
    spec = OpticParseToolSpec(api_key="test_key")
    assert "extract" in spec.spec_functions
    assert "inspect_threat" in spec.spec_functions
    tools = spec.to_tool_list()
    assert len(tools) == 2
