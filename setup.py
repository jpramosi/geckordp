import sys
from setuptools import setup, find_packages

NAME = "geckordp"
__version__ = "0.4.4"
CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

# check version
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of {} requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
""".format(
            NAME, *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

# set metadata
URL = "https://github.com/jpramosi/geckordp"
DESCRIPTION = "A client implementation of Firefox DevTools over remote debug protocol"
LONG_DESCRIPTION = open('README.md', 'r').read()
LONG_DESCRIPTION = LONG_DESCRIPTION.replace(
    '<img src="actor-hierarchy.png">', "![](https://raw.githubusercontent.com/jpramosi/geckordp/master/actor-hierarchy.png)")
classifiers = [
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

# install package itself
setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=classifiers,
    keywords="rdp remote-debug-protocol firefox crawler debug webconsole ui-testing",
    author="jpramosi",
    author_email="jpramosi@no-reply.com",
    url=URL,
    project_urls={
        'Documentation': 'https://jpramosi.github.io/geckordp',
        'Source': URL,
    },
    extras_require={
        "develop": [
            "pytest",
            "twine",
            "ipython",
            "scapy",
            "watchdog",
            "sphinx",
            "sphinx-rtd-theme",
            "myst-parser",
        ],
    },
    license="MIT",
    packages=find_packages(exclude=("tests", "tmp")),
    install_requires=[
        "jmespath",
        "psutil",
    ],
)
