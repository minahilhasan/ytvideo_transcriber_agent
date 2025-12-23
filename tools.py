import streamlit as st
import requests
import yt_dlp
from pytube import YouTube
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
        # Download audio from YouTube 
        try: 
            subprocess.run( 
                [ "yt-dlp", 
                 "--js-runtimes", 
                 "node", 
                 "-f", "bestaudio", 
                 "-x", "--audio-format", 
                 "mp3", 
                 "-o", audio_path, 
                 "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                 "AppleWebKit/537.36 (KHTML, like Gecko) " "Chrome/118.0.5993.90 Safari/537.36", 
                 video_url 
                ], 
                check=True ) 
        except subprocess.CalledProcessError as e: 
            return f"Failed to download or extract audio: {e}"
            if not os.path.exists(audio_path): 
                return "Audio file was not created. Download may have failed." 
            try: 
                model = client.audio.transcriptions.create( file=open(audio_path, "rb"), 
                    model="gemini-1.5-pro", instructions="Transcribe this audio accurately." ) 
                return model.text 
            except Exception as e: 
                return f"Error during transcription: {e}"

