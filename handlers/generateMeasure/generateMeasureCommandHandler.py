from handlers.baseCommandHandler import BaseCommandHandler
from db.mainSQL import SQLDataBase
import numpy as np

class GenerateMeasureCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Запрос к базе данных на заполнение данных
        data_base = SQLDataBase(parameters.name_of_database)
        data_base.create_session()
        data_base.request_delete_of_measured(parameters.name_of_table)
        data_base.generated_data_save_data_base(parameters.delta_thickness, parameters.delta_angle)
        ciphers = data_base.select_all_parans_in_table(parameters.name_of_table)
        return ciphers