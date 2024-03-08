import sqlite3
from pathlib import Path
from random import randint
from fastapi import FastAPI

from modules.controllers.Banco_controller import Banco_controller
from modules.controllers.Direcionamento_controller import Direcionamento_controller
from modules.controllers.Deposito_controller import Deposito_controller
from modules.controllers.Gasto_geral_controller import  Gasto_geral_controller
from modules.controllers.Gasto_periodizado_controller import Gasto_periodizado_controller
from modules.controllers.Historico_bancos_controller import Historico_bancos_controller
from modules.controllers.Historico_direcionamentos_controller import Historico_direcionamentos_controller
from modules.controllers.Transferencia_entre_bancos_controller import Transferencia_entre_bancos_controller
from modules.controllers.Transferencia_entre_direcionamentos_controller import Transferencia_entre_direcionamentos_controller
from modules.routes.Bancos_R import init_routes as init_routes_bancos
from modules.routes.Direcionamentos_R import init_routes as init_routes_direcionamentos


import pandas as pd

Banco_C = Banco_controller
Direcionamento_C = Direcionamento_controller
Deposito_C = Deposito_controller
Gasto_geral_C = Gasto_geral_controller
Gasto_periodizado_C = Gasto_periodizado_controller
Historico_bancos_C = Historico_bancos_controller
Historico_direcionamentos_C = Historico_direcionamentos_controller
Transferencia_entre_bancos_C = Transferencia_entre_bancos_controller
Transferencia_entre_direcionamentos_C = Transferencia_entre_direcionamentos_controller

TEST_DB_NAME = "DB_teste"

app = FastAPI(
    title="API Controle Financeiro",
    version="1.0.0",
)

routes = [
    init_routes_bancos,
    init_routes_direcionamentos]

for route in routes:
    route(app, db_name=TEST_DB_NAME)

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


        

if __name__ == '__main__':
    main()

    


