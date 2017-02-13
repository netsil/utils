from setuptools import setup

setup(
    name='Netsil AOC',
    version='0.1',
    py_modules=['netsilaoc'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        netsil_aoc=netsilaoc:cli
    ''',
)
