
class Gasto_periodizado_model:
    def __init__ (self, id_gasto: int, valor_parcela: float,
                   total_parcelas: int, controle_parcelas,
                   dia_abate: str ="", descricao: str = "") -> None:
        self.id_gasto = id_gasto
        self.total_parcelas = total_parcelas
        self.controle_parcelas = controle_parcelas
        if dia_abate:
            self.dia_abate = dia_abate
        if descricao:
            self.descricao = descricao

        self.valor_parcela = valor_parcela
        self.descricao = descricao
    @property
    def controle_parcelas (self) -> int:
        return self._controle_parcelas
    
    @controle_parcelas.setter
    def controle_parcelas (self, value) -> None:
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo controle_parcelas tem que possuir um valor inteiro.")
        
        self._controle_parcelas = value

    @property
    def valor_total (self) -> float:
        return self._valor_total
    
    @valor_total.setter
    def valor_total (self, _) -> None:
        self._valor_total = self.valor_parcela * self.controle_parcelas

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
    def total_parcelas (self):
        return self._total_parcelas
    
    @total_parcelas.setter
    def total_parcelas (self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo total_parcelas tem que possuir um valor inteiro.")
        
        self._total_parcelas = value

    @property
    def total_parcelas (self):
        return self._total_parcelas
    
    @total_parcelas.setter
    def total_parcelas (self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo total_parcelas tem que possuir um valor inteiro.")
        
        self._total_parcelas = value

    @property
    def dia_abate (self):
        return self._dia_abate
    
    @dia_abate.setter
    def dia_abate (self, value):
        if not isinstance(value, str):
            # Para SQLite toda data tem o tipo texto
            raise TypeError("Campo dia_abate tem que ser tipo texto.")
        
        self._dia_abate = value


    @property
    def descricao (self):
        return self._descricao
    
    @descricao.setter
    def descricao (self, value):
        if not isinstance(value, str):
            raise TypeError("Campo descricao tem que ser tipo texto.")
        
        self._descricao = value

    @property
    def valor_parcela (self):
        return self._valor_parcela
    
    @valor_parcela.setter
    def valor_parcela (self, value):
        if not isinstance(value, float) or not isinstance(value, int):
            try:
                value = float(value)
            except ValueError as e:
                raise TypeError("Campo valor_parcela tem que possuir um valor numérico.")
        
        self._valor_parcela = float(value)

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
            'name': 'Gastos_periodizados',
            'columns': ( "(" +
                "id_gasto INTEGER Primary key, " +
                "descricao TEXT, " +
                "valor_parcela REAL NOT NULL, " +
                "dia_abate TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now')) NOT NULL, " +
                "total_parcelas INTEGER NOT NULL, " +
                "controle_parcelas INTEGER DEFAULT 0 NOT NULL, " +
                "created_at TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now')) NOT NULL, " + 
                "Foreign key (id_gasto) references Gastos_gerais(id) ON DELETE CASCADE ON UPDATE CASCADE" +
                ")"
            ) 
        }

def main():
    teste = Gasto_periodizado_model(1, 532, 12, 0)

    print(teste.dados)

if __name__ == '__main__':
    main()