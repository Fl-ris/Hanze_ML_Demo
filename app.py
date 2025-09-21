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
import dash_daq as daq
import plotly.graph_objects as go


from ML import data_check, visualize_df, load_model, predict # Imports van het machine learning script.
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
                ],
            ),
        ],
    )
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

    questions = [vraag1,vraag2,vraag3,vraag5,vraag6]

    questions = [1 if v=="Ja" else 0 if v=="Nee" else v for v in questions]

    commit2database(questions[0],questions[1],questions[2],questions[3],questions[4]) 


@app.callback(
    Output("tabs", "value"),
    Input("submit_button", "n_clicks"),
    prevent_initial_call=True,
)
def go_to_prediction_tab(n_clicks):
    return "tab-4"


@app.callback(
    Output("age_graph","figure"),
    Input("submit_button","n_clicks"),
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
)

def feature_correlation_graph(n_clicks):
    db = connect_database()
    df = make_dataframe(db)

    cols = ["social_media", "mp3_speler", "krant", "bellen_of_email", "smileys"]
    corr = df[cols].corr()


    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        labels=dict(x="", y="", color="Correlation")
    )

    return fig


@app.callback(
    Output("prediction_graph", "figure"),
    Output("age_prediction", "figure"),
    Input("submit_button", "n_clicks"),
    State("vraag1", "value"),
    State("vraag2", "value"),
    State("vraag3", "value"),
    State("vraag5", "value"),
    State("vraag6", "value"),
    prevent_initial_call=True,
)
def prediction(n_clicks, vraag1, vraag2, vraag3, vraag5, vraag6):

    db = connect_database()
    df = make_dataframe(db)

    binary_answers = [vraag1, vraag2, vraag3, vraag5, vraag6]
    binary_answers = [1 if ans == "Ja" else 0 for ans in binary_answers]

    joblib_dict = load_model()
    pipeline = joblib_dict["pipeline"]
    lower = joblib_dict["lower"]
    upper = joblib_dict["upper"]
    predicted_age = pipeline.predict(np.array(binary_answers).reshape(1, -1))[0]

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=df["werkelijke_leeftijd"],
            name="Known Ages Distribution",
            opacity=0.7,
            marker_color="lightblue",
            nbinsx=20,
        )
    )

    fig.add_vline(
        x=predicted_age,
        line_dash="dash",
        line_color="red",
        line_width=3,
        annotation_text=f"Voorspelde leeftijd: {predicted_age:}",
        annotation_position="top",
    )

    fig.add_vrect(
        x0=lower,
        x1=upper,
        fillcolor="red",
        opacity=0.2,
        line_width=0,
        annotation_text="95% waarschijnlijkheidsinterval",
        annotation_position="top left",
    )
    fig.add_vline(
        x=lower,
        line_dash="dot",
        line_color="red",
        line_width=1,
        opacity=0.5,
    )
    fig.add_vline(
        x=upper,
        line_dash="dot",
        line_color="red",
        line_width=1,
        opacity=0.5,
    )

    fig.update_layout(
        title="Voorspelde leeftijd met 95% waarschijnlijkheidsinterval",
        xaxis_title="Age (years)",
        yaxis_title="Count",
        showlegend=True,
        hovermode="x unified",
        template="plotly_white",
    )

    return fig, fig



## Test:

def feature_graph(df: pd.DataFrame):
    binary_cols = ["social_media", "mp3_speler", "krant", "bellen_of_email", "smileys"]
    df_bin = df[binary_cols].replace({0: "Nee", 1: "Ja"})
    melted = df_bin.melt(var_name="vraag", value_name="antwoord")
    counts = (
        melted.groupby(["vraag", "antwoord"])
          .size()
          .reset_index(name="aantal")
          .sort_values(["vraag", "antwoord"])
    )
    fig = px.bar(
        counts,
        x="vraag",
        y="aantal",
        color="antwoord",
        barmode="group",
        title="Antwoordverdeling per vraag",
        labels={"vraag": "Vraag", "aantal": "Aantal antwoorden"},
    )
    return fig


@app.callback(
    Output("db_feature_counts", "figure"),
    Input("submit_button", "n_clicks"),
)
def update_db_feature_counts(_):
    db = connect_database()
    df = make_dataframe(db)
    return feature_graph(df)


@app.callback(
    Output("real_age_feedback", "children"),
    Input("real_age_submit", "n_clicks"),
    State("real_age_input", "value"),
    prevent_initial_call=True,
)
def store_real_age(n_clicks, real_age):
    if real_age is None:
        return "Voer eerst een leeftijd in."

    try:
        age_int = int(real_age) and age_int > 5 and age_int < 100 
    except:
        return "Klop dat wel?"

    db = connect_database()
    cur = db.cursor()
    cur.execute(
        """
        UPDATE vragenlijst_data
        SET werkelijke_leeftijd = ?
        WHERE id = (
            SELECT id FROM vragenlijst_data
            WHERE werkelijke_leeftijd IS NULL
            ORDER BY id DESC
            LIMIT 1
        )
        """,
        (age_int,),
    )
    db.commit()
    db.close()
    
    # Test:
    db = connect_database()
    df = make_dataframe(db)
    print(df)
    
    return f"Leeftijd {age_int} is opgeslagen."




if __name__ == "__main__":
    app.run(debug=True)