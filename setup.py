import os
from setuptools import setup

setup(
    name = "ITask",
    version = "0.1.0",
    author = "Jonathan Reil",
    author_email = "jonathanr@online.de",
    description = "Simple IServ Task Downloader",
    license = "GNU GPL 3",
    url = "https://github.com/JonaRL/itask",
    packages=['itask'],
    entry_points = {
        'gui_scripts' : ['itask = itask.itask']
    },
    data_files = [
        ('share/applications/', ['itask.desktop'])
        ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License Version 3",
    ],
    python_requires=">=3.6",
)

