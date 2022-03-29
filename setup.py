import sys
import os
from setuptools import setup, find_packages

req_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt")
with open(req_path) as f:
    reqs = f.read().splitlines()

readme_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
with open(readme_path) as f:
    long_description = f.read()

setup(name="chauffeur-pass",
      version="0.0.1",
      author="Jamison Polackwich",
      author_email='rjpolackwich@gmail.com',
      description="Python API for making OSM queries via Overpass",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/rjpolackwich/chauffeur",
      license="MIT",
      packages=find_packages(exclude=['docs', 'tests']),
      install_requires=reqs,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License"
    ],
      python_requires='>3.7',
      )

