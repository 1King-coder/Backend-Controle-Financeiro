from .DB_base_class import SQLite_DB_CRUD
from ..models.Transferencia_entre_bancos_model import Transferencia_entre_bancos_model
from pandas import DataFrame

class Transferencia_entre_bancos_controller (SQLite_DB_CRUD):

    def __init__ (self, db_name: str) -> None:
        super().__init__(db_name)

    def mostrar (self) -> list:
        return self.get_data(
            "Transferencias_entre_bancos"
        )

    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def get_id (self, descricao: str) -> int:
        return self.get_data(
            "Transferencias_entre_bancos",
            "id",
            f"descricao = {descricao}"
        )
    
    def get_dados (self, id_transf: int) -> dict:
        dados = self.get_data(
            "Transferencias_entre_bancos",
            "*",
            f"id = {id_transf}"
        )

        if not dados:
            return None
        
        return dados[0]

    def adicionar (self, id_banco_origem: int, id_banco_destino: int,
                   id_direcionamento: int, valor: float, descricao: str = "") -> bool:

        if valor < 0:
            return False

        if not descricao:
            descricao = f"Transferência {self.cursor.lastrowid}"

        transf_entre_bancos_model = Transferencia_entre_bancos_model(
            id_banco_origem, id_banco_destino, id_direcionamento,
            valor, descricao
        )

        return self.insert_data(
            "Transferencias_entre_bancos",
            transf_entre_bancos_model.dados
        )

    def editar (self, id_transf: int, novo_id_banco_origem: int = 0,
                novo_id_banco_destino: int = 0, novo_valor: float = 0,
                novo_id_direcionamento: int = 0, nova_descricao: str = "") -> bool:     
        
        novos_dados = {
            'valor': novo_valor,
            'descricao': nova_descricao,
            'id_direcionamento': novo_id_direcionamento,
            'id_banco_destino': novo_id_banco_destino,
            'id_banco_origem': novo_id_banco_origem
        }

        if novo_valor < 0:
            return False

        edit_command = ""

        for key, value in novos_dados.items():
            if value:
                edit_command += f"{key} = {value}, "

        edit_command = edit_command[:-2]

        return self.edit_data("Transferencias_entre_bancos", edit_command, f"id = {id_transf}")
    
    def deletar (self, id_transf: int) -> bool:
        return self.delete_data("Transferencias_entre_bancos", f"id = {id_transf}")