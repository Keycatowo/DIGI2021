import speech_recognition as sr
import time
import threading
import re
com = {'這是什麼':'1', '在哪裡':'2'}
def voice_input(commandDict, command):
    if command in commandDict:
        return commandDict[command]

