# Shutdown computer

from piwho import recognition
import subprocess
import re

WORDS = ['SHUTDOWN']

CMD = ['sudo','shutdown','-h','now']


def shutdown(mic, text):
    recog = recognition.SpeakerRecognizer('~/jasper/recordings/')
    mic.say('Do you want to shutdown the computer?')
    response = mic.ActiveListen()
    if response == 'YES':
        # prompt user for recording
        mic.say('Record your voice after high beep')
        # record your voice: Say anything
        mic.activeListen()

       # use voice file to identify speaker name
        name = recog.identify_speaker()
        if name == 'ABC':
            mic.say('Shutting down')
            subprocess.call(CMD)
        else:
            mic.say('
    


def handle(text, mic, profile):
    shutdown(mic, text)
