from fastapi import APIRouter, Depends, Body
from api.middlewares.auth import AuthHandler

# services
import services.users as service

router = APIRouter()
auth_handler = AuthHandler()


@router.get("/")
async def get_all_users(tokenUser=Depends(auth_handler.auth_wrapper)):
    print(tokenUser)
    users = await service.get_all()
    return users


@router.get("/{id}")
async def get_user(id: str, tokenUser=Depends(auth_handler.auth_wrapper)):
    print(tokenUser)
    user = await service.get_by_id(id)
    return user


@router.put("/{id}")
async def update_user(id: str, body=Body()):
    firstName = body["firstName"]
    lastName = body["lastName"]

    user = await service.update_by_id(id, firstName, lastName)
    return user


@router.delete("/{id}")
async def delete_user(id: str):
    result = await service.delete_by_id(id)
    return {"result": result}
