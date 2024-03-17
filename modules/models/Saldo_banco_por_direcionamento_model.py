

class Saldo_banco_por_direcionamento_model:
    def __init__ (self, id_banco: int, id_direcionamento: int, nome_banco: str, nome_direcionamento: str, saldo: float = 0) -> None:
        self.id_banco = id_banco
        self.id_direcionamento = id_direcionamento
        self.saldo = saldo
        self.nome_banco = nome_banco
        self.nome_direcionamento = nome_direcionamento


    @property
    def nome_banco(self):
        return self._nome_banco

    @nome_banco.setter
    def nome_banco(self, value):
        if not isinstance(value, str):
            raise TypeError("Campo nome_banco tem que ser tipo texto.")
        
        self._nome_banco = value

    @property
    def nome_direcionamento(self):
        return self._nome_direcionamento

    @nome_direcionamento.setter
    def nome_direcionamento(self, value):
        if not isinstance(value, str):
            raise TypeError("Campo nome_direcionamento tem que ser tipo texto.")
        
        self._nome_direcionamento = value


    @property
    def id_banco(self):
        return self._id_banco

    @id_banco.setter
    def id_banco(self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_banco tem que possuir um valor inteiro.")
        
        self._id_banco = value

    @property
    def id_direcionamento(self):
        return self._id_direcionamento

    @id_direcionamento.setter
    def id_direcionamento(self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                raise TypeError("Campo id_direcionamento tem que possuir um valor inteiro.")
        self._id_direcionamento = value

    @property
    def saldo(self):
        
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        if not isinstance(value, float) or not isinstance(value, int):
            try:
                value = float(value)
            except ValueError as e:
                raise TypeError("Campo saldo tem que possuir um valor numérico.")
        
        self._saldo = value
    
    @property
    def  dados (self) -> dict:
        # retorna um dict com as chaves sem o "_"
        return {
            key[1:]: value 
            for key, value in self.__dict__.items()
        }

    @staticmethod
    def structure ():
        return {
            'name': 'Saldo_banco_por_direcionamento',
            'columns': ( "(" +
                "id_banco INTEGER NOT NULL, " +
                "id_direcionamento INTEGER NOT NULL, " +
                "nome_banco TEXT NOT NULL, " +
                "nome_direcionamento TEXT NOT NULL, " +
                "saldo REAL NOT NULL DEFAULT 0, " +
                "PRIMARY KEY (id_banco, id_direcionamento), " +
                "FOREIGN KEY (id_banco) REFERENCES Bancos(id) ON DELETE CASCADE ON UPDATE CASCADE, " +
                "FOREIGN KEY (id_direcionamento) REFERENCES Direcionamentos(id) ON DELETE CASCADE ON UPDATE CASCADE" +
                ")")
        }
    
    @staticmethod
    def trigger_script ():
        return """
CREATE TRIGGER IF NOT EXISTS [add_sbpd_sdpb_bancos]
AFTER INSERT ON Bancos
BEGIN
    INSERT INTO Saldo_banco_por_direcionamento
    (id_banco, id_direcionamento, nome_banco, nome_direcionamento)
    SELECT b.id, d.id, b.nome, d.nome
    FROM Bancos b
    LEFT JOIN Direcionamentos d
    WHERE b.id = NEW.id;
    INSERT INTO Saldo_direcionamento_por_banco 
    (id_direcionamento, id_banco, nome_banco, nome_direcionamento)
    SELECT  d.id, b.id, b.nome, d.nome 
    FROM Direcionamentos d
    LEFT JOIN Bancos b
    WHERE b.id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS [add_sbpd_sdpb_direcionamentos]
AFTER INSERT ON Direcionamentos
BEGIN
    INSERT INTO Saldo_banco_por_direcionamento
    (id_banco, id_direcionamento, nome_banco, nome_direcionamento)
    SELECT b.id, d.id, b.nome, d.nome
    FROM Bancos b
    LEFT JOIN Direcionamentos d
    WHERE d.id = NEW.id;
    INSERT INTO Saldo_direcionamento_por_banco 
    (id_direcionamento, id_banco, nome_banco, nome_direcionamento)
    SELECT  d.id, b.id, b.nome, d.nome 
    FROM Direcionamentos d
    LEFT JOIN Bancos b
    WHERE d.id = NEW.id;
END;"""
