#!/usr/bin/env python3


"""I2C Interface ROS::2 package build tool."""


from os import path
from glob import glob
from setuptools import setup, find_packages
from distutils.command import build as build_module
from assurancetourix.map.map import creamapbleu, creamapjaune


class build(build_module.build):
    """Overloaded build module to run custom commands at build."""
    def run(self):
        creamapbleu()
        creamapjaune()
        build_module.build.run(self)


package_name = 'assurancetourix'


setup(
    name=package_name,
    version='0.2.0',
    packages=find_packages(),
    data_files=[
        (path.join('share', package_name), ['package.xml', 'launch/launch.py']),
        (path.join('share', package_name, 'map'), glob('map/*')),
    ],
    zip_safe=True,
    install_requires=['setuptools'],
    author='Ewen BRUN',
    author_email='ewen.brun@ecam.fr',
    maintainer='Ewen BRUN',
    maintainer_email='ewen.brun@ecam.fr',
    keywords=['ROS2', '', 'CDFR'],
    description='Code balise Assurancetourix.',
    license='Funtech Makers :: CDFR 2020',
    entry_points={
        'console_scripts': [
            'main = assurancetourix.main:main',
            'leds = assurancetourix.led_indicators:main',
            'controller = assurancetourix.controller:main',
        ],
    },
    cmdclass={'build': build},
)
