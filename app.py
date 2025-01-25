import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template('slate')

# Inicializando o App Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# ====== PREPARAÇÃO DOS DADOS ====== #
# Carregar os dados do arquivo CSV
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
        dbc.Col([
            dbc.Row([
                html.Div([
                    html.H1('Sports Car Dashboard', style={'textAlign': 'center'}),
                    # Dropdown para selecionar a marca do carro
                    dcc.Dropdown(
                        id='make_dropdown',
                        options=[{'label': make, 'value': make} for make in df_sorted['Car Make'].unique()],
                        value=None,
                        placeholder="Selecione uma marca",
                    ),
                    # Dropdown para selecionar o modelo do carro
                    dcc.Dropdown(
                        id='model_dropdown',
                        placeholder="Selecione um modelo",
                    ),
                    # Checklist para selecionar anos
                    dcc.Checklist(
                        id='year_checklist',
                        options=[{'label': str(year), 'value': year} for year in sorted(df_sorted['Year'].unique())],
                        value=df_sorted['Year'].unique().tolist(),
                        labelStyle={'display': 'inline-block'},
                        style={'marginTop': '10px'},
                    ),
                ], style={'padding': '20px', 'width': '100%'})
            ])
        ], md=2, style={'padding':'0'}),
        dbc.Col([
            dbc.Row([html.Div(dcc.Graph(id='graph-horsepower'))]),
            dbc.Row([html.Div(dcc.Graph(id='graph-price-time'))])
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
    [Output('graph-horsepower', 'figure'), Output('graph-price-time', 'figure')],
    [Input('make_dropdown', 'value'),
    Input('model_dropdown', 'value'),
    Input('year_checklist', 'value')]
)
def update_graphs(selected_make, selected_model, selected_years):
    filtered_df = df_sorted
    if selected_make:
        filtered_df = filtered_df[filtered_df['Car Make'] == selected_make]
    if selected_model:
        filtered_df = filtered_df[filtered_df['Car Model'] == selected_model]
    if selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

    filtered_df['text'] = filtered_df['Car Model'] + ' (' + filtered_df['Year'].astype(str) + ')'

    # Gráfico de Potência (Horsepower) x Modelos
    fig_horsepower = px.scatter(
        filtered_df,
        x='Car Model',
        y='Horsepower',
        color='Horsepower',
        title=f'Horsepower X Car Model ({selected_make or "Todos"})',
        labels={'Horsepower': 'Potência (HP)', 'Car Model': 'Modelo do Carro', 'text': 'Modelo e Ano'},
        text='text'
    )
    fig_horsepower.update_layout(
        xaxis_title='Car Model',
        yaxis_title='Horsepower (HP)',
        template='slate'
    )
    fig_horsepower.update_traces(textposition='top center', textfont=dict(size=10))

    # Gráfico de Tempo x Preço
    sorted_df_by_price_time = filtered_df.sort_values(by=['Price (in USD)', 'Time'], ascending=[False, False])

    fig_price_time = px.scatter(
        sorted_df_by_price_time,
        x='Price (in USD)',
        y='Time',
        color='Car Model',
        title=f'Time X Price ({selected_make or "Todos"})',
        labels={'Horsepower': 'Potência (HP)', 'Car Model': 'Modelo do Carro', 'text': 'Modelo e Ano'},
        text='text'
    )
    fig_price_time.update_layout(
        xaxis_title='Preço (USD)',
        yaxis_title='Tempo (segundos)',
        template='slate'
    )
    fig_price_time.update_traces(textposition='top center', textfont=dict(size=10))

    return fig_horsepower, fig_price_time


# ====== EXECUTAR O SERVIDOR ====== #
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
