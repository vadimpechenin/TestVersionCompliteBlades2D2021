from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class CalculationNominalscommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, thickness_B, angle, thickness_B_nom, shelf_width_B, shelf_width_half_B, slice_B, angle_slice, thickness_T, thickness_T_nom, shelf_width_T, shelf_width_half_T, slice_T):
        self.thickness_B = thickness_B
        self.angle = angle
        self.thickness_B_nom = thickness_B_nom
        self.shelf_width_B = shelf_width_B
        self.shelf_width_half_B = shelf_width_half_B
        self.slice_B = slice_B
        self.angle_slice = angle_slice
        self.thickness_T = thickness_T
        self.thickness_T_nom = thickness_T_nom
        self.shelf_width_T = shelf_width_T
        self.shelf_width_half_T = shelf_width_half_T
        self.slice_T = slice_T