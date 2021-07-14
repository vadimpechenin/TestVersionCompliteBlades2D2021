from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class LoadMeasureCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, name_of_database,name_of_table_meas, name_of_table_num, name_of_column_num):
        self.name_of_database = name_of_database
        self.name_of_table_meas = name_of_table_meas
        self.name_of_table_num = name_of_table_num
        self.name_of_column_num = name_of_column_num