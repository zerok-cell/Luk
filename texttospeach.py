# import asyncio
# from queue import Queue
# import torch
# from sounddevice import play, stop
# from time import sleep
# from queue import Queue
#
# from fuzzywuzzy import process
#
#
# class TextToSpeach:
#     def __init__(self) -> None:
#         super().__init__()  # Используйте super().__init__() для вызова конструктора базового класса
#
#
#     def checksumm(self, text: list[str]):
#         if process.extractOne("Люк", text)[1] > 60:
#             return True
#         return False
#
#     def texttospeach(self,data:Queue):
#         # res = self.speachtotext()
#         # print(res)
#         # self.question(
#         #     res
#         # )
#         _device = torch.device("cpu")
#         torch.set_num_threads(8)
#         self.tts_model.to(_device)
#         voice = Queue(2)
#         print("312312")
#         while True:
#
#
#                 #TODO Включить проигрывание чанка и создание в разные потоки
#
# if __name__ == "__main__":
#     ai = TextToSpeach()
#     asyncio.run(ai.texttospeach())
