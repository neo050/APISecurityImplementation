# app/validators.py

from pydantic import BaseModel, constr, ValidationError

class LoginModel(BaseModel):
    user_id: constr(min_length=3, max_length=50)

def validate_login(data):
    """
    Validates the login data using Pydantic.
    """
    try:
        login_data = LoginModel(**data)
        return login_data
    except ValidationError as e:
        return str(e), 400
