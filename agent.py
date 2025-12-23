import streamlit as st
from groq import Groq
import json
from tools import urlFinder, videotranscriber

TOOLS = {
    "search_youtube": urlFinder,
    "transcribe_video": videotranscriber
}

def aiagent(user_input):
    client = Groq(api_key=st.secrets["GROQ"]["GROQ_API_KEY"])
    current_input = user_input

    while True:
        # Ask LLM what to do next
        system_prompt = """
You are an AI agent. Respond ONLY with JSON with keys 'tool' and 'input':
1. If the input is a topic: {"tool": "search_youtube", "input": "<topic>"}
2. If the input is a URL: {"tool": "transcribe_video", "input": "<URL>"}
3. If the task is complete, respond: {"tool": "finish", "output": "<final answer>"}
"""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": current_input},
            ],
            temperature=0
        )

        try:
            decision = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            st.error(f"Failed to parse JSON: {response.choices[0].message.content}")
            return "Failed to parse LLM JSON."

        tool_name = decision.get("tool")
        tool_input = decision.get("input")
        if tool_name == "finish":
            return decision.get("output", "<no output>")

        if tool_name in TOOLS:
            st.info(f"Calling tool: {tool_name} with input: {tool_input}")
            tool_result = TOOLS[tool_name](tool_input)


            if isinstance(tool_result, dict):
                current_input = tool_result.get("output", "")
            else:
                current_input = str(tool_result)

        else:
            return f"<unknown tool: {tool_name}>"


    
