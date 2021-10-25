# Author: AnjanaMadu
# Project: seedr

import os
import re
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


# Version
with open('seedr/version.py', 'r', encoding='utf-8') as f: 
    version = re.search(r"^__version__\s*=\s*'(.*)'.*$",
                        f.read(), flags=re.MULTILINE).group(1)

setup(
    name='seedr',
    version=version,
    description='API wrapper for seedr.cc',
    url='https://github.com/AnjanaMadu/SeedrAPI',
    author='AnjanaMadu',
    author_email='AnjanaMadu@users.noreply.github.com',
    license='GNU',
    packages=find_packages(),
    download_url=f"https://github.com/AnjanaMadu/SeedrAPI/releases/tag/{version}",
    keywords=['seedr', 'seedr-api', 'seedr.cc'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Education',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
    ]
)
