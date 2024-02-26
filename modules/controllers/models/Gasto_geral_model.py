
class Gasto_geral_model:
    def __init__ (self, id_banco: int, id_direcionamento: int, tipo_gasto: str,
                  valor: float, descricao: str = ""):
        self.id_banco = id_banco
        self.id_direcionamento = id_direcionamento
        self.tipo_gasto = tipo_gasto
        self.descricao = descricao
        self.valor = valor


    @property
    def id_banco (self):
        return self._id_banco
    
    @id_banco.setter
    def id_banco (self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_banco tem que possuir um valor inteiro.")
        
        self._id_banco = value
    
    @property
    def id_direcionamento (self) -> int:
        return self._id_direcionamento
    
    @id_direcionamento.setter
    def id_direcionamento (self, value) -> None:
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_direcionamento tem que possuir um valor inteiro.")
        
        self._id_direcionamento = value

    @property
    def tipo_gasto (self) -> str:
        return self._tipo_gasto
    
    @tipo_gasto.setter
    def tipo_gasto (self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("Campo tipo_gasto tem que ser do tipo texto.")
        
        self._tipo_gasto = value

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
