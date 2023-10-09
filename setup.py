#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup process."""

from io import open
from os import path

from setuptools import find_packages, setup

with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    zip_safe=False,
    # Basic project information
    name="claims",
    version='0.1.11',
    # Authorship and online reference
    author="Eduardo Turiño",
    author_email="eturino@eturino.com",
    url="https://github.com/eturino/claims.py",
    # Detailled description
    description="Port of https://github.com/eturino/claims.ts. Library to manage claims and permissions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="claims permissions",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # Package configuration
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    python_requires=">= 3.6",
    package_data={"claims": ["py.typed"]},
    install_requires=[
        "pydantic>=2.4,<3",
        "key_set",
    ],
    # Licensing and copyright
    license="Apache 2.0",
)
