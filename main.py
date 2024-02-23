import sqlite3
from pathlib import Path
from random import randint
from modules.DB_class import Controle_Financeiro_DB, SQLite_DB

MAIN_DB_NAME = "Controle_Financeiro_DB"
TEST_DB_NAME = "DB_teste"


with SQLite_DB(TEST_DB_NAME) as test_db:
    print(test_db.get_data("teste_table", command="*, (id + weight)"))


# CF_db = Controle_Financeiro_DB(MAIN_DB_NAME)

# CF_db.init_connection()

# CF_db.close_connection()

