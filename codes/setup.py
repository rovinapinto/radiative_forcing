#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

setup(
    name="forcing_tools",
    version="1.0",
    author="Rovina Pinto",
    author_email="rpinto1@uni-koeln.de",
    packages=["forcing_tools"],
    url="https://github.com/rovinapinto/radiative_forcing",
    license="MIT License",
    description=("Computing and visualising radiaitve forcing at the TOA for CMIP6 data, particularly RFMIP project"),
    long_description=open("README.md").read(),
    #package_data={"forcing_tools": ["LICENSE", "data/*.txt", "data/*.nc", "data/*.csv",]},
    include_package_data=False,
    install_requires=["matplotlib", "numpy","netCDF4", "xarray", "dask", "scipy", "cartopy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False,
)