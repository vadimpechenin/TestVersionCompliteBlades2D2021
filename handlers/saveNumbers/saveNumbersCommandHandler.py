from handlers.baseCommandHandler import BaseCommandHandler
from db.mainSQL import SQLDataBase

class SaveNumbersCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Сохранение порядковых номеров в базу данных
        data_base = SQLDataBase(parameters.name_of_database)
        data_base.create_session()
        data_base.request_update_of_numbers(parameters.name_of_table, parameters.arrayNumberOfBlades)