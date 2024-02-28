from .models.Banco_model import Banco_model
from .Historico_bancos_controller import Historico_bancos_controller

from .DB_base_class import SQLite_DB_CRUD

class Banco_controller (SQLite_DB_CRUD):
    def __init__ (self) -> None:
        # super().__init__("Controle_Financeiro_DB")
        super().__init__("DB_teste")

    def cria_tabela_Bancos (self) -> bool:
        bancos_table_structure = {
            'name': 'Bancos',
            'columns': ( "(" +
                "id INTEGER Primary key autoincrement, " +
                "nome TEXT NOT NULL, " +
                "saldo REAL NOT NULL, " +
                "updated_at TEXT DEFAULT (strftime('%d-%m-%Y', 'now')) NOT NULL" +
                ")"
            )
        }

        return self._create_table(bancos_table_structure)
    
    def get_total_depositos (self, id_banco) -> float:
        total_depositos = self.get_data("Depositos", "SUM(valor) AS 'total'", f"id_banco = {id_banco}")

        return total_depositos[0]['total']

    def get_total_gastos_imediatos (self, id_banco) -> float:
        get_gastos_imediatos = f"""
        SELECT id_banco, SUM(Gastos_geral.valor) AS 'total' FROM Gastos_geral 
        JOIN Gastos_imediatos ON Gastos_imediatos.id_gasto = Gastos_geral.id 
        WHERE id_banco = {id_banco}"""

        self.cursor.executescript(get_gastos_imediatos)
        return self.cursor.fetchone()['total']
    
    def get_total_gastos_periodizados (self, id_banco) -> float:
        get_gastos_periodizados = f"""
        SELECT id_banco, SUM(Gastos_periodizados.valor_total) AS 'total' FROM Gastos_geral 
        JOIN Gastos_periodizados ON Gastos_imediatos.id_gasto = Gastos_geral.id 
        WHERE id_banco = {id_banco}"""

        self.cursor.executescript(get_gastos_periodizados)
        return self.cursor.fetchone()['total']
    
    def get_total_transferencias_recebidas (self, id_banco) -> float:
        total_transferencias_recebidas = self.get_data(
            "Transferencias_entre_bancos",
            "SUM(valor) AS 'total'", 
            f"id_banco_destino = {id_banco}"
        )

        return total_transferencias_recebidas[0]['total']

    def get_total_transferencias_enviadas (self, id_banco) -> float:

        total_transferencias_enviadas = self.get_data(
            "Transferencias_entre_bancos",
            "SUM(valor) AS 'total'", 
            f"id_banco_origem = {id_banco}"
        )

        return total_transferencias_enviadas[0]['total']

    def get_saldo (self, id_banco) -> float:
        saldo = self.get_data("Bancos", command="saldo", WHERE=f"id = {id_banco}" )

        return saldo[0]['saldo']

    def atualiza_saldo (self, id_banco: int, novo_saldo: float) -> bool:
        if self.verifica_saldo_precisa_att(id_banco):
            Historico_bancos_controller().adiciona_historico_banco(id_banco)
            return self.edit_data("Bancos", f"saldo = {novo_saldo}", f"id = {id_banco}")
        
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

        return saldo_atual != saldo_calculado

    def adiciona_banco(self, nome_banco: str) -> bool:

        novo_banco = Banco_model(nome_banco)

        return self.insert_data("Bancos", novo_banco.dados)

    