from ..models.Banco_model import Banco_model
from .Historico_bancos_controller import Historico_bancos_controller
from pandas import DataFrame

from .DB_base_class import SQLite_DB_CRUD

class Banco_controller (SQLite_DB_CRUD):
    def __init__ (self, db_name: str) -> None:
        super().__init__(db_name)


    def mostrar (self) -> list:
        return self.get_data(
            "Bancos"
        )
    
    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())
    
    def get_total_depositos (self, id_banco) -> float:
        total_depositos = self.get_data("Depositos", "SUM(valor) AS 'total'", f"id_banco = {id_banco}")
        if not total_depositos:
            return 0
        
        if not total_depositos[0].get('total'):
            return 0
        
        return total_depositos[0]['total']

    def get_total_gastos_imediatos (self, id_banco) -> float:
        get_gastos_imediatos = f"""
        SELECT id_banco, SUM(Gastos_gerais.valor) AS 'total' FROM Gastos_gerais 
        JOIN Gastos_imediatos ON Gastos_imediatos.id_gasto = Gastos_gerais.id 
        WHERE id_banco = {id_banco}"""
        self.cursor = self.connection.cursor()

        self.cursor.execute(get_gastos_imediatos)
        total = dict(self.cursor.fetchone())['total']
        if not total:
            return 0

        return total
    
    def get_total_gastos_periodizados (self, id_banco) -> float:
        get_gastos_periodizados = f"""
        SELECT id_banco, SUM(Gastos_periodizados.valor_parcela * Gastos_periodizados.controle_parcelas) AS 'total' FROM Gastos_gerais 
        JOIN Gastos_periodizados ON Gastos_periodizados.id_gasto = Gastos_gerais.id 
        WHERE id_banco = {id_banco}"""
        self.cursor = self.connection.cursor()

        self.cursor.execute(get_gastos_periodizados)
        total = dict(self.cursor.fetchone())['total']
        if not total:
            return 0

        return total
    
    def get_total_transferencias_recebidas (self, id_banco) -> float:
        total_transferencias_recebidas = self.get_data(
            "Transferencias_entre_bancos",
            "SUM(valor) AS 'total'", 
            f"id_banco_destino = {id_banco}"
        )

        if not total_transferencias_recebidas[0]['total']:
            return 0

        return total_transferencias_recebidas[0]['total']

    def get_total_transferencias_enviadas (self, id_banco) -> float:

        total_transferencias_enviadas = self.get_data(
            "Transferencias_entre_bancos",
            "SUM(valor) AS 'total'", 
            f"id_banco_origem = {id_banco}"
        )

        if not total_transferencias_enviadas[0]['total']:
            return 0

        return total_transferencias_enviadas[0]['total']

    def get_saldo (self, id_banco) -> float:
        saldo = self.get_data("Bancos", command="saldo", WHERE=f"id = {id_banco}" )

        return saldo[0]['saldo']
    
    def get_dados_banco (self, id_banco) -> int:
        dados_banco = self.get_data("Bancos", "nome, saldo", f"id = {id_banco}")
        if not dados_banco:
            return None
        
        return dados_banco[0]
    
    def get_dados_banco_por_direcionamento (self, id_banco) -> int:
        dados_banco = self.get_data("Saldo_banco_por_direcionamento", "nome_banco, nome_direcionamento, saldo", f"id_banco = 2")
        if not dados_banco:
            return None
        
        return dados_banco

    def get_id_banco (self, nome_banco: str = "", saldo: float = 0) -> int:

        if nome_banco:
            banco = self.get_data("Bancos", "id", f"nome = '{nome_banco}'")
            if banco:
                return banco[0]['id']
            
            return False
                
        if saldo:
            banco = self.get_data("Bancos", "id", f"saldo = {saldo}")
            if banco:
                return banco[0]['id']
            
            return False
        
        return None

    def edita_nome_banco (self, id_banco, novo_nome: str) -> bool:
        self.edit_data("Bancos", f"nome = '{novo_nome}'", f"id = {id_banco}")
        historico_banco_controller = Historico_bancos_controller(self.db_name)
        historico_was_edited = historico_banco_controller.edit_data("Historico_bancos", f"nome = '{novo_nome}'", f"id_banco = {id_banco}") 
        cursor = self.connection.cursor()
        cursor.executescript("""
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
        self.connection.commit()
        cursor.executescript(
                """
    WITH total_dep AS (
    SELECT 
    s.id_banco as id_b, s.id_direcionamento as id_d,
    SUM(IFNULL(dep.valor, 0)) AS total
    FROM Saldo_direcionamento_por_banco s
    LEFT JOIN Depositos dep
        ON s.id_banco = dep.id_banco 
        AND s.id_direcionamento  = dep.id_direcionamento
    GROUP BY s.id_banco , s.id_direcionamento
    ),
    total_tbrec AS (
    SELECT 
    s.id_banco as id_b, s.id_direcionamento as id_d,
    SUM(IFNULL(t.valor, 0)) AS total
    FROM Saldo_direcionamento_por_banco s
    LEFT JOIN Transferencias_entre_bancos t
        ON t.id_banco_destino = s.id_banco 
        AND t.id_direcionamento = s.id_direcionamento
    GROUP BY s.id_banco , s.id_direcionamento
    ),
    total_tdrec AS (
    SELECT 
    s.id_banco as id_b, s.id_direcionamento as id_d,
    SUM(IFNULL(t.valor, 0)) AS total
    FROM Saldo_direcionamento_por_banco s
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
    FROM Saldo_direcionamento_por_banco s
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
    FROM Saldo_direcionamento_por_banco s
    LEFT JOIN Transferencias_entre_bancos t
        ON t.id_banco_origem = s.id_banco 
        AND t.id_direcionamento = s.id_direcionamento
    GROUP BY s.id_banco , s.id_direcionamento
    ),
    total_tdenv AS (
    SELECT 
    s.id_banco as id_b, s.id_direcionamento as id_d,
    SUM(IFNULL(t.valor, 0)) AS total
    FROM Saldo_direcionamento_por_banco s
    LEFT JOIN Transferencias_entre_direcionamentos t
        ON t.id_direcionamento_origem = s.id_direcionamento 
        AND t.id_banco = s.id_banco
    GROUP BY s.id_banco , s.id_direcionamento
    )
    UPDATE Saldo_direcionamento_por_banco AS sdpb
    SET saldo = (
    SELECT
    (total_dep.total + total_tbrec.total + total_tdrec.total)
    - (total_gastos.total + total_tbenv.total + total_tdenv.total)
    AS total
    FROM Saldo_direcionamento_por_banco s
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
    WHERE 
    s.id_banco = sdpb.id_banco
    AND s.id_direcionamento = sdpb.id_direcionamento);"""
        )
        self.connection.commit()
        cursor.close()
        return historico_was_edited        

    def edita_saldo (self, id_banco: int, novo_saldo: float) -> bool:

        if novo_saldo < 0:
            return False
        
        cursor = self.connection.cursor()
        cursor.executescript("""
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
        self.connection.commit()
        cursor.executescript(
                """
    WITH total_dep AS (
    SELECT 
    s.id_banco as id_b, s.id_direcionamento as id_d,
    SUM(IFNULL(dep.valor, 0)) AS total
    FROM Saldo_direcionamento_por_banco s
    LEFT JOIN Depositos dep
        ON s.id_banco = dep.id_banco 
        AND s.id_direcionamento  = dep.id_direcionamento
    GROUP BY s.id_banco , s.id_direcionamento
    ),
    total_tbrec AS (
    SELECT 
    s.id_banco as id_b, s.id_direcionamento as id_d,
    SUM(IFNULL(t.valor, 0)) AS total
    FROM Saldo_direcionamento_por_banco s
    LEFT JOIN Transferencias_entre_bancos t
        ON t.id_banco_destino = s.id_banco 
        AND t.id_direcionamento = s.id_direcionamento
    GROUP BY s.id_banco , s.id_direcionamento
    ),
    total_tdrec AS (
    SELECT 
    s.id_banco as id_b, s.id_direcionamento as id_d,
    SUM(IFNULL(t.valor, 0)) AS total
    FROM Saldo_direcionamento_por_banco s
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
    FROM Saldo_direcionamento_por_banco s
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
    FROM Saldo_direcionamento_por_banco s
    LEFT JOIN Transferencias_entre_bancos t
        ON t.id_banco_origem = s.id_banco 
        AND t.id_direcionamento = s.id_direcionamento
    GROUP BY s.id_banco , s.id_direcionamento
    ),
    total_tdenv AS (
    SELECT 
    s.id_banco as id_b, s.id_direcionamento as id_d,
    SUM(IFNULL(t.valor, 0)) AS total
    FROM Saldo_direcionamento_por_banco s
    LEFT JOIN Transferencias_entre_direcionamentos t
        ON t.id_direcionamento_origem = s.id_direcionamento 
        AND t.id_banco = s.id_banco
    GROUP BY s.id_banco , s.id_direcionamento
    )
    UPDATE Saldo_direcionamento_por_banco AS sdpb
    SET saldo = (
    SELECT
    (total_dep.total + total_tbrec.total + total_tdrec.total)
    - (total_gastos.total + total_tbenv.total + total_tdenv.total)
    AS total
    FROM Saldo_direcionamento_por_banco s
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
    WHERE 
    s.id_banco = sdpb.id_banco
    AND s.id_direcionamento = sdpb.id_direcionamento);"""
        )
        self.connection.commit()
        cursor.close()

        return self.edit_data("Bancos", f"saldo = {novo_saldo}", f"id = {id_banco}")

    def atualiza_saldo (self, id_banco: int) -> bool:
        if self.verifica_saldo_precisa_att(id_banco):
            historico_banco_controller = Historico_bancos_controller(self.db_name)
            historico_banco_controller.adiciona_historico_banco(id_banco)
            
            saldo_novo = self._calcula_saldo(id_banco)
            return self.edita_saldo(id_banco, saldo_novo)      
        
        return False

    def _calcula_saldo (self, id_banco: int) -> float:
        recebimentos = (
            self.get_total_depositos(id_banco) + 
            self.get_total_transferencias_recebidas(id_banco)
        )

        gastos = (
            self.get_total_gastos_imediatos(id_banco) +
            self.get_total_gastos_periodizados(id_banco) +
            self.get_total_transferencias_enviadas(id_banco)
        )

        saldo_calculado = round(recebimentos - gastos, 2)

        return saldo_calculado

    def verifica_saldo_precisa_att (self, id_banco: int) -> bool:
        
        saldo_atual = self.get_saldo(id_banco)

        saldo_calculado = self._calcula_saldo(id_banco)

        if saldo_calculado < 0:
            return False

        return saldo_atual != saldo_calculado

    def adiciona_banco(self, nome_banco: str) -> bool:

        nome_banco = nome_banco.strip()

        if self.get_id_banco(nome_banco):
            return False

        novo_banco = Banco_model(nome_banco)

        return self.insert_data("Bancos", novo_banco.dados)

    def deleta_banco (self, id_banco: int) -> bool:
        return self.delete_data("Bancos", f"id = {id_banco}")
    