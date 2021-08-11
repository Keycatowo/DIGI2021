import speech_recognition as sr
import time
import threading
import re
import json
# import requests

def ReadCommand():
    commandFile = open("digiCommands.json","r")
    commandsInput = json.load(commandFile)
    commandFile.close()
    return commandsInput

def get_command():
    try:
        # 讀指令檔
        commandsInput = ReadCommand()
        while True:
            r = sr.Recognizer()
            m = sr.Microphone()
            m.RATE = 44100
            m.CHUNK = 512

            # print("")
            with m as source:
                r.adjust_for_ambient_noise(source)
                if (r.energy_threshold < 2000):
                    r.energy_threshold = 2000
                # print("Set minimum energy threshold to {}".format(r.energy_threshold))

                print("\r聆聽指令中...",end="")
                audio = r.listen(source)
                print("\r正在為您搜尋",end="")

                speechtext = r.recognize_google(audio,language='zh',show_all=True) #Load Google Speech Recognition API
                # print(type(speechtext)) #dict
                if len(speechtext) == 0:
                    pass
                else:
                    speechtext = speechtext['alternative'][0]['transcript']
                    speechtext = speechtext.replace(' ', '')
                    print("You said: " + speechtext)

                    for key in commandsInput.keys():
                        if key in speechtext:
                            print(commandsInput[key][1])
                            return commandsInput[key][0]

    except KeyboardInterrupt:
        print("Quit")
        return 



