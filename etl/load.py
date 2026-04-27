import json  #Importa a manipulação dos dados JSON
import os  #Importa a permissão de utilizar o sistema operacional, acessando arquivos e diretórios


#Salva os dados processados em formato GeoJSON
def save_data(data):
    os.makedirs("data", exist_ok=True)  #Cria pasta "data" se ela não existir

    #Define a estrutura inicial do GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    #Percorre cada item da lista de dados e ignora caso não hajam coordenadas válidas
    for item in data:
        if item["latitude"] is None or item["longitude"] is None:
            continue

        temp = item["temperatura"]  #Obtém temperatura

        #Trata casos sem temperatura
        if temp is None:
            temp = "Sem dado"
            classificacao = "Sem dado"
        else:
            classificacao = item["classificacao"]  #Obtém classificação

        #Cria uma feature no padrão GeoJSON
        feature = {
            "type": "Feature",
            "properties": {
                "nome": item["nome"],  
                "uf": item["uf"],  #Estado
                "temperatura": temp,
                "classificacao": classificacao
            },
            "geometry": {
                "type": "Point",  #Tipo de geometria
                "coordinates": [item["longitude"], item["latitude"]]
            }
        }
        #Adiciona feature ao GeoJSON
        geojson["features"].append(feature)

    #Salva o arquivo GeoJSON no disco
    with open("data/output.json", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)

    #Mostra quantidade pontos salvos
    print(f"GeoJSON salvo com {len(geojson['features'])} pontos")