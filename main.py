""""
Helper functies

Auteur: Floris Menninga
Datum: 20-07-2025
Versie: 0.2

"""

import sqlite3
import pandas as pd


def connect_database():
    """
    Verbind met het database bestand of maak een nieuwe db aan als deze nog niet bestaat.
    """

    try:

        with open("DB/database.sql", "r") as sql_file:
            sql_script = sql_file.read()


        db = sqlite3.connect(database="DB/database.db")
        cursor = db.cursor()
        
        cursor.executescript(sql_script)
        db.commit()

        return db

    except:
       print("Error: De database kon niet aangemaakt worden...")


def make_dataframe(db):
    """
    Maak een pandas dataframe van de Sqlite3 database.
    """
    df = pd.read_sql_query("select * from vragenlijst_data;", db)
    return df


def commit2database(vraag1,vraag2,vraag3,vraag4,vraag5,vraag6,vraag7):
    """
    Om de nieuwe waarden van het dashboard in de database op te nemen.
    """
    db = sqlite3.connect(database="DB/database.db")
    cursor = db.cursor()

    #df.to_sql("vragenlijst_data", db, if_exists="append", index=False)
    cursor.execute("INSERT INTO vragenlijst_data(social_media,mp3_speler,krant,tafel_van_vijf,bellen_of_email,smileys,email) VALUES (?,?,?,?,?,?,?)", (vraag1,vraag2,vraag3,vraag4,vraag5,vraag6,vraag7))
   # cursor.execute("select * from vragenlijst_data;") # Test
    db.commit()
    db.close()





def main():

    # In deze volgorde zal het Dash dashboard deze functies gebruiken... 
    db = connect_database()
    
    df = make_dataframe(db)

    #db = dataframe2database(df)


if __name__ == "__main__":
    main()
