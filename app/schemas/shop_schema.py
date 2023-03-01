

from pydantic import BaseModel 


class ShopProductSchemaBase(BaseModel): 

    product_description: str | None = None 
    product_price: float | None = None 
    product_type: str | None = None 

    class Config: 
        orm_mode = True 
        allow_population_by_field_name = True 
        arbitrary_type_allowed = True 



