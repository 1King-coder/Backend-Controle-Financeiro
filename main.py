import sqlite3
from pathlib import Path
from random import randint
from modules.DB_class import Controle_Financeiro_DB, SQLite_DB_CRUD
from datetime import datetime, timedelta

MAIN_DB_NAME = "Controle_Financeiro_DB"
TEST_DB_NAME = "DB_teste"


with SQLite_DB_CRUD(TEST_DB_NAME) as test_db:
    script = f"UPDATE teste_table SET data_start = date('now'), data_end = date(date('now'), '+24 DAYS') WHERE id = 6"
    # script = "ALTER TABLE teste_table ADD data_start TEXT; ALTER TABLE teste_table ADD data_end TEXT;"
    script = "SELECT *, (strftime('%Y', data_end) - strftime('%Y', data_start)) * 12 + (strftime('%m', data_end) - strftime('%m', data_start)) AS 'dif_datas' FROM teste_table WHERE id = 6"
    print(script)
    test_db.cursor.execute(
        script
    )

    print(dict(test_db.cursor.fetchall()[0]))
    


# CF_db = Controle_Financeiro_DB(MAIN_DB_NAME)

# CF_db.init_connection()

# CF_db.close_connection()
