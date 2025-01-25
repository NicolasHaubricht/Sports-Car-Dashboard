import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Estilos externos
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Inicializando o App Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ====== PREPARAÇÃO DOS DADOS ====== #
# Carregar os dados do arquivo CSV
df = pd.read_csv('sport_car_price.csv')

# Preencher dados ausentes
df = df.ffill()

# Formatar colunas
df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year  # Converter ano para formato numérico
df['Car Make'] = df['Car Make'].astype(str)  # Garantir que seja string
df['Car Model'] = df['Car Model'].astype(str)  # Garantir que seja string
df['Horsepower'] = pd.to_numeric(df['Horsepower'], errors='coerce')  # Converter para number
df['Time'] = df['0-60 MPH Time (seconds)']  # Renomear coluna para simplificação
df['Price (in USD)'] = df['Price (in USD)'].str.replace(',', '', regex=False).astype(float)  # Remover vírgulas e converter para float

# Ordenar os dados por fabricante (Car Make)
df_sorted = df.sort_values(by='Car Make', ascending=True)

# ====== LAYOUT DO DASH ====== #
app.layout = html.Div(
    children=[
        html.Section(
            children=[
                html.H1('Sports Car Dashboard', style={'textAlign': 'center'}),
                # Dropdown para selecionar a marca do carro
                dcc.Dropdown(
                    id='make_dropdown',
                    options=[{'label': make, 'value': make} for make in df_sorted['Car Make'].unique()],
                    value='Audi',
                    placeholder="Selecione uma marca",
                    className="custom-dropdown"
                ),
                # Checklist para selecionar anos
                dcc.Checklist(
                    id='year_checklist',
                    options=[{'label': str(year), 'value': year} for year in sorted(df_sorted['Year'].unique())],
                    value=df_sorted['Year'].unique().tolist(),
                    labelStyle={'display': 'inline-block'},
                    style={'marginTop': '10px'},
                    className="custom-checklist"
                ),
            ],
        ),
        # Gráficos interativos
        dcc.Graph(id='graph-horsepower'),
        html.Hr(),
        dcc.Graph(id='graph-price-time')
    ]
)

# ====== CALLBACKS ====== #
@app.callback(
    [Output('graph-horsepower', 'figure'), Output('graph-price-time', 'figure')],
    [Input('make_dropdown', 'value'), Input('year_checklist', 'value')]
)
def update_graphs(selected_make, selected_years):
    # Filtrar os dados com base na marca e anos selecionados
    filtered_df = df_sorted[(df_sorted['Car Make'] == selected_make) & (df_sorted['Year'].isin(selected_years))]
    
    # Adicionar uma coluna de texto com modelo e ano para exibição nos gráficos
    filtered_df['text'] = filtered_df['Car Model'] + ' (' + filtered_df['Year'].astype(str) + ')'

    # Gráfico de Potência (Horsepower) x Modelos
    fig_horsepower = px.scatter(
        filtered_df,
        x='Car Model',
        y='Horsepower',
        color='Horsepower',
        title=f'Horsepower por Modelo ({selected_make})',
        labels={'Horsepower': 'Potência (HP)', 'Car Model': 'Modelo do Carro'},
        text='text'
    )
    fig_horsepower.update_layout(
        xaxis_title='Car Model',
        yaxis_title='Horsepower (HP)',
        template='plotly_dark'
    )
    fig_horsepower.update_traces(textposition='top center', textfont=dict(size=10))

    # Ordenar os dados por preço e tempo para o segundo gráfico
    sorted_df = filtered_df.sort_values(by=['Price (in USD)', 'Time'], ascending=[True, True])

    # Gráfico de Tempo x Preço
    fig_price_time = px.scatter(
        sorted_df,
        x='Price (in USD)',
        y='Time',
        color='Car Model',
        title=f'Tempo x Preço ({selected_make})',
        labels={'Time': 'Tempo (segundos)', 'Price (in USD)': 'Preço (USD)'},
        text='text'
    )
    fig_price_time.update_layout(
        xaxis_title='Preço (USD)',
        yaxis_title='Tempo (segundos)',
        template='plotly_dark'
    )
    fig_price_time.update_traces(textposition='top center', textfont=dict(size=10))

    # Retornar os dois gráficos
    return fig_horsepower, fig_price_time

# ====== EXECUTAR O SERVIDOR ====== #
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)