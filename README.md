-----------DESCRIÇÃO DA SOLUÇÃO DO DESAFIO----------------

A solução implementa um pipeline de ETL geoespacial em Python baseado em dados reais do INMET, utilizando estações meteorológicas automáticas operantes no Brasil.

Os sites que foram consultados para o desenvolvimento da solução foram:

https://portal.inmet.gov.br/paginas/catalogoaut
https://mapas.inmet.gov.br/
https://portal.inmet.gov.br/

O processo foi desenvolvido a partir da análise do funcionamento do portal oficial do INMET, que fornece a temperatura de uma localidade com base na estação automática mais próxima. Durante essa análise, foi identificado que o portal consome uma API interna baseada no código IBGE da cidade, no formato:

https://apiprevmet3.inmet.gov.br/estacao/proxima/{CODIGO_IBGE}

E dentro dessa API, existe um atributo chamado "TEM_INS", no caso, a temperatura instantânea da estação, logo, será necessário buscar a temperatura instantânea de cada uma das estações automáticas do Brasil e fornecê-las em um mapa.

A partir disso, a solução foi construída com as seguintes etapas:

estacoes.json

No princípio, foi criado um JSON contendo o código de todas as estações automáticas do Brasil. Após isso, verificou-se quais cidades do Brasil utilizam as estações mais próximas para gerar uma resposta no site https://portal.inmet.gov.br/. Assim, foi-se associando cada estação com um código IBGE, onde obteve-se 450 pontos válidos.

extract.py

Foi criado um conjunto de dados contendo os códigos IBGE de cidades associadas a estações automáticas operantes no Brasil. Para cada código IBGE, a aplicação realiza requisições à API do INMET, obtendo a temperatura instantânea (TEM_INS) da estação mais próxima. (OBS: A aplicação considera exclusivamente estações meteorológicas automáticas operantes, garantindo consistência e confiabilidade nos dados coletados).

transform.py

Os dados extraídos passam por um processo de transformação onde a temperatura instantânea é classificada em três categorias: Baixa, Média e Alta. A classificação é feita dinamicamente com base em intervalos definidos, permitindo fácil ajuste e adaptação conforme o contexto climático. (OBS: Quando a estação automática está com problemas, ela não fornece uma temperatura instantânea, nem no site do INMET, nem na API, logo essas estações não ganham uma classificação, ficando sem cor, até que a estação volte a fornecer temperaturas).

load.py

Os dados transformados são armazenados em um novo arquivo (output.json), estruturado para consumo direto pela camada de visualização.

Visualização e Justificativa do intervalo das temperaturas (WebGIS)

A visualização é feita utilizando Leaflet, onde:
- Os dados são carregados via script.js
- Cada estação é representada no mapa como um círculo, usando uma simbologia baseada na classificação:
- Temperatura Baixa, abaixo de 20 graus Celsius, gera uma cor verde;
- Temperatura Média, abaixo de 30 graus Celsius, mas acima de 20 graus Celsius, gera uma cor amarela;
- Temperatura Alta, acima ou igual a 30 graus Celsius, gera uma cor vermelha;
- Caso não haja dados na API do INMET para aquela estação específica, gera uma cor cinza, indicando que não há temperatura registrada lá.

A definição desses intervalos considerou os seguintes aspectos:

- Contexto climático do Brasil: O Brasil possui predominância de clima tropical, onde temperaturas entre 20°C e 30°C são comuns na maior parte do ano. Dessa forma, essa faixa foi definida como Média, representando condições típicas.

- Percepção térmica: Abaixo de 20°C tende a representar sensação de frio ou clima ameno, classificado como Baixa

- Acima de 30°C caracteriza calor intenso, classificado como Alta

- Clareza na visualização geoespacial: A divisão em três faixas bem definidas permite melhor contraste visual no mapa, facilitando a identificação de padrões espaciais.

- Simplicidade e adaptabilidade: Os intervalos foram definidos de forma simples para facilitar entendimento e manutenção, podendo ser ajustados conforme necessidade ou contexto regional.

O projeto também inclui scripts para execução automatizada:

- run_etl.py que executa o pipeline ETL;
- run_api.py que inicia a API (quando aplicável);
- run_pipeline.bat que executa todo o fluxo automaticamente.

Essa abordagem permite rodar toda a aplicação com um único comando, facilitando testes e uso.

A arquitetura foi organizada de forma modular, separando claramente as etapas de extração, transformação e carga, além da camada de visualização e API, facilitando manutenção, escalabilidade e reutilização dos componentes.

O projeto também inclui um bloco de texto com os pacotes python necessários para executar o programa, assim como um arquivo de configuração que define as variáveis que vão ser importantes para a execução do programa (config.json).

-----------EXECUÇÃO DO PROGRAMA----------------

Para executar o programa, será necessário primeiro ter o interpretador Python na máquina. 

