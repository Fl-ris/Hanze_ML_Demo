"""
Dash dashboard
Datum: 29-08-2025
Auteur: Floris Menninga
Versie: 0.1
"""


from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np


from ML import data_check, visualize_df, load_model, predict# Imports van het machine learning script.
from main import make_dataframe, connect_database, commit2database


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], serve_locally=False)



app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Begin hier!', children=[
    dbc.Row(
        [
            # Vraag 1
            dbc.Label("Maak je gebruik van Snapchat of Tiktok?", width="auto", align="center", size="lg"),
                #dbc.Input(id="age_input", type="number", placeholder="Type hier je leeftijd (jaren)",size="lg"),
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
            # dbc.Label("Wat lijkt het meest op je eerste mobiele telefoon?", width="auto", size="lg"),
            #     #dbc.Input(id="height_input", type="number", placeholder="Type hier je lengte (cm)",size="lg"),
            #     dcc.RadioItems(["A","B","C","D","E","F","G","H","I","J","K","L"], inline=True, id="vraag4"),
            #    # html.Img(src="assets/telefoon.jpg"),
            # Vraag 5
            dbc.Label("Geef je de voorkeur aan bellen of emailen / Whatsapp etc.?", width="auto", size="lg"),
                #dbc.Input(id="height_input", type="number", placeholder="Type hier je lengte (cm)",size="lg"),
                dcc.RadioItems(["Bellen", "Whatsapp etc."], inline=True, id="vraag5"),
            # Vraag 6
            dbc.Label("Gebruik je bij het sturen van digitale berichten geregeld smileys zoals '😂'?", width="auto", size="lg"),
               # dbc.Input(id="height_input", type="number", placeholder="Type hier je lengte (cm)",size="lg"),
                dcc.RadioItems(["Ja", "Nee"], inline=True, id="vraag6"),

           # dbc.Button([dbc.Spinner(size="sm", show_initially="False"), "Voorspel leeftijd!"],n_clicks=0, id="submit_button",color="primary", size="lg"),
            # Verborgen variablen om de input waarden in op te slaan:
            dcc.Store(id="var_store"),
            dcc.Store(id="var_store_for_database"),

            

                   # Test:
                html.Div(
                    [html.Button("Bepaal je leeftijd", className="button", id="submit_button")],  
                ),

        ],

        className="g-2", justify="center",
    )
        ]),

        # Tabblad om een grafiek met voorgaande voorspellingen te zien.
        dcc.Tab(label='Voorgaande voorspellingen', children=[
        dcc.Graph(id="age_graph"),
        html.Div(id="age_prediction"),
        ]),

        
        # Tab met informatie over het ML model dat gebruikt wordt om de voorspellingen te maken.
        dcc.Tab(label='Hoe werkt dit?', children=[
        dcc.Markdown("""
                    ## SVR model ##
                    Op de achtergrond wordt een SVR model gebruikt om je leeftijd te voorspellen. 
                     SVR, "Support Vector Regression".
                    
                    ### Betrouwbaarheid ###
                    De resultaten van een model dat getrained is met data van vijf vragen 
                    kunnen onbetrouwbaar zijn, dit zou op te lossen zijn door meer vragen toe te voegen.
                     

                    

                    """)
                     
        ]),
    ])
])


@app.callback(
    Output("submit_button", "disabled"),
    Input("vraag1","value"),
    Input("vraag2","value"),
    Input("vraag3","value"),
  #  Input("vraag4","value"),
    Input("vraag5","value"),
    Input("vraag6","value"),
)

def submit_button_activate(vraag1,vraag2,vraag3,vraag5,vraag6):
    """
    Bepaal of de submit knop gebruikt kan worden, alleen wanneer alle waarden in gevuld zijn.
    """
    if None in [vraag1,vraag2,vraag3,vraag5,vraag6]:
        return True
    else:
        return False
    

@app.callback(
    Output("var_store","data"),
    Input("submit_button","n_clicks"),
    State("vraag1","value"),
    State("vraag2","value"),
    State("vraag3","value"),
#    State("vraag4","value"),
    State("vraag5","value"),
    State("vraag6","value"),
    prevent_initial_call = True
)

def get_userdata(n_clicks,vraag1,vraag2,vraag3,vraag5,vraag6):

    #print(vraag1)

    # db = connect_database()
    # df = make_dataframe(db)

    # new_row = {"leeftijd": "gewicht": weight_input, "lengte": height_input}
    # df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Sla de niewe waarden ook op in de database.

    questions = [vraag1,vraag2,vraag3,vraag5,vraag6]

    questions = [1 if v=="Ja" else 0 if v=="Nee" else v for v in questions]

    commit2database(questions[0],questions[1],questions[2],questions[3],questions[4]) 
    

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


@app.callback(
    Output("age_graph","figure"),
    Input("submit_button","n_clicks"),
    prevent_initial_call = True
)

def age_graph(n_clicks):

    db = connect_database()
    df = make_dataframe(db)

    index = df["id"]
    real_ages = pd.to_numeric(df["werkelijke_leeftijd"],errors="coerce").dropna()

    # Grafiek van gebruikers' leeftijd
    fig = px.histogram(
        real_ages,
        x="werkelijke_leeftijd",
        nbins=30,
        title="Leeftijd van deelnemers",
        labels={"Leeftijd": "Jaar"}
    )

    return fig



@app.callback(
    Output("age_prediction", "children"),
    Input("submit_button", "n_clicks"),
    State("vraag1", "value"),
    State("vraag2", "value"),
    State("vraag3", "value"),
    State("vraag5", "value"),
    State("vraag6", "value"),
    prevent_initial_call=True,

)
def prediction(n_clicks,vraag1,vraag2,vraag3,vraag5,vraag6):
    binary_answers = [vraag1, vraag2, vraag3, vraag5, vraag6]
    binary_answers = [1 if ans == "Ja" else 0 for ans in binary_answers]

    model = load_model()
    features = ["mp3_speler", "krant", "bellen_of_email", "smileys"]
    y_pred = model.y_pred
    y_prob_interval = model.y_prob_interval # 95% waarschijnlijkheid interval
    
    
    predicted_age = model.predict(np.array(binary_answers).reshape(1, -1))[0]
    print(y_pred)
    return f"Voorspelde leeftijd: {int(round(predicted_age))} jaar." # Test

if __name__ == "__main__":
    app.run(debug=True)