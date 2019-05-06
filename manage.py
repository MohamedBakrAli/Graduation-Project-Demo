from flask.ext.script import Manager

from app import app

manager = Manager(app)

def crazy_call():
    print("#########crazy_call")

@manager.command
def runserver():
    app.run()
    crazy_call()

if __name__ == "__main__":
    manager.run()
