from googletrans import Translator, LANGUAGES
import datetime
import openai
# import os
from dotenv import load_dotenv

# load_dotenv()


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
