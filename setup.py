from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='pcce',
    version='0.0.1',
    description='Package that enables access to multiple cryptocurrency exchanges.',
    packages=find_packages(include=["common", "providers"]),
    author='ToxinSpider',
    license='MIT',
    install_requires=required_packages,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
