import sqlite3
from pathlib import Path
from datetime import datetime
from copy import deepcopy

from ..Log import log

SQLITE_DOCKER = "sqlite_data:"


class SQLite_DB_CRUD:

    def __init__ (self, db_name: str) -> None:        
        self.db_name = db_name

        self.init_connection()

    def init_connection (self) -> None:

        try:
            db_name = self.db_name + ".sqlite3"
            db_path = SQLITE_DOCKER / Path(__file__).parent.parent.parent.joinpath("DB") / db_name

            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            self.connection.commit()
            self.cursor.close()

        except Exception as e:
            err_msg = f"Error occurred when trying to connect to database ({self.db_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return None

    def close_connection (self) -> None:
        try:
            self.connection.close()

        except Exception as e:
            err_msg = f"Error occurred when trying to close the connection with the database ({self.db_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return None

    def __enter__ (self):
        self.init_connection()
        return self

    def __exit__ (self, *args):
        self.close_connection()

    def _organize_data_in_dictionary (self, dataset: list):
        return [dict(entity) for entity in dataset]

    def _extract_columns_names (self, table_name) -> list:
        self.cursor = self.connection.cursor()

        sql_pragma = f"PRAGMA table_info([{table_name}])"

        try:
            self.cursor.execute(sql_pragma)

            columns_names = [column[1] for column in self.cursor.fetchall()]
            self.cursor.close()
            return columns_names
        
        except Exception as e:
            err_msg = f"Error occurred when trying to retrieve columns data from table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return [None]    

    def insert_data (self, table_name: str, data: dict) -> bool:
        """
        Equivalent to:
        INSERT INTO {table_name} {tuple(data.keys())} 
        VALUES {tuple(data.values())}
        """
        self.cursor = self.connection.cursor()

        columns_names = tuple(data.keys())

        binding_str = "(" + ("?, " * len(columns_names))[:-2] + ")"

        if len(columns_names) == 1:
            columns_names = str(columns_names)[:-2] + ")"

        sql_insert = (
            f"INSERT INTO {table_name} "
            + f"{columns_names} VALUES {binding_str}"
        )

        try:
            self.cursor.execute(sql_insert, tuple(data.values()))
            self.connection.commit()
            self.cursor.close()

            return True
        
        except Exception as e:
            self.cursor.close()
            err_msg = f"Error occurred when trying to insert data in the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return False

    def get_data (self, table_name: str, command: str = "", WHERE: str = "") -> dict:
        """
        Equivalent to:
        SELECT {command} FROM {table_name} WHERE {WHERE}
        """
        self.cursor = self.connection.cursor()

        if command and not WHERE:
            try:
                sql_select = f"SELECT {command} FROM {table_name}"
                if WHERE:
                    sql_select += f" WHERE {WHERE};"

                self.cursor.execute(sql_select)
                data = self._organize_data_in_dictionary(self.cursor.fetchall())
                self.cursor.close()
                return data
            
            
            except Exception as e:
                err_msg = f"Error occurred when trying to retrieve data from the table with command ({table_name})."
                print(err_msg)
                log(f"{err_msg}: {e}")
                return []
            
        if not WHERE:
            try:
                self.cursor.execute(f"SELECT * FROM {table_name}")
                
                data  = self._organize_data_in_dictionary(self.cursor.fetchall())
                self.cursor.close()

                return data

            except Exception as e:
                err_msg = f"Error occurred when trying to retrieve data from the table ({table_name})."
                print(err_msg)
                log(f"{err_msg}: {e}")
                self.cursor.close()
                return []

        sql_select = (
            f"SELECT {command} FROM {table_name} "
            + f"WHERE {WHERE}"
        )

        try:
            self.cursor.execute(sql_select)
            data = self._organize_data_in_dictionary(self.cursor.fetchall())
            self.cursor.close()
            return data

        except Exception as e:
            err_msg = f"Error occurred when trying to retrieve data from the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            self.cursor.close()
            return []

    def edit_data (self, table_name: str, change_cmd: str, WHERE: str) -> bool:
        """
        Equivalent to:
        UPDATE {table_name} SET {change_cmd} WHERE {WHERE};
        """
        self.cursor = self.connection.cursor()

        sql_update = (
            f"UPDATE {table_name} SET {change_cmd} " +
            f"WHERE {WHERE}"
        )

        try:
            self.cursor.execute(sql_update)
            self.connection.commit()
            self.cursor.close()
            return True
        except Exception as e:
            err_msg = f"Error occurred when trying to update data from the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            self.cursor.close()
            return False

    def delete_data (self, table_name: str, WHERE: str = "") -> bool:
        """
        Equivalent to:
        DELETE FROM {table_name} WHERE {WHERE}
        """
        self.cursor = self.connection.cursor()

        if not WHERE:
            try:
                err_msg = f"Cannot execute an DELETE without WHERE clausule. table: ({table_name})."
                raise ReferenceError(err_msg)
            except ReferenceError as e:
                print(err_msg)
                log(f"{err_msg}: {e}")
                self.cursor.close()
                return False
        
        sql_delete = (
            f"DELETE FROM {table_name} WHERE {WHERE}"
        )

        try:
            self.cursor.execute(sql_delete)
            self.connection.commit()
            self.cursor.close()
            return True
        except Exception as e:
            err_msg = f"Error occurred when trying to delete data from the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            self.cursor.close()
            return False

    


    

        


        