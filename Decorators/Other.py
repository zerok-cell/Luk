import time


def timedecorator(func):
    def wrapper(*args, **kwargs):
        s = time.time()
        result = func(*args, **kwargs)
        print(f"Время выполнения функции {func.__name__}: {time.time() - s}")
        return result

    return wrapper
