from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

from Services.authenticate import authenticate
from Services.atualizacaoBancoDeDadosService import AtualizacaoBancoDeDadosService
from Services.listagemParceirosService import ListagemParceirosService
from Services.dadosParceiros import DadosParceiros

from models import BodyAtualizacaoParceiros

app = FastAPI()

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/atualizacaoParceiros")
async def atualiza_banco_de_dados(Body: BodyAtualizacaoParceiros,token: str = Depends(authenticate)):
    
    SERVICE = AtualizacaoBancoDeDadosService()

    retorno = SERVICE.verifica_base_cnpjs(Body.url_csv_hosteado)
    base_input = retorno[0]
    validador = retorno[1]

    if validador == False:
        content = {"mensagem" : "CSV contem cpf na coluna cnpj ou esta vazio - Reveja seus dados", "response": {}}
        return JSONResponse(content=content, status_code=400)

    base_input = SERVICE.renomeia_colunas_data_frame(base_input)
    SERVICE.atualiza_banco_de_dados_via_data_frame(base_input,'parceiros','cnpj')

    base_ceps = SERVICE.pega_infs_ceps(base_input)
    SERVICE.atualiza_banco_de_dados_via_data_frame(base_ceps,'infs_cep_parceiros','cep')
    
    content = {"mensagem" : "Sucesso", "response": {}}
    return JSONResponse(content=content, status_code=200)

@app.get("/ListagemParceiros")
async def listagem(token: str = Depends(authenticate)):
    
    SERVICE = ListagemParceirosService()
    parceiros_atuais = SERVICE.listagem()
    
    return JSONResponse(content=parceiros_atuais, status_code=200)

@app.get("/DadosParceiros/{cnpj}")
async def dados_parceiros(cnpj: str,token: str = Depends(authenticate)):
    
    SERVICE = DadosParceiros()
    teste = SERVICE.first()
    
    return teste