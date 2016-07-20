
import time
import Rpi.GPIO as GPIO
from piwho import recognition


def blink(pin):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(1)

def authorize():
    recog = recognition.SpeakerRecognizer('./recordings/')
    name = recog.identify_speaker()
    if name == 'ABCD':
        return True
    else:
        return False


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    if authorize():
        for i in range(5):
            blink(11)

    GPIO.cleanup()
   
