# Author: AnjanaMadu
# Project: seedr

import os
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if os.path.isfile('requirements.txt'):
    with open('requirements.txt') as req:
        reques = req.read().splitlines()
else:
    reques = [
        'requests'
    ]

if os.path.isfile('README.md'):
    with open(('README.md'), encoding='utf-8') as readme:
        bdescription = readme.read()
else:
    bdescription = "An Unofficial API wrapper for seedr.cc"

# Version
v = "v1.0"

setup(
    name='seedr',
    version=v,
    description='API wrapper for seedr.cc',
    url='https://github.com/AnjanaMadu/SeedrAPI',
    author='AnjanaMadu',
    author_email='AnjanaMadu@users.noreply.github.com',
    license='GNU',
    packages=find_packages(),
    download_url=f"https://github.com/AnjanaMadu/SeedrAPI/releases/tag/{v}",
    keywords=['seedr', 'seedr-api', 'seedr.cc'],
    long_description=bdescription,
    long_description_content_type='text/markdown',
    install_requires=reques,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Education',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
    ]
)
