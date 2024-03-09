
class Transferencia_entre_direcionamentos_model:
    def __init__ (self, id_direcionamento_origem: int, id_direcionamento_destino: int, 
                  id_banco: int, valor: float, descricao: str = ""):
        self.id_direcionamento_origem = id_direcionamento_origem
        self.id_direcionamento_destino = id_direcionamento_destino
        self.id_banco = id_banco
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
    
    @staticmethod
    def structure () -> dict:
        return {
            'name': 'Transferencias_entre_direcionamentos',
            'columns': ( "(" +
                "id INTEGER Primary key, " +
                "id_direcionamento_origem INTEGER, " +
                "id_direcionamento_destino INTEGER, " +
                "id_banco INTEGER, " +
                "descricao TEXT, " +
                "valor REAL NOT NULL, " +
                "created_at TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now')) NOT NULL, " + 
                "Foreign key (id_direcionamento_origem) references Direcionamentos(id) ON DELETE CASCADE ON UPDATE CASCADE, " +
                "Foreign key (id_direcionamento_origem) references Direcionamentos(id) ON DELETE CASCADE ON UPDATE CASCADE, " +
                "Foreign key (id_banco) references Bancos(id) ON DELETE CASCADE ON UPDATE CASCADE" +
                ")"
            )
        }