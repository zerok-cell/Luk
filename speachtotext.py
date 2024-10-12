

from colorama import Fore, Style
from pyaudio import PyAudio, paInt16




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

    def checksumm(self, text):
        from fuzzywuzzy.process import extractOne
        if extractOne('коде', text)[1] >= 80:
            return True
        return False

    def speachtotext(self):
        from vosk import KaldiRecognizer, Model
        model = Model("model")
        recognizer = KaldiRecognizer(model, self.sampl)

        self.stream.start_stream()

        print(Fore.GREEN + Style.BRIGHT + "Начинаем распознавание...")

        while True:
            data = self.stream.read(1024, exception_on_overflow=False)
            if len(data) == 0:
                break

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                from json import loads
                text = str(loads(result)["text"])
                print(text.strip())
                if (text.strip() != '') and (len(text) > 2):
                    text_split = text.split()
                    exitstluk = self.checksumm(text_split)
                    if exitstluk:
                        return text
                    return False

            # else:
            #     partial_result = recognizer.PartialResult()
            #     partial_text = loads(partial_result)["partial"]

            #     if partial_text == "стоп":
            #         exit()
