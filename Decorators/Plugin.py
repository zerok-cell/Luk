

def serializer_combo_class(cls):
    class Wrapper(cls):
        def __init__(self, text):
            if isinstance(text, list):
                super().__init__(' '.join(text))
            else:
                super().__init__(text)
    return Wrapper
