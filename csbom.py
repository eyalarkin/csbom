import click

from app import application

@click.command()
@click.option('-s', '--sbom', required=True, help='Path to the SBOM file')
@click.option('-o', '--output', default='bom-analysis.csv', show_default=True, help='Intended name for output file')
def cli(sbom, output):
    application.parse_sbom(sbom, output)
