import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'scout_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='eduardofelix',
    maintainer_email='efelixcastano@seattleu.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'offboard_control = scout_bot.offboard_control:main',
            'tmc_node = scout_bot.tmc_node:main',
            'yolo_node = scout_bot.yolo_node:main',
        ],
    },
)
