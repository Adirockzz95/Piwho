
# Training model
# this code follows dev branch convention of writing modules
# If module executes successfully, you should see .gzbin model and 
# speakers.txt in your ~/jasper/ i.e where jasper.py sits.

"""
NOTE:
Even though you can train model by calling jasper modules, it is not an efficient way to do it.
Train model separately and just copy-paste the .gzbin model and speakers.txt into your jasper folder.
"""
from jasper import plugin
from piwho import recognition


class SpeakerPlugin(plugin.SpeechHandlerPlugin):
    def get_phrases(self):
        return [self.gettext("TRAIN")]

def handle(self, text, mic):
    recog = recognition.SpeakerRecognizer('/home/pi/jasper-client/recordings/')
    recog.speaker_name = 'Aditya'
    recog.train_new_data()


def is_valid(self, text):
    return any(p.lower() in text.lower() for p in self.get_phrases())
    

