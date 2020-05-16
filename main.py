import questionAnswerModule
import dataModule
import SpeechModule

while True:
    print("Listening . . . ")
    inputText = SpeechModule.get_audio()
    result = ""

    if inputText == "update":
        result = "Data is being updated"
        print("data is being update wait for some time")
        dataModule.Data("tJQXTbMLadnJ", "tvHRzqKBring").update_data()

    if inputText.find("stop") != -1:
        SpeechModule.speak("exiting")
        print("exit")
        break

    result = questionAnswerModule.Answer(inputText)

    if result:
        print(result)
        SpeechModule.speak(result)





