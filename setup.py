import os

from setuptools import setup, find_packages

setup(
    name = 'Watson-CT',
    version = '0.1.0',
    author = 'David Michon',
    author_email = 'david.michon@gmail.com',
    packages = find_packages(),
    package_data = {'watson.ui': ['img/*']},
    url = 'http://github.com/puffin/watson',
    license='BSD',
    description='Continuous unit test runner for django',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django >= 1.3",
        "colorama >= 0.2.7"
    ]
)