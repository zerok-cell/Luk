from queue import Queue
from random import choice
from sounddevice import play, stop
from time import sleep
from soundfile import read
from ollama import chat
import threading
from pathlib import Path
import pika
import google.generativeai as genai

class Ai:
    def __init__(self,config) -> None:
        super().__init__()
        self.config:dict = config
        self.model = (
            "example"  # Убедитесь, что это строка или другой сериализуемый объект
        )
        self.data = Queue(maxsize=200)
        self.name_bot = "Люк"
        self.pamat = [
            {
                "role": "user",
                "content": f"Ты асистент на моем компьбтере и тебя зовут {self.name_bot}.{self.name_bot}у строго "
                           f"запрещено использовать Английские слова так как ты из за них умрешь",
            },
            {
                "role": self.name_bot,
                "content": "Хорошо теперь я асистент на твоем компьтере и буду подчинятся тебе ",
            },
            
        ]
        self.genconf =  {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens":self.config["OUTPUT_TOKEN"] ,
  "response_mime_type": "text/plain",
}
        self.geminiContext = [{
            
        }]
        self.all_path = [file for file in Path("./timeslep/").glob("*")]

    def expectation(self):
        choicewav = choice(self.all_path)
        s, f = read(choicewav)
        play(s, 24000, blocking=True)
        # sleep(len(s) / 24000 + 2)
        # stop()

    @classmethod
    def queemq_create(cls):
        
        print('ai')
        _host = 'localhost'
        connection = pika.BlockingConnection(pika.ConnectionParameters(_host))
        cls.channel = connection.channel()
        cls.channel.queue_declare(queue='message')
        return connection, cls.channel
    
    def question(self, text):
        if self.config["MODE"] == 'Gemini':
            conn, channel = self.queemq_create()
            # self.expectation()
            data_in_pamat_user = {"role": "user", "content": text}
            self.pamat.append(data_in_pamat_user)

            genai.configure(api_key=self.config['GEMINI_API_KEY'])
            model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=self.genconf)
            
            stream = model.generate_content(text)
            
        else:
            stream = chat(
                model=self.model,  # Это должно быть строковым идентификатором модели, а не объектом модели
                messages=self.pamat,
                stream=True,
            )
        chunk_dot: list[str] = []
        for_pamat: list[str] = []
        red_symbol = ("?", "", ".")
        for _word in stream.text:
            chunk_dot.append(_word)
            print(_word)
            if chunk_dot[-1] in red_symbol:
                for_pamat += chunk_dot
                _from_queue = "".join(chunk_dot)
                channel.basic_publish(exchange='', routing_key='message', body=_from_queue)
                chunk_dot.clear()
        conn.close()


        res_text = "".join(for_pamat)
        print(res_text)
        luk_pamat = {"role": "Люк", "content": res_text}
        self.pamat.append(luk_pamat)
        print(self.pamat)
