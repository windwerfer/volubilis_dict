"""Setup script for volubilis-dict (legacy fallback).

Prefer `pyproject.toml` for modern builds and installation.
This file is kept for compatibility with older tools.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Version is now managed in pyproject.toml via dynamic + src/volubilis_dict/__init__.py
# but we still support reading it here for pure setup.py usage.
version = {}
try:
    with open("src/volubilis_dict/__init__.py", encoding="utf-8") as f:
        exec(f.read(), version)
except Exception:
    version["__version__"] = "1.1"

setup(
    name="volubilis-dict",
    version=version.get("__version__", "1.1"),
    author="Volubilis Dictionary Team",
    description="Process Volubilis Thai-English dictionary Excel files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
    # Console script is defined in pyproject.toml
    # Run with: python main.py (thin dev wrapper) or volubilis-dict after install
    include_package_data=True,
)