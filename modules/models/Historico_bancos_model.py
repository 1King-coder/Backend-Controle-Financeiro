
class Historico_bancos_model:
    def __init__ (self, id_banco: int, nome: str, saldo: float = 0) -> None:
        self.nome = nome
        self.saldo = saldo
        self.id_banco = id_banco

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

    @property
    def id_banco (self) -> int:
        return self._id_banco
    
    @id_banco.setter
    def id_banco (self, value) -> None:
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_banco tem que possuir um valor inteiro.")
        
        self._id_banco = value

    @staticmethod
    def structure () -> dict:
        return {
            'name': 'Historico_bancos',
            'columns': ("(" +
                "id INTEGER Primary key autoincrement, " +
                "id_banco INTEGER, " +
                "nome TEXT NOT NULL, " +
                "saldo REAL NOT NULL, " +
                "created_at TEXT DEFAULT (strftime('%d/%m/%Y', 'now', 'localtime')) NOT NULL, " +
                "FOREIGN KEY (id_banco) REFERENCES Bancos(id) ON DELETE CASCADE ON UPDATE CASCADE" +
                ")"
            )
        }


def main():
    teste = Historico_bancos_model('Teste')

    print(teste.dados)

if __name__ == '__main__':
    main()