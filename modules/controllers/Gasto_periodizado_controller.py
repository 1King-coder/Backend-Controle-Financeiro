
from ..models.Gasto_geral_model import Gasto_geral_model
from ..models.Gasto_periodizado_model import Gasto_periodizado_model
from .DB_base_class import SQLite_DB_CRUD
from pandas import DataFrame

from datetime import datetime

class Gasto_periodizado_controller (SQLite_DB_CRUD):

    def __init__ (self) -> None:
        # super().__init__("Controle_Financeiro_DB")
        super().__init__("DB_teste")

    def mostrar (self) -> list:
        return self.get_data(
            "Gastos_periodizados"
        )
    
    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def get_dados_gasto_periodizado (self, id_gasto: int, dados_desejados: str = "*") -> dict:

        dados_gasto = self.get_data("Gastos_periodizados", dados_desejados.strip(), f"id_gasto = {id_gasto}")
        if "," in dados_desejados:
            return dados_gasto[0]

        return dados_gasto[0][dados_desejados.strip()]
    
    def adiciona_gasto_periodizado (self, id_banco:int,
                                    id_direcionamento: int, valor_parcela: float, 
                                    total_parcelas: int, controle_parcelas: int = 0,
                                    descricao: str = "", dia_abate: str = "") -> bool:

        gasto_geral_model = Gasto_geral_model(
            id_banco, id_direcionamento, "periodizado",
            valor_parcela, descricao
        )

        if self.insert_data("Gastos_gerais", gasto_geral_model.dados):

            gasto_periodizado_model = Gasto_periodizado_model(
                self.cursor.lastrowid,
                valor_parcela, total_parcelas, 
                controle_parcelas, dia_abate, descricao
            )

            return self.insert_data("Gastos_periodizados", gasto_periodizado_model.dados)

        return False
    
    def get_dia_abate (self, id_gasto: int) -> str:
        dia_abate = self.get_dados_gasto_periodizado(
            id_gasto, "dia_abate"
        )
        return dia_abate
    
    def get_total_parcelas (self, id_gasto: int) -> int:
        total_parcelas = self.get_dados_gasto_periodizado(
            id_gasto, "total_parcelas"
        )
        return total_parcelas

    def get_controle_parcelas (self, id_gasto: int) -> int:
        controle_parcelas = self.get_dados_gasto_periodizado(
            id_gasto, "controle_parcelas"
        )
        return controle_parcelas

    def atualiza_controle_parcelas (self, id_gasto: int, qtd_dias_parcela: int) -> bool:
        dia_atual = datetime.now()

        dia_abate = datetime.strptime(self.get_dia_abate(id_gasto), "%d/%m/%Y")

        novo_controle_parcelas = (dia_atual - dia_abate).days // qtd_dias_parcela
        atual_controle_parcelas = self.get_controle_parcelas(id_gasto)
        total_parcelas = self.get_total_parcelas(id_gasto)

        dif_controle_novo_e_total = novo_controle_parcelas - total_parcelas

        if atual_controle_parcelas == total_parcelas:
            print(f"Parcelas já pagas id_gasto = {id_gasto}")
            return False
        
        if dif_controle_novo_e_total < 0:
            return self.edit_data(
                "Gastos_periodizados",
                f"controle_parcelas = {novo_controle_parcelas + dif_controle_novo_e_total}",
                f"id_gasto = {id_gasto}"
            )

        return self.edit_data(
            "Gastos_periodizados",
            f"controle_parcelas = {novo_controle_parcelas}",
            f"id_gasto = {id_gasto}"
        )
    