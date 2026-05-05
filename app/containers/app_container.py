from .user_container import User_DI
from .project_container import Project_DI
from .task_container import Task_DI

class AppContainer:
    user = User_DI
    project = Project_DI   
    task = Task_DI
        
    def register_dependencies():
            AppContainer.user.register_user_dependencies()
            AppContainer.project.register_project_dependencies()
            AppContainer.task.register_task_dependencies()