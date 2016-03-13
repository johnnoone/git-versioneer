#!/usr/bin/env python

from setuptools import setup
import versioneer

setup(
    name='git-versioneer',
    version=versioneer.get_version(),
    package_dir={'': 'src'},
    cmdclass=versioneer.get_cmdclass(),
    entry_points={
        'console_scripts': [
            'git-versioneer = git_versioneer:main'
        ],
    }
)
