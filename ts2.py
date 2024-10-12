import  pyttsx3
from time import sleep
ix = pyttsx3.init()

for i in range(1,1000):
    sleep(1)
    ix.say("спасибо папа")
    ix.runAndWait()
    print("Спасибо пап")