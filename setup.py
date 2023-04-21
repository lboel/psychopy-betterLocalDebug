#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='psychopy-betterLocalDebug',
    packages=['psychopy_betterLocalDebug'],
    include_package_data=True,
    author="Luke Boelling",
    author_email="boelling.luke@gmail.com",
    install_requires=[
        'flask>=2.2','bs4'
    ],
)