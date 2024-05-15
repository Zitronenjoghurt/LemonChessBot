from pydantic import BaseModel

class ApiKeyResponse(BaseModel):
    api_key: str

class RoomInfo(BaseModel):
    code: str
    created_stamp: int
    name: str
    public: bool
    user_name: str