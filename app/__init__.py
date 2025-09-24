from flask import Flask
from .config import Config
from .extensions import db, ma
from .routes import user_bp, project_bp, task_bp
from .models.user import User
from .models.project import Project
from .models.task import Task
import atexit


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    ma.init_app(app)

    # Create tables
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_data()

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    
        # Drop tables when app exits
    def drop_tables():
        with app.app_context():   # ensure we have context
            db.drop_all()
            print("✅ Dropped all tables on exit")
          
    atexit.register(drop_tables)    
    return app  

# Refactor this to be CLI for Flask, so not seeding by starting the server
def seed_data():
    user = User(
                username = "John",
                email = "janen@test.com",
                password_hash = "12345"
            )
    db.session.add(user)
    db.session.commit()
            
    project = Project(
                project_name = "Task Manager API",
                description = "RESTful API",
                owner_id = user.user_id       
            )
    db.session.add(project)
    db.session.commit()
            
    task1 = Task(
                task_name = "First Task in API",
                description = "This task is succesfully fulfilled",
                project_id = project.project_id
            )
    db.session.add(task1)
    db.session.commit()
    
            
    task2 = Task(
                task_name = "Second Task in the API",
                description = "This is the second task in the API, yaaaay!",
                project_id = project.project_id
            )
    db.session.add(task2)
    db.session.commit()
            
    print("Database seeded successfully!")