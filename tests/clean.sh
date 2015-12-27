#!/bin/sh

git init
git config user.email "you@example.com"
git config user.name "Your Name"
touch README.rst
git add README.rst
git commit -m "first commit"
git tag v0.0.1
touch foo.txt
git add foo.txt
git commit -m "second commit"
git tag v0.0.2
