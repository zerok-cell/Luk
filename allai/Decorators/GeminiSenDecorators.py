from other.tools import logging_message


class GeminiSendDecorators(object):
    def __init__(self, func):
        self.responseobj = None
        self.func = func

    def _no_quta(self):
        from colorama import Fore
        print("The quota per minute is exhausted, switch to the paid API tariff or wait 1 minute for the quota "
              "to become 15 requests again")
        print(Fore.RED + "Request send after 1 minute")

    @staticmethod
    def protest():
        from soundfile import read
        from sounddevice import play
        from pathlib import Path
        from random import choice
        _protest = [file for file in Path(r"C:\Works\Luk\allai\song_protest").glob("*")]
        choicewav = choice(_protest)
        s, f = read(choicewav)
        play(s, 24000, blocking=True)

    def __call__(self,  *args, **kwargs):
        print('Hel dec')
        from google.generativeai.types.generation_types import StopCandidateException
        from google.api_core.exceptions import ResourceExhausted
        from google.api_core.exceptions import FailedPrecondition
        try:
            try:
                try:
                    return self.func(*args, *kwargs)
                except ResourceExhausted as e:
                    logging_message('waning', e)
                    self._no_quta()

            except FailedPrecondition as position:
                logging_message('warning', f"Not correct your possition {position}")
                self.responseobj.reqstatus = False
                return None

        except StopCandidateException as trp:
            self.protest()
            logging_message('warning', f"Policy error on user text: {text} - {stp}")
            self.res.reqstatus = False
            return None


