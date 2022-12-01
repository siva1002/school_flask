from flask_script import Manager,Server
from flask_migrate import Migrate
from  demo import create_app
from  demo  import db
app=create_app()
manager = Manager(app=app)
manager.add_command("run", Server(host="0.0.0.0", port=8000))

@manager.command
def create():
    db.create_all()
    print ("Database created successfully")
    
@manager.command
def remove():
    db.drop_all()
    print ("Database removed successfully")
if __name__ == "__main__":
    manager.run() 
