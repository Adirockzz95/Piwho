Training model
--------------

-  You have to train model for at least two speakers.
-  All wav files should be of following format:

::

     Audio Format: PCM signed (WAV)
     Sample Rate: 8000 Hz
     Audio Sample Size: 16 bit
     Channels: 1 (mono)

If not then the file will be converted into above format. This will overwrite original file.

-  Running the training program for the first time will create a
   ``.gzbin`` model and ``speakers.txt`` in your current directory.

-  ``speakers.txt`` stores the file name with its ``speaker label`` and
   ``ID`` , ``.gzbin`` model stores the extracted features from your
   audio file.

-  Every time you train an existing model with a new file, model gets
   updated.

Use newly added file in current directory for training:

.. code:: python

    >> from piwho import recognition
    >> recog = recognition.SpeakerRecognizer()
    >> recog.speaker_name = 'ABC'
    # setting debug = True will print MARF's stdout as it is.
    >> recog.debug = True
    >> recog.train_new_data()

Or specify directory to get newly added file for training:

.. code:: python

    >>recog = recognition.SpeakerRecognizer('/home/pi/recordings/')
    >> recog.speaker_name = 'ABC'
    >>recog.train_new_data()

Or explicitly specify the file:

.. code:: python

    >>recog = recognition.SpeakerRecognizer()
    >> recog.speaker_name = 'ABC'
    >>recog.train_new_data('/home/pi/recordings/test1.wav')

.. code:: python

    # one liner
    # speaker name will be used for this single file or directory only.
    >> recog.train_new_data('/home/pi/recordings/test1.wav','ABC')

Or train an entire folder:

.. code:: python

    >>recog = recognition.SpeakerRecognizer()
    >> recog.speaker_name = 'ABC'
    >>recog.train_new_data('/home/pi/recordings/')

Once done with the training, you can get list of speakers from database.

.. code:: python

    >> print recog.get_speakers()
    ['ABC','DEF']

Python audio recording script is also included. Here's a complete
program which records audio and trains the model.

**Note:** This requires Pyaudio library installed.

.. code:: python


    from piwho import recognition
    from piwho import vad

    def train_speaker():
        recog = recognition.SpeakerRecognizer()
        recog.speaker_name = 'ABC'

        # Record audio until silence is detected
        # save WAV file
        vad.record()

        # train model with the newly recorded file
        recog.train_new_data()


Automatic training 
------------------

Automatic Training is used when you're recording files periodically.
This is done by creating a service that monitors specified directory and
trains the model automatically with newly added file.

.. code:: python

    >> from piwho import recognition
    >> import time
    >> recog = recognition.SpeakerService('/home/pi/recordings/')
    >> # set speaker name for service
    >> recog.speaker_name = 'ABC'
    >> try:
    >>     recog.start_service()
    >>     while True:
    >>         time.sleep(0.5)
    >> except KeyboardInterrupt:
    >>     recog.stop_service()

This will start a listener on the directory ``recordings``. All you need
to do is just copy-paste the wav files into the directory path passed in
the constructor. The program will train model with a new file under
given speaker name.

To stop the service press ``Ctrl+C`` .

**useful functions:**

Print pid of current service:

.. code:: python

    >> print recog.pid 
    2121

Check if service is alive:

.. code:: python

    >> recog.is_alive
    True

Set feature extraction option:

.. code:: python

    >> recog.set_feature_option('-lpc -cheb')
