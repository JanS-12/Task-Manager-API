from app.schemas.tasks.task_response_schema import TaskResponseSchema
from app.schemas.tasks.update_task_schema import UpdateTaskSchema
from app.services.tasks.modify import UpdateTaskService
from app.utils.responses import build_success_response
from flask import jsonify

class UpdateTaskController:
    def __init__(self, service: UpdateTaskService):
        self.service = service
        self.udpate_schema = UpdateTaskSchema()
        self.response_schema = TaskResponseSchema()
        
    def update_task(self, data, project_id, task_id, user_id):
        validated = self.udpate_schema.load(data)
        task = self.service.update_task(validated, project_id, task_id, user_id)
        return jsonify(
            build_success_response(
                "Task updated successfully",
                200, 
                self.response_schema.dump(task)
            )
        ), 200