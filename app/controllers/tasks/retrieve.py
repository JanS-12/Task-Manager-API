from app.services.tasks.retrieve import GetTaskService, GetTasksService
from app.schemas.tasks.task_response_schema import TaskResponseSchema
from app.utils.responses import build_success_response
from flask import jsonify

class GetTaskController:
    def __init__(self, service: GetTaskService):
        self.service = service
        self.response_schema = TaskResponseSchema()
        
    def get_task(self, project_id, task_id, user_id):
        task = self.service.get_task(project_id, task_id, user_id)
        return jsonify(
            build_success_response(
                "Task retrieved successfully",
                200, 
                self.response_schema.dump(task)
            )
        ), 200
    
class GetTasksController:
    def __init__(self, service: GetTasksService):
        self.service = service
        self.response_schema = TaskResponseSchema(many = True)
        
    def get_tasks(self, project_id, user_id):
        tasks = self.service.get_tasks(project_id, user_id)
        return jsonify(
            build_success_response(
                "Tasks retrieved successfully",
                200, 
                self.response_schema.dump(tasks)
            )
        ), 200