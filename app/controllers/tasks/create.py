from app.services.tasks.create import CreateTaskService
from app.utils.responses import build_success_response
from app.utils.custom_exceptions import NoDataError
from app.schemas.task_schema import TaskSchema
from flask import jsonify
class CreateTaskController:
    def __init__(self, service: CreateTaskService):
        self.service = service
        self.schema = TaskSchema()
        
    def create_task(self, data, project_id, user_id):
        if not data:
            raise NoDataError()
        
        task_data = self.schema.load(data)
        task = self.service.create_task(task_data, project_id, user_id)
        return jsonify(
            build_success_response(
                "Task created successfully",
                201, 
                self.schema.dump(task)
            )
        ), 201