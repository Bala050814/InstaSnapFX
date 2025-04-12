from setuptools import setup, Extension

setup(
    name="filterc",
    version="1.0",
    ext_modules=[Extension("filterc", ["grayscale_filter.c"])]
)
