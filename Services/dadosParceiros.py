import dotenv
import os
import pandas
from Database.connection import postgreSQL_pool_geral
dotenv.load_dotenv(dotenv.find_dotenv())

class DadosParceiros():
    
    def retorna_infs_parceiros(self,cnpj):

        if cnpj != '0':
            cnpj = self.formatar_cnpj(cnpj)
            
            query = '''
                SELECT
                    parceiros.*,
                    infs_cep_parceiros.*
                FROM
                    parceiros,
                    infs_cep_parceiros
                WHERE
                    parceiros.cep = infs_cep_parceiros.cep and
                    parceiros.cnpj = '%s';
            '''%(cnpj)
        else:

            query = '''
                SELECT
                    parceiros.*,
                    infs_cep_parceiros.*
                FROM
                    parceiros,
                    infs_cep_parceiros
                WHERE
                    parceiros.cep = infs_cep_parceiros.cep;
            '''

        con = postgreSQL_pool_geral.getconn()
        dados_parceiros = pandas.read_sql(query,con)
        postgreSQL_pool_geral.putconn(con)
        
        return dados_parceiros
    
    def formatar_cnpj(self,cnpj):

        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')  # Remove os pontos, barras e traços
        cnpj_formatado = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
        
        return cnpj_formatado