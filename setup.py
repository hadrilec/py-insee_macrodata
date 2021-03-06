# -*- coding: utf-8 -*-

import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynsee", 
    version="0.0.1",
    author="Hadrien Leclerc",
    author_email="hadrien.leclerc@insee.fr",
    description="Tools to Easily Download Data and Metadata from INSEE APIs",
    long_description = long_description,
    url="https://pynsee.readthedocs.io/en/latest/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OPEN LICENCE 2.0/LICENCE OUVERTE 2.0",
        "Operating System :: OS Independent",
    ],
    install_requires=[
            "pandas>=0.24.2",
            "tqdm>=4.56.0",
            #gc, hashlib, tempfile, zipfile, math, time
            "requests>=2.25.1",
            "appdirs>=1.4.4",
            "unidecode>=1.2.0",
            "datetime>=3.5.9"],
    include_package_data=True,
    package_data={'pynsee_data': ['macrodata/data/*',
                       'localdata/data/*',
                       'metadata/data/*']},
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose']
)
