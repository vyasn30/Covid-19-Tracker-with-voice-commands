import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time

API_KEY = "tJQXTbMLadnJ"
PROJECT_TOKEN = "tvHRzqKBring"
RUN_KEY = "tAq5YfAT6hCo"


# ---------- Class Data--------------------------------------------------------------pyth-----------------------------------


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token

        self.params = {
            "api_key": self.api_key
        }

        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)
        data = json.loads(response.text)
        return data

    def get_total_cases(self):
        data = self.data["total"]

        for val in data:
            if val["name"] == "Coronavirus Cases:":
                return val["value"]

        return "0"

    def get_total_deaths(self):
        data = self.data["total"]

        for val in data:
            if val["name"] == "Deaths:":
                return val["value"]

        return "0"

    def get_total_recovered(self):
        data = self.data["total"]

        for val in data:
            if val["name"] == "Recovered:":
                return val["value"]

        return "0"

    def get_country_data(self, country):
        data = self.data["countries"]

        for val in data:
            if val["name"] == country:
                return val

        return "0"

    def get_list_of_countries(self):
        data = self.data["countries"]
        countries = []
        for val in data:
            countries.append(val["name"])

        return countries

    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run',
                                 params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data Updated")
                    break

                time.sleep(5)

        t = threading.Thread(target=poll())
        t.start()


# -----------------------------------------------------------------------------------------------------------------------

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

    return said.lower()


# def test_for_patterns(inputText):
#     data = Data(API_KEY, PROJECT_TOKEN)
#
#     TOTAL_PATTERNS = {
#         re.compile("[\w\s] total [\w\s] cases"): data.get_total_cases,
#         re.compile("[\w\s] total cases"): data.get_total_cases,
#         re.compile("[\w\s] total [\w\s] deaths"): data.get_total_deaths,
#         re.compile("[\w\s] total deaths"): data.get_total_deaths,
#         re.compile("[\w\s] total [\w\s] recovered"): data.get_total_recovered,
#         re.compile("[\w\s] total recoverd"): data.get_total_recovered,
#
#     }
#
#     COUNTRY_PATTERNS = {
#         re.compile("[\w\s] cases [\w\s]"): lambda country: data.get_country_data(country)["total_cases"],
#         re.compile("[\w\s] new [\w\s] cases"): lambda country: data.get_country_data(country)["new_cases"],
#         re.compile("[\w\s] new cases"): lambda country: data.get_country_data(country)["new_cases"],
#         re.compile("[\w\s] deaths [\w\s]"): lambda country: data.get_country_data(country)["total_deaths"],
#         re.compile("[\w\s] recovered [\w\s]"): lambda country: data.get_country_data(country)["total_recovered"],
#         re.compile("[\w\s] active [\w\s] cases"): lambda country: data.get_country_data(country)["active_cases"],
#         re.compile("[\w\s] active cases"): lambda country: data.get_country_data(country)["active_cases"]
#     }
#
#     for pattern, func in TOTAL_PATTERNS.items():
#         if pattern.match(inputText):
#             print("Match Found in total category")
#             result = func()
#             break
#
#     for pattern, func in COUNTRY_PATTERNS.items():
#         if pattern.match(inputText):
#             words = inputText.split(" ")
#             for country in country_list:
#                 if country in words:
#                     result = func(country)
#                     break
#
#


def main():
    data = Data(API_KEY, PROJECT_TOKEN)
    print("Program Initialized")

    END_PHRASE = "stop"
    country_list = data.get_list_of_countries()



    while True:
        print("Listening . . .")

        inputText = get_audio()

        print(inputText)

        result = ""

        TOTAL_PATTERNS = {
            re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
            re.compile("[\w\s]+ total cases"): data.get_total_cases,
            re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
            re.compile("[\w\s]+ total deaths"): data.get_total_deaths
        }

        COUNTRY_PATTERNS = {
            re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
            re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
        }

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(inputText):
                print("Match Found in total category")
                result = func()
                break

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(inputText):
                words = inputText.split(" ")
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

        if inputText == "update":
            result = "Data is being updated, this may take a while"
            data.update_data()

        if result:
            speak(result)

        if inputText.find(END_PHRASE) != -1:
            speak("exiting")
            print("Exit")
            break

    print(result)

main()
