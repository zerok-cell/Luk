from other.tools import getconfig


class LocalModel(object):
    def __init__(self):
        self.config: dict = getconfig()
        self.__memory_local: list[dict[str, str]] = [{
                "role": "user",
                "content": f"{self.config['GEMINI']['LLAMA_PROMT']}",
            },
            {
                "role": 'model',
                "content": "Замётано!!",
            },]
        self.__model: str = self.config["GEMINI"]["MODEL_NAMELLM"]

    def localmodel(self, text: str) -> str:
        from ollama import chat
        _user_text = {
            "role": "user",
            "content": text,
        },
        local = chat(
            model=self.__model,
            messages=self.__memory_local,

        )
        self.__memory_local.append(_user_text)
        _llama_text = {
            "role": "user",
            "content": local['message']['content'],
        },

        self.__memory_local.append(_llama_text)
        return local['message']['content']
