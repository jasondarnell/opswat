import os
from setuptools import setup

dir_path = os.path.dirname(os.path.abspath(__file__))

description = """Opswat"""
package_name = open(os.path.join(dir_path, "NAME")).read().strip()
requirements = open(os.path.join(dir_path, "requirements.txt")).read()
version = open(os.path.join(dir_path, "VERSION")).read().strip()
license = open(os.path.join(dir_path, "LICENSE")).read().strip()

def package_files():
    paths = []
    for (path, directories, filenames) in os.walk(package_name):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

setup(
    name=package_name,
    version=version,
    description=description,
    install_requires=requirements,
    packages=[package_name],
    package_data = {'': package_files()},
    entry_points={
        "console_scripts": [

        ]
    },
    author="Jason Darnell",
    email="jason.darnell@abaco.com",
    license=license,
    url="http://agar/abaco-sw/devices/device"

)
