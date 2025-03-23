from flask import Flask
from backend.controllers.ga_controller import ga_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(ga_blueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
