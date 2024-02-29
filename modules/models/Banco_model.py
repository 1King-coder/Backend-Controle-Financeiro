class Banco_model:
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
            'name': 'Bancos',
            'columns': ( "(" +
                "id INTEGER Primary key autoincrement, " +
                "nome TEXT NOT NULL, " +
                "saldo REAL NOT NULL, " +
                "updated_at TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now')) NOT NULL" +
                ")"
            )
        }

def main():
    teste = Banco_model("teste")
    print(teste.dados_banco)

if __name__ == '__main__':
    main()