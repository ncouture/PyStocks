#!/usr/bin/env python

from distutils.core import setup
import os

setup(name='pystocks',
      version='0.1',
      description='Python Stocks Interfaces',
      author='Nicolas Couture',
      author_email='nicolas@stormvault.net',
      url='http://pystocks.stormvault.net',
      classifiers=['License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'Operating System :: OS Independent',
		   'Topic :: Office/Business :: Financial',
		   'Intended Audience :: Education',
		   'Intended Audience :: Financial and Insurance Industry',
		   'Intended Audience :: End Users/Desktop'
		   ],
      package_dir={'pystocks':'src'},
      packages=['pystocks']
      )
