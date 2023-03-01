
import pandas as pd 
import os 
import pathlib 

from app.models.shop_model import ShopProducts
from app.database import get_db
from app.database import engine 
import app 

from sqlalchemy.orm import Session

SUPPORTED_FILES = { 
    "csv": ".csv",
    "json": ".json"
}

MODELS = [ 
    ShopProducts,
]

class PopulateUtil(object): 

    """
        responsible for populating a orm model by reading a json, csv, etc files.
    """

    def __init__(self, module, cleanup=False): 

        self.module = os.path.dirname(module.__file__)
        self.session = Session(bind=engine)
        
        if cleanup: 
            self.clear_database() 



    def clear_database(self): 


        self.session.query(*[model for model in MODELS]).delete() 
        self.session.commit() 


    def read_file_data(self, file_path: str) -> pd.DataFrame: 

        dataframe: pd.DataFrame | None = None 
        file_dir = os.path.join(self.module, file_path)
        valid_extension: list[str] = [ext for ext in SUPPORTED_FILES.values()]


        file_extension = pathlib.Path(file_dir).suffix

        if not os.path.exists(file_dir): 
            raise FileExistsError(f"Error location file path: {file_dir}")
        
        if file_extension not in valid_extension: 
            raise ValueError(f"Extesion is not supported: {file_extension}")
        

        if file_extension == SUPPORTED_FILES["csv"]: 
            dataframe = pd.read_csv(file_dir)

        if file_extension == SUPPORTED_FILES["json"]: 
            dataframe = pd.read_json(file_dir)

        return dataframe
    

    def save_to_model(self, file_dir: str) -> None:

        directory = os.path.join(self.module, file_dir)
        bulk_data: list[ShopProducts] = [] 

        df = self.read_file_data(directory)
        data = df.to_dict() 
        data_len = len(data["product_type"])

        for id in range(data_len): 

            product_model = ShopProducts(
                product_description=data['product_description'][id],
                product_price = data['product_price'][id],
                product_type = data['product_type'][id]
            )
            bulk_data.append(product_model)

        #print(f'length of bulk_data: {len(bulk_data)}')
        self.session.add_all(bulk_data)
        self.session.commit() 



def populate_database(): 

    util = PopulateUtil(app, cleanup=True)
    util.save_to_model('datasets/products.csv')


populate_database() 


        




        