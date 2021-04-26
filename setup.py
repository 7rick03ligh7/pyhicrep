import os
from os.path import basename, splitext
from glob import glob

from setuptools import setup, find_packages


_PATH_ROOT = os.path.dirname(__file__)
_PATH_REQUIRE = os.path.join(_PATH_ROOT, 'requirements.txt')

with open(_PATH_REQUIRE) as f:
    requirements = f.read().splitlines()

setup(
    name="pyhicrep",
    version="0.8",
    url="https://github.com/7rick03ligh7/pyhicrep",
    author="Alexey",
    author_email="7rick03ligh7@gmail.com",
    description=("Python implementation of HiCRep with supporting sparse data "
                 "and parallel computation for multiple Hi-C data"),
    long_description=open('README.md').read(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=[
        "numpy>=1.19.5",
        "scipy>=1.6.0",
        "numba>=0.52.0",
        "pandas>=1.2.0",
        "tqdm>=4.55.2",
        "cooler>=0.8.10"
    ],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: BSD License"
        "Programming Language :: Python :: 3.7+",
    ],
    python_requires='>=3.7.* ',
    entry_points={"console_scripts": ["pyhicrep=pyhicrep.cli:main"]},
)
