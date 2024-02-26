
class Transferencia_entre_direcionamentos_model:
    def __init__ (self, id_direcionamento_origem: int, id_direcionamento_destino: int, 
                  valor: float, descricao: str = ""):
        self.id_direcionamento_origem = id_direcionamento_origem
        self.id_direcionamento_destino = id_direcionamento_destino
        self.descricao = descricao
        self.valor = valor


    @property
    def id_direcionamento_origem (self):
        return self._id_direcionamento_origem
    
    @id_direcionamento_origem.setter
    def id_direcionamento_origem (self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_direcionamento_origem tem que possuir um valor inteiro.")
        
        self._id_direcionamento_origem = value
    
    @property
    def id_direcionamento_destino (self) -> int:
        return self._id_direcionamento_destino
    
    @id_direcionamento_destino.setter
    def id_direcionamento_destino (self, value) -> None:
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_direcionamento_destino tem que possuir um valor inteiro.")
        
        self._id_direcionamento_destino = value
    

    @property
    def descricao (self):
        return self._descricao
    
    @descricao.setter
    def descricao (self, value):
        if not isinstance(value, str):
            raise TypeError("Campo descricao tem que ser tipo texto.")
        
        self._descricao = value

    @property
    def valor (self):
        return self._valor
    
    @valor.setter
    def valor (self, value):
        if not isinstance(value, float) or not isinstance(value, int):
            try:
                value = float(value)
            except ValueError as e:
                raise TypeError("Campo valor tem que possuir um valor numérico.")
        
        self._valor = float(value)