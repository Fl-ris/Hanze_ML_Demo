""""
Machine learning script
Gebruikt een SVR model om de leeftijd te voorspellen, deze leeftijd wordt vervolgens
als generatie (Gen X, Z etc.) aan de gebruiker weergeven aangezien de werkelijke leeftijd niet naukeurig genoeg 
bepaald kan worden aan de hand van 5 vragen.

"This is where the magic happens..."

Autheur: Floris Menninga
Datum: 20-07-2025
Versie: 0.1

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from main import connect_database
from main import make_dataframe
import joblib
from pathlib import Path


TRAINED_MODEL = Path("assets/model.joblib")


def data_check(df):
    df_valid = False

    if df is not None:
        nas = df[["gewicht", "leeftijd", "lengte"]].isna().sum() # Verkrijg lijst met NA's voor elke kolom (behalve de "voorspelling_correct" kolom )
        na_sum = nas.sum() # Sommeer de NA's van elke kolom

        if na_sum > 0:
            print(f"Er zijn {na_sum} NA's aanwezig...")
        else:
            df_valid = True
            return df_valid 
    else:
        return df_valid


def visualize_df(df, df_valid):
    """
    Om de gegevens te visualizeren die al aanwezig zijn in de database
    """
    # To-do: integreren in dashboard...

    # Paarsgewijze correlaties:
    axs = sns.heatmap(df[["social_media", "mp3_speler", "krant", "bellen_of_email", "smileys"]].corr(), annot=True, annot_kws={"fontsize": "x-small"}, cmap="jet", vmin=0.0, vmax=1.0, square=True)
    axs.set_title("Paarsgewijze correlaties")
        
    # Histogram    
    df.hist( figsize=(16.0, 15));





def train(df):

    db = connect_database()
    df = make_dataframe(db)


   # features_ordinal = df["telefoon"]
    features_categorical = df[["mp3_speler", "krant", "bellen_of_email", "smileys"]]

    to_predict = df["voorspelde_generatie"]

   # X = pd.concat([features_categorical,features_ordinal] , axis=1)
    X = features_categorical

    print(df[["mp3_speler", "krant", "bellen_of_email", "smileys"]].shape)
    print(df["werkelijke_leeftijd"].shape)

    y = df["werkelijke_leeftijd"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("SVR", SVR(kernel="linear"))
    ])

    pipeline.fit(X_train, y_train)

    joblib.dump(pipeline, TRAINED_MODEL)


def load_model():
    if not TRAINED_MODEL.is_file():
        print("Nog geen bestaand model gevonden. Er wordt nu een nieuwe getrained....")
        train()
    return joblib.load(TRAINED_MODEL)


def predict():
    prediction = pipeline.predict(placeholder)
    return prediction


def main():
    db = connect_database() # Initialiseer database / verbind met bestaande db

    df = make_dataframe(db) # Maak pandas dataframe van SQLite database
    
    df_valid = data_check(df) 

    visualize_df(df, df_valid) 

    train(df)


if __name__ == "__main__":
    main()
