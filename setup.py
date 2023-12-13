import io
import os
import setuptools


def read_description():
    url = ".github/Readme.md"
    """ Read and Return the description """
    return io.open(
        os.path.join(os.path.dirname(__file__), url), encoding="utf-8"
    ).read()


def def_requirements():
    """Check PIP Requirements"""
    with open("requirements.txt", encoding="utf-8") as file_content:
        pip_lines = file_content.read().splitlines()
    return pip_lines


setuptools.setup(
    name="faultybot",
    version="0.0.3",
    description="Faultybot Discord Handler",
    long_description=read_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="Python Discord Faultybot ",
    url="https://github.com/Donbur4156/faultybot",
    packages=["faultybot"],
    install_requires=def_requirements(),
    python_requires=">=3.8.*",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
