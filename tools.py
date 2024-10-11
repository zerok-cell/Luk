from yaml import safe_load
from functools import lru_cache


@lru_cache
def getconfig():
        with open("config.yaml", "r", encoding='utf-8') as file:
            config = safe_load(file)
            return config