(CASO NÃO TENHA O INTEPRETADOR PYTHON EM SUA MÁQUINA, você pode instalar aqui https://www.python.org/downloads)

Após o interpretador Python estiver na sua máquina, entre no diretório da pasta do programa usando o terminal, no caso ./desafio-etl-main/

Agora digite "pip install -r requirements.txt" para instalar os requisitos básicos do programa, no caso, será a biblioteca json, uvicorn e requests.

Agora clique no programa "pipeline.bat" e espere o programa carregar.

Após surgir o terceiro e último terminal, volte ao terminal que estavam sendo carregadas as temperaturas e copie o endereço mostrado no terminal (http://127.0.0.1:5500/ por exemplo) e cole no navegador para acessar o programa.

Após surgir o mapa no navegador, o projeto está rodando na sua máquina.

Por fim, para utilizar o programa, basta selecionar no mapa algum dos pontos para verificar a temperatura da estação. Caso deseje selecionar apenas os estados de uma determinada região, ou de um único estado, ou filtrar por categoria de temperatura, ou buscar uma estação a partir do nome dela, basta utilizar o filtro que está localizado no canto superior direito da tela.

-----------TECNOLOGIAS UTILIZADAS----------------

Python: A linguagem principal utilizada no desenvolvimento da aplicação, responsável por toda a lógica do ETL, permitindo uma organização modular em diferentes arquivos (extract.py, transform.py, load.py), assim como os scripts de execução (run_etl.py e run_api.py).

Requests: Biblioteca utilizada para realizar requisições HTTP à API do INMET. Teve consumo da API de estações meteorológicas baseada em código IBGE, uso de requests.Session() para reaproveitamento de conexões, implementação de timeout para evitar travamentos e tratamento de respostas e validação de status HTTP.

Concurrent Futures (ThreadPoolExecutor): Utilizado para execução paralela durante a etapa de extração, execução simultânea de múltiplas requisições à API, redução significativa do tempo total de coleta de dados e uso de ThreadPoolExecutor e as_completed para controle das threads.

JSON e GeoJSON: Formatos utilizados para entrada, processamento e saída dos dados:

JSON: Utilizado para o armazenamento das estações meteorológicas (estacoes.json), arquivo de configuração (config.json) e para a manipulação intermediária dos dados.

GeoJSON: Utilizado para o formato final de dados gerado (output.json), estrutura compatível com aplicações geoespaciais e permite integração direta com o Leaflet.

FastAPI: Framework utilizado para criação da API REST, disponibilização dos dados processados através do endpoint / dados, retorno dos dados no formato GeoJSON, integração direta com o frontend via fetch e separação entre camada de dados (backend) e visualização.

Uvicorn: Servidor ASGI utilizado para execução da aplicação FastAPI, Responsável por subir o servidor backend local, suporte a recarregamento automático (reload=True) e configuração dinâmica de host e porta via config.json.

API do IMNET: Utilizada como fonte principal de dados meteorológicos, endpoint utilizado para a obtenção da temperatura da estação mais próxima (https://apiprevmet3.inmet.gov.br/estacao/proxima/{CODIGO_IBGE}), retorna dados em formato JSON contendo informações meteorológicas, a seleção das estações é baseada em códigos IBGE previamente mapeados.

Leaflet.js: Biblioteca JavaScript utilizada para visualização geoespacial interativa, renderização do mapa utilizando OpenStreetMap, leitura direta de dados no formato GeoJSON, plotagem de pontos geográficos (estações) no mapa, aplicação de simbologia baseada na classificação de temperatura (Verde: Baixa, Amarelo: Média, Vermelho: Alta, Cinza: Sem dados) e exibição de popups com informações detalhadas.

HTML, CSS e JavaScript: Responsáveis pela construção da interface WebGIS:

HTML: Estrutura da aplicação e interface de filtros (região, estado, temperatura e nome da estação).

CSS: Estilização da interface e organização visual.

JavaScript: Consumo da API via fetch e renderização dinâmica do mapa, aplicação de filtros interativos (Região, Estado (UF), Classificação de temperatura, Nome da estação, Atualização em tempo real da visualização).

Scripts de Automação: Responsáveis por facilitar a execução do projeto:

run_etl.py: Orquestra as etapas de extração, transformação e carga.

run_api.py: Inicializa a API FastAPI utilizando Uvicorn.

pipeline.bat: Automatiza toda a execução do sistema (executa o ETL, inicia a API, inicia o servidor web, permite rodar toda a aplicação com um único comando).

Arquivo de Configuração (config.json): Utilizado para parametrizar a aplicação sem necessidade de alterar o código (URL da API do INMET, número de threads (max_workers), host e porta da API).

--------------------DECISÕES TÉCNICAS--------------------

Limitação da API do INMET e otimização da coleta: Durante o desenvolvimento, foi identificado que a API pública do INMET apresenta limitações para obtenção eficiente de todas as estações meteorológicas operantes. Inicialmente, a abordagem consistia em consultar o endpoint de estações (https://apitempo.inmet.gov.br/estacoes/T) para obter os IDs disponíveis, iterar sobre possíveis identificadores e realizar requisições adicionais para obter os dados de temperatura. Essa estratégia resultava em um alto número de requisições desnecessárias, tempo de execução elevado (superior a 30 minutos) e baixa eficiência no processo de extração.

Solução adotada: Para contornar essa limitação, foi criada uma base local (estacoes.json) contendo apenas estações meteorológicas automáticas operantes, com dados estruturados como código IBGE, nome, estado e coordenadas geográficas. A partir dessa base, a aplicação passou a utilizar diretamente o endpoint https://apiprevmet3.inmet.gov.br/estacao/proxima/{CODIGO_IBGE}, buscando apenas a informação necessária (TEM_INS), eliminando requisições redundantes.

Ganho de performance: Com essa abordagem, o tempo de execução foi reduzido de mais de 35 minutos para aproximadamente 39 segundos, além de diminuir significativamente o volume de requisições e tornar o processo mais eficiente e previsível.

Justificativa da abordagem: A criação de uma base local permitiu maior controle sobre os dados de entrada, redução da dependência de endpoints limitados e melhoria no desempenho geral da aplicação, tornando o pipeline mais estável e escalável.
