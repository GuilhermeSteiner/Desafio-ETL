#Classifica a temperatura em categorias
def classify_temp(temp):
    if temp is None:
        return "Sem dado"  #Sem temperatura disponível na API
    elif temp < 20:
        return "Baixa"  #Temperatura baixa
    elif temp < 30:
        return "Média"  #Temperatura média
    else:
        return "Alta"  #Temperatura alta


#Valida, trata e adiciona classificação aos dados
def transform_data(data):
    result = []  #Lista para armazenar resultados tratados

    #Percorre cada item dos dados, convertendo latitude e longitude, ignora se não conseguir converter
    for item in data:
        try:
            lat = float(item["latitude"])
            lon = float(item["longitude"])
        except:
            continue

        temp = item.get("temperatura")  # Obtém temperatura

        #Trata casos sem temperatura
        if temp is None:
            result.append({
                "nome": item["nome"],
                "uf": item["uf"], #Estado
                "latitude": lat,
                "longitude": lon,
                "temperatura": None,
                "classificacao": "Sem dado"
            })
            continue  #Vai para o próximo item

        try:
            #Tentativa de converter a temperatura para float, caso não funcione, é definida como None
            temp = float(temp)
        except:
            temp = None

        # Ignora coordenadas inválidas
        if lat == 0 or lon == 0:
            continue

        #Adiciona item tratado com classificação
        result.append({
            "nome": item["nome"],
            "uf": item["uf"], #estado
            "latitude": lat,
            "longitude": lon,
            "temperatura": temp,
            "classificacao": classify_temp(temp)  #Classifica temperatura
        })

    #Mostra quantidade válida de pontos no terminal
    print(f"Pontos válidos: {len(result)}")

    #Retorna dados transformados
    return result