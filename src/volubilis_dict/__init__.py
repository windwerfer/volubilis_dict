"""Volubilis dictionary processor package."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("volubilis-dict")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"  # fallback when running from source without install

