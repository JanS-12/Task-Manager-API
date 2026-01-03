class DI:
    user_repository = None
    token_repository = None
    project_repository = None
    task_repository = None
    
    auth_service = None
    user_service = None
    project_service = None
    task_service = None
    
    # New -> SRP and OCP -- Services and Controllers
    user_profile_service = None
    user_profile_controller = None
    
    users_profile_service = None
    users_profile_controller = None
    
    registration_service = None
    registration_controller = None
    
    login_service = None
    login_controller = None
    
    logout_service = None
    logout_controller = None
    
    update_service = None
    update_controller = None
    
    remove_service = None
    remove_controller = None