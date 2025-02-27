from beanie import Document
from datetime import datetime

class UsersModel(Document):
    email: str
    password: str
    firstName: str
    lastName: str
    lastName: str
    createdAt: datetime = datetime.now()

    class Settings:
        name = "users"