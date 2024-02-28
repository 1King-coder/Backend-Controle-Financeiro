from .models.Gasto_geral_model import Gasto_geral_model
from .models.Gasto_imediato_model import Gasto_imediato_model
from .models.Gasto_periodizado_model import Gasto_periodizado_model
from .DB_base_class import SQLite_DB_CRUD

class Gasto_geral_controller (SQLite_DB_CRUD):

    def __init__ (self) -> None:
        super().__init__("Gastos_gerais")

    def adiciona_gasto_geral (self, 
                              id_banco: int, id_direcionamento: int,
                              tipo_gasto: str, descricao: str, valor: float,
                              dados_gasto_periodizado: dict) -> bool:

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
        
        if data_was_insert and tipo_gasto == "periodizado":
            gasto_periodizado = Gasto_periodizado_model(
                self.cursor.lastrowid,
                valor,
                dados_gasto_periodizado["total_parcelas"],
                dados_gasto_periodizado["controle_parcelas"],
                dados_gasto_periodizado["dia_abate"],
                descricao
            )

            self.insert_data(
                "Gastos_periodizados",
                gasto_periodizado.dados
            )

            return True

        return False
    
    def get_gasto_geral_id (self, descricao: str) -> int:
        return self.get_data(
            "Gastos_gerais",
            "id",
            f"descricao = {descricao}"
        )

    def deleta_gasto_geral (self, id_gasto: int) -> bool:
        return self.delete_data("Gastos_gerais", f"id = {id_gasto}")
    
    def edita_gasto_geral (self): ...