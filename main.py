import sqlite3
from pathlib import Path
from random import randint
from modules.controllers.DB_base_class import SQLite_DB_CRUD
from datetime import datetime, timedelta
from modules.controllers.Banco_controller import *
from modules.controllers.Direcionamento_controller import *
from modules.controllers.Deposito_controller import *
from modules.controllers.Gasto_geral_controller import *
from modules.controllers.Gasto_periodizado_controller import *
from modules.controllers.Historico_bancos_controller import *
from modules.controllers.Historico_direcionamentos_controller import *
from modules.controllers.Transferencia_entre_bancos_controller import *
from modules.controllers.Transferencia_entre_direcionamentos_controller import *
import pandas as pd


MAIN_DB_NAME = "Controle_Financeiro_DB"
TEST_DB_NAME = "DB_teste"

def main(): ...

if __name__ == '__main__':
    main()

    


# with Controle_Financeiro_DB(TEST_DB_NAME) as test_db:
#     test_db._create_controle_financeiro_tables()

# CF_db = Controle_Financeiro_DB(MAIN_DB_NAME)

# CF_db.init_connection()

# CF_db.close_connection()
