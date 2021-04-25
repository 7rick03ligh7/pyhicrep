from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup, find_packages

with open('requirements.txt') as f:
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
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: BSD License"
        "Programming Language :: Python :: 3.7+",
    ],
    python_requires='>=3.7.* ',
    entry_points={"console_scripts": ["pyhicrep=pyhicrep.cli:main"]},
)
