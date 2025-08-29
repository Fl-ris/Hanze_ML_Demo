"""
Dash dashboard
Datum: 29-08-2025
Autheur: Floris Menninga
Versie: 0.1
"""


from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


from ML import data_check, visualize_df # Imports van het machine learning script.
from main import make_dataframe, connect_database



app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], serve_locally=False)

app.css.append_css({
    "external_url": "assets/button.css"
})

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Begin hier!', children=[
    dbc.Row(
        [
            dbc.Label("Leeftijd", width="auto"),
            dbc.Col(
                dbc.Input(id="age_input", type="number", placeholder="Type hier je leeftijd (jaren)",size="lg"),
                className="me-3",
            ),

            dbc.Label("Gewicht", width="auto"),
            dbc.Col(
                dbc.Input(id="weight_input", type="number", placeholder="Type hier je gewicht (kg)",size="lg"),
                className="me-3",
            ),
        
            dbc.Label("Lengte", width="auto"),
            dbc.Col(
                dbc.Input(id="height_input", type="number", placeholder="Type hier je lengte (cm)",size="lg"),
                className="me-3",
            ),
            
            dbc.Button([dbc.Spinner(size="sm", show_initially="False"), "Voorspel leeftijd!"],n_clicks=0, id="submit_button",color="primary", size="lg"),

            # Verborgen variablen om de input waarden in op te slaan:
            dcc.Store(id="var_store"),
            dcc.Store(id="var_store_for_database"),
        ],

        className="g-2",
    )
        ]),

        # Tabblad om een grafiek met voorgaande voorspellingen te zien.
        dcc.Tab(label='Voorgaande voorspellingen', children=[
        dcc.Graph(id="test_graph"),
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

        
        # Tab met informatie over het ML model dat gebruikt wordt om de voorspellingen te maken.
        dcc.Tab(label='Hoe werkt dit?', children=[
        dcc.Markdown("""
                    ## Placeholder ##
                     **informatie hier...**

                    """)
                     
        ]),
    ])
])


@app.callback(
    Output("submit_button", "disabled"),
    Input("age_input","value"),
    Input("weight_input", "value"),
    Input("height_input","value"),
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


@app.callback(
    Output("var_store","data"),
    Input("submit_button","n_clicks"),
    State("age_input","value"),
    State("weight_input","value"),
    State("height_input","value"),
    prevent_initial_call = True
)

def test_func(n_clicks,age_input,weight_input,height_input):

    db = connect_database()
    df = make_dataframe(db)

    new_row = {"leeftijd": age_input,"gewicht": weight_input, "lengte": height_input}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

   # df = df.loc[len(df)] = [age_input,weight_input,height_input]

    print(df)


@app.callback(
    Output("test_graph","figure"),
    Input("submit_button","n_clicks"),
    State("age_input","value"),
    State("weight_input","value"),
    prevent_initial_call = True
)

def test_graph(n_clicks,age_input, weight_input):

    test_df = pd.DataFrame({"age_input": [1,2,3],"weight_input": [3,4,5]}) # Test...

    fig = px.scatter(test_df, x="age_input", y="weight_input")
    return fig



@app.callback(
    Output("var_store_for_database","data"),
    Input("submit_button","n_clicks"),
    prevent_initial_call = True
)

def save_to_database(n_clicks):
    db = connect_database()
    df = make_dataframe(db)
    print(df)




if __name__ == "__main__":
    app.run(debug=True)