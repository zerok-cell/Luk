from abc import ABC, abstractmethod
from functools import lru_cache




@lru_cache(1)
def getconfig() -> dict:
    from os import environ
    with open("config.yaml", "r", encoding='utf-8') as file:
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
    def execute(self):
        pass

    @abstractmethod  
    def __str__(self):
        pass



    def word_check(self, text:dir, word:str, sensity:int):
        from fuzzywuzzy.process import extractOne
        if  extractOne(word, text)[1] >= sensity:
            self.execute()


   

