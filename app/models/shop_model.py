

from sqlalchemy import Integer, Float, String, TIMESTAMP, Column 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 



ProductBase = declarative_base() 


class ShopProducts(ProductBase): 

    __tablename__ = "shopproducts"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_description = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    product_type = Column(String, nullable=False)
    product_date = Column(TIMESTAMP(timezone=True), server_default=func.now())






    




