import click

from password_manager import app
from password_manager.models import Password, User, db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Password=Password, User=User)


@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")
    u = User(pwd="admin")
    db.session.add(u)
    db.session.commit()
    click.echo(f"{u.id} user created.")


@app.cli.command()
@click.option(
    "-p", "--pwd", prompt="Password", help="Create new user with password"
)
def createuser(pwd):
    u = User(pwd)
    db.session.add(u)
    db.session.commit()
    click.echo(f"{u.id} user created.")
