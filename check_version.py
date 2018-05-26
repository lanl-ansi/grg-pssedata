#!/usr/bin/env python

import sys
import subprocess
import grg_mpdata

git_describe = subprocess.check_output(['git', 'describe', '--tags']).rstrip().decode('ascii')

py_version = grg_mpdata.__version__

print('git describe: {}'.format(git_describe))

git_version = git_describe.split('-')[0].strip('v')
print('git version: {}'.format(git_version))

print('grg_mpdata version: {}'.format(py_version))

py_version_parts = [int(x) for x in py_version.split('.')]
git_version_parts = [int(x) for x in git_version.split('.')]

assert(len(py_version_parts) == len(git_version_parts))

for i in range(len(py_version_parts)):
    if git_version_parts[i] > py_version_parts[i]:
        print('git version is ahead of python version')
        sys.exit(1)

    if git_version_parts[i] < py_version_parts[i]:
        break
