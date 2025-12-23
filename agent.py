import streamlit as st
from groq import Groq
import json
from tools import urlFinder, videotranscriber

TOOLS = {
    "search_youtube": urlFinder,
    "transcribe_video": videotranscriber
}

def aiagent(user_input):
    """
    One-shot agent call:
    - Calls Groq to decide which tool to use
    - Executes the tool
    - Returns final output
    """
    client = Groq(api_key=st.secrets["GROQ"]["GROQ_API_KEY"])

    system_prompt = f"""
You are an AI agent. Respond ONLY with JSON:
1. If the input is a topic: {{ "tool": "search_youtube", "input": "<topic>" }}
2. If the input is a URL: {{ "tool": "transcribe_video", "input": "<URL>" }}
3. If the task is complete, respond: {{ "tool": "finish", "output": "<final answer>" }}
User input: {user_input}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Respond ONLY with valid JSON with keys 'tool' and 'input'."},
            {"role": "user", "content": system_prompt},
        ],
        temperature=0
    )

    try:
        decision = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {"tool": "finish", "output": "Failed to parse LLM JSON."}

    tool_name = decision.get("tool")
    if tool_name == "finish":
        return {"tool": "finish", "output": decision.get("output", "<no output>")}

    if tool_name in TOOLS:
        result = TOOLS[tool_name](decision["input"])
        return {"tool": "finish", "output": result}

    return {"tool": "finish", "output": "<unknown tool>"}


    
