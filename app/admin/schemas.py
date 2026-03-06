from pydantic import BaseModel


class ChangeUserRole(BaseModel):
    role_name: str