
from functools import lru_cache


@lru_cache(1)
def getconfig() -> dict:
    with open("config.yaml", "r", encoding='utf-8') as file:
        from yaml import safe_load
        config = safe_load(file)
        return config
