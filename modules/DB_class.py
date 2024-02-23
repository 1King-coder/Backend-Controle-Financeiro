import sqlite3
from pathlib import Path
from datetime import datetime
from copy import deepcopy

 
from .Log import log


class SQLite_DB:

    def __init__ (self, db_name: str) -> None:        
        self.db_name = db_name + ".sqlite3"

    def init_connection (self) -> None:
        db_path = Path(__file__).parent.parent.joinpath("DB") / self.db_name

        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()

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

    def _organize_data (self, table_name: str, data_set: list):
        column_names = self._extract_columns_names(table_name)
        organized_entitys_list = []
        organized_entity = dict()

        for entity in data_set:
            for col_data, col_name in zip(list(entity), column_names):
                organized_entity[col_name] = col_data

            organized_entitys_list.append(deepcopy(organized_entity))
        
        
        return organized_entitys_list

    def insert_data (self, table_name: str, data: dict) -> bool:
        columns_names = tuple(data.keys())
        
        binding_str = "(" + ("?, " * len(columns_names))[:-2] + ")"

        sql_insert = (
            f"INSERT INTO {table_name} "
            + f"{columns_names} VALUES {binding_str}"
        )

        try:
            self.cursor.execute(sql_insert, tuple(data.values()))
            self.connection.commit()

            return True
        
        except Exception as e:
            err_msg = f"Error occurred when trying to insert data in the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return False

    def get_data (self, table_name: str, command: str = "*", WHERE: str = "") -> dict:
        if command != "*":
            sql_select = f"SELECT {command} FROM {table_name}"

            if WHERE:
                sql_select += f" WHERE {WHERE}"

            self.cursor.execute(sql_select)
            return self.cursor.fetchall()
        
        if not WHERE:
            try:
                self.cursor.execute(f"SELECT * FROM {table_name}")
                
                organized_data = self._organize_data(table_name, self.cursor.fetchall())
                return organized_data
            
            except Exception as e:
                err_msg = f"Error occurred when trying to retrieve data from the table ({table_name})."
                print(err_msg)
                log(f"{err_msg}: {e}")
                return []
               
        sql_select = (
            f"SELECT {command} FROM {table_name} "
            + f"WHERE {WHERE}"
        )

        try:
            print(sql_select)
            self.cursor.execute(sql_select)
            return self.cursor.fetchall()[0]

        except Exception as e:
            err_msg = f"Error occurred when trying to retrieve data from the table ({table_name})."
            print(err_msg)
            log(f"{err_msg}: {e}")
            return []


class Controle_Financeiro_DB (SQLite_DB):

    def __init__ (self, db_name) -> None:
        super().__init__(db_name)
