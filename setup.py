from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='SemEvalABSADatasetReader',
      version='0.2.0',
      description='Python classes and parser to read the SemEval 2014, 2015 and 2016 Aspect-Based Sentiment Analysis (ABSA) datasets.',
      author='Soufian Jebbara',
      author_email='soufian@jebbara.com',
      url='https://github.com/sjebbara/SemEvalABSADatasetReader',
      install_requires=requirements,
      license='MIT',
      packages=find_packages())
