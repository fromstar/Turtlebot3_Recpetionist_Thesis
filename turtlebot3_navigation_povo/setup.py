from setuptools import find_packages, setup

package_name = 'turtlebot3_navigation_povo'

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
    maintainer='Davide Dalla Stella',
    maintainer_email='dallastella.davide@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'set_initial_pose = turtlebot3_navigation_povo.set_initial_pose:main',
            'go_to = turtlebot3_navigation_povo.go_to:main',
        ],
    },
)
