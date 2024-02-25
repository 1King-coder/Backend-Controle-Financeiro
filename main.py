import sqlite3
from pathlib import Path
from random import randint
from modules.DB_class import Controle_Financeiro_DB, SQLite_DB_CRUD
from datetime import datetime, timedelta

MAIN_DB_NAME = "Controle_Financeiro_DB"
TEST_DB_NAME = "DB_teste"


with SQLite_DB_CRUD(TEST_DB_NAME) as test_db:
    
    # script = f"UPDATE teste_table SET data_start = date('now'), data_end = date(date('now'), '+24 DAYS') WHERE id = 6"
    # script = "ALTER TABLE teste_table ADD data_start TEXT; ALTER TABLE teste_table ADD data_end TEXT;"
    # script = "SELECT *, (strftime('%Y', data_end) - strftime('%Y', data_start)) * 12 + (strftime('%m', data_end) - strftime('%m', data_start)) AS 'dif_datas' FROM teste_table WHERE id = 6"
    # script = "ALTER TABLE teste_table ADD updated_at TEXT ON UPDATE date('now');"
    script = ("CREATE TABLE IF NOT EXISTS teste_relacionamento (" +
        "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL," +
        "id_teste INTEGER NOT NULL, "+
        "atualizado_em TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')) NOT NULL, " +
        "FOREIGN KEY (id_teste) REFERENCES teste_table(id) ON DELETE CASCADE ON UPDATE CASCADE" +
    ");"
    )

    
    
    test_db.cursor.execute(
        script
    )
    test_db.connection.commit()

    # test_db.cursor.execute("DROP TRIGGER [update_date]")

    trigger_cmd = """
    CREATE TRIGGER IF NOT EXISTS [update_date]
        AFTER UPDATE ON teste_relacionamento
        FOR EACH ROW
        BEGIN
        UPDATE teste_relacionamento 
        SET atualizado_em = strftime('%Y-%m-%d %H:%M:%S', 'now')
        WHERE id = old.id; 
        END
        """
    test_db.cursor.executescript(trigger_cmd)
    test_db.connection.commit()

    # test_db.cursor.execute("DROP TABLE teste_relacionamento")
    test_db.edit_data("teste_relacionamento", "id_teste = 1", "id = 4")
    # test_db.insert_data("teste_relacionamento", {"id_teste": 9})
    
    print(test_db.get_data("teste_table"))

    # test_db.insert_data("teste_relacionamento", {"id_teste": 2})

# CF_db = Controle_Financeiro_DB(MAIN_DB_NAME)

# CF_db.init_connection()

# CF_db.close_connection()
