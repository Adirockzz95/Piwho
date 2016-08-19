import pyaudio
import wave
import audioop
from collections import deque
import time
import math
import datetime


# Microphone stream config.
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000

# The threshold intensity that defines silence
# and noise signal (an int. lower than THRESHOLD is silence).
THRESHOLD = 2400

# Silence limit in seconds. The max ammount of seconds where
# only silence is recorded. When this time passes the
# recording finishes and the file is delivered.
SILENCE_LIMIT = 0.6

# Previous audio (in seconds) to prepend. When noise
# is detected, how much of previously recorded audio is
# prepended. This helps to prevent chopping the beggining
# of the phrase.
PREV_AUDIO = 0.3


def record(threshold=THRESHOLD, silence=SILENCE_LIMIT):
    """
    Listens to Microphone, records voice until phrase ends.

    A "phrase" is sound surrounded by silence (according to threshold).

    :param int threshold: Intensity value that defines silence.
      lower than threshold is silence.
    :param silence: Max ammount of seconds where only silence is
      recorded. When this time passes the recording finishes.
    """

    # Open stream
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print ("* Listening mic. ")
    frames = []
    cur_data = ''
    rel = RATE/CHUNK
    window = deque(maxlen=silence * rel)
    prev_audio = deque(maxlen=PREV_AUDIO * rel)
    start = False
    exit_loop = 0

    while (exit_loop != 1):
        cur_data = stream.read(CHUNK)
        window.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        if(sum([x > THRESHOLD for x in window]) > 0):
            if(not start):
                print ("recording..")
                start = True
            frames.append(cur_data)
        elif start is True:
            print ("Finished")
            save_audio(list(prev_audio) + frames, p)
            start = False
            window = deque(maxlen=silence * rel)
            prev_audio = deque(maxlen=0.5 * rel)
            frames = []
            exit_loop = 1
        else:
            prev_audio.append(cur_data)

    print ("Done recording")
    stream.close()
    p.terminate()


def save_audio(data, params):
    """ Saves mic data to wav file."""

    filename = gettime()
    data = ''.join(data)
    wf = wave.open(filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(params.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def gettime():
    """
    Return timestamp string.
    """
    current = time.time()
    tformat = datetime.datetime.fromtimestamp(current).strftime('%d:%H:%M:%S')
    return tformat
