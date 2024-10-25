from models.userSchema import user_schema
from models.userSchema import User
from fastapi import HTTPException
from .databaseController import get_users_collection


async def create_user(phone_num : int , energy_consumption : float):
    try:
        user_collection = await get_users_collection()
        existing_user = await user_collection.find_one({"phone_number": phone_num})
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this phone number already exists")
        user_dict = {
            "phone_number": phone_num,
            "energy_consumption": energy_consumption,
            "active_stocks": [],
            "balance": 0
        }
        await user_collection.insert_one(user_dict)
        return user_dict
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")


async def get_user_by_phone(phone_number: str):
    try:
        user_collection = await get_users_collection()
        user = await user_collection.find_one({"phone_number": phone_number})
        if user:
            return user_schema(user)
        return None
    except Exception as e:
        print(f"Error fetching user by phone: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user by phone")
    

async def getHoldings(phone_num):
    
    user_collection = await get_users_collection()
    existing_user = await user_collection.find_one({"phone_number": phone_num})

    if existing_user:
        return existing_user["active_stocks"]
    else:
        raise HTTPException(status_code=404, detail="User not found")
    




