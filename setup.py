from setuptools import setup

setup(
    name='sola',
    version='0.1',
    py_modules=['experso'],
    install_requires=[
        'Click',
        'boto3',
        'awscli',
    ],
    entry_points='''
        [console_scripts]
        sola=experso:cli
    ''',
)