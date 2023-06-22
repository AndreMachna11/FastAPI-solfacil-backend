import dotenv
import os
import pandas
from Database.connection import postgreSQL_pool_geral
dotenv.load_dotenv(dotenv.find_dotenv())

class ListagemParceirosService():
    
    def listagem(self):
        
        con = postgreSQL_pool_geral.getconn()

        query = '''
            SELECT
                cnpj,
                razao_social
            FROM
                parceiros
        '''
        listagem = pandas.read_sql(query,con)
        
        postgreSQL_pool_geral.putconn(con)

        
        lista_dicts = []    
        for i in listagem.index:

            dict_linha = {
                "cnpj" : listagem.at[i,'cnpj'],
                "razao_social" : listagem.at[i,'razao_social']
            }

            lista_dicts.append(dict_linha)


        return lista_dicts