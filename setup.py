from setuptools import setup, find_packages

setup(
    name='woodyboxbot',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'python-telegram-bot==22.3',
        'dotenv',
        'pytest',
        'pytest-asyncio',
        'pytest-mock'
    ],
)