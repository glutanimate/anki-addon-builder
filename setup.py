#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aab',
    version='0.1.3',
    description='Anki Add-on Builder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/glutanimate/anki-addon-builder',
    author='Aristotelis P. (Glutanimate)',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: POSIX",
        "Operating System :: MacOS",
    ],
    keywords='anki development build-tools',
    packages=["aab"],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    install_requires=["jsonschema", "whichcraft",
                      "pathlib;python_version<'3.4'"],
    # e.g. $ pip install aab[anki21]
    extras_require={
        'anki21': ['PyQt5>=5.12']
    },
    entry_points={
        'console_scripts': [
            'aab=aab.cli:main',
        ],
    },
    package_data={
        'aab': ['schema.json']
    },
    project_urls={
        'Bug Reports': 'https://github.com/glutanimate/anki-addon-builder/issues',
        'Funding': 'https://glutanimate.com/support-my-work/',
        'Source': 'https://github.com/glutanimate/anki-addon-builder',
    },
)
