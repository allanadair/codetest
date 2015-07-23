#!/usr/bin/env python
"""
setup.py script for codetest
"""
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
from os.path import dirname, join


def readme(filepath):
    """
    Returns contents of a readme file.
    """
    with open(filepath, 'r') as rm:
        return rm.read()


def requirements(filepath):
    """
    Returns a list of required packages, presumably from a properly formatted
    ``requirements.txt``.
    """
    with open(filepath, 'r') as rq:
        return list(rq)


setup_options = dict(name='codetest',
                     version='0.1',
                     description='code test',
                     license='Other/Proprietary License',
                     long_description=readme(join(dirname(__file__),
                                                  'README.rst')),
                     author='Allan Adair',
                     author_email='allan.m.adair@gmail.com',
                     url='https://github.com/allanadair/codetest',
                     packages=find_packages('.'),
                     package_dir={'codetest': 'codetest'},
                     install_requires=requirements(join(dirname(__file__),
                                                        'requirements.txt')),
                     classifiers=('Development Status :: 1 - Planning',
                                  'Intended Audience :: Developers',
                                  'Intended Audience :: System Administrators',
                                  'Natural Language :: English',
                                  'License :: Other/Proprietary License',
                                  'Programming Language :: Python',
                                  'Programming Language :: Python :: 2.7',
                                  'Programming Language :: Python :: 3',
                                  'Programming Language :: Python :: 3.4'))
setup(**setup_options)
