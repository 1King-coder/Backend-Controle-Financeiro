class Direcionamento_model:
    def __init__(self, nome: str, saldo: float = 0) -> None:
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
    def  dados (self) -> dict:
        # retorna um dict com as chaves sem o "_"
        return {
            key[1:]: value 
            for key, value in self.__dict__.items()
        }

    @staticmethod
    def structure () -> dict:
        return {
            'name': 'Direcionamentos',
            'columns': ( "(" +
                "id INTEGER Primary key autoincrement, " +
                "nome TEXT NOT NULL, " +
                "saldo REAL NOT NULL, " +
                "updated_at TEXT DEFAULT (strftime('%d/%m/%Y %H:%M:%S', 'now', 'localtime')) NOT NULL)"
            )
        }
    
    @staticmethod
    def trigger_script () -> str:
        return """
        CREATE TRIGGER IF NOT EXISTS updated_at_Direcionamentos
            AFTER UPDATE ON Direcionamentos
            FOR EACH ROW
            BEGIN
                UPDATE Direcionamentos
                SET updated_at = (strftime('%d/%m/%Y %H:%M:%S', 'now', 'localtime'))
                WHERE id = OLD.id;
            END;
        """
