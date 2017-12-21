import click
from alert import alert
from query import query
from dashboard import dashboard

@click.group()
def cli():
    ''' Netsil AOC CLI '''
    pass


cli.add_command(alert)
cli.add_command(query)
cli.add_command(dashboard)


