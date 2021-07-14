from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class SaveNumbersCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, name_of_database, name_of_table, arrayNumberOfBlades):
        self.name_of_database = name_of_database
        self.name_of_table = name_of_table
        self.arrayNumberOfBlades = arrayNumberOfBlades