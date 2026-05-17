from app.schemas.tasks.task_response_schema import TaskResponseSchema
from app.schemas.tasks.create_task_schema import CreateTaskSchema
from app.services.tasks.create import CreateTaskService
from app.utils.responses import build_success_response
from flask import jsonify
class CreateTaskController:
    def __init__(self, service: CreateTaskService):
        self.service = service
        self.create_schema = CreateTaskSchema()
        self.response_schema = TaskResponseSchema()
        
    def create_task(self, data, project_id, user_id):
        validated = self.create_schema.load(data)
        task = self.service.create_task(validated, project_id, user_id)
        return jsonify(
            build_success_response(
                "Task created successfully",
                201, 
                self.response_schema.dump(task)
            )
        ), 201