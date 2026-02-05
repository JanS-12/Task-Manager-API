from app.utils.custom_exceptions import AccessDenied

class ProjectPolicy:
    def can_view_project(self, requester, project): 
        if requester.role != "admin" and requester.id != project.owner_id:
            raise AccessDenied()
        
        return True
        
    def can_view_all_projects(self, requester):
        if requester.role != "admin":
            return False
        
        return True
    
    def can_update_project(self, requester, project):
        if requester.role != "admin" and requester.id != project.owner_id:
            raise AccessDenied()
        
        return True
    
    def can_remove_project(self, requester, project):
        if requester.role != "admin" and requester.id != project.owner_id:
            raise AccessDenied()
        
        return True