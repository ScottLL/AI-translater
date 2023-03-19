import speech_recognition as sr
import pyttsx3
from langdetect import detect
from googletrans import Translator



# create recognizer object, a translator object and a text to speech object
r = sr.Recognizer()
translator = Translator(service_urls=['translate.google.com'])
tts = pyttsx3.init()

while True:
    # use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something ...")
        # adjust the recognizer sensitivity to ambient noise and record audio
        r.adjust_for_ambient_noise(source)
        # listen for the first phrase and extract it into audio data
        audio = r.listen(source)
    try:
        # recognize speech using Google Speech Recognition
        text = r.recognize_google(audio)
        input_language = detect(text)
        # translate speech to English if detected language is not Chinese
        if input_language == 'zh-CN':
            translation = translator.translate(text, dest='en')
            # speak the translated text
            tts.say(translation.text)
            tts.runAndwait()
        # translate speech to Chinese if detected language is English
        elif input_language == 'en':
            translation = translator.translate(text, dest='zh-CN')
            print(f"Translated to Chinese: {translation.text}")
            # speak the translated text
            tts.say(translation.text)
            tts.runAndwait()
        else:
            print("Unsupport language")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
