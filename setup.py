"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['PfkBNMController.py']
DATA_FILES = ['MainMenu.xib','itunes_lib.py','itunes_controller.py','pitchfork_module.py','PfkBNMModel.py']
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)