import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template('lux')

# Inicializando o App Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# ====== PREPARAÇÃO DOS DADOS ====== #
df = pd.read_csv('sport_car_price.csv')
df = df.ffill()
df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year
df['Car Make'] = df['Car Make'].astype(str)
df['Car Model'] = df['Car Model'].astype(str)
df['Horsepower'] = pd.to_numeric(df['Horsepower'], errors='coerce')
df['Price (in USD)'] = df['Price (in USD)'].str.replace(',', '', regex=False).astype(float)
df['Time'] = df['0-60 MPH Time (seconds)']
df['Time'] = df['Time'].str.replace(',', '', regex=False).str.strip()
df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
df['Time'] = df['Time'].fillna(0)
df_sorted = df.sort_values(by='Car Make', ascending=True)

# ====== LAYOUT DO DASH ====== #
app.layout = html.Div([
    dbc.Row([
        # Coluna para a sidebar
        dbc.Col([
            html.Div([
                html.H1('Sports Car', style={'textAlign': 'center'}),
                html.Hr(),
                # Dropdown para selecionar a marca do carro
                dcc.Dropdown(
                    id='make_dropdown',
                    options=[{'label': make, 'value': make} for make in df_sorted['Car Make'].unique()],
                    value=None,
                    placeholder="Selecione uma marca",
                    style={'margin-top': '40px', 'widht':'85%'},
                ),
                # Dropdown para selecionar o modelo do carro
                dcc.Dropdown(
                    id='model_dropdown',
                    placeholder="Selecione um modelo",
                    style={'margin-top': '20px', 'widht':'85%'},
                ),
                # Checklist para selecionar anos
                dcc.Checklist(
                    id='year_checklist',
                    options=[{'label': str(year), 'value': year} for year in sorted(df_sorted['Year'].unique())],
                    value=df_sorted['Year'].unique().tolist(),
                    labelStyle={'display': 'inline-block'},
                    style={'margin-top': '20px', 'display':'flex', 'flex-direction':'column', 'font-size':'1.5rem'},
                ),
            ], style={'padding': '20px', 'width': '100%'}),
        ], md=2, style={'padding':'0'}),
        # Coluna para os gráficos
        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id='graph-car-makes')], md=6),
                dbc.Col([dcc.Graph(id='graph-models')], md=6)
            ]),
            dbc.Row([html.Div(dcc.Graph(id='graph-horsepower'), style={'width':'100%'})]),
            dbc.Row([html.Div(dcc.Graph(id='graph-price-time'), style={'width':'100%'})]),
            dbc.Row([html.Div(dcc.Graph(id='graph-price-year'), style={'width':'100%'})])
        ], md=10, style={'padding':'0'}),
    ])
])

# ====== CALLBACK PARA FILTRAR MODELOS ====== #
@app.callback(
    Output('model_dropdown', 'options'),
    Input('make_dropdown', 'value')
)
def update_model_dropdown(selected_make):
    if selected_make:
        filtered_df = df_sorted[df_sorted['Car Make'] == selected_make]
    else:
        filtered_df = df_sorted
    return [{'label': model, 'value': model} for model in filtered_df['Car Model'].unique()]

# ====== CALLBACK PARA FILTRAR ANOS ====== #
@app.callback(
    Output('year_checklist', 'options'),
    [Input('make_dropdown', 'value'), Input('model_dropdown', 'value')]
)
def update_year_checklist(selected_make, selected_model):
    filtered_df = df_sorted
    if selected_make:
        filtered_df = filtered_df[filtered_df['Car Make'] == selected_make]
    if selected_model:
        filtered_df = filtered_df[filtered_df['Car Model'] == selected_model]
    return [{'label': str(year), 'value': year} for year in sorted(filtered_df['Year'].unique())]

