from setuptools import setup, find_packages
import sys

setup(
    name='lib_trader',
    packages=find_packages(),
    version='0.0.0',
    author='Justin Furuness',
    author_email='jfuruness@gmail.com',
    url='https://github.com/jfuruness/lib_trader.git',
    download_url='https://github.com/jfuruness/lib_trader.git',
    keywords=['Furuness', 'Trader', 'Robinhood', 'Webull', 'Stocks', 'Wrapper'],
    install_requires=[
        ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'],
    entry_points={},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
