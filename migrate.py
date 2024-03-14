import importlib
import os
from modules.controllers.DB_base_class import SQLite_DB_CRUD
from modules.Log import log

class Migration (SQLite_DB_CRUD):
    def __init__ (self, db_name) -> None:
        super().__init__(db_name)

    @property
    def get_models (self) -> list:
        nomes_models = [
            model[:-3]
            for model in os.listdir("modules/models")
            if model != "__pycache__" and model != "__init__.py"
        ]

        models_list = [
            importlib.import_module(f"modules.models.{nome_model}").__getattribute__(nome_model)
            for nome_model in nomes_models
        ]

        return models_list

    def migrate (self) -> bool:
        self.cursor = self.connection.cursor()

        for model in self.get_models:
            model_structure = model.structure()
            sql_create_table = (
                f"CREATE TABLE IF NOT EXISTS {model_structure['name']} {model_structure['columns']}"
            )

            try:
                self.cursor.execute(sql_create_table)
                self.connection.commit()
                
                if "trigger_script" in dir(model):
                    trigger_script = model.trigger_script()
                    self.cursor.execute(trigger_script)
                    self.connection.commit()
            
            except Exception as e:
                err_msg = f"Error occurred when trying to create the table {model_structure['name']}."
                print(err_msg)
                log(f"{err_msg}: {e}")
                return False
        
        return True

def main():
    DB_NAME = "Controle_Financeiro_DB_fase_testes"

    with Migration(DB_NAME) as migration:

        try:
            if not migration.migrate():
                raise Exception(f"Error occurred when trying to execute the migration.")

        except Exception as e:
            print(e)
            log(f"{e}")


if __name__ == '__main__':
    main()

