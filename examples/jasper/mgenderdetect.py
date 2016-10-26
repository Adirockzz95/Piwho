
import re
from piwho import recognition
try:
    from gdetect import genderdetect as gd
except:
    raise ImportError('genderdetect module is not installed')
    
WORDS = ["GOOD","MORNING"]


def sayHello(mic):
    recog = recognition.SpeakerRecognizer('/home/pi/jasper/recordings/')
    name = []
    name = recog.identify_speaker()

    # I have trained the model with 30 voice clips with lable 'Aditya'
    # These sound clips contain only my voice.
    if 'Aditya' in name:
        mic.say("Good morning "+ name)

    # Then trained the SAME model with 40 random voice clips with lable 'unknown'
    # excluding my voice.
    # This makes it easy to distinguish between two speakers.
    elif 'unknown' in name:
        gender = gd.identify_gender(recog.get_recently_added_file())
        if 'M' in gender:
            mic.say('Good morning Sir')
        elif 'F' in gender:
            mic.say('Good morning Madam')
            
def handle(text, mic, profile):
    sayHello(mic)

def isValid(text):
    return bool(re.search(r'\bgood morning\b',text,re.IGNORECASE))
