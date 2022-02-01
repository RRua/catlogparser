# !/bin/bash

rm -rf dist/*
python3 -m incremental.update logcatparser --patch
git add logcatparser/_version.py
git commit -m "bump _version"
python3 setup.py sdist
python3 -m twine upload dist/*
git push origin master