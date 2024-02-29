from ..models.Direcionamento_model import Direcionamento_model
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
        SELECT id_direcionamento, SUM(Gastos_gerais.valor) AS 'total' FROM Gastos_gerais 
        JOIN Gastos_imediatos ON Gastos_imediatos.id_gasto = Gastos_gerais.id 
        WHERE id_direcionamento = {id_direcionamento}"""

        self.cursor.execute(get_gastos_imediatos)
        
        return dict(self.cursor.fetchone())['total']
    
    def get_total_gastos_periodizados (self, id_direcionamento) -> float:
        get_gastos_periodizados = f"""
        SELECT id_direcionamento, SUM(Gastos_periodizados.valor_parcela * Gastos_periodizados.controle_parcelas) AS 'total' FROM Gastos_gerais 
        JOIN Gastos_periodizados ON Gastos_periodizados.id_gasto = Gastos_gerais.id 
        WHERE id_direcionamento = {id_direcionamento}"""

        self.cursor.execute(get_gastos_periodizados)
    
        return dict(self.cursor.fetchone())['total']
    
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

    def edita_saldo (self, id_direcionamento: int, novo_saldo: float) -> bool:

        return self.edit_data("Direcionamentos", f"saldo = {novo_saldo}", f"id = {id_direcionamento}")

    def atualiza_saldo (self, id_direcionamento: int) -> bool:
        if self.verifica_saldo_precisa_att(id_direcionamento):
            historico_dir_controller = Historico_direcionamentos_controller()
            historico_dir_controller.init_connection()
            historico_dir_controller.adiciona_historico_direcionamento(id_direcionamento)
            historico_dir_controller.close_connection()
            saldo_novo = self._calcula_saldo(id_direcionamento)
            return self.edita_saldo(id_direcionamento, saldo_novo)
        
        return False
 
    def get_id_direcionamento (self, nome_direcionamento: str = "", saldo: float = 0) -> int:

        if nome_direcionamento:
            return self.get_data("Direcionamentos", "id", f"nome = {nome_direcionamento}")[0]['id']
        
        if saldo:
            return self.get_data("Direcionamentos", "id", f"saldo = {saldo}")[0]['id']
        
        return None

    def edita_nome_direcionamentos (self, id_direcionamento: int, novo_nome: str) -> bool:
        self.edit_data("Direcionamentos", f"nome = {novo_nome}", f"id = {id_direcionamento}")
        historico_direcionamento_controller = Historico_direcionamentos_controller()
        historico_direcionamento_controller.init_connection()
        historico_was_edited = historico_direcionamento_controller.edit_data("Historico_direcionamentos", f"nome = {novo_nome}", f"id_direcionamento = {id_direcionamento}") 
        historico_direcionamento_controller.close_connection()
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

        return saldo_atual != saldo_calculado

    def adiciona_direcionamento(self, nome_direcionamento: str) -> bool:

        novo_direcionamento = Direcionamento_model(nome_direcionamento)

        return self.insert_data("Direcionamentos", novo_direcionamento.dados)
    
    def deleta_direcionamento (self, id_direcionamento: int) -> bool:
        return self.delete_data("Direcionamentos", f"id = {id_direcionamento}")
    