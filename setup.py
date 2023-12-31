from setuptools import setup, find_packages

__version__='0.0.1'

setup(
    name='api-practice',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "fastapi[all]",
        "pymongo[srv]",
        "python-dotenv",
    ]
)