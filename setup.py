# Author: AnjanaMadu
# Project: seedr

import os
from codecs import open
from setuptools import setup

requires = [
    "requests",
]

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "seedr", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=["seedr"],
    package_data={"": ["LICENSE"]},
    package_dir={"seedr": "seedr"},
    include_package_data=True,
    python_requires=">=3.7, <4",
    install_requires=requires,
    license=about["__license__"],
    zip_safe=False,
    keywords=[
        "seedr",
        "seedr.cc",
        "seedr-api"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
    ],
    project_urls={
        "Documentation": "https://github.com/AnjanaMadu/SeedrAPI/wiki",
        "Source": "https://github.com/AnjanaMadu/SeedrAPI",
    },
)