from app.services.tasks.modify import UpdateTaskService
from app.utils.custom_exceptions import NoDataError
from app.schemas.task_schema import TaskSchema


class UpdateTaskController:
    def __init__(self, service: UpdateTaskService):
        self.service = service
        self.schema = TaskSchema()
        
    def update_task(self, data, project_id, task_id, user_id):
        if not data:
            raise NoDataError()
        
        task_data = self.schema.load(data)
        task = self.service.update_task(task_data, project_id, task_id, user_id)
        return self.schema.jsonify(task), 200