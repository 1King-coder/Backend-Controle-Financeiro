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


MAIN_DB_NAME = "Controle_Financeiro_DB"
TEST_DB_NAME = "DB_teste"

def main():

    with Deposito_controller() as dep_ctrler:
        # dep_ctrler.adiciona_deposito(2, 2, 120.25, "Teste 127")
        ...

    with Transferencia_entre_bancos_controller() as transf_b_ctrlers:
        # transf_b_ctrlers.adicionar(1, 2, 1, 24, "teste 1")
        # transf_b_ctrlers.adicionar(2, 1, 2, 10, "teste 2")
        ...

    with Transferencia_entre_direcionamentos_controller() as transf_dir_ctrlers:
        # transf_dir_ctrlers.adicionar(1, 2, 24, "teste 1")
        # transf_dir_ctrlers.adicionar(2, 1, 10, "teste 2")
        ...

    with Direcionamento_controller() as dir_ctrler:
        # print(dir_ctrler.get_total_depositos(2))
        # print(dir_ctrler.get_total_transferencias_recebidas(2))
        ...
    

    with Banco_controller() as b_ctrler:
        # b_ctrler.atualiza_saldo(2)
        # b_ctrler.atualiza_saldo(1)
        ...

    with Gasto_geral_controller() as gg_ctrler:
        # gg_ctrler.adiciona_gasto_geral(1, 1, descricao="Teste 1", valor=110)
        # gg_ctrler.adiciona_gasto_geral(2, 1, descricao="Teste 2", valor=50.15)
        # gg_ctrler.adiciona_gasto_geral(1, 2, descricao="Teste 3", valor=64.23)
        # gg_ctrler.adiciona_gasto_geral(2, 2, descricao="Teste 4", valor=122.5)
        ...
    with Gasto_periodizado_controller() as gp_ctrler:
        # gp_ctrler.adiciona_gasto_periodizado(1, 2, 12, 5, descricao="Teste 5")
        # gp_ctrler.adiciona_gasto_periodizado(2, 1, 100.25, 10, controle_parcelas=1, descricao="Teste 6")
        # gp_ctrler.adiciona_gasto_periodizado(1, 2, 52.13, 13, descricao="Teste 7", dia_abate="05/11/2023")
        # gp_ctrler.adiciona_gasto_periodizado(2, 1, 12, 5, 2, "Teste 8", "12/09/2023")
        # gp_ctrler.atualiza_controle_parcelas(16, 30)
        ...

if __name__ == '__main__':
    main()

    


# with Controle_Financeiro_DB(TEST_DB_NAME) as test_db:
#     test_db._create_controle_financeiro_tables()

# CF_db = Controle_Financeiro_DB(MAIN_DB_NAME)

# CF_db.init_connection()

# CF_db.close_connection()
