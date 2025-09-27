from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mlua",
    version="0.0.1",
    author="FreeStar007",
    author_email="3089666858@qq.com",
    description="A lua module manager library for python, it can transfer lua module to python object and call it.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FreeStar007/mlua",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        "lupa",
        "colorama"
    ],
)
