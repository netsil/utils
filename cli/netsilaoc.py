import click
from service import service
from alert import alert

@click.group()
def cli():
    ''' Netsil AOC CLI '''
    pass


cli.add_command(service)
cli.add_command(alert)



