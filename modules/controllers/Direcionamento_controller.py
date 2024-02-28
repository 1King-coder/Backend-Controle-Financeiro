from .models.Direcionamento_model import Direcionamento_model
from .Historico_direcionamentos_controller import Historico_direcionamentos_controller

from .DB_base_class import SQLite_DB_CRUD

class Direcionamento_controller (SQLite_DB_CRUD):

    def __init__ (self) -> None:
        # super().__init__("Controle_Financeiro_DB")
        super().__init__("DB_teste")

    def get_total_depositos (self, id_direcionamento) -> float:
        total_depositos = self.get_data("Depositos", "SUM(valor) AS 'total'", f"id_direcionamento = {id_direcionamento}")

        return total_depositos[0]['total']

    def get_total_gastos_imediatos (self, id_direcionamento) -> float:
        get_gastos_imediatos = f"""
        SELECT id_direcionamento, SUM(Gastos_geral.valor) AS 'total' FROM Gastos_geral 
        JOIN Gastos_imediatos ON Gastos_imediatos.id_gasto = Gastos_geral.id 
        WHERE id_direcionamento = {id_direcionamento}"""

        self.cursor.executescript(get_gastos_imediatos)
        return self.cursor.fetchone()['total']
    
    def get_total_gastos_periodizados (self, id_direcionamento) -> float:
        get_gastos_periodizados = f"""
        SELECT id_direcionamento, SUM(Gastos_periodizados.valor_total) AS 'total' FROM Gastos_geral 
        JOIN Gastos_periodizados ON Gastos_imediatos.id_gasto = Gastos_geral.id 
        WHERE id_direcionamento = {id_direcionamento}"""

        self.cursor.executescript(get_gastos_periodizados)
        return self.cursor.fetchone()['total']
    
    def get_total_transferencias_recebidas (self, id_direcionamento) -> float:
        total_transferencias_recebidas = self.get_data(
            "Transferencias_entre_bancos",
            "SUM(valor) AS 'total'", 
            f"id_direcionamento_destino = {id_direcionamento}"
        )

        return total_transferencias_recebidas[0]['total']

    def get_total_transferencias_enviadas (self, id_direcionamento) -> float:

        total_transferencias_enviadas = self.get_data(
            "Transferencias_entre_bancos",
            "SUM(valor) AS 'total'", 
            f"id_direcionamento_origem = {id_direcionamento}"
        )

        return total_transferencias_enviadas[0]['total']

    def get_saldo (self, id_direcionamento) -> float:
        saldo = self.get_data("Bancos", command="saldo", WHERE=f"id = {id_direcionamento}" )

        return saldo[0]['saldo']

    def atualiza_saldo (self, id_direcionamento: int, novo_saldo: float) -> bool:
        if self.verifica_saldo_precisa_att(id_direcionamento):
            Historico_direcionamentos_controller().adiciona_historico_direcionamento(id_direcionamento)
            return self.edit_data("Direcionamentos", f"saldo = {novo_saldo}", f"id = {id_direcionamento}")
        
        return False

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

        return saldo_atual != saldo_calculado

    def adiciona_direcionamento(self, nome_direcionamento: str) -> bool:

        novo_direcionamento = Direcionamento_model(nome_direcionamento)

        return self.insert_data("Direcionamento", novo_direcionamento.dados)