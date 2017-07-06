from application import create_app,db
from application.Models import User,Post,Role
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand

app=create_app('development')
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Post=Post,Role=Role)

manager.add_command("Shell",Shell(make_context=make_shell_context))
mamager.add_command("db", MigrateCommand)

if __name__=='__main__':
    manager.run()


