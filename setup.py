from setuptools import setup, find_packages

setup(
    name='backend_controle_financeiro',
    version='1.0.1',
    packages=find_packages(include=("modules", "modules.*")),
    install_requires=[
        'pandas_datareader',
        'pandas',
        'matplotlib',
        'numpy',
    ],
)