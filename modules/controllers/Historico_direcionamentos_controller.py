from ..models.Historico_direcionamentos_model import Historico_direcionamentos_model
from pandas import DataFrame

from .DB_base_class import SQLite_DB_CRUD

class Historico_direcionamentos_controller (SQLite_DB_CRUD):
    def __init__ (self, db_name: str) -> None:
        super().__init__(db_name)

    def mostrar (self) -> list:
        return self.get_data(
            "Historico_direcionamentos"
        )
    
    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def get_dados_direcionamento (self, id_direcionamento) -> int:
        dados_direcionamento = self.get_data("Direcionamentos", "nome, saldo", f"id = {id_direcionamento}")
        return dados_direcionamento[0]

    def adiciona_historico_direcionamento (self, id_direcionamento: str) -> bool:

        dados_direcionamento = self.get_dados_direcionamento(id_direcionamento)

        novo_direcionamento = Historico_direcionamentos_model(id_direcionamento, dados_direcionamento['nome'], dados_direcionamento['saldo'])

        return self.insert_data("Historico_direcionamentos", novo_direcionamento.dados)
    


    