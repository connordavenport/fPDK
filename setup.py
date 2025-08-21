# -*- coding: utf-8 -*-

from setuptools import setup

# def readme():
#     with open("README.md") as f:
#         return f.read()

setup(name="fPDK",
      version="0.1.5",
      description="an API for proofing fonts",
      long_description="an API for proofing fonts",
      classifiers=[
        "Development Status :: 4 - Beta",
        "License :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      author="Connor Davenport",
      author_email="info@connordavenport.com",
      url="https://github.com/connordavenport/fPDK",
      license="All rights reserved",
      packages=[
        "fPDK",
        ],
      install_requires=[
        "drawBot",
        "drawBotGrid",
        "more_itertools",
        "fontTools"
      ],
      include_package_data=True,
      zip_safe=False)