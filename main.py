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
async def pergunta_com_arquivo(Body: BodyAtualizacaoParceiros,token: str = Depends(authenticate)):
    SERVICE = AtualizacaoBancoDeDadosService()

    teste = SERVICE.first()

    return teste

@app.get("/DadosParceiros/{cnpj}")
async def dados_parceiros(cnpj: str,token: str = Depends(authenticate)):
    
    SERVICE = DadosParceiros()
    teste = SERVICE.first()
    
    return teste

@app.get("/ListagemParceiros")
async def listagem(token: str = Depends(authenticate)):
    
    SERVICE = ListagemParceirosService()
    teste = SERVICE.first()
    
    return teste

