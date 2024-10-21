
from Command.ExecutePlugins import LaunchPlugin
from Other.tools import getconfig


class SpeachToText:
    def __init__(self):
        from pyaudio import PyAudio, paInt16
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
        self.x = LaunchPlugin()

    def checksumm(self, text):
        from fuzzywuzzy.process import extractOne
        if extractOne('раджаб', text)[1] >= 90:
            print(extractOne('раджаб', text)[1])
            return True
        else:
            x = self.x.executeplugin(text)
            return False

    def speachtotext(self):
        from colorama import Fore, Style

        from vosk import KaldiRecognizer, Model
        model = Model(r"C:\Users\User\PycharmProjects\CodyV2\VoiceAi\model")
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
                exitstluk = self.checksumm(split_text)

                if exitstluk:
                    return ' '.join(split_text)
                continue
            # else:
            #     partial_result = recognizer.PartialResult()
            #     partial_text = loads(partial_result)["partial"]

            #     if partial_text == "стоп":
            #         exit()



