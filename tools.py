import streamlit as st
import requests
import yt_dlp
import tempfile
import subprocess
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

        # yt-dlp command with better user-agent & Node.js JS runtime
        ytdlp_cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "-x",
            "--audio-format", "mp3",
            "-o", audio_path,
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36",
            "--js-runtimes", "node",  # Use Node.js if installed
            video_url
        ]

        try:
            subprocess.run(ytdlp_cmd, check=True)
        except subprocess.CalledProcessError as e:
            return f"Error downloading video: {e}"

        # Make sure the file exists
        if not os.path.exists(audio_path):
            return "Audio download failed, file not found."

        # Open the audio file and send to Gemini
        with open(audio_path, "rb") as f:
            model = client.audio_model("gemini-1.5-pro")  # Updated Gemini method
            response = model.generate_audio(
                input_audio=f,
                instructions="Transcribe this audio accurately."
            )

        return response.output_text
