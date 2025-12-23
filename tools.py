import streamlit as st
import requests
import yt_dlp
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
        # Output path for audio
        audio_path = os.path.join(tmpdir, "audio.mp3")

        # yt-dlp options
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_path,
            "quiet": True,
            "nocheckcertificate": True,
            "ignoreerrors": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.90 Safari/537.36"
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                if info is None:
                    return "Failed to download or extract audio."
        except Exception as e:
            return f"Error downloading video: {e}"

        with open(audio_path, "rb") as audio_file:
            response = client.audio.speech_to_text(
                audio=audio_file,
                model="gemini-1.5",
                instructions="Transcribe this audio accurately."
            )

    return response.output_text
