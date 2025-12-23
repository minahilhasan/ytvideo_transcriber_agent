import streamlit as st
from agent import aiagent,execute_tool


def main(): 
    st.title("Youtube Videos Transcriber")
    user_request = st.text_input("Enter the topic you would like to search for:")

    if not user_request.strip():
        return

    state = f"User request: {user_request}"
    st.write("The agent is performing the asked tasks")
      
    decision = aiagent(state)
    while decision["tool"] != "finish":
        time.sleep(2) 
        result = execute_tool(decision)
        state += f"\n{decision['tool']} result: {result}"   
        decision = aiagent(state)
      
    st.write(decision["output"]) 

if __name__=="__main__":
    main()
