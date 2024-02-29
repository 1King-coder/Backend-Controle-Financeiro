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
        return total_depositos[0]['total']

    def get_total_gastos_imediatos (self, id_banco) -> float:
        get_gastos_imediatos = f"""
        SELECT id_banco, SUM(Gastos_gerais.valor) AS 'total' FROM Gastos_gerais 
        JOIN Gastos_imediatos ON Gastos_imediatos.id_gasto = Gastos_gerais.id 
        WHERE id_banco = {id_banco}"""

        self.cursor.execute(get_gastos_imediatos)
        return dict(self.cursor.fetchone())['total']
    
    def get_total_gastos_periodizados (self, id_banco) -> float:
        get_gastos_periodizados = f"""
        SELECT id_banco, SUM(Gastos_periodizados.valor_parcela * Gastos_periodizados.controle_parcelas) AS 'total' FROM Gastos_gerais 
        JOIN Gastos_periodizados ON Gastos_periodizados.id_gasto = Gastos_gerais.id 
        WHERE id_banco = {id_banco}"""

        self.cursor.execute(get_gastos_periodizados)
        return dict(self.cursor.fetchone())['total']
    
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

    def get_id_banco (self, nome_banco: str = "", saldo: float = 0) -> int:

        if nome_banco:
            return self.get_data("Bancos", "id", f"nome = {nome_banco}")[0]['id']
        
        if saldo:
            return self.get_data("Bancos", "id", f"saldo = {saldo}")[0]['id']
        
        return None

    def edita_nome_banco (self, id_banco, novo_nome: str) -> bool:
        self.edit_data("Bancos", f"nome = {novo_nome}", f"id = {id_banco}")
        historico_banco_controller = Historico_bancos_controller()
        historico_banco_controller.init_connection()
        historico_was_edited = historico_banco_controller.edit_data("Historico_bancos", f"nome = {novo_nome}", f"id_banco = {id_banco}") 
        historico_banco_controller.close_connection()
        return historico_was_edited        

    def edita_saldo (self, id_banco: int, novo_saldo: float) -> bool:

        return self.edit_data("Bancos", f"saldo = {novo_saldo}", f"id = {id_banco}")

    def atualiza_saldo (self, id_banco: int) -> bool:
        if self.verifica_saldo_precisa_att(id_banco):
            historico_banco_controller = Historico_bancos_controller()
            historico_banco_controller.init_connection()
            historico_banco_controller.adiciona_historico_banco(id_banco)
            historico_banco_controller.close_connection()
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

        return saldo_atual != saldo_calculado

    def adiciona_banco(self, nome_banco: str) -> bool:

        novo_banco = Banco_model(nome_banco)

        return self.insert_data("Bancos", novo_banco.dados)

    def deleta_banco (self, id_banco: int) -> bool:
        return self.delete_data("Bancos", f"id = {id_banco}")
    