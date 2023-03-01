from datetime import timedelta
from app.models.user_model import ShopUser
from app.schemas.user_schema import ShopUserSchemaBase, Token
from app.database import get_db
from app.security.auth_token import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


from fastapi import Depends, HTTPException, APIRouter, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi_utils.cbv import cbv

from sqlalchemy.orm import Session 


user_router = APIRouter() 



@cbv(user_router)
class ShopUserApi(object): 

    session: Session = Depends(get_db)


    @user_router.post('/', status_code=status.HTTP_201_CREATED)
    def create_user(self, payload: ShopUserSchemaBase): 

        new_user = ShopUser(**payload.dict())

        self.session.add(new_user)
        self.session.commit() 
        self.session.refresh(new_user)

        content = { 
            "status": status.HTTP_201_CREATED, 
            "user": new_user 
        }
        return content 
    
    
    @user_router.post('/', status_code=status.HTTP_200_OK)
    def login_user(self, payload: ShopUserSchemaBase): 
        pass 
    

    @user_router.patch('/', status_code=status.HTTP_201_CREATED)
    def update_user(self, userId: int, payload: ShopUserSchemaBase): 

        user_query = self.session.query(ShopUser).filter(ShopUser.id == userId)
        user_data = user_query.first() 

        if not user_data: 
            raise HTTPException(f"User not found with given ID: {userId}")
        
        update_data = payload.dict(exclude_unset=True)
        user_query.filter(ShopUser.id == userId).update(update_data, synchronize_session=False)

        self.session.commit() 
        self.session.refresh(update_data)

        return { 
            "status": status.HTTP_200_OK,
            "user": user_data
        }
    

    @user_router.get("/{userId}", status_code=status.HTTP_200_OK)
    def get_user_by_id(self, userId: int): 

        if userId: 
            user_query = self.session.query(ShopUser).filter(ShopUser.id == userId).first() 

        if not user_query: 
            raise HTTPException(f"User cannot be found with given ID: {userId}")
        
        content = {
            "status": status.HTTP_200_OK,
            "user": user_query 
        }
        return content 
    




@cbv(user_router)
class AccessToken(object): 

    session: Session = Depends(get_db)

    @user_router.post('/access', status_code=status.HTTP_200_OK, response_model=Token)
    async def get_user_token(self, form_data: OAuth2PasswordRequestForm = Depends()): 
        
        user = authenticate_user(form_data.username, form_data.password)
        if not user: 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=f"Incorrect Username or Password, {form_data.username}, {form_data.password}, {user_db}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        return { 
            "access_token": access_token,
            "token_type": "bearer"
        }
    

    
