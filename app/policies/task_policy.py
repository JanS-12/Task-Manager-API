from app.utils.custom_exceptions import AccessDenied, TaskIncorrectProject

class TaskPolicy:
    def can_view_all_tasks(self, user):
        if user.role != "admin":
            return False
        
        return True
    
    def can_create_task(self, user, project):
        if user.role != "admin" and user.id != project.owner_id:
            raise AccessDenied()
        
        return True
    
    def can_view_task(self, user, project):
        if user.role != "admin" and project.owner_id != user.id:
            raise AccessDenied()
        
        return True
    
    def can_modify_task(self, user, project):
        if user.role != "admin" and project.owner_id != user.id:
            raise AccessDenied()
        
        return True
    
    def can_delete_task(self, user, project):
        if user.role != "admin" and project.owner_id != user.id:
            raise AccessDenied()
        
        return True
    
    def belong_to_project(self, project, task):
        if task.project_id != project.id:
            raise TaskIncorrectProject()
        
        return True
        

    
      
      
     
        