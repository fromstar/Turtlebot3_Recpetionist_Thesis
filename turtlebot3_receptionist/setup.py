from setuptools import find_packages, setup

package_name = 'turtlebot3_receptionist'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='davide',
    maintainer_email='davide@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'set_initial_pose = turtlebot3_receptionist.set_initial_pose:main',
            'receptionist = turtlebot3_receptionist.receptionist:main',
        ],
    },
)
