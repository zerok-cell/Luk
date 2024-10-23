import time


def timedecorator(func):
    def wrapper(*args, **kwargs):
        s = time.time()
        result = func(*args, **kwargs)
        print(f"Время выполнения функции {func.__name__}: {time.time() - s}")
        return result

    return wrapper


def repeat(count: int):
    if not isinstance(count, int) or count <= 0:
        raise ValueError("Аргумент count должен быть положительным целым числом.")

    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(count):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    from Errors.RepeatErrors import RepeatErrors
                    raise RepeatErrors(
                        f"Calling {func} again did not lead to anything, try looking at the logs or "
                        f"find out the cause of the error yourself: {e}")

        return wrapper

    return decorator



