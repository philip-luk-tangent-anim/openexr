# -*- coding: utf-8 -*-

name = 'openexr'

version = '2.2.0'

authors = [
    'philip.luk'
]

requires = [
]

build_requires = [
    'python-2',
    'ninja',
]

variants = [
    ['platform-windows'],
    ['platform-linux'],
]

build_command = "python {root}/install_openexr.py"

def commands():
    pass

