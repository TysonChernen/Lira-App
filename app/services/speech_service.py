import os
import io
from google.cloud import speech

# Initialize Google Speech Client
client = speech.SpeechClient()

def transcribe_audio(audio_data: bytes) -> str:
    """Convert spoken words to text using Google Speech-to-Text API."""
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    if not response.results:
        return ""

    return response.results[0].alternatives[0].transcript.lower()

