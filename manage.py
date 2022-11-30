from flask_script import Manager,Server
from demo import create_app
manager = Manager(app=create_app())
manager.add_command("run", Server())
if __name__ == "__main__":
    manager.run()
