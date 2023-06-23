# FastAPI-solfacil-backend

* API desenvolvida usando o framework FastAPI para resolver o desafio https://github.com/solfacil/desafio-solfacil/blob/main/README.md
* Todo o processo de deploy foi feito e sua documentação interativa pode ser acessada em https://solfacil.dev-andre-machna.com.br/
* Serviços AWS utilizados

  -RDS: Para banco de dados postgreSQL

  -Route 53: - Para configuração de dominio e DNS

  -EC2: Para hostear a API

# Instruçoes para Execução
```sh
git clone https://github.com/AndreMachna11/FastAPI-solfacil-backend.git
```

```sh
cd FastAPI-solfacil-backend
```

```sh
pip install pipenv
```

```sh
pipenv shell
```

```sh
pipenv install pipfile
```

```sh
uvicorn main:app --reload
```

# Instruçoes para Uso dos endpoints

Todos os endpoints exigem um token no header da requisição, nesta api ele é unico e estatico 
```sh
d9520359df50574372fb8022fb56b90671cbf5c388132953a69b28d5ec37bfb6
```
So caso do csv especifico, para simular um dado vindo de um possivel front end, hosteei o csv de exemplo em um link e este link é passado no body do endpoint de atualização

Base completa:
```sh
https://ucarecdn.com/b840097e-41b2-4916-b0f5-299c6749be29/
```

Contendo apenas cnpjs:
```sh
https://ucarecdn.com/a2123485-6b43-437b-a3be-8b7612367352/
```



