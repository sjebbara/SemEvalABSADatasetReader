from setuptools import setup
from setuptools import find_packages


setup(name='SemEvalABSADatasetReader',
      version='0.1.0',
      description='Python classes and parser to read the SemEval 2015 and 2016 Aspect-Based Sentiment Analysis (ABSA) datasets.',
      author='Soufian Jebbara',
      author_email='soufian@jebbara.com',
      url='https://github.com/sjebbara/SemEvalABSADatasetReader',
      # download_url='https://github.com/sjebbara/SemEvalABSADatasetReader/tarball/0.3.1',
      license='MIT',
      install_requires=['bs4'],
      packages=find_packages())
