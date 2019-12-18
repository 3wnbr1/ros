#!/usr/bin/env python3


"""Asterix metapackage."""


from os import path
from glob import glob
from setuptools import setup


package_name = 'asterix'


setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        (path.join('share', package_name), ['package.xml', 'launch/launch.py']),
        (path.join('share', package_name, 'param'), glob('param/*')),
        (path.join('share', package_name, 'robot'), glob('robot/*')),
    ],
    zip_safe=True,
    install_requires=['setuptools'],
    author='Ewen BRUN',
    author_email='ewen.brun@ecam.fr',
    maintainer='Ewen BRUN',
    maintainer_email='ewen.brun@ecam.fr',
    keywords=['ROS2', '', 'CDFR'],
    description='Asterix RO2 System',
    license='Funtech Makers :: CDFR 2020',
    entry_points={
        'console_scripts': [
            'asterix = asterix.main:main',
        ],
    },
)
