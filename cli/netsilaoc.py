import click
from service import service
from alert import alert
from query import query

@click.group()
def cli():
    ''' Netsil AOC CLI '''
    pass


cli.add_command(service)
cli.add_command(alert)
cli.add_command(query)


