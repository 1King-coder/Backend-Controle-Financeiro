from ..models.Historico_bancos_model import Historico_bancos_model
from pandas import DataFrame

from .DB_base_class import SQLite_DB_CRUD

class Historico_bancos_controller (SQLite_DB_CRUD):
    def __init__ (self, db_name: str) -> None:
        super().__init__(db_name)

    def mostrar (self) -> list:
        return self.get_data(
            "Historico_bancos"
        )
    
    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def get_dados_banco (self, id_banco) -> int:
        dados_banco = self.get_data("Bancos", "nome, saldo", f"id = {id_banco}")

        return dados_banco[0]

    def adiciona_historico_banco (self, id_banco: str) -> bool:

        dados_banco = self.get_dados_banco(id_banco)

        novo_banco = Historico_bancos_model(id_banco, dados_banco['nome'], dados_banco['saldo'])

        return self.insert_data("Historico_bancos", novo_banco.dados)
    


    