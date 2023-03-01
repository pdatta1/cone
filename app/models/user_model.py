
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates 

from passlib.hash import bcrypt





UserBase = declarative_base() 

class ShopUser(UserBase): 

    __tablename__ = "shop_users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False, index=True)
    hash_password = Column("password", String, nullable=False)


    @hybrid_property
    def password(self): 
        return self.hash_password
    
    @password.setter 
    def password(self, password): 
        self.hash_password = bcrypt.hash(password)

    @validates("username")
    def validate_username(self, key, value): 
        if not value: 
            raise ValueError("Username cannot be empty")
        return value 
    
    @validates("password")
    def validate_password(self, key, value): 
        if not value: 
            raise ValueError("Password cannot be empty")
        
    def verify_password(self, password): 
        return bcrypt.verify(password, self.password)
    


    def __repr__(self): 
        return f"<User username={self.username}, password={self.hash_password}/>"