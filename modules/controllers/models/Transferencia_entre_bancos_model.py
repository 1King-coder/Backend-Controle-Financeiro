
class Transferencia_entre_bancos_model:
    def __init__ (self, id_banco_origem: int, id_banco_destino: int, 
                  valor: float, descricao: str = ""):
        self.id_banco_origem = id_banco_origem
        self.id_banco_destino = id_banco_destino
        self.descricao = descricao
        self.valor = valor


    @property
    def id_banco_origem (self):
        return self._id_banco_origem
    
    @id_banco_origem.setter
    def id_banco_origem (self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_banco_origem tem que possuir um valor inteiro.")
        
        self._id_banco_origem = value
    
    @property
    def id_banco_destino (self) -> int:
        return self._id_banco_destino
    
    @id_banco_destino.setter
    def id_banco_destino (self, value) -> None:
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_banco_destino tem que possuir um valor inteiro.")
        
        self._id_banco_destino = value
    

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

    @property
    def  dados (self) -> dict:
        # retorna um dict com as chaves sem o "_"
        return {
            key[1:]: value 
            for key, value in self.__dict__.items()
        }