
from Other.tools import BaseFromCommand
from Decorators.Plugin import serializer_combo_class


@serializer_combo_class
class Plugin(BaseFromCommand):
    def __init__(self, text: str):
        self.text: str = text
        self.word = [
            'выключить',
            'открыть проводник',
            'закрыть',
            'открой'

        ]

        from Other.tools import word_association_table
        self.off = word_association_table(['выключить',
                                           'выкл',
                                           'выключи',
                                           'выключать',
                                           'выключено',
                                           'выключение'], func=self.offpc)
        self.open = word_association_table(['открыть', 'открой'], func=self.openapp)

        # Добавляем все возможные формы слов для Fuzz

        super().__init__(text, self.word)

    def openapp(self):
        pass

    def offpc(self):
        print('off')

    def __call__(self):
        print('2')

    def __str__(self):
        docs: str = "Pligin from open explorer"
        return docs

    def word_check(self):
        from fuzzywuzzy.process import extractBests

        return extractBests(query=self.text, choices=self.word, limit=4)