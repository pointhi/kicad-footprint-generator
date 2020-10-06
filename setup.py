#!/usr/bin/env python3

import os
import sys

from setuptools import setup
from setuptools import find_packages


long_description = open(os.path.join(sys.path[0], 'README.md')).read()

setup(
    name='KicadModTree',
    version='1.1.2',
    author='Thomas Pointhuber',
    author_email='thomas.pointhuber@gmx.at',
    url='https://github.com/pointhi/kicad-footprint-generator',
    description="creating kicad footprints using python scripts",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPL3+",

    install_requires=[
        'future',
        'pyyaml'
    ],
    extras_require={
        'test': [
            'pep8',
            'flake8',
            'unittest2',
            'nose2',
            'nose2-cov'
        ]
    },
    packages=find_packages('.', exclude=["*tests*", "*examples*"]),
    test_suite='tests',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
    ],
)
