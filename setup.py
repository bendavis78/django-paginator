from setuptools import setup, find_packages

setup(
    name='django-paginator',
    version='0.1',
    test_suite='paginator.tests',
    packages=find_packages(),
    install_requires=[],
    package_data={'paginator': []},
    include_package_data=True,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
)
