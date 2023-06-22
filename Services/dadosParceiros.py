import dotenv
import os
from Database.connection import postgreSQL_pool_geral
dotenv.load_dotenv(dotenv.find_dotenv())

class DadosParceiros():
    
    def first(self):
        return 'ok do service DadosParceiros'