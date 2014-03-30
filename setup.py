"""
py2app build script for MyApplication

Usage:
    python setup.py py2app
# """

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup
setup(
    app=["main.py"],
setup_requires=["py2app"],
)