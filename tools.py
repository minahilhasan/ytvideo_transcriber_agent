import streamlit as st
import requests
import yt_dlp
from pytube import YouTube
import tempfile
import subprocess
import os
from google import genai
from genai import Client as genaiClient

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
        audio_path = os.path.join(tmpdir, "audio.mp4")

        # Download audio using pytube
        try:
            yt = YouTube(video_url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            if not audio_stream:
                return "No audio streams available for this video."
            audio_stream.download(output_path=tmpdir, filename="audio.mp4")
        except Exception as e:
            return f"Failed to download audio: {e}"

        # Transcribe audio
        try:
            with open(audio_path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    file=f,
                    model="gemini-1.5-pro",
                    instructions="Transcribe this audio accurately."
                )
            return transcript.text
        except Exception as e:
            return f"Error during transcription: {e}"
