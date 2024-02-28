import sqlite3
from pathlib import Path
from datetime import datetime
from copy import deepcopy
from ..Log import log


class SQLite_DB_CRUD:

    def __init__ (self, db_name: str) -> None:        
        self.db_name = db_name + ".sqlite3"

    def init_connection (self) -> None:
        db_path = Path(__file__).parent.parent.parent.joinpath("DB") / self.db_name

        try:
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            self.connection.commit()

        except Exception as e:
            err_msg = f"Error occurred when trying to connect to database ({self.db_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return None

    def close_connection (self) -> None:
        try:
            self.cursor.close()
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
        sql_pragma = f"PRAGMA table_info([{table_name}])"

        try:
            self.cursor.execute(sql_pragma)

            columns_names = [column[1] for column in self.cursor.fetchall()]

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

        columns_names = tuple(data.keys())

        binding_str = "(" + ("?, " * len(columns_names))[:-2] + ")"

        if len(columns_names) == 1:
            columns_names = str(columns_names)[:-2] + ")"

        sql_insert = (
            f"INSERT INTO {table_name} "
            + f"{columns_names} VALUES {binding_str}"
        )

        print(sql_insert)

        try:
            self.cursor.execute(sql_insert, tuple(data.values()))
            self.connection.commit()

            return True
        
        except Exception as e:
            err_msg = f"Error occurred when trying to insert data in the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return False

    def get_data (self, table_name: str, command: str = "", WHERE: str = "") -> dict:
        """
        Equivalent to:
        SELECT {command} FROM {table_name} WHERE {WHERE}
        """

        if command:
            try:
                sql_select = f"SELECT {command} FROM {table_name}"

                if WHERE:
                    sql_select += f" WHERE {WHERE}"

                self.cursor.execute(sql_select)
                return self._organize_data_in_dictionary(self.cursor.fetchall())
            
            except Exception as e:
                err_msg = f"Error occurred when trying to retrieve data from the table with command ({table_name})."
                print(err_msg)
                log(f"{err_msg}: {e}")
                return []
            
        if not WHERE:
            try:
                self.cursor.execute(f"SELECT * FROM {table_name}")
                
                return self._organize_data_in_dictionary(self.cursor.fetchall())
            
            except Exception as e:
                err_msg = f"Error occurred when trying to retrieve data from the table ({table_name})."
                print(err_msg)
                log(f"{err_msg}: {e}")
                return []

        sql_select = (
            f"SELECT * FROM {table_name} "
            + f"WHERE {WHERE}"
        )

        try:
            self.cursor.execute(sql_select)
            return self._organize_data_in_dictionary(self.cursor.fetchall())

        except Exception as e:
            err_msg = f"Error occurred when trying to retrieve data from the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return []

    def edit_data (self, table_name: str, change_cmd: str, WHERE: str) -> bool:
        """
        Equivalent to:
        UPDATE {table_name} SET {change_cmd} WHERE {WHERE};
        """
        sql_update = (
            f"UPDATE {table_name} SET {change_cmd} " +
            f"WHERE {WHERE}"
        )

        try:
            self.cursor.execute(sql_update)
            self.connection.commit()
            return True
        except Exception as e:
            err_msg = f"Error occurred when trying to update data from the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return False

    def delete_data (self, table_name: str, WHERE: str = "") -> bool:
        """
        Equivalent to:
        DELETE FROM {table_name} WHERE {WHERE}
        """
        if not WHERE:
            try:
                err_msg = f"Cannot execute an DELETE without WHERE clausule. table: ({table_name})."
                raise ReferenceError(err_msg)
            except ReferenceError as e:
                print(err_msg)
                log(f"{err_msg}: {e}")
                return False
        
        sql_delete = (
            f"DELETE FROM {table_name} WHERE {WHERE}"
        )

        try:
            self.cursor.execute(sql_delete)
            self.connection.commit()
            return True
        except Exception as e:
            err_msg = f"Error occurred when trying to delete data from the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return False

    


    

        


        