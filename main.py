from googletrans import Translator, LANGUAGES
import datetime
import openai
from dotenv import load_dotenv

# load_dotenv()
import speech_recognition as sr

# Add the following imports
import io
import os
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account


# Load dotenv
load_dotenv()

# Function to transcribe audio using Google Speech-to-Text API
def transcribe_audio(file_path: str, language: str, api_key: str) -> str:
    # Set Google Cloud credentials and API key
    credentials = service_account.Credentials.from_service_account_file(api_key)

    client = speech.SpeechClient(credentials=credentials)

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language,
        enable_automatic_punctuation=True,
        model="default",
        use_enhanced=True,
    )

    response = client.recognize(config=config, audio=audio)

    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript

    return transcription




# openai.api_key = os.getenv('OPENAI_API_KEY')

def detect_language(text: str):
    translator = Translator()
    detected_language = translator.detect(text)
    return detected_language.lang

def translate(text: str, input_language: str, target_language: str, api_key: str) -> str:
    # Add the following two lines
    import openai
    openai.api_key = api_key
    
    if input_language not in LANGUAGES.keys():
        input_language = detect_language(text)

    if input_language == target_language:
        return text

    translator = Translator()
    translation = translator.translate(text, src=input_language, dest=target_language)

    if translation:
        return translation.text
    else:
        return "Translation failed"


def save_conversation(conversation_history):
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    with open(filename, "w") as f:
        for original_text, translated_text in conversation_history:
            f.write("Original Text:\n" + original_text + "\n")
            f.write("Translated Text:\n" + translated_text + "\n")
            f.write("\n")


def generate_summary(text: str, max_tokens: int = 300, api_key=None) -> str:
    openai.api_key = api_key
    prompt = f"Summarize the following conversation into bullet points, and make each bullet points in one line: {text} Summary:"
    message_log = [{"role": "user","content": prompt}]
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message_log,
        max_tokens=max_tokens,
        stop=None,
        temperature=0.7,
    )
    
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    text = response.choices[0].message.content
    return text
    
    
    return response.choices[0].text.strip()
