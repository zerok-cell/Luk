from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Callable


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
    global __flags
    from loguru import logger
    from os import environ
    recursion_prevention_flag = 0
    try:
        __flags = environ['CodyDebug'] == 'On'
    except KeyError:
        getconfig()
        if recursion_prevention_flag == 3:
            from Errors.LoguruErrors import FailedToCreateVariable
            raise FailedToCreateVariable
        else:
            recursion_prevention_flag += 1
            logging_message(level, text)

    if __flags:
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

    def __new__(cls, *args, **kwargs):
        __metadata: dict = {cls.__name__: __file__}
        logging_message('info', f'Plugin Running {cls.__name__} from {__file__}. '
                                f'Metadata: {__metadata}')
        return super().__new__(cls)

    def word_check(self):
        from fuzzywuzzy.process import extractOne
        data = extractOne(self.word, self.text)[1]
        if data >= self.sensity:
            self()
            return True
        return False


def word_association_table(*args, func: Callable) -> dict[str, Callable]:
    def addindict(element: str, call: Callable):
        if isinstance(word, str):
            result[element] = element

    result: [str, Callable] = {}
    if isinstance(args[0], list):
        for word in args[0]:
            addindict(word, func)
    for word in args:
        addindict(word, func)
    return result


def checkdander(word):
    end = word[:2]
    start = word[-2:]
    if end and start == "__":
        return True
    return False
