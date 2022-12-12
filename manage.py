from flask_script import Server, Manager
from flask_migrate import Migrate
from core import create_app
# from core import db, alembic

app = create_app()
manager = Manager(app=app)
manager.add_command("run", Server(host="127.0.0.0", port=8000))

# @manager.command
# def migrate():
#     alembic.revision('making changes')
#     alembic.upgrade()

# @manager.command
# def create():
#     db.create_all()
#     print("Database created successfully")

# @manager.command
# def drop():
#     db.drop_all()
#     print("Database removed successfully")

if __name__ == "__main__":
    manager.run()
