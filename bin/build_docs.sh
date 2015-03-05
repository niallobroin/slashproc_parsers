#!/bin/bash


set -e


cd docs

sphinx-apidoc -o source ../slashproc_parser -f

make html



