from setuptools import setup

package_name = 'python_package_example'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ROS2 Student',
    maintainer_email='student@example.com',
    description='Python包示例',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_publisher = python_package_example.simple_publisher:main',
            'simple_subscriber = python_package_example.simple_subscriber:main',
        ],
    },
)
