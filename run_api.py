import uvicorn #Importa o servidor ASGI para rodar a API FastAPI
import json #Importa a manipulação dos dados JSON

#Abre o arquivo de configuração
with open("config.json", encoding="utf-8") as f:
    config = json.load(f) #Carrega os dados do config.json

#Executa apenas se o arquivo for rodado diretamente
if __name__ == "__main__":
    uvicorn.run("api.main:app", #Caminho do app FastAPI 
                host=config["api_host"], #IP onde o servidor vai rodar
                port=config["api_port"], #Porta do servidor
                reload=True #Reinicia automaticamente quando o código muda
                )