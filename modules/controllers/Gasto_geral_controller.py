from ..models.Gasto_geral_model import Gasto_geral_model
from ..models.Gasto_imediato_model import Gasto_imediato_model
from .DB_base_class import SQLite_DB_CRUD

class Gasto_geral_controller (SQLite_DB_CRUD):

    def __init__ (self) -> None:
        # super().__init__("Controle_Financeiro_DB")
        super().__init__("DB_teste")

    def adiciona_gasto_geral (self, 
                              id_banco: int, id_direcionamento: int,
                              valor: float, tipo_gasto: str= "imediato", descricao: str="") -> bool:

        """
        Sempre que um gasto for inserido, ele automaticamente irá inserir um
        gasto na tabela de gastos imediatos ou periodizados, de acordo com seu
        tipo de gasto.
        """

        if not descricao:
            descricao = f"Gasto {self.cursor.lastrowid}"

        descricao += f" {self.cursor.lastrowid}"
        

        gasto_geral = Gasto_geral_model(
            id_banco, id_direcionamento,
            tipo_gasto, valor, descricao
        )            

        data_was_insert = self.insert_data(
            "Gastos_gerais",
            gasto_geral.dados
        )

        if data_was_insert and tipo_gasto == "imediato":
            gasto_imediato = Gasto_imediato_model(
                self.cursor.lastrowid,
                valor,
                descricao
            )

            self.insert_data(
                "Gastos_imediatos",
                gasto_imediato.dados
            )

            return True

        return False
    
    def get_gasto_geral_id (self, descricao: str) -> int:
        return self.get_data(
            "Gastos_gerais",
            "id",
            f"descricao = {descricao}"
        )
    
    def get_tipo_gasto (self, id_gasto: int) -> str:

        descricao = self.get_data("Gastos_gerais", "descricao", f"id = {id_gasto}")[0]['descricao']

        return descricao

    def deleta_gasto_geral (self, id_gasto: int) -> bool:
        return self.delete_data("Gastos_gerais", f"id = {id_gasto}")

    def edita_gasto_geral (self,
                           id_gasto: int, novo_valor: float = 0,
                           nova_descricao: str = "", novo_id_banco: int = 0,
                           novo_id_direcionamento: int = 0) -> bool:
        
        novos_dados = {
            'valor': novo_valor,
            'descricao': nova_descricao,
            'id_banco': novo_id_banco,
            'id_direcionamento': novo_id_direcionamento
        }

        tipo_gasto = self.get_tipo_gasto(id_gasto)

        if tipo_gasto == "periodizado":
            print(
                "Não pode editar gasto periodizado através de Gastos_gerais, "
                + "utilize a função de Gastos_periodizados"
            )
            return False

        edit_command = ""

        for key, value in novos_dados.items():
            if value:
                edit_command += f"{key} = {value}, "

        edit_command = edit_command[:-2]

        if self.edit_data("Gastos_geral", edit_command, f"id = {id_gasto}") and tipo_gasto == "imediato":
            if not novo_id_banco and not novo_id_direcionamento:
                self.edit_data("Gastos_imediatos", edit_command, f"id_gasto = {id_gasto}")
            return True
        
        return False
        
            
            

        

        
