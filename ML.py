""""
Machine learning

"This is where the magic happens..."

Autheur: Floris Menninga
Datum: 20-07-2025

"""

import pandas as pd
import matplotlib.pyplot as plt


from main import connect_database
from main import make_dataframe



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

    # Paarsgewijze correlaties:
    axs = sns.heatmap(df[["social_media", "mp3_speler", "krant", "telefoon", "bellen_of_email", "smileys"]].corr(), annot=True, annot_kws={"fontsize": "x-small"}, cmap="jet", vmin=0.0, vmax=1.0, square=True)
    axs.set_title("Paarsgewijze correlaties ($R$)")
        
    # Histogram    
    df.hist( figsize=(16.0, 15));





def train():
    
    features_ordinal = ["telefoon"]
    features_categorical = ["mp3_speler", "krant", "bellen_of_email", "smileys"]

    to_predict = ["voorspelde_generatie"]

    all_features = features_ordinal + features_categorical





def predict():
    pass



def main():
    db = connect_database() # Initialiseer database / verbind met bestaande db

    df = make_dataframe(db) # Maak pandas dataframe van SQLite database
    
    df_valid = data_check(df) 

    visualize_df(df, df_valid) 

    train()


if __name__ == "__main__":
    main()
