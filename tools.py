import streamlit as st
import requests
import subprocess
import tempfile
import os
from google import genai

def urlFinder(user_query):
    serpai_key = st.secrets["SERPAI"]["SERPAI_API_KEY"]

    params = {
        "engine": "youtube",
        "search_query": user_query,
        "api_key": serpai_key
    }

    response = requests.get("https://serpapi.com/search.json", params=params)
    if response.status_code != 200:
        return None

    results = response.json().get("video_results", [])
    if not results:
        return None

    return results[0]["link"]  # return ONLY URL


def videotranscriber(video_url):
    client = genai.Client(api_key=st.secrets["GEMINI"]["GEMINI_API_KEY"])

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.mp3")
        try:
            subprocess.run(
                [
                    "yt-dlp",
                    "-f", "bestaudio",
                    "-x",
                    "--audio-format", "mp3",
                    "-o", audio_path,
                    video_url
                ],
                check=True
                )
        except subprocess.CalledProcessError:
            return "Failed to download or extract audio."
        audio_file = client.upload_file(
            path=audio_path,
            mime_type="audio/mpeg"
        )

        model = client.generative_model("models/gemini-1.5-pro")
        response = model.generate_content(
            input_audio=audio_file,
            instructions="Transcribe this audio accurately."
        )

    return response.output_text
