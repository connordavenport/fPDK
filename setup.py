# -*- coding: utf-8 -*-

from setuptools import setup

# def readme():
#     with open("README.md") as f:
#         return f.read()

setup(name="fPDK",
      version="0.1.3",
      description="an API for proofing fonts",
      long_description="an API for proofing fonts",
      classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Build Tools",
      ],
      author="Connor Davenport",
      author_email="info@connordavenport.com",
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