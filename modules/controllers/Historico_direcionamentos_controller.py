from .models.Historico_bancos_model import Historico_direcionamentos_model

from .DB_base_class import SQLite_DB_CRUD

class Historico_direcionamentos_controller (SQLite_DB_CRUD):
    def __init__ (self) -> None:
        # super().__init__("Controle_Financeiro_DB")
        super().__init__("DB_teste")

    def get_saldo_direcionamento (self, id_direcionamento) -> int:
        dados_direcionamento = self.get_data("Direcionamentos", "saldo", f"id = {id_direcionamento}")

        return dados_direcionamento[0]

    def adiciona_historico_direcionamento (self, id_direcionamento: str) -> bool:

        dados_direcionamento = self.get_dados_direcionamentos(id_direcionamento)

        novo_direcionamento = Historico_direcionamentos_model(id_direcionamento, dados_direcionamento['saldo'])

        return self.insert_data("Historico_direcionamentos", novo_direcionamento.dados)
    


    