
class Gasto_periodizado_model:
    def __init__ (self, id_gasto: int, valor_parcela: float,
                   total_parcelas: int, controle_parcelas,
                   dia_abate: str ="", descricao: str = "") -> None:
        self.id_gasto = id_gasto
        self.total_parcelas = total_parcelas
        self.controle_parcelas = controle_parcelas
        self.dia_abate = dia_abate
        self.valor_parcela = valor_parcela
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

def main():
    teste = Gasto_periodizado_model(1, 532, 12, 0)

    print(teste.__dict__)

if __name__ == '__main__':
    main()