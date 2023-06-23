import dotenv
import pandas
import os
import re
import psycopg2
import psycopg2.extras
import requests
from Database.connection import postgreSQL_pool_geral
dotenv.load_dotenv(dotenv.find_dotenv())

class AtualizacaoBancoDeDadosService():
    
    def verifica_base_cnpjs(self,url_csv):
        
        #Transforma url em DataFrame
        try:
            base_input = pandas.read_csv(url_csv,keep_default_na=False)
        except:
            base_input = pandas.DataFrame()

        if base_input.empty == True:
            validador = False
        else:
            validador = True

        if validador == True:
            #Verifica se existe um cpf em meio aos cnpjs
            for i in base_input.index:
                cnpj = base_input.at[i,'CNPJ']
                validador = self.valida_cnpj(cnpj)
                if validador == False:
                    break
        else:
            pass

        return base_input, validador

    def renomeia_colunas_data_frame(self,base_input):

        base_input_para_upsert = pandas.DataFrame()
        base_input_para_upsert['cnpj'] = base_input['CNPJ']
        base_input_para_upsert['razao_social'] = base_input['Razão Social']
        base_input_para_upsert['nome_fantasia'] = base_input['Nome Fantasia']
        base_input_para_upsert['telefone'] = base_input['Telefone']
        base_input_para_upsert['email'] = base_input['Email']
        base_input_para_upsert['cep'] = base_input[' CEP']

        for i in base_input_para_upsert.index:
            base_input_para_upsert.at[i,'cnpj'] = self.formatar_cnpj(base_input_para_upsert.at[i,'cnpj'])

        return base_input_para_upsert
       
    def valida_cnpj(self,cnpj):
        cnpj = re.sub(r'\D', '', cnpj)

        if len(cnpj) != 14:
            return False

        if cnpj == cnpj[0] * 14:
            return False

        soma = 0
        peso = 5
        for i in range(12):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        digito1 = soma % 11
        digito1 = 0 if digito1 < 2 else 11 - digito1

        soma = 0
        peso = 6
        for i in range(13):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        digito2 = soma % 11
        digito2 = 0 if digito2 < 2 else 11 - digito2

        if int(cnpj[12]) != digito1 or int(cnpj[13]) != digito2:
            return False

        return True

    def formatar_cnpj(self,cnpj):
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')  # Remove os pontos, barras e traços
        cnpj_formatado = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
        return cnpj_formatado

    def atualiza_banco_de_dados_via_data_frame(self,df_com_dados_atualizados,nome_tabela,nome_pk):

        con = postgreSQL_pool_geral.getconn()
    
        df_columns = list(df_com_dados_atualizados)
        # create (col1,col2,...)
        columns = ",".join(df_columns)

        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns])) 

        lista_colunas = list(df_com_dados_atualizados.columns)
        
        lista_colunas_str = ''
        for i in lista_colunas:
            lista_colunas_str = lista_colunas_str + i + ','
        lista_colunas_str = lista_colunas_str[:-1]

        lista_colunas_exclued = ''
        for i in lista_colunas:
            lista_colunas_exclued = lista_colunas_exclued + 'EXCLUDED.' + i + ','
        lista_colunas_exclued = lista_colunas_exclued[:-1]

        #create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO {} ({}) {}".format(nome_tabela,columns,values) + '''
                        ON CONFLICT (%s) DO UPDATE SET (%s) = (%s)''' %(nome_pk,lista_colunas_str,lista_colunas_exclued)

        cur = con.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt, df_com_dados_atualizados.values)
        con.commit()
        cur.close()
        postgreSQL_pool_geral.putconn(con)

    def pega_infs_ceps(self,base_input):

        lista_ceps = list(pandas.unique(list(base_input.cep.values)))
        lista_dicts = []

        for i in lista_ceps:
            response = requests.get('https://viacep.com.br/ws/' + i + '/json/')
            data = response.json()
            
            lista_dicts.append(data)
        
        return pandas.DataFrame(lista_dicts)