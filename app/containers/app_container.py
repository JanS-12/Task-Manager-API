from .user_container import UserContainer
from .project_container import ProjectContainer
from .task_container import TaskContainer

class AppContainer:
    def __init__(self):
        self.user = UserContainer()
        self.project = ProjectContainer()
        self.task = TaskContainer()