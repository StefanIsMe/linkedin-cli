#!/usr/bin/env python3
"""Setup script for linkedin-api-cli package."""
from setuptools import setup, find_packages

setup(
    name="linkedin-api-cli",
    version="0.1.0",
    description="Unofficial LinkedIn CLI client using cookie authentication",
    author="Stefan Carter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "curl_cffi>=0.5.0",
    ],
    entry_points={
        "console_scripts": [
            "linkedincli=linkedin_api.cli:main",
        ],
    },
    python_requires=">=3.10",
)
