from pydantic import BaseModel
import uuid

class LoginRequest(BaseModel):
    username: str
    password: str

# Response after login
class LoginResponse(BaseModel):
    message: str
    id: uuid.UUID