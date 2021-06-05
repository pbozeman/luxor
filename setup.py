from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="luxor",
    version="0.0.1",
    license="Apache License 2.0",
    author="Patrick Bozeman",
    author_email="pbozeman@gmail.com",
    description="Python module to control FX Luminaire Luxor low voltage controllers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbozeman/luxor",
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.7.4,<4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
