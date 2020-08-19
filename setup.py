from setuptools import setup, find_packages

setup(
    name='MergeKeepass',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    py_modules = [ 'merge_keepass' 'keepassmerge' ],

    install_requires=['pykeepass >= 3', 'Click'],

    entry_points='''
        [console_scripts]
        merge_keepass=MergeKeepass.merge_keepass:cli
    ''',

    # metadata to display on PyPI
    author='Scott Hamilton',
    author_email='sgn.hamilton+python@protonmail.com',
    description='Keepass Databases 2.x Merging module and command line utility',
    keywords='keepass merge',
    url='https://github.com/SCOTT-HAMILTON/merge-keepass',
    project_urls={
        'Source Code': 'https://github.com/SCOTT-HAMILTON/merge-keepass',
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)
