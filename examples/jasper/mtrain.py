# Training model
# If module executes successfully, you should see .gzbin model and 
# speakers.txt in your ~/jasper/ i.e where jasper.py sits.

"""
NOTE:
Even though you can train model by calling jasper modules, it is not an efficient way to do it.
Train model separately and just copy-paste the .gzbin model and speakers.txt into your jasper folder.
"""

#import piwho library
from piwho import recogntion
import re

WORDS = ["TRAIN"]

def train():
    # use recently added file from the directory 'recordings'
    recog = recognition.SpeakerRecognizer('/home/pi/jasper/recordings/')
    # set speaker lable for training
    recog.speaker_name = 'Aditya'
    # this will print some useful logs for debugging
    # you should see a message saying "done training with [filename].wav"
    recog.debug = True
    # train model
    recog.train_new_data()

def handle(text, mic, profile):
    train()

def isValid(text):
    return bool(re.search(r'\btrain\b',text,re.IGNORECASE))
