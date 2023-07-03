# setup.py

from setuptools import setup 

from expense_tracker import __version__



setup( 
    name = "exptrack", 
    version = __version__, 
    packages=[".expense_tracker"], 
)