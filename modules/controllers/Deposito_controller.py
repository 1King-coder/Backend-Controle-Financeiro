from ..models.Deposito_model import Deposito_model
from .DB_base_class import SQLite_DB_CRUD
from pandas import DataFrame


class Deposito_controller (SQLite_DB_CRUD):

    def __init__ (self) -> None:
        # super().__init__("Controle_Financeiro_DB")
        super().__init__("DB_teste")

    def mostrar (self) -> list:
        return self.get_data(
            "Depositos"
        )
    
    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def adiciona_deposito (self, 
                              id_banco: int, id_direcionamento: int,
                              valor: float, descricao: str="") -> bool:

        """
        Sempre que um gasto for inserido, ele automaticamente irá inserir um
        gasto na tabela de gastos imediatos ou periodizados, de acordo com seu
        tipo de gasto.
        """

        if not descricao:
            descricao = f"Deposito {self.cursor.lastrowid}"

        deposito = Deposito_model(
            id_banco, id_direcionamento,
            valor, descricao
        )                

        return self.insert_data(
            "Depositos",
            deposito.dados
        )
    
    def get_deposito_id (self, descricao: str) -> int:
        return self.get_data(
            "Depositos",
            "id",
            f"descricao = {descricao}"
        )
    
    def deleta_deposito (self, id_deposito: int) -> bool:
        return self.delete_data("Depositos", f"id = {id_deposito}")

    def edita_deposito (self,
                           id_deposito: int, novo_valor: float = 0,
                           nova_descricao: str = "", novo_id_banco: int = 0,
                           novo_id_direcionamento: int = 0) -> bool:
        
        novos_dados = {
            'valor': novo_valor,
            'descricao': nova_descricao,
            'id_banco': novo_id_banco,
            'id_direcionamento': novo_id_direcionamento
        }

        edit_command = ""

        for key, value in novos_dados.items():
            if value:
                edit_command += f"{key} = {value}, "

        edit_command = edit_command[:-2]

        if self.edit_data("Deposito", edit_command, f"id = {id_deposito}"):
            if not novo_id_banco and not novo_id_direcionamento:
                self.edit_data("Depositos", edit_command, f"id_deposito = {id_deposito}")
            return True
        
        return False
