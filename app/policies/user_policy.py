from app.utils.custom_exceptions import AccessDenied

class UserPolicy:    
    def can_create_profile(self, requester):
        print("Create Policy")
        if requester.role != "admin":
            raise AccessDenied()
        
        return True
    
    def can_view_profile(self, requester, user):
        if requester.role != "admin" and requester.id != user.id:
            raise AccessDenied()
        
        return True
        
    def can_list_users(self, requester):
        if requester.role != "admin":
            raise AccessDenied()
        
        return True
        
    def can_modify_profile(self, requester, user):
        if requester.role != "admin" and requester.id != user.id:
            raise AccessDenied()
        
        return True
    
    def can_delete_profile(self, requester):
        if requester.role != "admin":
            raise AccessDenied()
        
        return True
    