# ====== CALLBACK PARA ATUALIZAR GRÁFICOS ====== #
@app.callback(
    [   
        Output('graph-car-makes', 'figure'),
        Output('graph-models', 'figure'),
        Output('graph-horsepower', 'figure'), 
        Output('graph-price-time', 'figure'), 
        Output('graph-price-year', 'figure')
    ],
    [
        Input('make_dropdown', 'value'),
        Input('model_dropdown', 'value'),
        Input('year_checklist', 'value')
    ]
)
def update_graphs(selected_make, selected_model, selected_years,):
    filtered_df = df_sorted
    if selected_make:
        filtered_df = filtered_df[filtered_df['Car Make'] == selected_make]
    if selected_model:
        filtered_df = filtered_df[filtered_df['Car Model'] == selected_model]
    if selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

    filtered_df['text'] = filtered_df['Car Model'] + ' (' + filtered_df['Year'].astype(str) + ')'

    # Gráfico de barras para total de veículos por marca
    car_make_counts = filtered_df['Car Make'].value_counts().reset_index()
    car_make_counts.columns = ['Car Make', 'Total Vehicles']
    fig_car_makes = px.bar(car_make_counts, x='Car Make', y='Total Vehicles', color='Car Make', title='Total de Veículos por Marca', template='lux')
    fig_car_makes.update_layout(xaxis_title='Marca', yaxis_title='Total de Veículos', showlegend=False)

    # Gráfico de barras para total de veículos por modelo
    car_model_counts = filtered_df['Car Model'].value_counts().reset_index()
    car_model_counts.columns = ['Car Model', 'Total Vehicles']
    fig_car_models = px.bar(car_model_counts, x='Car Model', y='Total Vehicles', color='Car Model', title='Total de Veículos por Modelo', template='lux')
    fig_car_models.update_layout(xaxis_title='Modelo', yaxis_title='Total de Veículos', showlegend=False)

    # Gráfico de Potência (Horsepower) x Modelos
    fig_horsepower = px.scatter(filtered_df, x='Car Model', y='Horsepower', color='Horsepower', title=f'Distribuição de Potência (HP) entre Modelos de Veículos ({selected_make or "Todos"})', labels={'Price (in USD)': 'Preço (USD)', 'Time': '0 a 100Km/h (Segundos)', 'Horsepower': 'Potência (HP)', 'Car Model': 'Modelo do Carro', 'text': 'Modelo e Ano'}, text='text')
    fig_horsepower.update_layout(xaxis_title='Modelo do Carro', yaxis_title='Potência (HP)', template='lux')
    fig_horsepower.update_traces(textposition='top center', textfont=dict(size=10))

    # Gráfico de 0 a 100 (Segundos) x Preço
    sorted_df_by_price_time = filtered_df.sort_values(by=['Price (in USD)', 'Time'], ascending=[False, False])
    fig_price_time = px.scatter(sorted_df_by_price_time, x='Price (in USD)', y='Time', color='Time', title=f'Análise de Preço em Relação ao Tempo de Aceleração (0-100 km/h) ({selected_make or "Todos"})', labels={'Price (in USD)': 'Preço (USD)', 'Time': '0 a 100Km/h (s)', 'Horsepower': 'Potência (HP)', 'Car Model': 'Modelo do Carro', 'text': 'Modelo e Ano'}, text='text')
    fig_price_time.update_layout(xaxis_title='Preço (USD)', yaxis_title='0 a 100Km/h (Segundos)', template='lux')
    fig_price_time.update_traces(textposition='top center', textfont=dict(size=10))

    # Gráfico de Preço x Ano
    fig_price_year = px.scatter(sorted_df_by_price_time, x='Year', y='Price (in USD)', color='Price (in USD)', title=f'Evolução do Preço Médio por Ano ({selected_make or "Todos"})', labels={'Price (in USD)': 'Preço (USD)', 'Year' : 'Ano', 'Car Model': 'Modelo do Carro', 'text': 'Modelo e Ano'}, text='text')
    fig_price_year.update_layout(xaxis_title='Ano', yaxis_title='Preço (USD)', template='lux')
    fig_price_year.update_traces(textposition='top center', textfont=dict(size=10))

    return fig_car_makes, fig_car_models, fig_horsepower, fig_price_time, fig_price_year


# ====== EXECUTAR O SERVIDOR ====== #
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)