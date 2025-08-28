# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(name="fPDK",
      version="0.1.6",
      description="an API for proofing fonts",
      author="Connor Davenport",
      author_email="info@connordavenport.com",
      maintainer="Connor Davenport",
      maintainer_email="info@connordavenport.com",
      url="https://github.com/connordavenport/fPDK",
      license="All rights reserved",
      package_dir={"":"Lib"},
      packages=find_packages("Lib"),
      package_data={'Lib': ['fonts/*']},
      include_package_data=True,
      install_requires=parse_requirements('requirements.txt'),
      zip_safe=False)