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
    df = pd.read_sql_query("select * from vragenlijst_data;", db)
    print(df)
    return df



def main():
    db = connect_database()
    df = make_dataframe(db)

if __name__ == "__main__":
    main()
