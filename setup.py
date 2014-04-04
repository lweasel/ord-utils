import sys

from distutils.core import setup
from setuptools.command.test import test as TestCommand

# Many parts liberally adapted from
# "http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/"

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name="OrdUtils",
    version="0.1",
    packages=["ordutils"],
    install_requires=[
        "schema >= 0.2.0"
    ],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    extras_require={
        'testing': ['pytest'],
    }
)
