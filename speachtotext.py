from json import loads

from colorama import Fore, Style
from pyaudio import PyAudio, paInt16
from vosk import KaldiRecognizer, Model


class SpeachToText:
    def speachtotext(self):
        model = Model("model")

        sampl = 16000
        device = 1

        recognizer = KaldiRecognizer(model, sampl)

        mic = PyAudio()
        stream = mic.open(
            format=paInt16,
            channels=device,
            rate=sampl,
            input=True,
            frames_per_buffer=2048,
        )
        stream.start_stream()

        print(Fore.GREEN + Style.BRIGHT + "Начинаем распознавание...")

        while True:
            data = stream.read(1024, exception_on_overflow=False)
            if len(data) == 0:
                break

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = loads(result)["text"]

                if (text != "" and " ") and (len(text) > 2):
                    # exitstLuk = self.checksumm(text.split())
                    # if exitstLuk:
                    return text

            else:
                partial_result = recognizer.PartialResult()
                partial_text = loads(partial_result)["partial"]

                if partial_text == "стоп":
                    exit()
