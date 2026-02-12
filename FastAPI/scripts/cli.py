import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import click
from scripts.create_db import create_database
from scripts.create_tables import create_tables
from scripts.seed_data import seed_all

@click.group()
def cli():
    """Database management commands."""
    pass

@cli.command()
def initdb():
    """Create database, tables, and seed initial data."""
    click.echo("Creating database...")
    create_database()
    click.echo("Creating tables...")
    create_tables()
    click.echo("Seeding data...")
    seed_all()
    click.echo("Done.")

if __name__ == "__main__":
    cli()