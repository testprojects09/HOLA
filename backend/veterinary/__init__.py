import os

from flask import Flask
from flask_cors import CORS, cross_origin

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder="../frontend/build", static_url_path="")
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'veterinary.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    @cross_origin()
    def hello():
        return 'Hello, World!'

    @app.route("/")
    @cross_origin()
    def serve(app):
        return send_from_directory(app.static_folder, 'index.html')


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import citas
    app.register_blueprint(citas.bp)

    from . import products
    app.register_blueprint(products.bp)
    
    from . import animals
    app.register_blueprint(animals.bp)

    from . import users
    app.register_blueprint(users.bp)

    from . import pedidos
    app.register_blueprint(pedidos.bp)

    from . import emails
    app.register_blueprint(emails.bp)

    # from .admin import admin 

    return app