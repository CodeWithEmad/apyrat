#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages

from apyrat.utils import get_about_information

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()


ABOUT = get_about_information()

requirements = ["click==7.1.2", "requests==2.31.0", "wget==3.2"]

test_requirements = [
    "pytest>=3",
]

setup(
    author=ABOUT["__author__"],
    author_email=ABOUT["__email__"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="An Aparat video downloader. simple, but elegant.",
    entry_points={
        "console_scripts": [
            "apyrat=apyrat.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="apyrat",
    name="apyrat",
    packages=find_packages(include=["apyrat", "apyrat.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url=ABOUT["__url__"],
    version=ABOUT["__version__"],
    zip_safe=False,
)
