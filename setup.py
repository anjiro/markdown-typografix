#! /usr/bin/env python
from setuptools import setup

setup(
    name='mdx_typografix',
    version='1.00.0',
    author='KNX Corp',
    author_email='',
    description='A python markdown extension for automatic french typographic tweaks',
    url='https://github.com/anjiro/markdown-typografix',
    py_modules=['mdx_typografix'],
    install_requires=['Markdown>=2.0',],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
