import sqlite3
from pathlib import Path
from random import randint
from modules.DB_class import Controle_Financeiro_DB, SQLite_DB_CRUD

MAIN_DB_NAME = "Controle_Financeiro_DB"
TEST_DB_NAME = "DB_teste"


with SQLite_DB_CRUD(TEST_DB_NAME) as test_db:
    test_db.delete_data("teste_table", WHERE="id BETWEEN 10 AND 12")

    data = test_db.get_data("teste_table", WHERE="id BETWEEN 9 AND 13")
    
    print(data)


# CF_db = Controle_Financeiro_DB(MAIN_DB_NAME)

# CF_db.init_connection()

# CF_db.close_connection()
