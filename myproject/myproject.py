#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

# Third-party libraries
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade
from flask_cors import CORS

# User define module
from app import create_app, db
from app.models import User, Role

# ------------------------------------------------------Global Variables----------------------------------------------------
app = create_app(os.getenv('FLASK_CONFIG') or 'default')               # create application
cors = CORS(app, resource={'/api/*':{'origins': '*'}})                 # for cross-domain requests
manager = Manager(app)                                                 # applicaton management
migrate = Migrate(app, db)


def make_shell_context():                                                      
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))   # define commands 'shell' and 'db'for app management
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    """Run deployment tasks.
    """
    upgrade()                                                          # migrate database to latest revision
    Role.insert_roles()                                                # create user roles


# -----------------------------------------------------------Main-----------------------------------------------------------
if __name__ == '__main__':
    manager.run()