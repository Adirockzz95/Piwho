# recognizing the speaker
# This assumes that you've trained the model and .gzbin and speakers.txt 
# exists in ~/jasper/ folder i.e where jasper.py sits.

from piwho import recognition
import re
WORDS = ["GOOD","MORNING"]

def greetings():
    recog = recognition.SpeakerRecognizer('/path/to/recordings/')
    name = []
    name = recog.identify_speaker()
    return name[0]

def handle(text, mic, profile):
    speaker = greetings()
    mic.say(" Good morning " + speaker)

def isValid(text):
    return bool(re.search(r'\bgood morning\b',text,re.IGNORECASE))

