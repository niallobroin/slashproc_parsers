#!/bin/bash


set -e


cd docs

sphinx-apidoc -o source .. -f

make html



