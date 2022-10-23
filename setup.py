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
        "plotly >= 5.10.0",
        "networkx >= 2.8.7",
        "pandas >= 1.5.0",
        "matplotlib >= 3.6.1",
        "GraVE >= 0.0.3",
        "pydot",
        "graphviz",
        "tcl",
        "pyyaml"
    ],
    python_requires='>=3.6'
)
