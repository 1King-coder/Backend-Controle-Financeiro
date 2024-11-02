from ..models.Direcionamento_model import Direcionamento_model
from .Historico_direcionamentos_controller import Historico_direcionamentos_controller
from pandas import DataFrame


from .DB_base_class import SQLite_DB_CRUD

class Direcionamento_controller (SQLite_DB_CRUD):

    def __init__ (self, db_name: str) -> None:
        super().__init__(db_name)

        
    def mostrar (self) -> list:
        return self.get_data(
            "Direcionamentos"
        )
    
    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def get_total_depositos (self, id_direcionamento) -> float:
        total_depositos = self.get_data("Depositos", "SUM(valor) AS 'total'", f"id_direcionamento = {id_direcionamento}")
        if not total_depositos:
            return 0
        
        if not total_depositos[0].get('total'):
            return 0
        
        return total_depositos[0]['total']

    def get_total_gastos_imediatos (self, id_direcionamento) -> float:
        get_gastos_imediatos = f"""
        SELECT id_direcionamento, SUM(Gastos_gerais.valor) AS 'total' FROM Gastos_gerais 
        JOIN Gastos_imediatos ON Gastos_imediatos.id_gasto = Gastos_gerais.id 
        WHERE id_direcionamento = {id_direcionamento}"""
        self.cursor = self.connection.cursor()

        self.cursor.execute(get_gastos_imediatos)
        total = dict(self.cursor.fetchone())['total']
        if not total:
            return 0

        return total
        
    
    def get_total_gastos_periodizados (self, id_direcionamento) -> float:
        get_gastos_periodizados = f"""
        SELECT id_direcionamento, SUM(Gastos_periodizados.valor_parcela * Gastos_periodizados.controle_parcelas) AS 'total' FROM Gastos_gerais 
        JOIN Gastos_periodizados ON Gastos_periodizados.id_gasto = Gastos_gerais.id 
        WHERE id_direcionamento = {id_direcionamento}"""
        self.cursor = self.connection.cursor()


        self.cursor.execute(get_gastos_periodizados)

        total = dict(self.cursor.fetchone())['total']
        if not total:
            return 0

        return total

    def get_total_transferencias_recebidas (self, id_direcionamento) -> float:
        total_transferencias_recebidas = self.get_data(
            "Transferencias_entre_direcionamentos",
            "SUM(valor) AS 'total'", 
            f"id_direcionamento_destino = {id_direcionamento}"
        )

        if not total_transferencias_recebidas[0]['total']:
            return 0

        return total_transferencias_recebidas[0]['total']

    def get_total_transferencias_enviadas (self, id_direcionamento) -> float:

        total_transferencias_enviadas = self.get_data(
            "Transferencias_entre_direcionamentos",
            "SUM(valor) AS 'total'", 
            f"id_direcionamento_origem = {id_direcionamento}"
        )

        if not total_transferencias_enviadas[0]['total']:
            return 0

        return total_transferencias_enviadas[0]['total']

    def get_saldo (self, id_direcionamento) -> float:
        saldo = self.get_data("direcionamentos", command="saldo", WHERE=f"id = {id_direcionamento}" )

        return saldo[0]['saldo']

    def editar (self, id_direcionamento: int, novo_saldo: float) -> bool:
        if novo_saldo < 0:
            return False

        return self.edit_data("Direcionamentos", f"saldo = {novo_saldo}", f"id = {id_direcionamento}")

    def atualizar (self, id_direcionamento: int) -> bool:
        if self.verifica_saldo_precisa_att(id_direcionamento):
            historico_dir_controller = Historico_direcionamentos_controller(self.db_name)
            historico_dir_controller.adiciona_historico_direcionamento(id_direcionamento)
            saldo_novo = self._calcula_saldo(id_direcionamento)
            cursor = self.connection.cursor()

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
            cursor.close()
            return self.editar(id_direcionamento, saldo_novo)
        
        return False
    
    def get_dados_direcionamento (self, id_direcionamento: int):
        dados_direcionamento = self.get_data("Direcionamentos", "nome, saldo", f"id = {id_direcionamento}")

        if not dados_direcionamento:
            return None
        
        return dados_direcionamento[0]
    
    def get_dados_direcionamento_por_banco (self, id_direcionamento: int):
        dados_direcionamento = self.get_data("Saldo_direcionamento_por_banco", "nome_direcionamento, nome_banco, saldo", f"id_direcionamento = {id_direcionamento}")

        if not dados_direcionamento:
            return None
        
        return dados_direcionamento
 
    def get_id_direcionamento (self, nome_direcionamento: str = "", saldo: float = 0) -> int:

        if nome_direcionamento:
            direcionamento = self.get_data("Direcionamentos", "id", f"nome = '{nome_direcionamento}'")
            if direcionamento:
                return direcionamento[0]['id']
            
            return None
        
        if saldo:
            direcionamento = self.get_data("Direcionamentos", "id", f"saldo = {saldo}")
            if direcionamento:
                return direcionamento[0]['id']
            
            return None
        
        return None

    def edita_nome_direcionamentos (self, id_direcionamento: int, novo_nome: str) -> bool:
        self.edit_data("Direcionamentos", f"nome = '{novo_nome}'", f"id = {id_direcionamento}")
        historico_direcionamento_controller = Historico_direcionamentos_controller(self.db_name)
        historico_was_edited = historico_direcionamento_controller.edit_data("Historico_direcionamentos", f"nome = '{novo_nome}'", f"id_direcionamento = {id_direcionamento}") 
        return historico_was_edited
    

    def _calcula_saldo (self, id_direcionamento: int) -> float:
        recebimentos = (
            self.get_total_depositos(id_direcionamento) + 
            self.get_total_transferencias_recebidas(id_direcionamento)
        )

        gastos = (
            self.get_total_gastos_imediatos(id_direcionamento) +
            self.get_total_gastos_periodizados(id_direcionamento) +
            self.get_total_transferencias_enviadas(id_direcionamento)
        )

        saldo_calculado = round(recebimentos - gastos, 2)

        return saldo_calculado

    def verifica_saldo_precisa_att (self, id_direcionamento: int) -> bool:
        
        saldo_atual = self.get_saldo(id_direcionamento)
        saldo_calculado = self._calcula_saldo(id_direcionamento)

        if saldo_calculado < 0:
            return False

        return saldo_atual != saldo_calculado

    def adiciona_direcionamento(self, nome_direcionamento: str) -> bool:
        nome_direcionamento = nome_direcionamento.strip()

        if self.get_id_direcionamento(nome_direcionamento):
            return False
        
        novo_direcionamento = Direcionamento_model(nome_direcionamento)


        return self.insert_data("Direcionamentos", novo_direcionamento.dados)
    
    def deleta_direcionamento (self, id_direcionamento: int) -> bool:
        return self.delete_data("Direcionamentos", f"id = {id_direcionamento}")
    