import click

from app import application

@click.group
def cli():
    pass

@cli.command()
@click.argument('sbom')
@click.option('-o', '--output', default='bom-analysis.csv', show_default=True, help='Intended name for output file')
def file2table(sbom, output):
    """Given an SBOM, output a table of important info"""
    application.parse_sbom(sbom, output)

@cli.command()
@click.argument('sbom')
@click.option('-o', '--output', default='dep-analysis.csv', show_default=True, help='Intended name for output file')
def dep2table(sbom, output):
    """Given an SBOM, output a table of dependencies"""
    if application.dependencies(sbom):
        application.parse_dependencies(sbom, output)
    else:
        click.echo('ERROR: This SBOM file does not contain any dependencies. Please ensure the SBOM has a dependencies array as one of the initial keys in the JSON object.')
