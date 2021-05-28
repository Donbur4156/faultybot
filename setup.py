import io
import os
import setuptools


def read_description():
    """ Read and Return the description """
    return io.open(os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8").read()


def read_pip():
    """ Read and Return the pip dependencies """
    datei = open('requirements.txt', 'r')
    output_stream = []
    for zeile in datei:
        zeile = zeile.replace("\n", "")
        output_stream.append(zeile)
    datei.close()
    return output_stream


setuptools.setup(
    name="faultybot",
    version='0.0.1',
    description='Faultybot Discord Handler',
    long_description=read_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="Python Discord Faultybot ",
    url="https://github.com/jplight/faultybot",
    packages=["faultybot"],
    install_requires=read_pip(),
    python_requires=">=3.8.*",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
