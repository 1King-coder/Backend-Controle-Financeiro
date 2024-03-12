from .DB_base_class import SQLite_DB_CRUD
from ..models.Transferencia_entre_direcionamentos_model import Transferencia_entre_direcionamentos_model
from pandas import DataFrame

class Transferencia_entre_direcionamentos_controller (SQLite_DB_CRUD):

    def __init__ (self, db_name: str) -> None:
        super().__init__(db_name)

    def mostrar (self) -> list:
        return self.get_data(
            "Transferencias_entre_direcionamentos"
        )
    
    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def get_id (self, descricao: str) -> int:
        return self.get_data(
            "Transferencias_entre_direcionamentos",
            "id",
            f"descricao = {descricao}"
        )
    
    def get_dados (self, id_transf: int) -> dict:
        dados = self.get_data(
            "Transferencias_entre_direcionamentos",
            "*",
            f"id = {id_transf}"
        )

        if not dados:
            return None
        
        return dados[0]

    def adicionar (self, id_direcionamento_origem: int, id_direcionamento_destino: int, id_banco: int,valor: float, descricao: str = "") -> bool:

        if not descricao:
            descricao = f"Transferência {self.cursor.lastrowid}"

        transf_entre_direcionamentos_model = Transferencia_entre_direcionamentos_model(
            id_direcionamento_origem, id_direcionamento_destino, id_banco,
            valor, descricao
        )

        return self.insert_data(
            "Transferencias_entre_direcionamentos",
            transf_entre_direcionamentos_model.dados
        )

    def editar (self, id_transf: int, novo_id_direcionamento_origem: int = 0,
                novo_id_direcionamento_destino: int = 0, novo_id_banco: int = 0,
                novo_valor: float = 0, nova_descricao: str = "") -> bool:     
        
        novos_dados = {
            'valor': novo_valor,
            'descricao': nova_descricao,
            'id_banco': novo_id_banco,
            'id_direcionamento_destino': novo_id_direcionamento_destino,
            'id_direcionamento_origem': novo_id_direcionamento_origem
        }

        edit_command = ""

        for key, value in novos_dados.items():
            if value:
                edit_command += f"{key} = {value}, "

        edit_command = edit_command[:-2]

        return self.edit_data("Transferencias_entre_direcionamentos", edit_command, f"id = {id_transf}")
    
    def deletar (self, id_transf: int) -> bool:
        return self.delete_data("Transferencias_entre_direcionamentos", f"id = {id_transf}")