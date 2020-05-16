import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time
import dataModule

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))

    question = said.lower()
    words = question.split(" ")
    countryList = dataModule.Data("tJQXTbMLadnJ", "tvHRzqKBring").get_country_list()


    for val in words:
        if val.capitalize() in countryList:
            words.remove(val)
            words.append(val.capitalize())
            print(val)

    question = ' '.join(map(str, words))
    return question
