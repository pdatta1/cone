
from pydantic import BaseModel 
from app.models.user_model import ShopUser


class ShopUserSchemaBase(BaseModel): 

    username: str 
    password: str 

    class Config: 

        orm_mode = True 
        allow_population_by_field_name = True 
        arbitrary_type_allowed = True 



class Token(BaseModel): 

    access_token: str 
    token_type: str 


class TokenData(BaseModel): 

    username: str | None = None 


class UserInDB(ShopUser): 

    hash_password: str 






        