
from sqlalchemy.orm import Session

from app.database import get_db
from app.database import engine 
from app.models.user_model import ShopUser
from app.schemas.user_schema import UserInDB


session = Session(bind=engine)

def test_get_user(username: str): 

    user = session.query(ShopUser).filter(ShopUser.username == username).first() 
    


test_get_user("dev1")

    