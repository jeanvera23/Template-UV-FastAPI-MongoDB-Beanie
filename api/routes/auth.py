from fastapi import APIRouter, Body
from api.middlewares.auth import AuthHandler

# services
import services.users as service

router = APIRouter()
auth_handler = AuthHandler()


@router.post('/login')
async def login(body=Body()):
    email = body["email"]
    password = body["password"]
    token = await service.login(email, password)
    return {"token": token}


@router.post("/signup")
async def create_user(body=Body()):
    firstName = body["firstName"]
    lastName = body["lastName"]
    email = body["email"]
    password = body["password"]
    user = await service.signup(email, password, firstName, lastName)
    return user
