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
from main import make_dataframe, connect_database, dataframe2database



app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], serve_locally=False)

app.css.append_css({
    "external_url": "assets/button.css"
})

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Begin hier!', children=[
    dbc.Row(
        [
            # Vraag 1
            dbc.Label("Maak je gebruik van Snapchat of Tiktok?", width="auto", align="center", size="lg"),
                dbc.Input(id="age_input", type="number", placeholder="Type hier je leeftijd (jaren)",size="lg"),
                dcc.RadioItems(["Ja", "Nee"], inline=True, id="vraag1"),
            # Vraag 2
            dbc.Label("Heb je ooit een Sony Walkman / discman gekocht?", width="auto", size="lg"),
                #dbc.Input(id="weight_input", type="number", placeholder="Type hier je gewicht (kg)",size="lg"),
                dcc.RadioItems(["Ja", "Nee"], inline=True, id="vraag2"),
            # Vraag 3
            dbc.Label("Lees je regelmatig de krant?", width="auto", size="lg"),
              #  dbc.Input(id="height_input", type="number", placeholder="Type hier je lengte (cm)",size="lg"),
                dcc.RadioItems(["Ja", "Nee"], inline=True, id="vraag3"),
            # Vraag 4
            dbc.Label("Wat lijkt het meest op je eerste mobiele telefoon?", width="auto", size="lg"),
                #dbc.Input(id="height_input", type="number", placeholder="Type hier je lengte (cm)",size="lg"),
                dcc.RadioItems(["A","B","C","D","E","F","G","H","I","J","K","L"], inline=True, id="vraag4"),
               # html.Img(src="/home/floris/Documenten/git_repo/Hanze_ML_Demo/assets/telefoon.jpg"),
            # Vraag 5
            dbc.Label("Geef je de voorkeur aan bellen of emailen / Whatsapp etc.?", width="auto", size="lg"),
                #dbc.Input(id="height_input", type="number", placeholder="Type hier je lengte (cm)",size="lg"),
                dcc.RadioItems(["Ja", "Nee"], inline=True, id="vraag5"),
            # Vraag 6
            dbc.Label("Gebruik je bij het sturen van digitale berichten geregeld smileys zoals '😂'?", width="auto", size="lg"),
               # dbc.Input(id="height_input", type="number", placeholder="Type hier je lengte (cm)",size="lg"),
                dcc.RadioItems(["Ja", "Nee"], inline=True, id="vraag6"),

            dbc.Button([dbc.Spinner(size="sm", show_initially="False"), "Voorspel leeftijd!"],n_clicks=0, id="submit_button",color="primary", size="lg"),
            # Verborgen variablen om de input waarden in op te slaan:
            dcc.Store(id="var_store"),
            dcc.Store(id="var_store_for_database"),
                   
                   # Test:
                html.Div(
                    [html.Button("Bepaal je leeftijd", className="button")],  
                )
        ],

        className="g-2", justify="center",
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
    Input("vraag1","value"),
    Input("vraag2","value"),
    Input("vraag3","value"),
    Input("vraag4","value"),
    Input("vraag5","value"),
    Input("vraag6","value"),
)

def submit_button_activate(vraag1,vraag2,vraag3,vraag4,vraag5,vraag6):
    """
    Bepaal of de submit knop gebruikt kan worden, alleen wanneer alle waarden in gevuld zijn.
    """
    if None in [vraag1,vraag2,vraag3,vraag4,vraag5,vraag6]:
        return True
    else:
        return False
    # To-do: extra clausules toevoegen voor rare waarden etc. 


@app.callback(
    Output("var_store","data"),
    Input("submit_button","n_clicks"),
    State("age_input","value"),
    State("vraag1","value"),
    State("vraag2","value"),
    prevent_initial_call = True
)

def test_func(n_clicks,vraag1,vraag2,vraag3):

    db = connect_database()
    df = make_dataframe(db)

    # new_row = {"leeftijd": age_input,"gewicht": weight_input, "lengte": height_input}
    # df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # dataframe2database(df) # Sla de niewe waarden ook op in de database.

    print(df)


@app.callback(
    Output("test_graph","figure"),
    Input("submit_button","n_clicks"),
    State("vraag1","value"),
    State("vraag2","value"),
    prevent_initial_call = True
)

def test_graph(n_clicks,vraag1, vraag2):

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