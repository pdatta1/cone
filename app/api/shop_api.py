

from app.database import get_db 
from app.models.shop_model import ShopProducts
from app.schemas.shop_schema import ShopProductSchemaBase

from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi_utils.cbv import cbv 

from sqlalchemy.orm import Session 


shop_router = APIRouter() 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@cbv(shop_router)
class ShopProductsApi(object): 


    session: Session = Depends(get_db)


    
    @shop_router.get('/', status_code=status.HTTP_200_OK)
    def get_shop_product(self, limit: int = 100, page: int = 1, search: str = '') -> dict: 

        skip = (page  - 1) * limit 

        product_query = self.session.query(ShopProducts).filter(ShopProducts.product_id.contains(search)).limit(limit).offset(skip).all() 
        content = { 
            "status": status.HTTP_200_OK, 
            "results": len(product_query), 
            "products": product_query
        }
        return content 
    

    @shop_router.post('/', status_code=status.HTTP_201_CREATED)
    def create_shop_product(self, payload: ShopProductSchemaBase): 

        product = ShopProducts(**payload.dict())
        self.session.add(product)
        self.session.commit() 
        self.session.refresh(product)

        content = { 
            "status": status.HTTP_201_CREATED, 
            "product": product
        }
        return content 
    

    @shop_router.patch('/{productId}', status_code=status.HTTP_200_OK)
    def update_product(self, productId: int, payload: ShopProductSchemaBase): 

        product_query = self.session.query(ShopProducts).filter(ShopProducts.product_id == productId)
        product_data = product_query.first() 

        if not product_query: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product cannot be found with ID: {productId}")
        
        update_data = payload.dict(exclude_unset=True)

        if update_data.get('product_price') > 20: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price cannot be greater than 20 bucks")
        

        product_query.filter(ShopProducts.product_id == productId).update(update_data, synchronize_session=False)

        self.session.commit() 
        self.session.refresh(product_data)

        return { 
            "status": status.HTTP_200_OK,
            "update": product_data
        }
    
    
    @shop_router.get('/{productId}', status_code=status.HTTP_200_OK)
    def get_product_by_id(self, productId: int): 

        product_query = self.session.query(ShopProducts).filter(ShopProducts.product_id == productId).first() 
        
        if not product_query: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product cannot be found with ID: {productId}")
        
        content = { 
            "status": status.HTTP_200_OK,
            "product": product_query
        }

        return content 







