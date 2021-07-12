from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class AllCalculationAssemblyConditionParameter(BaseCommandHandlerParameter):
    def __init__(self, delta_chord_T_array, delta_chord_B_array,gap):
        self.delta_chord_T_array = delta_chord_T_array
        self.delta_chord_B_array = delta_chord_B_array
        self.gap = gap
