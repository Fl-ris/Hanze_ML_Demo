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

    if df != None:
        nas = df[["gewicht", "leeftijd", "lengte"]].isna().sum() # Verkrijg lijst met NA's voor elke kolom (behalve de "voorspelling_correct" kolom )
        na_sum = nas.sum() # Sommeer de NA's van elke kolom

        if na_sum > 0:
            print(f"Er zijn {na_sum} NA's aanwezig...")
        else:
            df_valid = True
            return df_valid 

    return df_valid


def visualize_df(df, df_valid):
    """
    Om de gegevens te visualizeren die al aanwezig zijn in de database
    """

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df['leeftijd'])

    ax.set_title('Age distribution')
    ax.set_xlabel('Age')
    ax.set_ylabel('Count')
    plt.tight_layout()
    plt.show()

    if df_valid:
        df.hist()






    
    pass





def train():
    pass



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
