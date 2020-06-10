from setuptools import setup, find_packages
setup(
    name="merge-keepass",
    version="0.1",
    packages=find_packages(),
    scripts=["merge-keepass.py"],

    install_requires=["libkeepass>=0.3"],

    # metadata to display on PyPI
    author="Scott Hamilton",
    author_email="sgn.hamilton+pipy@protonmail.com",
    description="Keepass Databases 2.x Merging script",
    keywords="keepass merge",
    url="https://github.com/SCOTT-HAMILTON/merge-keepass",
    project_urls={
        "Source Code": "https://github.com/SCOTT-HAMILTON/merge-keepass",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]
)
