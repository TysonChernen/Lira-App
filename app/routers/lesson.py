from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from openai import OpenAI

import io
import string
import tempfile
import subprocess
import os
from app.database import SessionLocal
from app.services.auth_service import get_current_user

router = APIRouter()

# ✅ Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ Use an env variable

lesson_words = ["bat", "cop", "bib", "pan", "rut", "fed"]

# ✅ Track user progress
user_progress = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clean_text(text: str) -> str:
    """Removes punctuation and converts text to lowercase."""
    return text.lower().translate(str.maketrans('', '', string.punctuation))

def highlight_mistakes(expected: str, corrected: str) -> str:
    """Highlights incorrect parts of the corrected word compared to the expected word."""
    expected = clean_text(expected)
    corrected = clean_text(corrected)
    
    highlighted = []
    
    # Determine the length of the shorter word to avoid index errors
    min_length = min(len(expected), len(corrected))
    
    # Compare letters in both words
    for i in range(min_length):
        if expected[i] == corrected[i]:
            highlighted.append(expected[i])  # ✅ Correct letter
        else:
            highlighted.append(f"<span style='color:red;'>{expected[i]}</span>")  # ❌ Incorrect letter
    
    # If the words are different lengths, mark extra letters in expected word as mistakes
    if len(expected) > len(corrected):
        for i in range(min_length, len(expected)):
            highlighted.append(f"<span style='color:red;'>{expected[i]}</span>")  # ❌ Missing letters in spoken word
    
    return "".join(highlighted)


def convert_audio_to_mp3(file: UploadFile) -> str:
    """Converts an audio file to MP3 format using FFmpeg and returns the file path."""
    # ✅ Ensure correct file extension
    input_extension = file.filename.split('.')[-1].lower()
    if input_extension not in ["mp3", "wav", "ogg", "flac", "m4a"]:
        input_extension = "wav"  # Default to WAV if unknown

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{input_extension}") as temp_input:
        temp_input.write(file.file.read())
        temp_input.flush()

    temp_output = temp_input.name.replace(f".{input_extension}", ".mp3")  # Convert to MP3

    try:
        # ✅ Convert audio using FFmpeg
        subprocess.run([
            "ffmpeg", "-i", temp_input.name, "-c:a", "libmp3lame", "-ar", "16000", "-ac", "1", temp_output, "-y"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return temp_output  # ✅ Return file path

    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg conversion error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Audio conversion failed: {str(e)}")

    finally:
        os.remove(temp_input.name)  # ✅ Remove input file after conversion


def correct_with_chatgpt(whisper_transcription: str, expected_word: str) -> str:
    """Uses GPT-4 to correct misheard words but ensures vowel swaps and dyslexic errors are detected."""
    try:
        print("🧠 Sending to ChatGPT for phonetic correction...")

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are an AI that detects phonetic mistakes in spoken words. "
                    "Your task is to determine whether the transcribed word is a mishearing or a genuine pronunciation mistake.\n\n"
                    
                    "Rules:\n"
                    "1. If Whisper misheard a correctly pronounced word, return the expected word.\n"
                    "2. If the user made a phonetic mistake (e.g., vowel swap: 'pen' instead of 'pan'), return the incorrect word **exactly as spoken**.\n"
                    "3. If the spoken word is completely unrelated, return 'invalid'.\n"
                    "4. Vowel swaps, consonant errors, or syllable shifts **must NOT be corrected** to the expected word—they must be marked as incorrect.\n"
                    "5. Only return a **single word** with no extra text or formatting."
                )},
                {"role": "user", "content": (
                    f"Expected word: {expected_word}\n"
                    f"Transcription from Whisper: {whisper_transcription}\n"
                    "Provide only the corrected word, or 'invalid' if the transcription is unrelated."
                )}
            ],
            temperature=0.1,  # 🔥 Lower temperature to reduce leniency
            max_tokens=10  # 🚀 Ensuring it only returns a single word
        )

        corrected_word = response.choices[0].message.content.strip().lower()
        print(f"✅ GPT-4 Response: {corrected_word}")

        # ✅ Ensure GPT-4 returns only a single word
        corrected_word = corrected_word.split()[0] if " " in corrected_word else corrected_word  

        return corrected_word  # ✅ Return corrected word

    except Exception as e:
        print(f"❌ GPT Correction Error: {e}")
        return whisper_transcription  # If GPT fails, fallback to Whisper's original output






@router.post("/lesson/speech")
async def check_speech(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("id")

    # ✅ Ensure user progress is initialized
    if user_id not in user_progress:
        user_progress[user_id] = 0

    word_index = user_progress[user_id]

    # ✅ Ensure the user hasn't finished all words
    if word_index >= len(lesson_words):
        return {"message": "🎉 Lesson complete!", "correct": True, "next_word": None}

    expected_word = lesson_words[word_index]

    # ✅ Convert audio before sending it to OpenAI Whisper
    try:
        audio_filepath = convert_audio_to_mp3(file)
        print(f"🔊 Audio converted successfully: {audio_filepath}")
    except Exception as e:
        print(f"❌ Audio conversion error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Audio conversion failed: {str(e)}")

    # ✅ Send Audio to OpenAI Whisper API
    try:
        with open(audio_filepath, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        transcript = clean_text(response.text)  # ✅ Extract text properly
        print(f"📜 Whisper Transcription: {transcript}")

    except Exception as e:
        print(f"❌ Whisper API Error: {e}")
        raise HTTPException(status_code=500, detail=f"Whisper API Request Failed: {str(e)}")

    finally:
        os.remove(audio_filepath)  # ✅ Remove temp file after processing

    # ✅ Use GPT-4 to correct misheard words with phonetic consideration
    corrected_transcript = correct_with_chatgpt(transcript, expected_word)

    # ✅ If the user said the correct word, move to the next word
    if corrected_transcript == expected_word:
        user_progress[user_id] += 1  # ✅ Move to the next word

        # ✅ Determine the next word or complete the lesson
        if user_progress[user_id] < len(lesson_words):
            next_word = lesson_words[user_progress[user_id]]
        else:
            next_word = None  # Lesson completed

        return {
            "correct": True,
            "message": "Correct!",
            "spoken": corrected_transcript,
            "expected": expected_word,
            "highlighted": expected_word,  # No highlight needed for correct words
            "next_word": next_word
        }

    # ✅ If incorrect, highlight mistakes
    highlighted_word = highlight_mistakes(expected_word, corrected_transcript)

    return {
        "correct": False,
        "message": "Incorrect",
        "spoken": corrected_transcript,
        "expected": expected_word,
        "highlighted": highlighted_word,
        "next_word": expected_word  # Keep the same word if incorrect
    }
