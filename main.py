import sqlite3
from pathlib import Path
from random import randint
from fastapi import FastAPI

from modules.routes.Bancos_R import init_routes as init_routes_bancos
from modules.routes.Direcionamentos_R import init_routes as init_routes_direcionamentos
from modules.routes.Depositos_R import init_routes as init_routes_depositos
from modules.routes.Gastos_gerais_R import init_routes as init_routes_gastos_gerais
from modules.routes.Gastos_periodizados_R import init_routes as init_routes_gastos_periodizados
from modules.routes.Transferencia_bancos_R import init_routes as init_routes_transferencias_bancos
from modules.routes.Transferencia_direcionamentos_R import init_routes as init_routes_transferencias_direcionamentos

import pandas as pd

TEST_DB_NAME = "DB_teste"

app = FastAPI(
    title="API Controle Financeiro",
    version="1.0.0",
)

routes = [
    init_routes_bancos,
    init_routes_direcionamentos,
    init_routes_depositos,
    init_routes_gastos_gerais,
    init_routes_gastos_periodizados,
    init_routes_transferencias_bancos,
    init_routes_transferencias_direcionamentos
]

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

    


