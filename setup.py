#!/usr/bin/env python

from setuptools import setup
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

def read_readme():
    with open(os.path.join(here, 'README.md')) as f:
        return f.read()

def get_requirements():
    with open(os.path.join(here, 'requirements.txt')) as f:
        return f.readlines()

setup(
    name = "concourse-ecr-tag-resource",
    version = '0.1.0',
    description = 'Concourse CI resource for tagging images in an ECR repository.',
    long_description = read_readme(),
    url = 'https://github.com/petegoo/concourse-ecr-tag-resource',
    author = 'petegoo',
    classifiers = [
    ],
    keywords = [
    ],
    packages = [ 'ecr_tag_resource' ],
    install_requires = get_requirements(),
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'check = ecr_tag_resource.check:main',
            'in = ecr_tag_resource.in_:main',
            'out = ecr_tag_resource.out:main',
        ]
    }
)