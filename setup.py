#!/usr/bin/env python

from setuptools import setup


exec(open('scrapy_rotate/version.py').read())

setup(
    name='scrapy_rotate',
    packages=['scrapy_rotate'],
    version=__version__,
    install_requires=['fake-useragent>=0.1.2'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license='MIT',
    description='A set of Scrapy middlewares useful for rotating user agents and proxies.',
    author='Walter Trevino',
    author_email='walter.trevino@gmail.com',
    url='https://github.com/wtrevino/scrapy_rotate',
    keywords = ['scrapy', 'proxy', 'user agents', 'rotate', 'rotating'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Scrapy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
