from abc import ABC, abstractmethod
from functools import lru_cache


@lru_cache(1)
def getconfig() -> dict:
    from os import environ
    from os.path import join, dirname
    config_path = join(dirname(__file__), "config.yaml")
    with open(config_path, "r", encoding='utf-8') as file:
        from yaml import safe_load
        config = safe_load(file)
        environ['CodyDebug'] = config['DEBUG']['STATUS']
        print(environ['CodyDebug'])
        return config


def logging_message(level: str, text: str):
    from loguru import logger
    from os import environ
    if environ['CodyDebug']:
        match level:
            case "info":
                logger.info(text)
            case "debug":
                logger.debug(text)
            case "warning":
                logger.warning(text)
            case "critical":
                logger.critical(text)
    else:
        return


class BaseFromCommand(ABC):
    @abstractmethod
    def __init__(self, text: list[str], word: str):
        self.text = text
        self.word = word
        self.sensity = getconfig()['COMMAND']['sensity']

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    def word_check(self, ):
        from fuzzywuzzy.process import extractOne
        data = extractOne(self.word, self.text)[1]
        if data >= self.sensity:
            return True
        return False
