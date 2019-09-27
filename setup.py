#!/usr/bin/env python
import setuptools

setuptools.setup(
    name='gitlab-enum',
    version='1.1',
    description='Python GitLab users enumerator',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'gitlabenum=gitlab_enum:main',
        ],
    },
    install_requires=[
        'requests[socks]==2.21.0'
    ]
)
