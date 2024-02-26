

class Deposito_model:
    def __init__ (self, id_banco: int, id_direcionamento: int, 
                  descricao: str, valor: float):
        self.id_banco = id_banco
        self.id_direcionamento = id_direcionamento
        self.descricao = descricao
        self.valor = valor

    @property
    def descricao (self):
        return self.__descricao
    
    @descricao.setter
    def descricao (self, value):
        if not isinstance(value, str):
            raise TypeError("Campo descricao tem que ser tipo texto.")
        
        self.__descricao = value

    @property
    def valor (self):
        return self.__valor
    
    @valor.setter
    def valor (self, value):
        if not isinstance(value, float) or not isinstance(value, int):
            try:
                value = float(value)
            except ValueError as e:
                raise TypeError("Campo valor tem que possuir um valor numérico.")
        
        self.__valor = float(value)

