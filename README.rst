piwho
=====

Piwho is python wrapper around `MARF <http://marf.sourceforge.net/>`__
speaker recognition framework for the Raspberry pi and other SBCs. Piwho
brings speaker recognition into your Pi projects.


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

Then install **piwho**

.. code:: bash

    $ pip install piwho

or clone the project from github

.. code:: bash

    $ git clone https://www.github.com/Adirockzz95/Piwho.git
    $ cd piwho
    $ python setup.py install

Documentation
-------------
See `Github Repository <https://www.github.com/Adirockzz95/Piwho/>`__ for documentation.

