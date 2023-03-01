
from fastapi import FastAPI

from app.api.shop_api import shop_router
from app.api.user_api import user_router


app = FastAPI() 


app.include_router(shop_router, tags=["Shop Products"], prefix="/api/shop")
app.include_router(user_router, tags=["Shop User"], prefix="/api/users")

@app.get('/healthchecker')
async def root(): 
    return { 
        "message": "Fast API app is running smoothly"
    }

