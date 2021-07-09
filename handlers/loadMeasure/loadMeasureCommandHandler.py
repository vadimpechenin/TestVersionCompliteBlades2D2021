from handlers.baseCommandHandler import BaseCommandHandler
from db.mainSQL import SQLDataBase

class LoadMeasureCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Запрос к базе данных на получение всех номинальных значений
        data_base = SQLDataBase(parameters.name_of_database)
        data_base.create_session()
        ciphers = data_base.select_all_parans_in_table(parameters.name_of_table)
        count_blades = data_base.request_count_of_blades(parameters.name_of_table)
        ciphers.append(count_blades)
        return ciphers