import streamlit as st
import time
from agent import aiagent

def main():
    st.title("YouTube Videos Transcriber")

    user_request = st.text_input(
        "Enter the topic you would like to search for:"
    )
   
    if st.button("Run Agent") and user_request.strip():
        st.write("Running agent...")
        decision = aiagent(user_request)
        st.write(decision["output"])


if __name__ == "__main__":
    main()
