from setuptools import setup, find_packages
from os import path

home = path.abspath(path.dirname(__file__))

setup(
    name='conduktor',
    version='1.0.0',
    description='A simple URL shortener written in Python',
    packages=find_packages(path.join(home, 'conduktor')),
    entry_points={
        'console_scripts': [
            'conduktor = conduktor.__main__:main',
            'create_tables = conduktor.__main__:create_tables',
        ]
    },
    install_requires=[
        'tornado>=5.1,<6',
        'sqlalchemy>=1.2.10,<1.3',
        'psycopg2>=2.7.5,<3',
    ]
)
