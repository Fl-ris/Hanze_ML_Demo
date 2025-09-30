# Maak een Sqlite3 db met ~100 voorbeeld entries:

# Maak de table:
sqlite3 database.db < database.sql

# Vul table met 2* 50 voorbeeld entries:
sqlite3 database.db < test_data.sql
sqlite3 database.db < test_data.sql

