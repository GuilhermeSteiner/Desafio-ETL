import requests #Importa as requisições HTTP
import json #Importa a manipulação dos dados JSON
from concurrent.futures import ThreadPoolExecutor, as_completed #Importa a execução em paralelo para acelerar a coleta de dados de temperatura

#Carrega as configurações do arquivo de configuração config.json
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

API_URL = config["api_url"] #Usa a URL base da API
MAX_WORKERS = config["max_workers"] #Define a quantidade de threads utilizadas

#Função para obter a temperatura de uma estação usando um ID IBGE
def get_temperatura(session, id_ibge):
    try:
        #Monta a URL com o ID IBGE e az uma requisição GET, caso a resposta não seja bem sucedida, retorna None
        url = API_URL.format(id_ibge)
        r = session.get(url, timeout=5)
        if r.status_code != 200:
            return None
        data = r.json()  #A resposta é convertida em JSON

        #Função recursiva para encontrar "TEM_INS" no JSON
        def buscar_temp(obj):
            #Verifica se o JSON obtido é um dicionário
            if isinstance(obj, dict):
                for k, v in obj.items():

                    #Se a chave desejada for encontrada retorna o valor convertido em float, retorna None caso não tenha sido possível converter
                    if k == "TEM_INS" and v is not None:
                        try:
                            return float(v)
                        except:
                            return None
                        
                    #A função é chamada novamente e só retorna quando encontrar um valor válido   
                    res = buscar_temp(v)
                    if res is not None:
                        return res
                    
            #Caso não seja um dicionário, é verificado se o JSON obtido é uma lista
            elif isinstance(obj, list):

                for item in obj:
                    #Chama a função recursiva para cada elemento da lista, retorna quando obter um valor válido
                    res = buscar_temp(item)
                    if res is not None:
                        return res
                    
            #No caso de não encontrar nenhum "TEM_INS", retorna-se None
            return None
        
        #Retorna a temperatura encontrada
        return buscar_temp(data)

    #No caso de erro, retorna None e printa no terminal o ID IBGE que está com problemas na API
    except Exception as e:
        print(f"Erro no ID {id_ibge}: {e}")
    return None


#Para evitar erros de conversão, troca-se a vírgula do valor float por ponto
def parse_float(valor):
    if valor is None:
        return None
    return float(valor.replace(",", "."))

#Processa uma estação: valida dados, busca temperatura e retorna organizado
def process_estacao(session, est):
    id_ibge = est.get("id") # Obtém o ID IBGE da estação

    #Retorna none caso não encontre o ID da estação
    if not id_ibge:
        return None

    #Obtém nome e estado da estação
    nome = est.get("nome")
    uf = est.get("estado")

    #Obtém latitude e longitudade da estação
    lat = parse_float(est.get("lat")) 
    lon = parse_float(est.get("lon"))

    #Caso uma das duas tiverem um valor inválido, retorna None
    if lat is None or lon is None:
        return None

    #Obtém a temperatura que a estação está denotando na API
    temp = get_temperatura(session, id_ibge)

    #Printa no terminal o nome e a temperatura obtida da estação
    print(f"{nome}: {temp}")

    #Retorna em output.json as informações obtidas daquela estação
    return {
        "nome": nome,
        "uf": uf,
        "codigo_ibge": id_ibge,
        "latitude": lat,
        "longitude": lon,
        "temperatura": temp
    }

#Carrega estações, busca temperaturas em paralelo e retorna lista de dados processados
def extract_data():
    print("Carregando estações do JSON...")

    #Abre o JSON com as estações
    with open("data/estacoes.json", "r", encoding="utf-8") as f:
        conteudo = json.load(f)

    #Obtém todas as estações dentro do JSON
    estacoes = conteudo.get("data", [])

    #Lista para armazenar os resultados
    dados = []

    print("Buscando temperaturas (threads)...")

    #Reutiliza-se as conexões HTTP e cria uma pool de threads
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            #Cria tarefas para processar cada estação em paralelo
            futures = [
                executor.submit(process_estacao, session, est)
                for est in estacoes
            ]

            #Coleta os resultados e adiciona na lista
            for future in as_completed(futures):
                result = future.result()
                if result:
                    dados.append(result)

    #Mostra a quantidade de estações encontradas
    print(f"Dados coletados: {len(dados)}")

    #Retorna a lista com os resultados armazenados
    return dados