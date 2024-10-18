from other.tools import BaseFromCommand


class Plugin(BaseFromCommand):
    def __init__(self, text:str):
        self.text = text

    def execute(self):
        print(self.text)

    def __str__(self):
        docs: str = "RJB"
        return docs
    
