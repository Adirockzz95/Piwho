# speaker recognition module for jasper
# this module follows dev branch convention of writing modules

from jasper import plugin

from piwho import recognition

class SpeakerPlugin(plugin.SpeechHandlerPlugin):
    def get_phrases(self):
        return [self.gettext("GOOD MORNING")]

def handle(self, text, mic):
    recog = recognition.SpeakerRecognizer('/home/pi/jasper-client/recordings/')
    name = []
    name = recog.identify_speaker()
    mic.say("Good morning " + name[0])


def is_valid(self, text):
    return any(p.lower() in text.lower() for p in self.get_phrases())
    

