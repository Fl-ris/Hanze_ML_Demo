from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container(dbc.Form(
    dbc.Row(
        [
            dbc.Label("Leeftijd", width="auto"),
            dbc.Col(
                dbc.Input(type="number", placeholder="Type hier je leeftijd (jaren)"),
                className="me-3",
            ),

            dbc.Label("Gewicht", width="auto"),
            dbc.Col(
                dbc.Input(type="number", placeholder="Type hier je gewicht (kg)"),
                className="me-3",
            ),
        
            dbc.Label("Lengte", width="auto"),
            dbc.Col(
                dbc.Input(type="number", placeholder="Type hier je lengte (cm)"),
                className="me-3",
            ),
            dbc.Col(dbc.Button("Voorspel leeftijd!", color="primary"), width="auto"),
        
        ],

        className="g-2",
    )
), fluid=True)



if __name__ == '__main__':
    app.run(debug=True)