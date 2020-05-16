import dataModule

def Answer(question):
    API_KEY = "tJQXTbMLadnJ"
    PROJECT_TOKEN = "tvHRzqKBring"
    RUN_KEY = "tAq5YfAT6hCo"

    words = question.split(" ")



    countryQuestionFlag = False

    data = dataModule.Data(API_KEY, PROJECT_TOKEN)

    countries_list = data.get_country_list()
    country = ""

    mapper_total = {
        "total cases": data.get_total_cases,
        "recovered": data.get_total_recovered,
        "deaths": data.get_total_deaths,
    }

    mapper_country = {
        "total cases": lambda country: data.get_country_data(country)["total_cases"],
        "new": lambda country: data.get_country_data(country)["new_cases"],
        "deaths": lambda country: data.get_country_data(country)["total_deaths"],
        "recovered": lambda country: data.get_country_data(country)["total_recovered"],
        "active": lambda country: data.get_country_data(country)["active_cases"],
        "serious": lambda country:data.get_country_data(country)["serious_cases"]
    }


    for val in countries_list:
        if val in words:
            countryQuestionFlag = True

            country = val

    if countryQuestionFlag == False:
        keywordsTotal = ["total", "new", "deaths", "recovered", "active", "serious", "total cases"]
        temp_words = words
        targetWord = ""
        for i in range(0, len(temp_words)):
            if words[i] == "total":
                if words[i+1] == "cases":
                    targetWord = words[i] + " " + words[i + 1]
                    print(targetWord)
                    break

                else:
                    temp_words.remove(temp_words[i])
                    break

        if targetWord != "total cases":
            for val in temp_words:
                if val in keywordsTotal:
                    targetWord = val

        func = mapper_total.get(targetWord)
        if func:
            result = func()
        else:
            result = "Please say that again."


    elif countryQuestionFlag == True:
        temp_words = words
        targetWord = ""
        keywordsTotal = ["total", "new", "deaths", "recovered", "active", "serious", "total cases"]
        for i in range(0, len(temp_words)):
            if words[i] == "total":
                if words[i + 1] == "cases":
                    targetWord = words[i] + " " + words[i + 1]
                    break

                else:
                    temp_words.remove(temp_words[i])
                    break

            if targetWord != "total cases":
                for val in temp_words:
                    if val in keywordsTotal:
                        targetWord = val

        print(targetWord)
        func = mapper_country.get(targetWord)

        if func:
            func = mapper_country[targetWord]
            result = func(country)
        else:
            result = "Please say that again"


    return result


