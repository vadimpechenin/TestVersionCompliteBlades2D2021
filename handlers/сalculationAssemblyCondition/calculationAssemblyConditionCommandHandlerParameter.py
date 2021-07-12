from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class CalculationAssemblyConditionCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, arrayNumberOfBlades, pointsBackThroughParams, delta_thickness, delta_angle, angle, thickness_T, thickness_B, thickness):
        self.arrayNumberOfBlades = arrayNumberOfBlades
        self.pointsBackThroughParams = pointsBackThroughParams
        self.delta_thickness = delta_thickness
        self.delta_angle = delta_angle
        self.angle = angle
        self.thickness_T = thickness_T
        self.thickness_B = thickness_B
        self.thickness = thickness