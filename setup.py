from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup, find_packages

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
        # "cooler",
        "scipy",
        "numpy",
        "pandas",
        "tqdm"
        ],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Programming Language :: Python :: 3.6+",
    ],
    python_requires='>=3.7.* ',
    entry_points={"console_scripts": ["pyhicrep=pyhicrep.cli:main"]},
)
