from .security import hash_password
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.extensions import db

def seed_data():
    users_id = seed_users()
    projects_id = seed_projects(users_id)
    seed_tasks(projects_id)
    print("Database seeded successfully!")
    
def seed_users():
    users = [
        User(
            username = "John Smith",
            email = "johnsmith@test.com",
            password_hash = hash_password("abcdfghjkl"),
            role = "admin"
        ),
        User(
            username = "Jane Miranda",
            email = "jane.miranda@test.com",
            password_hash = hash_password("jane34678_23"),
            role = "user"
        ),
        User(
            username = "Manuel Garcia",
            email = "garcia0823@test.com",
            password_hash = hash_password("nicole_234891$"),
            role = "user"
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    return [user.user_id for user in users]

def seed_projects(users_ids):
    projects = [
        Project(
            project_name = "Task Manager API",
            description = "RESTful API",
            owner_id = users_ids[0]       
        ),
        Project(
            project_name = "Repairing BMW",
            description = "Repairing an old damaged BMW",
            owner_id = users_ids[1]
        ),
        Project(
            project_name = "Building a Website",
            description = "Designing a Website for a poet and writer",
            owner_id = users_ids[2]
        )
    ]
    
    db.session.add_all(projects)
    db.session.commit()   
    
    return [project.project_id for project in projects] 
    
def seed_tasks(projects_ids):    
    tasks = [
        # Tasks for first Project
        Task(
            task_name = "Understand the business logic",
            description = "Make sure to understand the logical aspect of the API",
            project_id = projects_ids[0]
        ),
        Task(
            task_name = "Define the Logic of the API",
            description = "Upon understanding the business logic, define the structure of the API",
            project_id = projects_ids[0]
        ), 
        Task(
            task_name = "Understand missing functionality",
            description = "Make sure to understand what's not working with the car",
            project_id = projects_ids[1]
        ),
        Task(
            task_name = "Order Parts",
            description = "Based on what's not working, get the properly functionaning parts",
            project_id = projects_ids[1]
        ),
        Task(
            task_name = "Understand the service of the website",
            description = "What is the purpose that the client has for the website",
            project_id = projects_ids[2]
        ),
        Task(
            task_name = "Discuss the layout of the website",
            description = "Provide samples for client to determine how they want the layout for their website",
            project_id = projects_ids[2]
        )
    ]
    
    db.session.add_all(tasks)
    db.session.commit()