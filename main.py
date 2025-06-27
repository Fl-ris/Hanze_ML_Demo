import sqlite3
import pandas as pd


def connect_database():
    """
    Verbind met het database bestand of maak een nieuwe db aan als deze nog niet bestaat.
    """

    try:
            #To-do: Pad relatief maken....
        with open("/home/floris/Documenten/Github/Hanze_ML_Demo/DB/database.sql", "r") as sql_file:
            sql_script = sql_file.read()

        db = sqlite3.connect(database="database")
        cursor = db.cursor()
        
        cursor.executescript(sql_script)
        db.commit()

        df = pd.read_sql_query("select * from vragenlijst_data;", db)
        print(df)

        return db

    except:
       print("Error: De database kon niet aangemaakt worden...")


def make_dataframe(db):
    pass



def main():
    db = connect_database()
    make_dataframe(db)

if __name__ == "__main__":
    main()
