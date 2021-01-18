import setuptools

setuptools.setup(
    name="pyhicrep",
    version="0.8",
    url="https://github.com/7rick03ligh7/pyhicrep",
    author="Alexey",
    author_email="-",
    description=("Python implementation of HiCRep with supporting sparse data "
                 "and parallel computation for multiple Hi-C data"),
    long_description=open('README.md').read(),
    packages=["pyhicrep"],
    install_requires=[
        # "cooler",
        "scipy",
        "numpy",
        "pandas",
        "tqdm"
        ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Programming Language :: Python :: 3.6+",
    ],
    entry_points={"console_scripts": ["pyhicrep=pyhicrep.cli:main"]}
)
