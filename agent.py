import streamlit as st
import google.generativeai as genai
import json
from tools import urlFinder, videotranscriber

TOOLS = (
    {
        "name": "search_youtube",
        "description": "Search YouTube and return a video URL.",
        "function": urlFinder,
    },
    {
        "name": "transcribe_video",
        "description": "Transcribe a YouTube video using its URL.",
        "function": videotranscriber,
    },
)

def aiagent(state):
    tool_prompt = "\n".join(
        f"- {tool['name']}: {tool['description']}"
        for tool in TOOLS
    )

    genai.configure(api_key=st.secrets["GEMINI"]["GEMINI_API_KEY"])

    system_prompt = f"""
You are an AI agent.

Tools:
{tool_prompt}

Rules:
1. If the input is a topic, respond in JSON:
   { "tool": "search_youtube", "input": "<topic>" }
2. If the input is a YouTube URL, respond in JSON:
   { "tool": "transcribe_video", "input": "<URL>" }
3. If the task is complete, respond:
   { "tool": "finish", "output": "<final answer>" }
"""

    model = genai.GenerativeModel("models/gemini-1.5-pro")
    response = model.generate_content(system_prompt)

    return json.loads(response.text)


def execute_tool(decision):
    for tool in TOOLS:
        if tool["name"] == decision["tool"]:
            return tool["function"](decision["input"])
    return None

    
