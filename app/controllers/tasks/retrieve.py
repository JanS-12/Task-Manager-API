from app.services.tasks.retrieve import GetTaskService, GetTasksService
from app.schemas.task_schema import TaskSchema

class GetTaskController:
    def __init__(self, service: GetTaskService):
        self.service = service
        self.schema = TaskSchema()
        
    def get_task(self, project_id, task_id, user_id):
        task = self.service.get_task(project_id, task_id, user_id)
        return self.schema.jsonify(task), 200
    
class GetTasksController:
    def __init__(self, service: GetTasksService):
        self.service = service
        self.schema = TaskSchema(many = True)
        
    def get_tasks(self, project_id, user_id):
        tasks = self.service.get_tasks(project_id, user_id)
        return self.schema.jsonify(tasks), 200