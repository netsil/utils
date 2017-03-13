from setuptools import setup

setup(
    name='Netsil AOC SlackBot',
    version='0.1',
    py_modules=['netsilbot'],
    install_requires=[
        'requests',
        'slackclient'
    ],
    entry_points='''
        [console_scripts]
        netsil_bot=netsilbot:runbot
    ''',
)
