from fastapi import FastAPI #Importa a classe principal do FastAPI
from fastapi.middleware.cors import CORSMiddleware #Importa middleware para permitir requisições externas (CORS)
import json #Importa biblioteca para manipular JSONs

app = FastAPI() #Cria a aplicaçao FastAPI

#Adiciona configuração de CORS permitindo qualquer origem, método e cabeçalho
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)


#Define rota GET no endpoint /dados
@app.get("/dados")
def get_data():
    #Abre o arquivo JSON com encoding UTF-8
    with open("data/output.json", encoding="utf-8") as f:
        return json.load(f)