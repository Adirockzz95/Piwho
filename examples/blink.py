
import time
import Rpi.GPIO as GPIO
from piwho import recognition


def blink(pin):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(1)

def identify():
    recog = recognition.SpeakerRecognizer('./recordings/')
    friends = ['Abhishek', 'Ankit', 'Abhinav']
    name = recog.identify_speaker()
    if name[0] in names:
        for i in range(10):
            blink(11)
    elif name[1] in friends:
        for in range(10):
            blink(12) 


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    identify()
    GPIO.cleanup()
   
