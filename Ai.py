from queue import Queue
from random import choice
from sounddevice import play, stop
from time import sleep
from soundfile import read
from ollama import chat
from texttospeach import TextToSpeach
import threading
from pathlib import Path


class Ai(TextToSpeach):
    def __init__(self) -> None:
        super().__init__()
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
        self.all_path = [file for file in Path("./timeslep/").glob("*")]

    def expectation(self):
        choicewav = choice(self.all_path)
        s, f = read(choicewav)
        play(s, 24000)
        sleep(len(s) / 24000 + 1)
        stop()

    def question(self, text):
        self.expectation()
        data_in_pamat_user = {"role": "user", "content": text}
        self.pamat.append(data_in_pamat_user)
        stream = chat(
            model=self.model,  # Это должно быть строковым идентификатором модели, а не объектом модели
            messages=self.pamat,
            stream=True,
        )
        chunk_dot = []
        for_pamat = []
        red_symbol = ("?", "", ".")
        for _word in stream:
            chunk_dot.append(_word["message"]["content"])

            if chunk_dot[-1] in red_symbol:
                self.data.put("".join(chunk_dot))
                print("1")
                for_pamat = for_pamat + chunk_dot
                chunk_dot.clear()
                x = threading.Thread(target=self.texttospeach)
                x.start()

        res_text = "".join(for_pamat)
        print(res_text)
        luk_pamat = {"role": "Люк", "content": res_text}
        self.pamat.append(luk_pamat)
        print(self.pamat)
