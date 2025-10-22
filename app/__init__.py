from flask  import Flask
from .config import Config
from .extensions import db, ma, jwt, limiter
from .routes import user_bp, project_bp, task_bp, auth_bp
from .utils.seed import seed_data


def create_app(config_name = "default"):
    app = Flask(__name__)
    if config_name == "testing":
        app.config.from_object("app.config.TestingConfig")
    else:
        app.config.from_object("app.config.Config")

    # Init extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    
    # Create tables
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_data()

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(auth_bp)
    
    return app  

