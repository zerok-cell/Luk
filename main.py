import ollama
import asyncio
from queue import Queue
import torch
from sounddevice import play, stop, RawInputStream
from time import sleep
from pathlib import Path
import os
import random
from soundfile import read
import vosk
from vosk import KaldiRecognizer
import json
import pyaudio
from fuzzywuzzy import fuzz, process
from commands import syscom


class Ai:
    def __init__(self) -> None:
        self.model = (
            "example"  # Убедитесь, что это строка или другой сериализуемый объект
        )
        self.data = Queue(maxsize=200)
        self.name_bot = "Люк"
        self.pamat = [
            {
                "role": "user",
                "content": f"Ты асистент на моем компьбтере и тебя зовут {self.name_bot}.{self.name_bot} твои ответы должны  максимально краткие потомучто ты работаешь на моем пк и у тебя 8 милиардов параметров, моему пк будет тяжело поэтому пократче,Также тебе строго запрещено использовать Английские слова так как ты из за них умрешь",
            },
            {
                "role": self.name_bot,
                "content": "Хорошо теперь я асистент на твоем компьтере и буду подчинятся тебе ",
            },
            {
                "role": "user",
                "content": """Теперь я раскажу про некоторые команды которые ты должен определить из моего сообщение(ты должен понять что я имею ввиду и использовать нужную команду) 
                1) Выключение устройства - shutdown now  
                
                Если ты не смог определить являеться мое сообщение запросом на команду то просто ответь на него. Также если я говорю что то вроде 'Пока люк','Выключись люк','Люк прощай'(Определи контекст моего сообщения сам) это значит что я выключаю тебя и ты должен вернуть просто '0'              
                """,
            },
        ]

    def expectation(self):
        choice = random.choice(self.all_path)
        s, f = read(choice)
        play(s, 24000)
        sleep(len(s) / 24000 + 0.2)
        stop()

    def question(self, text):
        self.expectation()

        data_in_pamat_user = {"role": "user", "content": text}
        self.pamat.append(data_in_pamat_user)
        stream = ollama.chat(
            model=self.model,  # Это должно быть строковым идентификатором модели, а не объектом модели
            messages=self.pamat,
            stream=True,
        )
        _ = []
        for _word in stream:
            print(_)
            _.append(_word["message"]["content"])
        res_text = "".join(_)
        luk_pamat = {"role": "Люк", "content": res_text}
        self.pamat.append(luk_pamat)
        print(self.pamat)
        self.data.put(res_text)  # Убедитесь, что здесь добавляются только строки


class TextToSpeach(Ai):
    def __init__(self) -> None:
        super().__init__()  # Используйте super().__init__() для вызова конструктора базового класса
        self.local_file = "./v4_ru.pt"
        self.tts_model = torch.package.PackageImporter(self.local_file).load_pickle(
            "tts_models", "model"
        )
        self.speaker = "aidar"
        self.all_path = [file for file in Path("./timeslep/").glob("*")]

    def schecksum(self, text: list[str]):
        print(text)
        if process.extractOne("Люк", text)[1] > 60:
            return True
        return False

    def speachtotext(self):
        model = vosk.Model("model")

        sampl = 16000
        device = 1
        samplerate = 16000
        recognizer = vosk.KaldiRecognizer(model, samplerate)

        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
        stream.start_stream()

        print("Начинаем распознавание...")

        while True:
            data = stream.read(3000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)["text"]
                if text == "стоп":
                    exit()

                if (text != "" and " ") and (len(text) > 2):
                    syscom.off(text)
                    print(",".split("dawdwd dwwd"))
                    exitstLuk = self.schecksum(text.split())
                    if exitstLuk:
                        return text
                    continue
            else:
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result)["partial"]
                print(partial_text)
                if partial_text == "стоп":  # Проверка частичного результата
                    exit()

    async def texttospeach(self):
        while True:
            res = self.speachtotext()
            self.question(
                res
            )  # Вызовите question без использования super(), так как он уже наследуется
            _device = torch.device("cpu")
            torch.set_num_threads(8)
            self.tts_model.to(_device)  # Используйте self.tts_model вместо self.model

            if self.data.qsize() != 0:
                _message: str = self.data.get()
                if _message == "0":
                    exit()
                _sample_rate = 24000
                audio = self.tts_model.apply_tts(
                    text=_message, speaker=self.speaker, sample_rate=_sample_rate
                )
                play(audio, _sample_rate)
                sleep(len(audio) / _sample_rate + 2)
                stop()


if __name__ == "__main__":
    ai = TextToSpeach()
    asyncio.run(ai.texttospeach())
