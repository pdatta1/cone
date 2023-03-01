
from datetime import datetime, timedelta

from app.models.user_model import ShopUser

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status 

from passlib.context import CryptContext

from jose import JWTError, jwt

from decouple import config 

from app.schemas.user_schema import UserInDB
from app.schemas.user_schema import TokenData

from sqlalchemy.orm import Session 

from app.database import engine 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
session = Session(bind=engine)



SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')


def verify_password(plain_password: str, hashed_password: str): 
    return password_context.verify(plain_password, hashed_password)


def get_password(password: str): 
    return password_context.hash(password)


def get_user(username: str): 
    user = session.query(ShopUser).filter(ShopUser.username == username).first() 
    return user 
    

def authenticate_user(username: str, password: str): 

    user = get_user(username)
    if not user: 
        return False 
    
    if not verify_password(password, user.hash_password): 
        return False 
    
    return user 


def create_access_token(data: dict, expires_delta: timedelta | None = None): 

    """
        check if expire delta, if so, set expire variable to the current datetime plus the expires_delta,
                               if not, create a new x minutes timedelta, starting from the current datetime
    """
    to_encode = data.copy() 

    if expires_delta: 
        expires = datetime.utcnow() + expires_delta
    else: 
        expires = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)): 

    credentials_exception = HTTPException(
        status_Code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        if not username: 
            raise credentials_exception
        
        token_data = TokenData(username=username)
    
    except JWTError: 
        raise credentials_exception
    
    user_db = session.query(ShopUser).all()
    user = get_user(user_db, username=token_data.username)
    if user is None: 
        raise credentials_exception
    
    return user 
        

    



    


