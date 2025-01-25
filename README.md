# Sports Car | Dashboard

Este projeto é um dashboard interativo desenvolvido com o framework Dash, destinado à análise de dados sobre carros esportivos. Ele permite visualizar informações como potência, preço, aceleração e distribuição de veículos por marca e modelo.

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

### 📋 Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:
<li><a href='https://www.python.org/'>Python:</a> versão 3.8 ou superior.</li>

### 🛠️ Bibliotecas Utilizadas
<li><a href="https://dash.plotly.com/" target="_blank">dash</a> - Biblioteca para criação de interfaces web interativas</li> 
<li><a href="https://dash-bootstrap-components.opensource.faculty.ai/" target="_blank">dash-bootstrap-components</a> - Componentes de interface baseados em Bootstrap para Dash</li> 
<li><a href="https://github.com/AnnMarieW/dash-bootstrap-templates" target="_blank">dash-bootstrap-templates</a> - Biblioteca para templates visuais em Dash com integração ao Bootstrap.</li>
<li><a href="https://pandas.pydata.org/" target="_blank">pandas</a> - Biblioteca para manipulação e análise de dados.</li>
<li><a href="https://plotly.com/" target="_blank">plotly</a> - Biblioteca para geração de gráficos interativos e visualizações de dados.</li>

### 🔧 Instalação

Siga estas etapas para configurar o ambiente:

1. Clone o repositório:

```
git clone https://github.com/NicolasHaubricht/Sports-Car-Dashboard.git
```
2. Acesse o diretório do projeto:
```
cd Sports-Car-Dashboard
```
3. Instale as bibliotecas:
```
pip install dash dash-bootstrap-components dash-bootstrap-templates pandas plotly
```
4. Execute o script:
```
python app.py
```
5. Abra o navegador e acesse http://127.0.0.1:8050 para visualizar o projeto

### 📈 Funcionalidades

#### Filtros
  <li>Marca do Carro: Dropdown que permite selecionar a marca desejada.</li>
  <li>Modelo do Carro: Dropdown atualizado dinamicamente com os modelos disponíveis para a marca selecionada.</li>
  <li>Ano: Checklist para selecionar um ou mais anos.</li>
  
#### Gráficos
  <li>Total de Veículos por Marca: Gráfico de barras.</li>
  <li>Total de Veículos por Modelo: Gráfico de barras.</li>
  <li>Potência por Modelo: Gráfico de dispersão.</li>
  <li>Preço vs. Tempo de Aceleração (0-100 km/h): Gráfico de dispersão.</li>
  <li>Preço Médio por Ano: Gráfico de dispersão.</li>

### 💻 Exemplos Visuais
#### Gráfico de todos os veículos dos anos 1965, 2014, 2015, 2017, 2019, 2020, 2023
![image](https://github.com/user-attachments/assets/5f351b08-70a6-4e7d-986d-6fc1244fa909)

#### Gráfico de todos os modelos da marca Lamborghini dos anos 2020, 2021, 2022
![image](https://github.com/user-attachments/assets/0c44bd16-c305-492f-9a81-838e412688ad)



## ✒️ Autores

<li>Desenvolvimento e documentação - <a href='https://github.com/NicolasHaubricht/'>Nicolas Haubricht</a></li> 

##
Feito com dedicação por <a href='https://github.com/NicolasHaubricht/'>Nicolas Haubricht</a>
