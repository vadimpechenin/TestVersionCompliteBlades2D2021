from handlers.baseCommandHandler import BaseCommandHandler
from db.mainSQL import SQLDataBase

class GenerateMeasureCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Запрос к базе данных на заполнение данных
        data_base = SQLDataBase(parameters.name_of_database)
        data_base.create_session()
        data_base.request_delete_of_measured(parameters.name_of_table_meas)
        data_base.request_delete_of_measured(parameters.name_of_table_num)
        data_base.generated_data_save_data_base(parameters.delta_thickness, parameters.delta_angle)
        ciphers = data_base.select_all_params_in_table(parameters.name_of_table_meas)
        numbers = data_base.select_one_params_in_table(parameters.name_of_table_num, parameters.name_of_column_num)
        responce_dict={'meas':ciphers, 'number':numbers}

        return responce_dict