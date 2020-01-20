#!/bin/bash
# https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project

set -e

tox -r
rm -rf dist
python setup.py bdist_wheel
