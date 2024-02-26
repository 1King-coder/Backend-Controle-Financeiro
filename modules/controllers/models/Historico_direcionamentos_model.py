from .Direcionamento_model import Direcionamento_model

class Historico_direcionamentos_model (Direcionamento_model):
    def __init__ (self, nome: str, saldo: float = 0) -> None:
        super().__init__(nome, saldo)