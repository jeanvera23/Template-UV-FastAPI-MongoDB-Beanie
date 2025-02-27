import json
from fastapi import HTTPException
from api.middlewares.auth import AuthHandler
from models.UsersModel import UsersModel

auth_handler = AuthHandler()


async def signup(email, password, firstName, lastName):
    hashed_password = auth_handler.get_password_hash(password)

    # Create a new user object
    user = UsersModel(
        email=email,
        password=hashed_password,
        firstName=firstName,
        lastName=lastName
    )

    # Save the user
    await user.create()
    return user


async def login(email, password):
    # Find user by email
    user = await UsersModel.find_one(UsersModel.email == email)
    print(user)
    if user:
        # Verify password
        isMatch = auth_handler.verify_password(password, user.password)
        if (isMatch):
            token = auth_handler.encode_token(user)
            return token
        else:
            raise HTTPException(
                status_code=401, detail='Invalid username and/or password')
    else:
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')


async def get_all():
    users_list = await UsersModel.find_all().to_list()
    return users_list


async def get_by_id(id):
    user = await UsersModel.get(id)

    if user == None:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")

    return user


async def update_by_id(id, firstName, lastName):
    user = await UsersModel.get(id)

    if user == None:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")

    # Update values
    user.firstName = firstName
    user.lastName = lastName

    # Save changes
    await user.save()
    return user


async def delete_by_id(id):
    user = await UsersModel.get(id)

    if user == None:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")
        
    await user.delete()
    
    return True
