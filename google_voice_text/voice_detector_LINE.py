import speech_recognition as sr
import time
import threading
import re
import requests

event_name_line='XXXXXXXXXXXXXXXXXXXXXXX'

key='KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK'

URL_line='https://maker.ifttt.com/trigger/' + event_name_line + '/with/key/' + key

AC=0
FAN=0
LIGHT=0

try:

    while True:
        r = sr.Recognizer()
        m = sr.Microphone()
        m.RATE = 44100
        m.CHUNK = 512

        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
            if (r.energy_threshold < 2000):
                r.energy_threshold = 2000
            print("Set minimum energy threshold to {}".format(r.energy_threshold))

            print("Say something!")
            audio = r.listen(source)
            print("Got it! Now to recognize it...")

            speechtext = r.recognize_google(audio,language='zh',show_all=True) #Load Google Speech Recognition API
            print(type(speechtext)) #dict

            if len(speechtext) == 0:
                pass
            else:
                speechtext = speechtext['alternative'][0]['transcript']
                speechtext = speechtext.replace(' ', '')
                print("You said: " + speechtext)

                if re.search('\s*開冷氣\s*',speechtext):
                    print('冷氣機已開啟')
                    AC=1

                elif re.search('\s*關冷氣\s*',speechtext):
                    print('冷氣機已關閉')
                    AC=0   

                elif re.search('\s*開電扇\s*',speechtext):
                    print('電風扇已開啟')
                    FAN=1  

                elif re.search('\s*關電扇\s*',speechtext):
                    print('電風扇已關閉')
                    FAN=0   

                elif re.search('\s*開電燈\s*',speechtext):
                    print('電燈已開啟')
                    LIGHT=1

                elif re.search('\s*關電燈\s*',speechtext):
                    print('電燈已關閉')
                    LIGHT=0

                elif re.search('\s*發送手機訊息\s*',speechtext):
                    print('訊息已發送至手機')
                    if (AC==1):
                        text_AC = '冷氣已開啟'
                    else:
                        text_AC = '冷氣已關閉'

                    if (FAN==1):
                        text_FAN = '電風扇已開啟'
                    else:
                        text_FAN = '電風扇已關閉'

                    if (LIGHT==1):
                        text_LIGHT = '電燈已開啟'
                    else:
                        text_LIGHT = '電燈已關閉'
                    
                    r_line = requests.post(URL_line, params={"value1":text_AC,"value2":text_FAN,"value3":text_LIGHT})

                elif re.search('\s*結束程式\s*',speechtext):
                    print('結束程式運作')
                    break
 
                    
except KeyboardInterrupt:
    print("Quit")



