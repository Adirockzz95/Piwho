Piwho
=====

Piwho is python wrapper around `MARF <http://marf.sourceforge.net/>`__
speaker recognition framework for the Raspberry pi and other SBCs. With
the Piwho you can implement speaker recognition in your projects.

.. image :: https://travis-ci.org/Adirockzz95/Piwho.svg?branch=master

|

**Blink example**

.. code:: python


    import RPi.GPIO as GPIO
    import time
    from piwho import recognition

    def blink(pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT) 

        for i in range(0,10):
            GPIO.output(pin,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(pin,GPIO.LOW)
            time.sleep(1)
       
    if __name__ == "__main__":
       recog = recognition.SpeakerRecognizer()
       name = recog.identify_speaker()
       if name == 'Ankit':
           blink(11)

Tested on
---------

-  Ubuntu 15.10
-  Pi 1 model B (raspbian wheezy, jessie)
-  Pi 2 model B (raspbian wheezy, jessie)
-  CHIP

Installation
------------

Update the Pi

.. code:: bash

    $ sudo apt-get update
    $ sudo apt-get upgrade

You need to have JDK (min version: 1.6) installed on your Pi.

.. code:: bash

    # verify jdk is installed
    $ java -version

SoX is required for wav resampling

.. code:: bash

    $ sudo apt-get install sox

Pyaudio is required to run audio recording script. (Optional)

.. code:: bash

    # Install portaudio
    $ sudo apt-get install portaudio19-dev
    # Install python2.7-dev
    $ sudo apt-get install python2.7-dev
    # Install pyaudio
    $ pip install pyaudio 

Piwho is on PyPI

.. code:: bash

    $ pip install piwho

or clone the project from github

.. code:: bash

    $ git clone https://www.github.com/Adirockzz95/Piwho.git
    $ cd piwho
    $ python setup.py install

Tests
-----

Tests are implemented using unittest framework:

.. code:: bash

    $ sudo apt-get install sox
    $ pip install -r requirements.txt
    $ python -m unittest discover -v ./tests

Documentation
-------------

-  `Training the model <docs/trainingmodel.rst>`__\ 
-  `Recognition <docs/recognition.rst>`__\ 
-  `Gender detection <docs/gender_piwho.rst>`__\ 
-  `integrating with Jasper <docs/jasper.rst>`__
-  `API <docs/API.rst>`__

Tips / Caveats
--------------

-  Even though it works on Raspberry Pi, it is relatively slow. :(
-  Recognition/Training time depends on the length of an audio file.
-  If possible overclock your Pi- use Turbo mode.
-  Give maxmium RAM to CPU.
-  Read `MARF
   manual <http://marf.sourceforge.net/docs/marf/0.3.0.5/report.pdf>`__
   to know how the MARF works.
-  Recognition speed is directly proportional to the CPU power.

Misc
----

Here are resources/similar projects I came across while working on this
project.

-  `recognito <https://github.com/amaurycrickx/recognito>`__ : Works
   very well on Pi, but data storage is not implemented.
-  `voiceid <https://code.google.com/archive/p/voiceid/>`__
-  `ALIZE <http://mistral.univ-avignon.fr/>`__
-  `Shout <http://shout-toolkit.sourceforge.net/use_case_diarization.html>`__
-  `MARF
   manual <http://marf.sourceforge.net/docs/marf/0.3.0.5/report.pdf>`__
-  `LIUM
   site <http://www-lium.univ-lemans.fr/diarization/doku.php/welcome>`__


LICENSE
-------
`MIT <./LICENSE>`__
