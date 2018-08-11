#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data

ingredient = []

def jarvis(data):
    if 'record' in data:
        speak('recording, say starting with "ingredient" or "step"')

    if 'ingredient' in data:
        ingredient.append(data)
        speak('next ingredient?')

    if "done" in data:
        speak("OK, done")
        print(ingredient)

    if "what time is it" in data:
        speak(ctime())

    if "where is" in data:
        data = data.split(" ")
        location = data[2]
        speak("Hold on Frank, I will show you where " + location + " is.")
        os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")
    if "get" and "recipe" in data:
        data = data.split(" ")
        speak("What kind of bread recipe do you want?")
        data = 'mm'
        find_recipe(data)
    if "lets start cooking" in data:
        data = data.split(" ")
        speak("Do you want me to remind you the steps completion?")
        data ='ll'
        find_recipe(data)


# initialization
time.sleep(2)
speak("Hi Lilit, what can I do for you?")
while 1:
    data = recordAudio()
    jarvis(data)