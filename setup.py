# pylint: disable=missing-function-docstring
# pylint: disable=consider-using-f-string
# pylint: disable=missing-module-docstring

import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

# The directory containing this file
HERE = os.path.dirname(__file__)

NAME = "givesendgoscraper"
DESCRIPTION = "Server to run a webtorrent movie"
URL = f"https://github.com/zackees/{NAME}"
EMAIL = "dont@email.me"
AUTHOR = "Zach Vorhies"
REQUIRES_PYTHON = ">=3.10.4"
VERSION = None

# The text of the README file
with open(os.path.join(HERE, "README.md"), encoding="utf-8", mode="rt") as fd:
    LONG_DESCRIPTION = fd.read()

with open(os.path.join(HERE, "requirements.txt"), encoding="utf-8", mode="rt") as fd:
    REQUIREMENTS = [line.strip() for line in fd.readlines() if line.strip()]

with open(os.path.join(HERE, "src", "version.py"), encoding="utf-8", mode="rt") as fd:
    for line in fd.readlines():
        if line.startswith("VERSION"):
            VERSION = line.split("=")[1].strip().strip('"')
            break

assert VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        pass

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(HERE, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system('"{0}" setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(VERSION))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    python_requires=REQUIRES_PYTHON,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    author="Zach Vorhies",
    author_email="dont@email.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Environment :: Console",
    ],
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_data={},
    include_package_data=True,
    extras_require={
        "test": ["pytest"],
    },
    cmdclass={
        "upload": UploadCommand,
    },
)
