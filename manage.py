from time import process_time
import configparser

import click

from models import dbhandler
from controller import schedules

# ************** Read "config.ini" ********************
config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8-sig")
logging = config['LOGGING']
DB = config["DATABASE"]
SCHEDULES = config["SCHEDULES"]
# ************** END **********************************

db = dbhandler.DBHandler(DB.get('uri'))
sc = schedules.Schedule(SCHEDULES.get('hour'))

@click.command()
@click.option("--database",
              type=click.Choice(["create", "delete"]),
              help='Create or delete all table '
              'with all data. Оperation, '
              'by default, creates all tables')
@click.option("--schedules",
              type=click.Choice(["run", "delete"]),
              help='Run or delete cron job '
              'where started parser.py with period'
              'Perion settings in config.ini')
def main(database, schedules):
    if database == "create":
        start_time = process_time()
        db.create()
        click.echo(f'Table is createt at: '
                   f'{process_time() - start_time} sec.')
    elif database == "delete":
        start_time = process_time()
        db.delete()
        click.echo(f'Table is deleted at: '
                   f'{process_time() - start_time} sec.')
    elif schedules == "run":
        click.echo(f"{sc.create()} and {sc.run()}")
    elif schedules == "delete":
        click.echo(f"{sc.delete()}")


if __name__ == "__main__":
    main()
