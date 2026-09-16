from setuptools import find_packages, setup
from glob import glob
import os

package_name = "ros2_image_pub_sub_demo"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        (
            "share/" + package_name,
            ["package.xml"],
        ),
        (
            os.path.join("share", package_name),
            glob("ros2_image_pub_sub_demo/*.jpg"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="krish",
    maintainer_email="krish@example.com",
    description="ROS 2 image publisher and subscriber exercise",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "image_publisher = ros2_image_pub_sub_demo.image_publisher:main",
            "image_subscriber = ros2_image_pub_sub_demo.image_subscriber:main",
        ],
    },
)
