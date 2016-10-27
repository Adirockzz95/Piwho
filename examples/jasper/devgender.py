
# speaker recognition module for jasper
# this code follows dev branch convention of writing modules
# gender detection

from jasper import plugin
from piwho import recognition
try:
   from gdetect import genderdetect as gd
except:
   raise ImportError('genderdetect modules is not installed')

class SpeakerPlugin(plugin.SpeechHandlerPlugin):
    def get_phrases(self):
        return [self.gettext("GOOD MORNING")]

def handle(self, text, mic):
    recog = recognition.SpeakerRecognizer('/home/pi/jasper-client/recordings/')
    name = []
    name = recog.identify_speaker()

    if name[0] == 'Aditya':
	mic.say("Good morning "+ name)
    else:
	if name[0] == 'unknown':
		gen = gd.identify_gender(recog.get_recently_added_file())
		if gen == 'M':
			mic.say("Good morning sir")
		elif gen == 'F':
			mic.say("Good morning madam")  


def is_valid(self, text):
    return any(p.lower() in text.lower() for p in self.get_phrases())
    

