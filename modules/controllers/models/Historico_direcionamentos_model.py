

class Historico_direcionamentos_model:
    def __init__ (self, id_direcionamento: int, nome: str, saldo: float = 0) -> None:
        self.id_direcionamento = id_direcionamento
        self.nome = nome
        self.saldo = saldo

    @property
    def nome (self):
        return self._nome
    
    @nome.setter
    def nome (self, value):
        if not isinstance(value, str):
            raise TypeError("Campo nome tem que ser tipo texto.")
        
        self._nome = value

    @property
    def saldo (self):
        return self._saldo
    
    @saldo.setter
    def saldo (self, value):
        if not isinstance(value, float) or not isinstance(value, int):
            try:
                value = float(value)
            except ValueError as e:
                raise TypeError("Campo saldo tem que possuir um valor numérico.")
                return None
        
        self._saldo = float(value)

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

    @staticmethod
    def structure () -> dict:
        return {
            'name': 'Historico_direcionamentos',
            'columns': ("(" +
                "id INTEGER Primary key autoincrement, " +
                "id_direcionamento INTEGER, " +
                "nome TEXT NOT NULL, " +
                "saldo REAL NOT NULL, " +
                "created_at TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now')) NOT NULL, " +
                "FOREIGN KEY (id_direcionamento) REFERENCES Direcionamentos(id) ON DELETE CASCADE ON UPDATE CASCADE" +
                ")"
            )
        }

    @property
    def  dados (self) -> dict:
        # retorna um dict com as chaves sem o "_"
        return {
            key[1:]: value 
            for key, value in self.__dict__.items()
        }