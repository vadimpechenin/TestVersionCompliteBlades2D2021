from handlers.baseCommandHandler import BaseCommandHandler
#from handlers.calculationNominals.calculationNominalsСommandHandler import CalculationNominalscommandHandler
#from handlers.calculationNominals.pointsForSquare import PointsForSquare
#from .allCalculationAssemblyConditionParameter import AllCalculationAssemblyConditionParameter


import numpy as np
#import copy

class CalculationAssemblyConditionCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):

        gap = self.cycle_of_calculate_gaps(parameters.assemblyChord.delta_chord_B_array, parameters.assemblyChord.delta_chord_T_array, parameters.arrayNumberOfBlades, parameters.arrayNumberOfBlades.shape[0])

        return gap

    def function_calculate_gaps_1(self, delta_chord_B, delta_chord_T):
        # Упрощенная функция расчета натягов - зазоров - сумма превышения длин по
        # хорде

        # delta_chord_B, delta_chord_T - отклонения хорд со стороны спинки и корыта

        # gap - зазор - натяг в соединении
        gap = delta_chord_B + delta_chord_T
        return gap

    def cycle_of_calculate_gaps(self, delta_chord_B_array, delta_chord_T_array, arrayNumberOfBlades, number_of_blades):
        # Расстановка лопаток по порядковым номерам, оценка зазоров - натягов
        arrayNumberOfBlades_num = arrayNumberOfBlades-1
        delta_chord_B_array_new = delta_chord_B_array[arrayNumberOfBlades_num]
        delta_chord_T_array_new = delta_chord_T_array[arrayNumberOfBlades_num]
        gaps = np.zeros(number_of_blades)
        for i in range(number_of_blades):
            if i < number_of_blades-1:
                gaps[i] = self.function_calculate_gaps_1(delta_chord_B_array_new[i], delta_chord_T_array_new[i + 1])
            else:
                gaps[i] = self.function_calculate_gaps_1(delta_chord_B_array_new[i], delta_chord_T_array_new[1])

        return gaps