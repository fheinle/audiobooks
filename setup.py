#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""audiobooks

helps with preparation of audio book files (.m4b)

 * chapter marks
 * metadata
"""

from setuptools import setup

setup(name='audiobooks',
      version='0.1',
      description='helper for audiobook (.m4b) creation',
      url='http://github.com/fheinle/audiobooks',
      author='Florian Heinle',
      author_email='launchpad@planet-tiax.de',
      license='MIT',
      packages=['audiobooks'],
      zip_safe=False,
      install_requires=[
        'mutagen',
        'cached-property',
      ],
      entry_points={
            'console_scripts':[
                'audiobooks = audiobooks.app:main',
        ]
      }
)
