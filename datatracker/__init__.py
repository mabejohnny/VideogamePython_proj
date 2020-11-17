import os

from flask import Flask,redirect

from datatracker.modules import videogames


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from datatracker import videogames
    app.register_blueprint(videogames.bp)

    # app.add_url_rule('/', endpoint='index')

    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app
