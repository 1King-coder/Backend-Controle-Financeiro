import importlib
import os
from modules.controllers.DB_base_class import SQLite_DB_CRUD
from modules.Log import log

class Migration (SQLite_DB_CRUD):
    def __init__ (self, db_name) -> None:
        super().__init__(db_name)

    def get_models (self) -> list:
        nomes_models = [
            model[:-3]
            for model in os.listdir("modules/controllers/models")
            if model != "__pycache__"
        ]

        models_list = [
            importlib.import_module(f"modules.controllers.models.{nome_model}").__getattribute__(nome_model)
            for nome_model in nomes_models
        ]

        return models_list

    def migrate (self) -> bool:
        models = self.get_models()
        for model in models:
            model_structure = model.structure()
            sql_create_table = (
                f"CREATE TABLE IF NOT EXISTS {model_structure['name']} {model_structure['columns']}"
            )

            try:
                self.cursor.execute(sql_create_table)
                self.connection.commit()
            
            except Exception as e:
                err_msg = f"Error occurred when trying to create the table {model_structure['name']}."
                print(err_msg)
                log(f"{err_msg}: {e}")
                return False
        
        return True

def main():
    with Migration("DB_teste") as migration:

        try:
            if not migration.migrate():
                raise Exception(f"Error occurred when trying to execute the migration.")

        except Exception as e:
            print(e)
            log(f"{e}")


if __name__ == '__main__':
    main()

