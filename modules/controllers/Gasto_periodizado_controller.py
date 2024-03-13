
from ..models.Gasto_geral_model import Gasto_geral_model
from ..models.Gasto_periodizado_model import Gasto_periodizado_model
from .Banco_controller import Banco_controller
from .Direcionamento_controller import Direcionamento_controller
from requests import request
from .DB_base_class import SQLite_DB_CRUD
from pandas import DataFrame

from datetime import datetime

class Gasto_periodizado_controller (SQLite_DB_CRUD):

    def __init__ (self, db_name: str) -> None:
        super().__init__(db_name)

        self.banco_c = Banco_controller(self.db_name)
        self.direc_C = Direcionamento_controller(self.db_name)



    def mostrar (self) -> list:
        return self.get_data(
            "Gastos_periodizados"
        )
    
    def dataframe (self) -> 'DataFrame':
        return DataFrame(self.mostrar())

    def get_dados (self, id_gasto: int, dados_desejados: str = "*") -> dict:

        dados_gasto = self.get_data("Gastos_periodizados", dados_desejados.strip(), f"id_gasto = {id_gasto}")
        
        if not dados_gasto:
            return None

        return dados_gasto[0]
    
    def adicionar (self, id_banco:int,
                                    id_direcionamento: int, valor_parcela: float, 
                                    total_parcelas: int, controle_parcelas: int = 0,
                                    descricao: str = "Gasto periodizado", dia_abate: str = "") -> bool:

        if valor_parcela < 0:
            return False
        
        if total_parcelas < 0:
            return False
        
        if controle_parcelas < 0:
            return False
        
        banco_saldo = self.banco_c.get_saldo(id_banco)
        direc_saldo = self.direc_C.get_saldo(id_direcionamento)

        if banco_saldo < valor_parcela * controle_parcelas:
            return False
        
        if direc_saldo < valor_parcela * controle_parcelas:
            return False
        

        descricao += f" {self.cursor.lastrowid}"

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
        dia_abate = self.get_dados(
            id_gasto, "dia_abate"
        )
        if not dia_abate:
            return None

        return dia_abate['dia_abate']
    
    def get_total_parcelas (self, id_gasto: int) -> int:
        total_parcelas = self.get_dados(
            id_gasto, "total_parcelas"
        )
        if not total_parcelas:
            return None

        return total_parcelas['total_parcelas']

    def get_controle_parcelas (self, id_gasto: int) -> int:
        controle_parcelas = self.get_dados(
            id_gasto, "controle_parcelas"
        )
        if not controle_parcelas:
            return None

        return controle_parcelas['controle_parcelas']

    def atualiza_controle_parcelas (self, id_gasto: int, qtd_dias_parcela: int) -> bool:
        dia_atual = datetime.now()

        dia_abate = datetime.strptime(self.get_dia_abate(id_gasto), "%d/%m/%Y")

        novo_controle_parcelas = (dia_atual - dia_abate).days // qtd_dias_parcela
        atual_controle_parcelas = self.get_controle_parcelas(id_gasto)
        total_parcelas = self.get_total_parcelas(id_gasto)

        dif_controle_novo_e_total = total_parcelas - novo_controle_parcelas

        if atual_controle_parcelas == total_parcelas:
            return 2
        
        if atual_controle_parcelas == novo_controle_parcelas:
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
    
    def editar (self,
                           id_gasto: int, novo_valor: float = 0,
                           nova_descricao: str = "", novo_id_banco: int = 0,
                           novo_id_direcionamento: int = 0, novo_total_parcelas: int = 0,
                           novo_controle_parcelas: int = 0, novo_dia_abate: str = "") -> bool:

        if novo_valor < 0:
            return False
        
        if novo_total_parcelas < 0:
            return False
        
        if novo_controle_parcelas < 0:
            return False
        
        saldo_banco = self.banco_c.get_saldo(novo_id_banco)
        saldo_direc = self.direc_C.get_saldo(novo_id_direcionamento)

        if saldo_banco < novo_valor * novo_controle_parcelas:
            return False
        
        if saldo_direc < novo_valor * novo_controle_parcelas:
            return False

        novos_dados = {
            'valor_parcela': novo_valor,
            'total_parcelas': novo_total_parcelas,
            'dia_abate': novo_dia_abate,
            'id_direcionamento': novo_id_direcionamento,
            'id_banco': novo_id_banco,
            'controle_parcelas': novo_controle_parcelas,
            'descricao': nova_descricao,
        }

        edit_command = ""

        for key, value in novos_dados.items():
            if value:
                if key == 'descricao':
                    edit_command += f"{key} = {value} {self.cursor.lastrowid}, "
                    continue

                edit_command += f"{key} = {value}, "

        edit_command = edit_command[:-2]

        if novo_id_banco or novo_id_direcionamento:
            request(
                "PUT",
                f"http://localhost:8000/gastos_gerais/{id_gasto}", 
                json={
                    key: value 
                    for key, value in novos_dados.items()
                    if key != 'valor_parcela' or key != 'total_parcelas' or key != 'dia_abate' or key != 'controle_parcelas'}, 
            )

            edit_command = edit_command.replace(f"id_banco = {novo_id_banco}, ", "").replace(f"id_direcionamento = {novo_id_direcionamento}, ", "")

        self.edit_data("Gastos_gerais", f"valor = {novo_valor}", f"id = {id_gasto}")

        return self.edit_data("Gastos_periodizados", edit_command, f"id_gasto = {id_gasto}")
            