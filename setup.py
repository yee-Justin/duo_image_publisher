from glob import glob
import os
from setuptools import setup

package_name = 'duo_image_publisher'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],  # assumes your Python code is in a folder named duo_image_publisher
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 🚀 include launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='justin',
    maintainer_email='justin@todo.todo',
    description='Publishes images from two cameras without calibration.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'camera_node = duo_image_publisher.duo_image_publisher:main',
            'stereo_sync_node = duo_image_publisher.stereo_sync:main'
        ],
    },
)
