# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 16:53:01 2023

@author: karen
"""
import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

columnas = ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal","num"]
datos_iniciales = pd.read_csv('https://raw.githubusercontent.com/karen0c/Proyecto_1_ACTD/main/processed.cleveland.data',header=None, names=columnas, na_values="?")

datos_iniciales = datos_iniciales.dropna().reset_index(drop=True) #elimina filas con valores faltantes
print(datos_iniciales.head())
print(datos_iniciales.tail())

#Estadística descriptiva general
datos_iniciales.describe()

# crear unos nuevos datos donde guardaremos la información con los datos discretizados
datos = datos_iniciales
for i in range(0,297):
  if datos_iniciales.loc[i, 'age'] <= 40:
    datos.loc[i, 'age'] = 1
  elif datos_iniciales.loc[i, 'age'] > 40 and datos_iniciales.loc[i, 'age'] <= 50:
    datos.loc[i, 'age'] = 2
  elif datos_iniciales.loc[i, 'age'] > 50 and datos_iniciales.loc[i, 'age'] <= 60:
    datos.loc[i, 'age'] = 3
  else:
    datos.loc[i, 'age'] = 4



for i in range(0,297):
  if datos_iniciales.loc[i, "trestbps"] <= 120:
    datos.loc[i, "trestbps"] = 1
  elif datos_iniciales.loc[i, "trestbps"] > 120 and datos_iniciales.loc[i, "trestbps"] <= 139:
    datos.loc[i, "trestbps"] = 2
  elif datos_iniciales.loc[i, "trestbps"] >= 140 and datos_iniciales.loc[i, "trestbps"] <= 159:
    datos.loc[i, "trestbps"] = 3
  elif datos_iniciales.loc[i, "trestbps"] >= 160 and datos_iniciales.loc[i, "trestbps"] <= 179:
    datos.loc[i, "trestbps"] = 4
  else:
    datos.loc[i, "trestbps"] = 5
    

for i in range(0,297):
  if datos_iniciales.loc[i, "chol"] <= 200:
    datos.loc[i, "chol"] = 1
  elif datos_iniciales.loc[i, "chol"] > 200 and datos_iniciales.loc[i, "chol"] < 240:
    datos.loc[i, "chol"] = 2
  else:
    datos.loc[i, "chol"] = 3
    

for i in range(0,297):
  if datos_iniciales.loc[i, "thalach"] <= 120:
    datos.loc[i, "thalach"] = 1
  elif datos_iniciales.loc[i, "thalach"] > 120 and datos_iniciales.loc[i, "thalach"] <= 140:
    datos.loc[i, "thalach"] = 2
  elif datos_iniciales.loc[i, "thalach"] > 140 and datos_iniciales.loc[i, "thalach"] < 160:
    datos.loc[i, "thalach"] = 3
  else:
    datos.loc[i, "thalach"] = 4
    
for i in range(0,297):
  if datos_iniciales.loc[i, "oldpeak"] <= 1:
    datos.loc[i, "oldpeak"] = 1
  elif datos_iniciales.loc[i, "oldpeak"] > 1 and datos_iniciales.loc[i, "oldpeak"] <= 2:
    datos.loc[i, "oldpeak"] = 2
  else:
    datos.loc[i, "oldpeak"] = 3
    

#Valores distintos de cada variable
datos.nunique()

#pip install pgmpy 

#pip install numpy



from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

modelo = BayesianNetwork([("sex", "num"), ("age", "chol"), ("age", "fbs"),("age", "trestbps"),("thal", "trestbps"), ("chol", "num"),("fbs", "trestbps"), ("trestbps", "num"),("num", "ca"),("num", "thalach"),("num", "exang"),("num", "oldpeak"),("num", "slope"),("exang", "cp"),("cp", "oldpeak"),("oldpeak", "restecg"),("slope","restecg")])

from pgmpy.estimators import MaximumLikelihoodEstimator 
emv = MaximumLikelihoodEstimator(model=modelo, data=datos)

modelo.fit(data=datos, estimator = MaximumLikelihoodEstimator) 

for i in modelo.nodes(): 
  print(modelo.get_cpds(i)) 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
    html.H6("Modifique el valor en la caja de texto para ver el funcionamiento de los callbacks"),
    html.Div(["Edad: ",
              dcc.Input(id='input_age', value='valor inicial', type='number')]),
    
    html.Div(["Sexo: ",
              dcc.Input(id='my-input', value='valor inicial', type='number')]),
    html.H6('Sexo:'),
    dcc.Dropdown(
        id='input_sex',
        options=[
            {'label': 'Mujer', 'value': '0'},
            {'label': 'Hombre', 'value': '1'}
        ],
        value='Selecciona tu sexo'
    ),
    
    html.Br(),
    html.Div(id='my-output'),
    ]
)


@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id={'age':'input_age','sex':'input_sex'}, component_property='value')]
   
    
)
def update_output_div(input_value):
    return 'Aqui te indico lo que estas ingresanso (Output): {}'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
'''
@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
    return 'Aqui te indico lo que estas ingresanso (Output): {}'.format(input_value)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])



@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.choropleth(filtered_df, locations="country", color="lifeExp",
                      
                     hover_name="country", range_color=[20,80],
                  
                     labels={
                     "pop": "Population",
                     "gdpPercap": "GDP per cápita",
                     "lifeExp": "Life Expectancy",
                     "continent": "Continent"
                     },
                     title="Life expectancy ")

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
'''