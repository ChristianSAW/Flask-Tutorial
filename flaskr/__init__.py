import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index',view_func=blog.index) # doen't seem to be necessary. 

    # # a simple home page 
    # @app.route('/')
    # def home():
    #     return 'YEEEEEEEEET'

    # Test 
    @app.route('/<name>')
    def nametest(name):
        return name + ", I've been expecting you for some time now."

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app