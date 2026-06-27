from setuptools import find_packages,setup
from typing import List
import os

hypen_dot = '-e .'
def get_requirements(filename:str)->list[str]:
    """
        :parameters:name of the requirements file
        :return:list of packages which are required to install
    """
    path = next((os.path.join(root, filename) for root, _, files in os.walk(".") if filename in files), None)
    with open(path) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if hypen_dot in requirements:
            requirements.remove(hypen_dot)
        return requirements

setup(
    name="ML_project",
    version="0.0.1",
    author="Kalp",
    author_email="kalp.b0450@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    entry_points={'console_scripts': ['app=app:main']},
)