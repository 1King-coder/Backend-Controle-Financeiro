from .Banco_model import Banco_model

class Historico_bancos_model(Banco_model):
    def __init__ (self, nome: str, saldo: float = 0) -> None:
        super().__init__(nome, saldo)