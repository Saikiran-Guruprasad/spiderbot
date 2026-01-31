from setuptools import setup
import os
from glob import glob

package_name = 'jetson_stm32_poc'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include message files
        (os.path.join('share', package_name, 'msg'), glob('msg/*.msg')),
        # Include launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='saikirang',
    maintainer_email='saikiranpr@example.com',
    description='Interface between Jetson and STM32 via serial',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'values_giver = jetson_stm32_poc.values_giver:main',
            'values_getter_sender = jetson_stm32_poc.values_getter_sender:main',
        ],
    },
)
