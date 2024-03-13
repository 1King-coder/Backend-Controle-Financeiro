from ..models.Gasto_geral_model import Gasto_geral_model
from ..models.Gasto_imediato_model import Gasto_imediato_model
from .Banco_controller import Banco_controller
from .Direcionamento_controller import Direcionamento_controller
from .DB_base_class import SQLite_DB_CRUD
from pandas import DataFrame


class Gasto_geral_controller (SQLite_DB_CRUD):

    def __init__ (self, db_name: str) -> None:
        super().__init__(db_name)

        self.banco_c = Banco_controller(self.db_name)
        self.direc_C = Direcionamento_controller(self.db_name)

    def mostrar (self) -> list:
        return self.get_data(
            "Gastos_gerais"
        )

    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def adicionar (self, 
                              id_banco: int, id_direcionamento: int,
                              valor: float, tipo_gasto: str= "imediato", descricao: str="Gasto") -> bool:

        """
        Sempre que um gasto for inserido, ele automaticamente irá inserir um
        gasto na tabela de gastos imediatos ou periodizados, de acordo com seu
        tipo de gasto.
        """

        if valor < 0:
            return False
        
        saldo_banco = self.banco_c.get_saldo(id_banco)
        saldo_direc = self.direc_C.get_saldo(id_direcionamento)

        if saldo_banco < valor:
            return False
        
        if saldo_direc < valor:
            return False

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
    
    def get_dados (self, id_gasto: int) -> dict:

        dados_gasto = self.get_data("Gastos_gerais", "*", WHERE=f"id = {id_gasto}")

        if not dados_gasto:
            return None
        
        return dados_gasto[0]
        
    
    def get_id (self, descricao: str) -> int:
        return self.get_data(
            "Gastos_gerais",
            "id",
            f"descricao = {descricao}"
        )
    
    def get_tipo_gasto (self, id_gasto: int) -> str:

        tipo_gasto = self.get_data("Gastos_gerais", "tipo_gasto", f"id = {id_gasto}")

        if tipo_gasto:
            return tipo_gasto[0]['tipo_gasto']

        return None

    def deletar (self, id_gasto: int) -> bool:
        return self.delete_data("Gastos_gerais", f"id = {id_gasto}")

    def editar (self,
                           id_gasto: int, novo_valor: float = 0,
                           nova_descricao: str = "", novo_id_banco: int = 0,
                           novo_id_direcionamento: int = 0) -> bool:
        
        
        if novo_valor < 0:
            return False
        
        saldo_banco = self.banco_c.get_saldo(novo_id_banco)
        saldo_direc = self.direc_C.get_saldo(novo_id_direcionamento)

        if saldo_banco < novo_valor:
            return False
        
        if saldo_direc < novo_valor:
            return False

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

        if self.edit_data("Gastos_gerais", edit_command, f"id = {id_gasto}") and tipo_gasto == "imediato":
            if not novo_id_banco and not novo_id_direcionamento:
                self.edit_data("Gastos_imediatos", edit_command, f"id_gasto = {id_gasto}")
            return True
        
        return False
        
            
            

        

        
