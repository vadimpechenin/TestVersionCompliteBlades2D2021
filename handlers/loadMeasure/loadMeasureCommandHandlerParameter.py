from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class LoadMeasureCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, name_of_database,name_of_table):
        self.name_of_database = name_of_database
        self.name_of_table = name_of_table