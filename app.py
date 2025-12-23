import streamlit as st
import time
from agent import aiagent

def main():
    st.title("YouTube Videos Transcriber")
    st.write("First enter the title of the video you want to transcribe, then click run agent. The agent will first show you the youtube link that it is transcribing and will then move on to display the full transcription")
    user_request = st.text_input(
        "Enter the topic you would like to search for:"
    )
   
    if st.button("Run Agent") and user_request.strip():
        st.write("Running agent...")
        decision = aiagent(user_request)
        st.write(decision["output"])


if __name__ == "__main__":
    main()
