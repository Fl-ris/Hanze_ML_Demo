""""
Machine learning

"This is where the magic happens..."

Autheur: Floris Menninga
Datum: 20-07-2025

"""

import pandas as pd


from main import connect_database
from main import make_dataframe



def data_check(df):
    checked_df = None
    nas = df[["gewicht", "leeftijd", "lengte"]].isna().sum() # Verkrijg lijst met NA's voor elke kolom (behalve de "voorspelling_correct" kolom )
    na_sum = nas.sum() # Sommeer de NA's van elke kolom

    if na_sum > 0:
        print(f"Er zijn {na_sum} NA's aanwezig...")
    else:
        checked_df = df

    return checked_df 



def visualiseer_data(checked_df):
    """
    Om de gegevens te visualizeren die al aanwezig zijn in de database
    """


    checked_df.hist()

    
    pass




def train():
    pass




def main():
    db = connect_database() # Initialiseer database / verbind met bestaande db

    df = make_dataframe(db) # Maak pandas dataframe van SQLite database
    
    checked_df = data_check(df)

    train()


if __name__ == "__main__":
    main()
