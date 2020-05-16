import json
import requests
import time
import threading

API_KEY = "tJQXTbMLadnJ"
PROJECT_TOKEN = "tvHRzqKBring"
RUN_KEY = "tAq5YfAT6hCo"


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

    def get_country_list(self):
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

    def get_country_data(self, country):
        data = self.data["countries"]

        for val in data:
            if val["name"] == country:
                return val

        return "0"

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
