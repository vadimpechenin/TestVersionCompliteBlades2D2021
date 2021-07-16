from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class PlotMeasuresCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, T_thickness,T_angle,delta_thickness,delta_angle,name_thickness, name_angle):
        self.T_thickness = T_thickness
        self.T_angle = T_angle
        self.delta_thickness = delta_thickness
        self.delta_angle = delta_angle
        self.name_thickness = name_thickness
        self.name_angle = name_angle