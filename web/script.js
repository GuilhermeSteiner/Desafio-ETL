//Inicializa o mapa centrado no Brasil
var map = L.map('map').setView([-15, -55], 4);

//Adiciona camada base do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let dadosGlobais = []; //Armazena os dados completos da API
let camadaAtual = null; //Armazena a camada atual desenhada no mapa

//Retorna a região correspondente ao atributo "uf" (estado)
function obterRegiao(uf) {

    if (["AC","AP","AM","PA","RO","RR","TO"].includes(uf)) return "Norte";

    if (["MA","PI","CE","RN","PB","PE","AL","SE","BA"].includes(uf)) return "Nordeste";

    if (["MT","MS","GO","DF"].includes(uf)) return "Centro-Oeste";

    if (["SP","RJ","MG","ES"].includes(uf)) return "Sudeste";

    if (["PR","SC","RS"].includes(uf)) return "Sul";

    return null;
}

//Inicializa o carregamento de dados
async function init() {
    await carregarDadosMapa(); //Aguarda o carregamento dos dados antes de continuar
}

//Busca os dados da API e desenha o mapa no navegador
async function carregarDadosMapa() {
    let res = await fetch("http://127.0.0.1:8000/dados"); //Faz uma requisição HTTP para o backend, o FastAPI
    let data = await res.json(); //Converte pra GeoJSON

    dadosGlobais = data; //Armazena os dados globalmente

    desenharMapa(data); //Desenha o mapa com os dados recebidos
}

//Desenha o mapa usando o GeoJSON e renderiza os pontos no mapa
function desenharMapa(data) {

    //Se já existe uma camada desenhada anteriormente, remove a camada antiga antes de desenhar a nova
    if (camadaAtual) {map.removeLayer(camadaAtual);}

    //Cria uma nova camada GeoJSON
    camadaAtual = L.geoJSON(data, {

        //Define como cada ponto será representado visualmente
        pointToLayer: function (feature, latlng) {

            let classe = feature.properties.classificacao; //Obtém a classificação de temperatura
            let color = "gray"; //Os pontos começam cinzas

            //Define a cor de cada ponto, verde para baixa, amarelo para média e vermelho para alta. Caso não tenha sido encontrada nenhuma temperatura, o ponto continua cinza
            if (classe === "Baixa") color = "green";
            else if (classe === "Média") color = "yellow";
            else if (classe === "Alta") color = "red";

            //Retorna um círculo colorido apontando na localização da estação
            return L.circleMarker(latlng, {
                radius: 8,
                color: "#333",
                weight: 1,
                fillColor: color,
                fillOpacity: 0.8
            });
        },
        //Define comportamento de cada ponto após ser criado
        onEachFeature: function (feature, layer) {
            let temp = feature.properties.temperatura; //Obtém temperatura
            temp = temp === "Sem dado" ? "Sem dado" : temp + "°C"; //Formata a temperatura, adicionando "°C" ou mantendo "Sem dado"

            //Define o conteúdo do popup exibido após clicar em um ponto
            layer.bindPopup(`
                <b>${feature.properties.nome}</b><br>
                Temp: ${temp}<br>
                Classe: ${feature.properties.classificacao}<br>
                UF: ${feature.properties.uf}
            `);
        }
        //Adiciona a camada ao mapa
    }).addTo(map);
}

//Aplica filtros selecionados pelo usuário e atualiza o mapa
function aplicarFiltros() {

    let estado = document.getElementById("estadoFilter").value; //Valor de estado
    let regiao = document.getElementById("regiaoFilter").value; //Valor de região
    let temp = document.getElementById("tempFilter").value; //Valor de classificação de temperatura
    let nome = document.getElementById("nomeFilter").value.toLowerCase(); //Valor de nome da estação

    //Cria um novo objeto GeoJSON filtrado
    let filtrado = {
        type: "FeatureCollection",

        //Filtra os pontos com base nos critérios
        features: dadosGlobais.features.filter(f => {

            let p = f.properties;

            //Determina a região da UF do ponto
            let regiaoUF = obterRegiao(p.uf);

            //Retorna apenas os pontos que atendem todos os filtros
            return (
                (!estado || p.uf === estado) &&
                (!regiao || regiaoUF === regiao) &&
                (!temp || p.classificacao === temp) &&
                (!nome || p.nome.toLowerCase().includes(nome))
            );
        })
    };
    //Desenha o mapa após a seleção de filtros
    desenharMapa(filtrado);
}

//Devolve o mapa ao estado inicial, retirando todos os filtros
function resetarMapa() {

    document.getElementById("estadoFilter").value = "";
    document.getElementById("regiaoFilter").value = "";
    document.getElementById("tempFilter").value = "";
    document.getElementById("nomeFilter").value = "";

    //Desenha o mapa após a retirada dos filtros
    desenharMapa(dadosGlobais);
}

//Execução após o HTML terminar de carregar
document.addEventListener("DOMContentLoaded", () => {

    //Inicializa a aplicação
    init();

    //Adiciona eventos para atualizar o mapa quando os filtros mudam
    document.getElementById("estadoFilter").addEventListener("change", aplicarFiltros);
    document.getElementById("regiaoFilter").addEventListener("change", aplicarFiltros);
    document.getElementById("tempFilter").addEventListener("change", aplicarFiltros);
    document.getElementById("nomeFilter").addEventListener("input", aplicarFiltros);
});