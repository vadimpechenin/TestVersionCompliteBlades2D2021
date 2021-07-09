from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class GenerateMeasureCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, name_of_database,name_of_table,delta_thickness, delta_angle):
        self.name_of_database = name_of_database
        self.delta_thickness = delta_thickness
        self.delta_angle = delta_angle
        self.name_of_table = name_of_table