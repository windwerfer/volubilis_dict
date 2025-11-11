"""Setup script for volubilis-dict."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="volubilis-dict",
    version="1.0.5",
    author="Volubilis Dictionary Team",
    description="Process Volubilis Thai-English dictionary Excel files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openpyxl>=3.0.0",
        "regex>=2020.0.0",
    ],
    entry_points={
        "console_scripts": [
            "volubilis-dict=src.main:main",
        ],
    },
    include_package_data=True,
)