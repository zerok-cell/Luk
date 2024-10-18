from colorama import Fore, Style
from pyaudio import PyAudio, paInt16
from logging import debug
from other.tools import getconfig



class SpeachToText:
    def __init__(self):
        self.device = 1
        self.sampl = 16000
        self.mic = PyAudio()
        self.stream = self.mic.open(
            format=paInt16,
            channels=self.device,
            rate=self.sampl,
            input=True,
            frames_per_buffer=2048,
        )
        self.config = getconfig()

    def checksumm(self, text):
        from fuzzywuzzy.process import extractOne
        print(text)
        if len(text) >= 2:
            if extractOne('раджаб', text)[1] >= 40:
                print(12)
                return True
            return False

    async def speachtotext(self):
        from vosk import KaldiRecognizer, Model
        model = Model("model")
        recognizer = KaldiRecognizer(model, self.sampl)
        self.stream.start_stream()
        print(Fore.GREEN + Style.BRIGHT + "Начинаем распознавание...")
        while True:
            data = self.stream.read(1024, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                from json import loads
                text = str(loads(result)["text"])
                split_text = text.split()
                if len(text) == 0:
                    continue
                if exitstluk := self.checksumm(split_text):
                    return ' '.join(split_text)
                continue
            # else:
            #     partial_result = recognizer.PartialResult()
            #     partial_text = loads(partial_result)["partial"]

            #     if partial_text == "стоп":
            #         exit()
