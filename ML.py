""""
Machine learning script
Gebruikt een SVR model om de leeftijd te voorspellen.
Deze leeftijd zal bepaald worden aan de hand van 5 vragen.

Auteur: Floris Menninga
Datum: 20-07-2025
Versie: 0.2

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split, ShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from mapie.regression import MapieRegressor
from sklearn.metrics import mean_absolute_error

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
    if df is None:
        db = connect_database()
        df = make_dataframe(db)

    mask = df["werkelijke_leeftijd"].notna()
    df = df.loc[mask].copy()

    # if len(df) < 1:
    #     print(f"Niet genoeg data om model te trainen... Maar {len(df)} regels in DF gevonden.")
    #     joblib.dump({"model": None, "has_interval": False, "mae": None}, TRAINED_MODEL)
    #     return

    features_categorical = df[["social_media", "mp3_speler", "krant", "bellen_of_email", "smileys"]]

    X = features_categorical 
    y = df["werkelijke_leeftijd"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    base_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("SVR", SVR(kernel="linear"))
    ])

    joblib_dict = {}
    fitted_model = None

    if len(df) < 60:
        print("Standaard SVR model aan het trainen, niet genoeg data voor MAPIE...")
        base_pipeline.fit(X_train, y_train)
        joblib_dict["model"] = base_pipeline
        joblib_dict["has_interval"] = False
        fitted_model = base_pipeline
    else:
        print("SVR model met MAPIE aan het trainen...")
    
        simple_split = ShuffleSplit(n_splits=1, test_size=0.5, random_state=42)
        
        mapie = MapieRegressor(estimator=base_pipeline, cv=simple_split, n_jobs=-1)
        
        mapie.fit(X_train, y_train)
        joblib_dict["model"] = mapie
        joblib_dict["has_interval"] = True
        fitted_model = mapie

    y_pred = fitted_model.predict(X_test)
    if isinstance(y_pred, tuple):
        y_pred = y_pred[0]


    mae = mean_absolute_error(y_test, y_pred)
    joblib_dict["mae"] = mae
    
    print(f"Model evaluatie:")
    print(f"Mean Absolute Error: {mae:.2f} jaar")

    joblib.dump(joblib_dict, TRAINED_MODEL)
    print("Training van het model klaar.")


def load_model():
    db = connect_database()
    df = make_dataframe(db)
    if not TRAINED_MODEL.is_file():
        print("Nog geen bestaand model gevonden. Er wordt nu een nieuwe getrained....")
        train(df)
    return joblib.load(TRAINED_MODEL)


def predict(features,df):
    model = load_model()
    X = np.array(features, dtype=float).reshape(1, -1)
    return model.predict(X)[0] 


def main():
    db = connect_database() # Initialiseer database / verbind met bestaande db

    df = make_dataframe(db) # Maak pandas dataframe van SQLite database
    
    df_valid = data_check(df) 

    visualize_df(df, df_valid) 

    train(df)


if __name__ == "__main__":
    main()
