from hrflow.database.models.base_db_model import BaseDBModel

def get_declarative_base():
    from hrflow.database.models.jobpost_model import JobPostModel
    from hrflow.database.models.application_model import ApplicationModel
    from hrflow.database.models.user_model import UserModel
    
    return BaseDBModel