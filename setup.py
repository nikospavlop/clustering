#!/usr/bin/env python

from setuptools import setup
from src.app import segmentation


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='Distutils',
      version='1.0',
      description='Python Distribution Utilities',
      author='Greg Ward',
      author_email='gward@python.net',
      url='https://www.python.org/sigs/distutils-sig/',
      scripts=['src/app.py'],
      install_requires=required,
     )