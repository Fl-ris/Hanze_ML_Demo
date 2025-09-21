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


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



app.layout = html.Div([
    dcc.Tabs(
        id="tabs",
        value="tab-1",
        children=[dcc.Tab(label="Begin hier!",value="tab-1",children=[
                    dbc.Row([dbc.Label(
                                "Maak je gebruik van Snapchat of Tiktok?",
                                width="auto",
                                align="center",
                                size="lg",
                            ),
                            dcc.RadioItems(
                                ["Ja", "Nee"],
                                inline=True,
                                className="d-flex justify-content-center",
                                id="vraag1",
                            ),

                            dbc.Label(
                                "Heb je ooit een Sony Walkman / discman gekocht?",
                                width="auto",
                                size="lg",
                            ),
                            dcc.RadioItems(
                                ["Ja", "Nee"],
                                inline=True,
                                className="d-flex justify-content-center",
                                id="vraag2",
                            ),

                            dbc.Label(
                                "Lees je regelmatig de krant?",
                                width="auto",
                                size="lg",
                            ),
                            dcc.RadioItems(
                                ["Ja", "Nee"],
                                inline=True,
                                className="d-flex justify-content-center",
                                id="vraag3",
                            ),

                            # Vraag 5
                            dbc.Label(
                                "Geef je de voorkeur aan bellen of emailen / Whatsapp etc.?",
                                width="auto",
                                size="lg",
                            ),
                            dcc.RadioItems(
                                options=[
                                    {"label": "Bellen", "value": 0},
                                    {"label": "Whatsapp etc.", "value": 1},
                                ],
                                inline=True,
                                className="d-flex justify-content-center",
                                id="vraag5",
                            ),

                            # Vraag 6
                            dbc.Label(
                                "Gebruik je bij het sturen van digitale berichten geregeld smileys zoals '😂'?",
                                width="auto",
                                size="lg",
                            ),
                            dcc.RadioItems(
                                ["Ja", "Nee"],
                                inline=True,
                                className="d-flex justify-content-center",
                                id="vraag6",
                            ),

                            dcc.Store(id="var_store"),
                            dcc.Store(id="var_store_for_database"),
                            dbc.Col(html.Div([
                                        html.Button(
                                            "Voorspel je leeftijd",
                                            className="button",
                                            id="submit_button",
                                        )
                                    ],
                                    className="justify-content-center",
                                ),
                            ),
                        ],

                        className="g-2",
                        justify="center",
                    )
                ],
            ),

            dcc.Tab(
                label="Voorgaande voorspellingen",
                value="tab-2",
                children=[
                    dcc.Graph(id="age_graph"),
                    dcc.Graph(id="age_prediction"),
                    dcc.Graph(id="db_feature_counts"),
                ],
            ),

            dcc.Tab(
                label="Resultaat",
                value="tab-4",
                children=[
                    dcc.Graph(id="prediction_graph"), 
                    dbc.Input(
                                        id="real_age_input",
                                        type="number",
                                        min=0,
                                        placeholder="Voer je werkelijke leeftijd in",
                                        style={"width": "180px"},
                                    ),
                    dbc.Col(
                                    dbc.Button(
                                        "Leeftijd opslaan",
                                        id="real_age_submit",
                                        color="primary",
                                        className="ms-2 mt-2",
                                    ),
                                    width="auto",),
                    html.Div(id="age-int"),
                    html.Div(id="real_age_feedback"),
                ],
                style={"padding": "20px"},
            ),
            dcc.Tab(
                label="Hoe werkt dit?",
                value="tab-3",
                children=[
                    dcc.Markdown(
                        """
                        ## SVR model ##
                        Op de achtergrond wordt een SVR (Support Vector Regression) model gebruikt om je leeftijd te voorspellen. 
                        
                        
                        ### Betrouwbaarheid ###
                        De resultaten van een model dat getrained is met data van vijf vragen 
                        kunnen onbetrouwbaar zijn, dit zou op te lossen zijn door meer vragen toe te voegen.
                        Er zijn nu vijf vragen met twee antwoorden per vraag die 2^5 = 32 unieke antwoord combinaties geven.
                        Als we er van uit gaan dat iedereen die deze vragen invult tussen de 8 en 100 jaar oud is
                        In het beste geval zit er ongeveer 3 jaar tussen antwoord combinaties ((92-80)/32) = 2,97 jaar.
                        
                        
                        ## Correlaties tussen de vragen ##
                        De paarsgewijze correlaties zijn weergeven op de onderstaande heatmap. 
                        """
                    ),
                    dcc.Graph(id="feature_correlation_graph"),
                     
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
    

# @app.callback(
#     Output("tab-2", "value"),
#     Input("submit_button", "n_clicks"),
#     prevent_initial_call=True,
# )
# def go_to_prediction_tab(n_clicks):
#     return "tab-2"


@app.callback(
    Output("var_store_for_database","data"),
    Input("submit_button","n_clicks"),
    prevent_initial_call = True
)

# def save_to_database(n_clicks):
#     db = connect_database()
#     df = make_dataframe(db)
#     print(df)


@app.callback(
    Output("age_graph","figure"),
    Input("submit_button","n_clicks"),
    #prevent_initial_call = True
)

def age_graph(n_clicks):

    db = connect_database()
    df = make_dataframe(db)

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
    Output("feature_correlation_graph","figure"),
    Input("submit_button","n_clicks"),
    #prevent_initial_call = True
)

def feature_correlation_graph(n_clicks):
    db = connect_database()
    df = make_dataframe(db)

    #real_ages = pd.to_numeric(df["werkelijke_leeftijd"],errors="coerce").dropna()

    cols = ["social_media", "mp3_speler", "krant", "bellen_of_email", "smileys"]
    corr = df[cols].corr()


    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        labels=dict(x="", y="", color="Correlation")
    )

    return fig


# @app.callback(
#     Output("scatter_graph","figure"),
#     Input("submit_button","n_clicks"),
# )

# def scatter_graph(n_clicks):
#     db = connect_database()
#     df = make_dataframe(db)

#     #real_ages = pd.to_numeric(df["werkelijke_leeftijd"],errors="coerce").dropna()

#     cols = ["social_media", "mp3_speler", "krant", "bellen_of_email", "smileys"]
#     corr = df[cols].corr()


#     fig = px.imshow(
#         corr,
#         text_auto=True,
#         aspect="auto",
#         labels=dict(x="", y="", color="Correlation")
#     )

#     return fig


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

    joblib_dict = load_model()
    pipeline = joblib_dict["pipeline"]

   # y_pred = model.get(y_pred)
    #y_prob_interval = model.get(y_prob_interval) # 95% waarschijnlijkheids interval

    predicted_age = pipeline.predict(np.array(binary_answers).reshape(1, -1))[0]

    return f"Voorspelde leeftijd: {int(round(predicted_age))} {joblib_dict["lower"]} {joblib_dict["upper"]} jaar." # Test


if __name__ == "__main__":
    app.run(debug=True)