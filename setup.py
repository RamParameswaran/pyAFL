import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="pyAFL",
    version="0.4.1",
    description="Python data fetching library for the Australian Football League",
    long_description="pyAFL is a AFL (Australian Football League) data fetching libary. It scrapes data from https://afltables.com/ and converts results to structured Python objects for easier analytics.",
    url="https://github.com/RamParameswaran/pyAFL",
    author="Ram Parameswaran",
    author_email="ram@findram.dev",
    license="MIT",
    packages=setuptools.find_packages(
        exclude=[
            "tests",
        ]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=required,
)
