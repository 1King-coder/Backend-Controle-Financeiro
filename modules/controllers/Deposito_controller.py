from ..models.Deposito_model import Deposito_model
from .DB_base_class import SQLite_DB_CRUD
from pandas import DataFrame


class Deposito_controller (SQLite_DB_CRUD):

    def __init__ (self, db_name: str) -> None:
        super().__init__(db_name)

    def mostrar (self) -> list:
        return self.get_data(
            "Depositos"
        )
    
    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def adicionar (self, 
                              id_banco: int, id_direcionamento: int,
                              valor: float, descricao: str="Deposito") -> bool:

        """
        Sempre que um gasto for inserido, ele automaticamente irá inserir um
        gasto na tabela de gastos imediatos ou periodizados, de acordo com seu
        tipo de gasto.
        """

        descricao += f" {self.cursor.lastrowid}"

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
    
    def deletar (self, id_deposito: int) -> bool:
        return self.delete_data("Depositos", f"id = {id_deposito}")

    def editar (self,
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
                if key == "descricao":
                    edit_command += f"{key} = {value} {self.cursor.lastrowid}, "
                    continue

                edit_command += f"{key} = {value}, "

        edit_command = edit_command[:-2]

        if self.edit_data("Deposito", edit_command, f"id = {id_deposito}"):
            if not novo_id_banco and not novo_id_direcionamento:
                self.edit_data("Depositos", edit_command, f"id_deposito = {id_deposito}")
            return True
        
        return False
