

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

    @staticmethod
    def structure ():
        return {
            'name': 'Saldo_banco_por_direcionamento',
            'columns': ( "(" +
                "id_banco INTEGER NOT NULL, " +
                "id_direcionamento INTEGER NOT NULL, " +
                "nome_banco TEXT NOT NULL, " +
                "nome_direcionamento TEXT NOT NULL, " +
                "saldo REAL NOT NULL, " +
                "PRIMARY KEY (id_banco, id_direcionamento), " +
                "FOREIGN KEY (id_banco) REFERENCES Bancos(id) ON DELETE CASCADE ON UPDATE CASCADE, " +
                "FOREIGN KEY (id_direcionamento) REFERENCES Direcionamentos(id) ON DELETE CASCADE ON UPDATE CASCADE" +
                ")")
        }
    
    @staticmethod
    def trigger_script ():
        return """
        CREATE TRIGGER IF NOT EXISTS [att_sdpb_Bancos]
            AFTER UPDATE ON Bancos
            BEGIN
                WITH total_dep AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(dep.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Depositos dep
                    ON s.id_banco = dep.id_banco 
                    AND s.id_direcionamento  = dep.id_direcionamento
                GROUP BY s.id_banco , s.id_direcionamento
                ),
                total_tbrec AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(t.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Transferencias_entre_bancos t
                    ON t.id_banco_destino = s.id_banco 
                    AND t.id_direcionamento = s.id_direcionamento
                GROUP BY s.id_banco , s.id_direcionamento
                ),
                total_tdrec AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(t.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Transferencias_entre_direcionamentos t
                    ON t.id_direcionamento_destino = s.id_direcionamento 
                    AND t.id_banco = s.id_banco
                GROUP BY s.id_banco , s.id_direcionamento
                ),
                total_gastos AS (
                SELECT s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(gi.valor, 0) + 
                    IFNULL(gp.valor_parcela * gp.controle_parcelas, 0))
                    as total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Gastos_gerais gg
                    ON gg.id_banco = s.id_banco 
                    AND gg.id_direcionamento = s.id_direcionamento
                LEFT JOIN Gastos_imediatos gi
                    ON gi.id_gasto = gg.id
                LEFT JOIN Gastos_periodizados gp
                    ON gp.id_gasto = gg.id
                GROUP BY s.id_banco ,s.id_direcionamento
                ),
                total_tbenv AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(t.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Transferencias_entre_bancos t
                    ON t.id_banco_origem = s.id_banco 
                    AND t.id_direcionamento = s.id_direcionamento
                GROUP BY s.id_banco , s.id_direcionamento
                ),
                total_tdenv AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(t.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Transferencias_entre_direcionamentos t
                    ON t.id_direcionamento_origem = s.id_direcionamento 
                    AND t.id_banco = s.id_banco
                GROUP BY s.id_banco , s.id_direcionamento
                )
                UPDATE Saldo_direcionamento_por_banco as sdpb
                SET saldo = (
                SELECT
                (total_dep.total + total_tbrec.total + total_tdrec.total)
                - (total_gastos.total + total_tbenv.total + total_tdenv.total)
                AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN total_dep
                    ON total_dep.id_b = s.id_banco 
                    AND total_dep.id_d = s.id_direcionamento 
                LEFT JOIN total_tbrec
                    ON total_tbrec.id_b = s.id_banco
                    AND total_tbrec.id_d = s.id_direcionamento 
                LEFT JOIN total_tdrec
                    ON total_tdrec.id_b = s.id_banco 
                    AND total_tdrec.id_d = s.id_direcionamento
                LEFT JOIN total_gastos
                    ON total_gastos.id_b = s.id_banco
                    AND total_gastos.id_d = s.id_direcionamento
                LEFT JOIN total_tbenv
                    ON total_tbenv.id_b = s.id_banco
                    AND total_tbenv.id_d = s.id_direcionamento 
                LEFT JOIN total_tdenv
                    ON total_tdenv.id_b = s.id_banco 
                    AND total_tdenv.id_d = s.id_direcionamento
                WHERE 
                s.id_banco = sdpb.id_banco
                AND s.id_direcionamento = sdpb.id_direcionamento);
            END;
            
        CREATE TRIGGER IF NOT EXISTS [att_sdpb_Direcionamentos]
            AFTER UPDATE ON Direcionamentos
            BEGIN
                WITH total_dep AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(dep.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Depositos dep
                    ON s.id_banco = dep.id_banco 
                    AND s.id_direcionamento  = dep.id_direcionamento
                GROUP BY s.id_banco , s.id_direcionamento
                ),
                total_tbrec AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(t.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Transferencias_entre_bancos t
                    ON t.id_banco_destino = s.id_banco 
                    AND t.id_direcionamento = s.id_direcionamento
                GROUP BY s.id_banco , s.id_direcionamento
                ),
                total_tdrec AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(t.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Transferencias_entre_direcionamentos t
                    ON t.id_direcionamento_destino = s.id_direcionamento 
                    AND t.id_banco = s.id_banco
                GROUP BY s.id_banco , s.id_direcionamento
                ),
                total_gastos AS (
                SELECT s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(gi.valor, 0) + 
                    IFNULL(gp.valor_parcela * gp.controle_parcelas, 0))
                    as total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Gastos_gerais gg
                    ON gg.id_banco = s.id_banco 
                    AND gg.id_direcionamento = s.id_direcionamento
                LEFT JOIN Gastos_imediatos gi
                    ON gi.id_gasto = gg.id
                LEFT JOIN Gastos_periodizados gp
                    ON gp.id_gasto = gg.id
                GROUP BY s.id_banco ,s.id_direcionamento
                ),
                total_tbenv AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(t.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Transferencias_entre_bancos t
                    ON t.id_banco_origem = s.id_banco 
                    AND t.id_direcionamento = s.id_direcionamento
                GROUP BY s.id_banco , s.id_direcionamento
                ),
                total_tdenv AS (
                SELECT 
                s.id_banco as id_b, s.id_direcionamento as id_d,
                SUM(IFNULL(t.valor, 0)) AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN Transferencias_entre_direcionamentos t
                    ON t.id_direcionamento_origem = s.id_direcionamento 
                    AND t.id_banco = s.id_banco
                GROUP BY s.id_banco , s.id_direcionamento
                )
                UPDATE Saldo_direcionamento_por_banco as sdpb
                SET saldo = (
                SELECT
                (total_dep.total + total_tbrec.total + total_tdrec.total)
                - (total_gastos.total + total_tbenv.total + total_tdenv.total)
                AS total
                FROM Saldo_direcionamento_por_banco s
                LEFT JOIN total_dep
                    ON total_dep.id_b = s.id_banco 
                    AND total_dep.id_d = s.id_direcionamento 
                LEFT JOIN total_tbrec
                    ON total_tbrec.id_b = s.id_banco
                    AND total_tbrec.id_d = s.id_direcionamento 
                LEFT JOIN total_tdrec
                    ON total_tdrec.id_b = s.id_banco 
                    AND total_tdrec.id_d = s.id_direcionamento
                LEFT JOIN total_gastos
                    ON total_gastos.id_b = s.id_banco
                    AND total_gastos.id_d = s.id_direcionamento
                LEFT JOIN total_tbenv
                    ON total_tbenv.id_b = s.id_banco
                    AND total_tbenv.id_d = s.id_direcionamento 
                LEFT JOIN total_tdenv
                    ON total_tdenv.id_b = s.id_banco 
                    AND total_tdenv.id_d = s.id_direcionamento
                WHERE 
                s.id_banco = sdpb.id_banco
                AND s.id_direcionamento = sdpb.id_direcionamento);
            END;
        """
