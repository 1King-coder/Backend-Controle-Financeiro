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


TEST_DB_NAME = "DB_teste"

def main():
    """
    ÁREA DE TESTES

    Primeiro - crie o arquivo da base de dados.
    Segundo - execute o arquivo migrate.py para
              criar as tabelas e triggers.
    Terceiro - pode fazer seus testes por aqui,
               os controladores contam com os methods __enter__
               e __exit__ para que haja a garantia do fechamento da
               conexão com o banco de dados, então ao utilizar um controlador
               recomendo fortemente que utilize context managers.
    """

    with Banco_controller(TEST_DB_NAME) as b_ctrler:
        ...


        

if __name__ == '__main__':
    main()

    


