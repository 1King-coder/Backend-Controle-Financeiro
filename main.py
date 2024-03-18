from fastapi import FastAPI
from modules.routes.Bancos_R import init_routes as init_routes_bancos
from modules.routes.Direcionamentos_R import init_routes as init_routes_direcionamentos
from modules.routes.Depositos_R import init_routes as init_routes_depositos
from modules.routes.Gastos_gerais_R import init_routes as init_routes_gastos_gerais
from modules.routes.Gastos_periodizados_R import init_routes as init_routes_gastos_periodizados
from modules.routes.Transferencia_bancos_R import init_routes as init_routes_transferencias_bancos
from modules.routes.Transferencia_direcionamentos_R import init_routes as init_routes_transferencias_direcionamentos


TEST_DB_NAME = "DB_teste"
MAIN_DB_NAME = "Controle_Financeiro_DB"

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
    route(app, db_name=MAIN_DB_NAME)

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

    from modules.controllers.Banco_controller import Banco_controller

    with Banco_controller(db_name=MAIN_DB_NAME) as banco_controller:
        
        cursor = banco_controller.connection.cursor()

        cursor.execute(
            """
WITH total_dep AS (
        SELECT 
        s.id_banco as id_b, s.id_direcionamento as id_d,
        SUM(IFNULL(dep.valor, 0)) AS total
        FROM Saldo_banco_por_direcionamento s
        LEFT JOIN Depositos dep
            ON s.id_banco = dep.id_banco 
            AND s.id_direcionamento  = dep.id_direcionamento
        GROUP BY s.id_banco , s.id_direcionamento
        ),
        total_tbrec AS (
        SELECT 
        s.id_banco as id_b, s.id_direcionamento as id_d,
        SUM(IFNULL(t.valor, 0)) AS total
        FROM Saldo_banco_por_direcionamento s
        LEFT JOIN Transferencias_entre_bancos t
            ON t.id_banco_destino = s.id_banco 
            AND t.id_direcionamento = s.id_direcionamento
        GROUP BY s.id_banco , s.id_direcionamento
        ),
        total_tdrec AS (
        SELECT 
        s.id_banco as id_b, s.id_direcionamento as id_d,
        SUM(IFNULL(t.valor, 0)) AS total
        FROM Saldo_banco_por_direcionamento s
        LEFT JOIN Transferencias_entre_direcionamentos t
            ON t.id_direcionamento_destino = s.id_direcionamento 
            AND t.id_banco = s.id_banco
        GROUP BY s.id_banco , s.id_direcionamento
        ),
        total_gastos AS (
        SELECT s.id_banco as id_b, s.id_direcionamento as id_d,
        SUM(IFNULL(gi.valor, 0) + 
            IFNULL(gp.valor_parcela * gp.controle_parcelas, 0))
            as total
        FROM Saldo_banco_por_direcionamento s
        LEFT JOIN Gastos_gerais gg
            ON gg.id_banco = s.id_banco 
            AND gg.id_direcionamento = s.id_direcionamento
        LEFT JOIN Gastos_imediatos gi
            ON gi.id_gasto = gg.id
        LEFT JOIN Gastos_periodizados gp
            ON gp.id_gasto = gg.id
        GROUP BY s.id_banco ,s.id_direcionamento
        ),
        total_tbenv AS (
        SELECT 
        s.id_banco as id_b, s.id_direcionamento as id_d,
        SUM(IFNULL(t.valor, 0)) AS total
        FROM Saldo_banco_por_direcionamento s
        LEFT JOIN Transferencias_entre_bancos t
            ON t.id_banco_origem = s.id_banco 
            AND t.id_direcionamento = s.id_direcionamento
        GROUP BY s.id_banco , s.id_direcionamento
        ),
        total_tdenv AS (
        SELECT 
        s.id_banco as id_b, s.id_direcionamento as id_d,
        SUM(IFNULL(t.valor, 0)) AS total
        FROM Saldo_banco_por_direcionamento s
        LEFT JOIN Transferencias_entre_direcionamentos t
            ON t.id_direcionamento_origem = s.id_direcionamento 
            AND t.id_banco = s.id_banco
        GROUP BY s.id_banco , s.id_direcionamento)
        UPDATE Saldo_banco_por_direcionamento AS sbpd
        SET saldo = (
        SELECT
        (total_dep.total + total_tbrec.total + total_tdrec.total)
        - (total_gastos.total + total_tbenv.total + total_tdenv.total)
        AS total
        FROM Saldo_banco_por_direcionamento s
        LEFT JOIN total_dep
            ON total_dep.id_b = s.id_banco 
            AND total_dep.id_d = s.id_direcionamento 
        LEFT JOIN total_tbrec
            ON total_tbrec.id_b = s.id_banco
            AND total_tbrec.id_d = s.id_direcionamento 
        LEFT JOIN total_tdrec
            ON total_tdrec.id_b = s.id_banco 
            AND total_tdrec.id_d = s.id_direcionamento
        LEFT JOIN total_gastos
            ON total_gastos.id_b = s.id_banco
            AND total_gastos.id_d = s.id_direcionamento
        LEFT JOIN total_tbenv
            ON total_tbenv.id_b = s.id_banco
            AND total_tbenv.id_d = s.id_direcionamento 
        LEFT JOIN total_tdenv
            ON total_tdenv.id_b = s.id_banco 
            AND total_tdenv.id_d = s.id_direcionamento
        WHERE s.id_banco = sbpd.id_banco
        AND s.id_direcionamento = sbpd.id_direcionamento);
"""
        )

        banco_controller.connection.commit()
        cursor.close()


        

if __name__ == '__main__':
    main()

    


