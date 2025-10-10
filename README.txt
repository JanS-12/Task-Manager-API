This is a Task Manager RESTFul API


File Structure
taskmanager/
│── app.py                  # Entry point
│── requirements.txt
│── .env
│── .gitignore
│
└── app/
    │── __init__.py          # Creates Flask app, loads config, registers blueprints
    │── config.py            # Config class
    │── extensions.py        # db, etc.
    │
    ├── models/             
    │   ├── __init__.py
    │   ├── user.py
    │   ├── project.py
    │   └── task.py
    │
    ├── schemas/
    │   ├── __init__.py
    │   ├── user_schema.py
    │   ├── project_schema.py
    │   └── task_schema.py
    │
    ├── routes/             # Blueprints, endpoints
    │    ├── __init__.py
    │    ├── users.py        
    │    ├── projects.py
    │    └── tasks.py
    │    
    ├── tests/
    │    ├── __init__.py
    │    ├── auth_tests.py
    │    ├── user_tests.py        
    │    ├── project_tests.py
    │    └── task_tests.py
    │
    └── utils/
        ├── security.py
        └── seed.py
