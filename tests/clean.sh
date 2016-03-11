#!/bin/sh

git init
git config user.email "you@example.com"
git config user.name "Your Name"
touch README.rst
git add README.rst
git commit -m "first commit"
git tag v0.0.1a

echo "first patch" >> README.rst
git commit -m "first patch" README.rst
git tag v0.0.1b

echo "second patch" >> README.rst
git commit -m "second patch" README.rst
git tag v0.0.1pre

echo "release candidate" >> README.rst
git commit -m "release candidate" README.rst
git tag v0.0.1rc

echo "release" >> README.rst
git commit -m "release" README.rst
git tag v0.0.1

touch foo.txt
git add foo.txt
git commit -m "second commit"
git tag v0.0.2
