from etl.extract import extract_data #Importa a função que extrai os dados da API/Arquivos
from etl.transform import transform_data #Importa a função que limpa e trata os dados
from etl.load import save_data #Importa a função que salva os dados processados

#Função principal que executa todo o pipeline ETL
def run():
    print("Extraindo dados...") #Log de início de extração
    data = extract_data() #Executa a função para extrair os dados

    print("Transformando dados...") #Log de início da transformação
    data = transform_data(data) #Executa a função para transformar os dados

    print("Salvando dados...") #Log de início do salvamento de dados
    save_data(data) #Executa a função para salvar os dados

    print("ETL finalizado com sucesso!") #Log informando o sucesso das 3 etapas

#Executa o ETL apenas se o arquivo for rodado diretamente
if __name__ == "__main__":

    #Executa a funçao principal
    run()