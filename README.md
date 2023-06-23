# FastAPI-solfacil-backend

* API desenvolvida usando o framework FastAPI para resolver o desafio https://github.com/solfacil/desafio-solfacil/blob/main/README.md
* Todo o processo de deploy foi feito e sua documentação interativa pode ser acessada em https://solfacil.dev-andre-machna.com.br/
* Serviços AWS utilizados

  -RDS: Para banco de dados postgreSQL

  -Route 53: - Para configuração de dominio e DNS

  -EC2: Para hostear a API

# Instruçoes para Execução:

git clone https://github.com/AndreMachna11/FastAPI-solfacil-backend.git

cd FastAPI-solfacil-backend

pip3 install pipenv

pipenv shell

uvicorn main:app --reload

