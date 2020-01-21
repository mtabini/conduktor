from setuptools import setup, find_packages
from os import path

home = path.abspath(path.dirname(__file__))

print(find_packages(home))

setup(
    name='conduktor',
    version='1.0.0',
    description='A simple URL shortener written in Python',
    packages=find_packages(home),
    entry_points={
        'console_scripts': [
            'conduktor = conduktor.__main__:main',
            'migrate = conduktor.__main__:migrate',
        ]
    },
    install_requires=[
        'tornado>=5.1,<6',
        'sqlalchemy>=1.2.10,<1.3',
        'psycopg2>=2.7.5,<3',
        'validators==0.12.6',
        'alembic>=1',
        'requests>=2.19.1',
        'google-auth>=1.5',
    ],
    include_package_data=True,
)
