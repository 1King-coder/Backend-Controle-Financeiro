
class Gasto_imediato_model:
    def __init__ (self, id_gasto: int, valor: float, descricao: str = "") -> None:
        self.id_gasto = id_gasto
        self.valor = valor
        self.descricao = descricao

    @property
    def id_gasto (self):
        return self._id_gasto
    
    @id_gasto.setter
    def id_gasto (self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_gasto tem que possuir um valor inteiro.")
        
        self._id_gasto = value


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