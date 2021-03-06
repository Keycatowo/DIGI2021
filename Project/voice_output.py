from gtts import gTTS
from pygame import mixer
import tempfile
import time

def speak(sentence, lang="en", loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(1)

def praise(label):
    s = []
    s.append(("you are awesome!", "en"))
    s.append(("恭喜你找到了%s" % label, "zh"))

    for sentence, lang in s:
        # print(sentence)
        speak(sentence,lang)
        time.sleep(2)


def ans_is_wrong(find, right):
    s = []
    s.append(("You found %s" % find, "en"))
    s.append(("This is not the answer", "en"))
    s.append(("You should find %s" % right , "en"))

    for sentence,lang in s:
        # print(sentence)
        speak(sentence,lang)
        time.sleep(2)

def say_welcome():
    s = []
    s.append(("歡迎使用DIGI牌學習相機", "zh"))
    s.append(("Welcome to using DIGI study camera!", "en"))
    s.append(("請選擇自由拍照模式或是物品探索模式", "zh"))

    for sentence,lang in s:
        # print(sentence)
        speak(sentence,lang)
        time.sleep(3)
