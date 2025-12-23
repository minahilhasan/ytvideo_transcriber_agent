import streamlit as st
import time
from agent import aiagent, execute_tool

def main():
    st.title("YouTube Videos Transcriber")

    user_request = st.text_input(
        "Enter the topic you would like to search for:"
    )

    # Button prevents automatic reruns
    if st.button("Run Agent"):

        if not user_request.strip():
            st.warning("Please enter a request")
            return

        st.session_state.state = f"User request: {user_request}"
        st.session_state.running = True

    if st.session_state.get("running", False):

        st.write("The agent is performing the asked tasks...")

        decision = aiagent(st.session_state.state)

        max_steps = 5  # hard safety cap
        steps = 0

        while decision["tool"] != "finish" and steps < max_steps:
            time.sleep(2)  # respect Groq RPM

            result = execute_tool(decision)
            st.session_state.state += f"\n{decision['tool']} result: {result}"

            decision = aiagent(st.session_state.state)
            steps += 1

        st.session_state.running = False
        st.write(decision["output"])


if __name__ == "__main__":
    main()
