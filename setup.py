from setuptools import setup, find_packages
import os

from piwho import config

curr = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(curr,'README.rst')) as f:
    description = f.read()

setup(
      name='piwho',

      version=config.__VERSION__,

      url='https://github.com/Adirockzz95/PiWho',

      license='MIT',

      author='Aditya Khandkar',

      author_email='khandkar.adi@gmail.com',

      description=('A python wrapper around MARF speaker recognition framework'
                   'for raspberry pi and other SBCs'),

      long_description=description,

      packages=find_packages(exclude=['tests']),

      zip_safe=False,

      install_requires=[
          'watchdog>=0.8.3'
      ],
      include_package_data=True,
      package_data = {
            'piwho': ['marf/*.jar']
            },
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'Topic :: Multimedia :: Sound/Audio :: Speech',
      'Topic :: Multimedia :: Sound/Audio :: Analysis',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: Implementation :: CPython'
      ],
      
      keywords  = 'Speaker recognition Raspberry Pi MARF',
      )













