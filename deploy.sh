# !/bin/bash
sem_ver="patch"
test "$1" == "patch" && sem_ver="patch"
test "$1" == "minor" && sem_ver="minor"
test "$1" == "major" && sem_ver="major"
rm -rf dist/*
python3 -m incremental.update logcatparser "--${sem_ver}"
git add logcatparser/_version.py
git commit -m "bump ${semver} _version"
python3 setup.py sdist
python3 -m twine upload dist/*
git push origin master