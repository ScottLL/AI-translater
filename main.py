from googletrans import Translator, LANGUAGES

import datetime

def detect_language(text: str):
    translator = Translator()
    detected_language = translator.detect(text)
    return detected_language.lang

def translate(text: str, input_language: str, target_language: str) -> str:
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
