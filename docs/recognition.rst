Recognition
===========

-  make sure you have ``.gzbin`` model and ``speakers.txt`` in your
   current directory i.e where your python script is located.
-  make sure ``speakers.txt`` is not empty.

 Use newly added file in current directory for recognition:

.. code:: python

    >> from piwho import recognition
    >> recog = recog.SpeakerRecognizer()
    >> name = recog.identify_speaker()
    >> print name

Or specify directory to get newly added file for recognition:

.. code:: python

    >> from piwho import recognition
    >> recog = recog.SpeakerRecognizer('/home/pi/recordings/')
    >> name = recog.identify_speaker()
    >> print name

Or specify the file explicitly:

.. code:: python

    >> from piwho import recognition
    >> recog = recog.SpeakerRecognizer()
    >> name = recog.identify_speaker('/home/pi/recordings/test1.wav')
    >> print name

After running recognizer for at least one time, you can print distance
of each speaker from the recognized audio file.

.. code:: python

    >> dictn = recog.get_speaker_scores()
    >> print dictn
    {'ABC':'0.838262623','CDF':'1.939837286'}
    >> #Lower the distance closer the speaker to the recognized audio


Python audio recording script is also included. Here's a complete
program which records audio and recognizes the speaker.

**Note:** This requires Pyaudio library installed.

.. code:: python


    from piwho import recognition
    from piwho import vad

    def find_speaker():
        recog = recognition.SpeakerRecognizer()

        # Record voice until silence is detected.
        # save WAV file
        vad.record()
     
        # use newly recorded file.
        name = recog.identify_speaker()
        return name
        
    if __name__ == "__main__":
        speaker = find_speaker()
        print speaker
