import sqlite3
from pathlib import Path
from random import randint
from modules.DB_class import Controle_Financeiro_DB, SQLite_DB_CRUD
from datetime import datetime, timedelta

MAIN_DB_NAME = "Controle_Financeiro_DB"
TEST_DB_NAME = "DB_teste"


with Controle_Financeiro_DB(TEST_DB_NAME) as test_db:
    test_db._create_controle_financeiro_tables()

# CF_db = Controle_Financeiro_DB(MAIN_DB_NAME)

# CF_db.init_connection()

# CF_db.close_connection()
