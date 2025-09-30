"""
Dash dashboard
Datum: 29-08-2025
Auteur: Floris Menninga
Versie: 0.1
"""


from dash import Dash, html, dcc, callback, Output, Input, State,callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import dash_daq as daq
from dash import no_update
import plotly.graph_objects as go


from ML import data_check, visualize_df, load_model, predict, train # Imports van het machine learning script.
from main import make_dataframe, connect_database, commit2database # Imports van de helper functies voor de DB en DF.


app = Dash(external_stylesheets=[dbc.themes.SOLAR])#,requests_pathname_prefix='/app/')



app.layout = html.Div([
    dcc.Tabs(
        id="tabs",
        value="tab-1",
        children=[dcc.Tab(label="Begin hier!",value="tab-1",children=[
        html.Div(
            daq.LEDDisplay(
                id='participant-counter',
                label='Aantal deelnemers',
                value='0',
                size=30,
                color="#00FF22",
                backgroundColor='#111111'
            ),
            style={
                'position': 'fixed',
                'bottom': '20px',
                'right': '20px',
            }
        ),
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
                            dbc.Col(
                                html.Button(
                                    "Voorspel je leeftijd",
                                    className="button",
                                    id="submit_button",
                                ),
                                width="auto",
                                className="d-flex justify-content-center",
                            ),
                        ],

                        className="g-2",
                        justify="center",
                    ),
                        dbc.Row(
      #  dbc.Col(

    ),
                ],
            ),

            dcc.Tab(
                label="Voorgaande voorspellingen",
                value="tab-2",
                children=[
                    dcc.Graph(id="age_graph"),
                    #dcc.Graph(id="age_prediction"),
                    dcc.Graph(id="db_feature_counts"),
                    dbc.Card(id="mae_reporter", className="mt-2 mb-4 p-3"),
                ],
            ),

            dcc.Tab(
                label="Resultaat",
                value="tab-4",
                children=[
                #dcc.Graph(id="prediction_graph"), \
                dcc.Graph(id="age_distribution"),
                daq.LEDDisplay(
                    id='age_display',
                    label='Je voorspelde leeftijd:',
                    value='0',
                    size=40,
                    color="#00FF22",
                    backgroundColor='#111111'
                ),
              #  html.Div(id='confidence_interval', style={'textAlign': 'center', 'margin': '20px'}),
               # dcc.Graph(id="age_distribution"),
                    dbc.Row(
                        [dcc.Markdown("Vul je echte leeftijd in op het onderstaande veld zodat het SVR model er van kan leren.",style={'textAlign': 'center',}),
                            dcc.Markdown("Je zal nu automatisch terug gaan naar het beginscherm zodat de volgende deelnemer hem in kan vullen. ",style={'textAlign': 'center',}),
                         
                            dbc.Col(
                                
                                dbc.Input(
                                    id="real_age_input",
                                    type="number",
                                    min=0,
                                    placeholder="Leeftijd",
                                    style={"width": "220px"},
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Leeftijd opslaan",
                                    id="real_age_submit",
                                    color="primary",
                                    className="ms-2",
                                ),
                                width="auto",
                            ),
                        ],
                        justify="center",
                        align="center",
                        className="mt-4",
                    ),
                    html.Div(id="age-int"),
                    html.Div(id='confidence_interval', style={'textAlign': 'center', 'margin': '10px'}),
                    html.Div(id="real_age_feedback"),
                        html.Div(id="predicted_age_text",
                        style={"marginTop": "10px", "fontSize": "1.2rem"}),
                         ],

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
                        Als iedereen die deze vragen invult tussen de 8 en 100 jaar oud zou zijn kan het model onderscheid maken tussen
                        een leeftijdverschil van ~3 jaar ((92-80)/32) = 2,97 jaar, als deze vragen perfect onderscheid kunnen maken tussen leeftijdsgroepen.
                        
                        
                        ## Correlaties tussen de vragen ##
                        De paarsgewijze correlaties zijn weergeven op de onderstaande heatmap. 
                        """
                    ),
                    dcc.Graph(id="feature_correlation_graph"),
                ],
            ),
        ],
    )
]
    )


@app.callback(
    Output("submit_button", "disabled"),
    Input("vraag1","value"),
    Input("vraag2","value"),
    Input("vraag3","value"),
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
    State("vraag5","value"),
    State("vraag6","value"),
    prevent_initial_call = True
)

def get_userdata(n_clicks,vraag1,vraag2,vraag3,vraag5,vraag6):

    questions = [vraag1,vraag2,vraag3,vraag5,vraag6]

    questions = [1 if v=="Ja" else 0 if v=="Nee" else v for v in questions]

    commit2database(questions[0],questions[1],questions[2],questions[3],questions[4]) 
    
    return {"saved": True}


@app.callback(
    Output("vraag1","value"),
    Output("vraag2","value"),
    Output("vraag3","value"),
    Output("vraag5","value"),
    Output("vraag6","value"),
    Input("submit_button","n_clicks"),
    prevent_initial_call=True,
)
def reset_questions(_):
    # Reset de radiobuttons na het voorspellen voor de volgende gebruiker:
    return None, None, None, None, None



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
        labels={"Leeftijd": "Jaar"},
        template="plotly_dark"
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
        labels=dict(x="", y="", color="Correlation"),
    )

    return fig




@app.callback(
    Output("age_display", "value"),
    Output("confidence_interval", "children"),
    Output("age_distribution", "figure"),
    Input("submit_button", "n_clicks"),
    State("vraag1", "value"),
    State("vraag2", "value"),
    State("vraag3", "value"),
    State("vraag5", "value"),
    State("vraag6", "value"),
    prevent_initial_call=True,
)
def prediction(n_clicks, vraag1, vraag2, vraag3, vraag5, vraag6):
    binary_answers = [vraag1, vraag2, vraag3, vraag5, vraag6]
    processed_answers = []
    for ans in binary_answers:
        if ans == "Ja":
            processed_answers.append(1)
        elif ans == "Nee":
            processed_answers.append(0)
        else:
            processed_answers.append(ans)

    user_input = np.array(processed_answers).reshape(1, -1)

    joblib_dict = load_model()
    model = joblib_dict["model"]
    has_interval = joblib_dict.get("has_interval", False)

    predicted_age = 0
    ci_display = ""

    if has_interval:
        y_pred, y_pis = model.predict(user_input, alpha=0.05)
        predicted_age = y_pred[0]
        intervals = np.squeeze(y_pis)
        lower_val, upper_val = intervals[0], intervals[1]
        ci_display = html.Div([
            html.P("95% waarschijnlijkheidsinterval"),
            html.P(f"Volgens het model ben je minimaal {lower_val:.1f} jaar en maximaal {upper_val:.1f}] jaar oud.",
                   style={'margin': '0', 'fontSize': '18px', 'fontWeight': 'bold'})
        ])
    else:
        predicted_age = model.predict(user_input)[0]
        ci_display = html.P("Niet genoeg data om een waarschijnlijkheidsinterval te geven...")

    pred_int = int(round(float(predicted_age)))

    upd_conn = connect_database()
    cur = upd_conn.cursor()
    cur.execute(
        """
        UPDATE vragenlijst_data
        SET voorspelde_leeftijd = ?
        WHERE id = (SELECT MAX(id) FROM vragenlijst_data WHERE voorspelde_leeftijd IS NULL)
        """,
        (pred_int,),
    )
    upd_conn.commit()
    upd_conn.close()

    db = connect_database()
    df = make_dataframe(db)

    if 'werkelijke_leeftijd' in df.columns:
        valid_ages = pd.to_numeric(df['werkelijke_leeftijd'], errors='coerce').dropna()
    else:
        valid_ages = pd.Series(dtype='float64')

    if not valid_ages.empty:
        fig = go.Figure()
        fig.add_trace(go.Box(
            x=valid_ages,
            marker_color='rgb(9,56,125)',
            boxpoints=False
        ))
        fig.add_trace(go.Scatter(
            x=[predicted_age],
            mode='markers',
            name='Voorspelde leeftijd',
            marker=dict(color='red', size=15, symbol='star')
        ))
        fig.update_layout(
            xaxis_title="Leeftijd",
            yaxis_title="",
            showlegend=True
        )
    else:
        fig = go.Figure()
        fig.update_layout(title_text="Te weinig data om iets te weergeven...", height=400)

    return str(pred_int), ci_display, fig


## Test:

def feature_graph(df: pd.DataFrame):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title_text="Geen data")
        return fig

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
        template="plotly_dark"
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
        age_int = int(real_age)
    except (ValueError, TypeError):
        return "Ongeldige waarde."

    if not (5 < age_int < 100):
        return "Is dat wel je leeftijd?"

    db = connect_database()
    cur = db.cursor()
    cur.execute(
        """
        UPDATE vragenlijst_data
        SET werkelijke_leeftijd = ?
        WHERE id = (
            SELECT id
            FROM vragenlijst_data
            WHERE werkelijke_leeftijd IS NULL
            ORDER BY id DESC
            LIMIT 1
        )
        """,
        (age_int,),
    )
    db.commit()
    db.close()


    db = connect_database()
    df = make_dataframe(db)
    print(df)
    
    try:
        train(df)
        train_msg = "Model opnieuw getrained met deze nieuwe data..."
    except Exception as e:
        train_msg = f"Error tijdens trainen op deze data... {e}"

    return f"Leeftijd {age_int} opgeslagen.{train_msg}"

@app.callback(
    Output('participant-counter', 'value'),
    Input('submit_button', 'n_clicks')
)
def update_participant_counter(n_clicks):
    db = connect_database()
    cur = db.cursor()
    cur.execute('SELECT COUNT(*) FROM vragenlijst_data')
    count = cur.fetchone()[0]
    db.close()
    return str(count)

@app.callback(
    Output("mae_reporter", "children"),
    Input("tabs", "value"),
    Input("real_age_feedback", "children") 
)
def update_mae_reporter(tab_value, age_feedback):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'tabs' and tab_value != 'tab-3':
        return no_update

    joblib_dict = load_model()
    mae = joblib_dict.get("mae")

    if mae is not None:
        report_text = f"Gemiddeld wijken de voorspellingen van dit model {mae:.2f} jaar af van de werkelijke leeftijd."
        return html.P(report_text)
    else:
        report_text = "Nog niet genoeg data verzameld om de accuratesse te berekenen."
        return html.P(report_text, className="text-warning")

if __name__ == "__main__":
    app.run(debug=True)