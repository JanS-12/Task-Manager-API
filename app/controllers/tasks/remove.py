from app.services.tasks.remove import RemoveTaskService

class RemoveTaskController:
    def __init__(self, service: RemoveTaskService):
        self.service = service
        
    def remove_task(self, project_id, task_id, user_id):
        self.service.remove_task(project_id, task_id, user_id)