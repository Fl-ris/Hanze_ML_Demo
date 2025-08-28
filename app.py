from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], serve_locally=False)

app.css.append_css({
    "external_url": "assets/button.css"
})

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Voorspel je leeftijd', children=[
    dbc.Row(
        [
            dbc.Label("Leeftijd", width="auto"),
            dbc.Col(
                dbc.Input(id="age_input", type="number", placeholder="Type hier je leeftijd (jaren)"),
                className="me-3",
            ),

            dbc.Label("Gewicht", width="auto"),
            dbc.Col(
                dbc.Input(id="weight_input",type="number", placeholder="Type hier je gewicht (kg)"),
                className="me-3",
            ),
        
            dbc.Label("Lengte", width="auto"),
            dbc.Col(
                dbc.Input(id="length_input",type="number", placeholder="Type hier je lengte (cm)"),
                className="me-3",
            ),
            
            dbc.Button("Voorspel leeftijd!",id="submit_button", color="primary", size="lg"),
        
        ],

        className="g-2",
    )
        ]),
        dcc.Tab(label='Tab two', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': 'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Tab three', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': 'Montréal'},
                    ]
                }
            )
        ]),
    ])
])



@app.callback(
    Output("submit_button", "disabled"),
    Input("age_input","value"),
    Input("weight_input", "value"),
    Input("length_input","value"),
)

def submit_button_activate(leeftijd,gewicht,lengte):
    """
    Bepaal of de submit knop gebruikt kan worden, alleen wanneer alle waarden in gevuld zijn.
    """
    if leeftijd is None or gewicht is None or lengte is None:
        return True
    else:
        return False
    # To-do: extra clausules toevoegen voor rare waarden etc. 





if __name__ == '__main__':
    app.run(debug=True)