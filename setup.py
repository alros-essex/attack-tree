"""setup tool"""
from setuptools import setup, find_packages

### graphviz is also required
### python-tk is also to be installed

setup(
    name='attack-trees',
    version='0.1.0',
    packages=find_packages(include=['attack']),
    test_suite = 'test',
    install_requires=[
        "networkx >= 2.8.7",
        "matplotlib >= 3.6.1",
        "numpy>=1.23.4",
        "graphviz>=0.20.1",
        "PyYAML>=6.0"
    ],
    python_requires='>=3.6'
)
