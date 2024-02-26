from models.Banco_model import Banco_model

from DB_base_class import SQLite_DB_CRUD


class Banco_controller (SQLite_DB_CRUD):
    def __init__ (self) -> None:
        # super().__init__("Controle_Financeiro_DB")
        super().__init__("DB_teste")