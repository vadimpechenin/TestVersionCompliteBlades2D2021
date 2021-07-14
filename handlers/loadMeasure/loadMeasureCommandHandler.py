from handlers.baseCommandHandler import BaseCommandHandler
from db.mainSQL import SQLDataBase

class LoadMeasureCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Запрос к базе данных на получение всех номинальных значений
        data_base = SQLDataBase(parameters.name_of_database)
        data_base.create_session()
        ciphers = data_base.select_all_params_in_table(parameters.name_of_table_meas)
        count_blades = data_base.request_count_of_blades(parameters.name_of_table_meas)
        ciphers.append(count_blades)

        numbers = data_base.select_one_params_in_table(parameters.name_of_table_num, parameters.name_of_column_num)

        responce_dict = {'meas': ciphers, 'number': numbers}

        return responce_dict