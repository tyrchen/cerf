
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from setuptools import setup, find_packages

__version__ = 1.3

METADATA = dict(
    name='pyramid',
    version=__version__,
    author='chen chiyuan',
    author_email='chenchiyuan03@.com',
    description='easter python client',
    long_description=open('README.md').read(),
    url='http://github.com/tyrchen/pyramid',
    keywords='pyramid client',
    install_requires=['requests'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    packages=find_packages(),
)

if __name__ == '__main__':
    setup(**METADATA)

