#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created by Anoniji
Library made available under the terms of the license
Creative Commons Zero v1.0 Universal
https://creativecommons.org/publicdomain/zero/1.0/
'''

import sys
import os
from cx_Freeze import setup, Executable
import site
import shutil

VERSION = '0.1.0'
cible = Executable(script='main.py', base='Console', targetName="voicemaker.exe")

setup(
    name='Data Colors',
    version=VERSION,
    author='Anoniji',
    options={
        'build_exe': {
            'path': sys.path,
            'includes': [
                'logger',
            ],
            'excludes': [],
            'packages': [],
            'optimize': 1,
            'silent': True,
            'zip_include_packages': '*',
            'zip_exclude_packages': '',
            'include_msvcr': True,
            'build_exe': './build/',
        },
    },
    executables=[cible],
)


if not os.path.isdir('.\\build\\lib\\_soundfile_data\\'):
    os.mkdir('.\\build\\lib\\_soundfile_data\\')

shutil.copyfile(
    site.getsitepackages()[-1] + '\\_soundfile_data\\libsndfile64bit.dll',
    '.\\build\\lib\\_soundfile_data\\libsndfile64bit.dll'
)

shutil.copytree(
    '.\\dictionaries',
    '.\\build\\dictionaries'
)
