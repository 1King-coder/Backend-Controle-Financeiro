from setuptools import setup, find_packages

setup(
    name='backend_controle_financeiro',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas_datareader',
        'pandas',
        'matplotlib',
        'numpy',
    ],
)