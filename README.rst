git-versioneer
--------------

Defines version from git.

For example, if your release the *HEAD* of *prod* branch that is 10 commits
behind *tag v1.2.3* with the *hash afe7651*, the version will be
*1.2.3-1.gafe7651*.

Usage::

  usage: git versioneer <commit-ish>

  define version number

  positional arguments:
    commit-ish            Commit-ish object names to describe. Defaults to HEAD
                          if omitted.

  optional arguments:
    -h, --help            show this help message and exit
    --directory DIRECTORY
    --tag-prefix TAG_PREFIX

Example::

    cd /MY/REPO
    git versioneer

