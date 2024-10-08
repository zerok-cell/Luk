import asyncio

import torch
from sounddevice import play, stop
from time import sleep


from fuzzywuzzy import process


class TextToSpeach:
    def __init__(self) -> None:
        super().__init__()  # Используйте super().__init__() для вызова конструктора базового класса
        self.local_file = "./voiceModel/v4_ru.pt"
        self.tts_model = torch.package.PackageImporter(self.local_file).load_pickle(
            "tts_models", "model"
        )
        self.speaker = "aidar"

    def checksumm(self, text: list[str]):
        if process.extractOne("Люк", text)[1] > 60:
            return True
        return False

    def texttospeach(self):
        # res = self.speachtotext()
        # print(res)
        # self.question(
        #     res
        # )
        _device = torch.device("cpu")
        torch.set_num_threads(8)
        self.tts_model.to(_device)
        print("312312")
        while True:
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
