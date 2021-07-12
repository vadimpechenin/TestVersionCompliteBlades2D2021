from handlers.baseCommandHandler import BaseCommandHandler
from handlers.calculationNominals.calculationNominalsСommandHandler import CalculationNominalscommandHandler
from handlers.calculationNominals.pointsForSquare import PointsForSquare
from .allCalculationAssemblyConditionParameter import AllCalculationAssemblyConditionParameter


import numpy as np
import copy

class CalculationAssemblyConditionCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Вычисления зазоров и натягов с заданных порядком лопаток
        thickness_T_array = parameters.delta_thickness * parameters.thickness_T / parameters.thickness
        thickness_B_array = parameters.delta_thickness * parameters.thickness_B / parameters.thickness
        arrayNumberOfBlades_num = parameters.arrayNumberOfBlades - 1

        P_B = PointsForSquare(parameters.pointsBackThroughParams.pointsBackParams.Point_1_B,
                              parameters.pointsBackThroughParams.pointsBackParams.Point_2_B,
                                 parameters.pointsBackThroughParams.pointsBackParams.Point_3_B,
                              parameters.pointsBackThroughParams.pointsBackParams.Point_4_B)
        P_T = PointsForSquare(parameters.pointsBackThroughParams.pointsTroughParams.Point_1_T, parameters.pointsBackThroughParams.pointsTroughParams.Point_2_T,
                                 parameters.pointsBackThroughParams.pointsTroughParams.Point_3_T, parameters.pointsBackThroughParams.pointsTroughParams.Point_4_T)
        calcSquare = CalculationNominalscommandHandler()
        gap_Squre_B = np.zeros(arrayNumberOfBlades_num.shape[0])
        gap_Squre_T = np.zeros(arrayNumberOfBlades_num.shape[0])
        delta_chord_T_B_array=np.zeros((arrayNumberOfBlades_num.shape[0],2))
        for i in arrayNumberOfBlades_num:
            gap_Squre_B[i] = self.model_blade_error_2D_B(thickness_B_array[i], parameters.delta_angle[i],
                                                         parameters.angle, parameters.pointsBackThroughParams.pointsBackParams.k0B,
                                                         parameters.pointsBackThroughParams.pointsBackParams.b0B, P_B,calcSquare)
            gap_Squre_T[i] = self.model_blade_error_2D_T(thickness_T_array[i], parameters.delta_angle[i],
                                                         parameters.angle, parameters.pointsBackThroughParams.pointsTroughParams.k0T,
                                                         parameters.pointsBackThroughParams.pointsTroughParams.b0T, P_T, calcSquare)

            delta_chord_T_B_array[i,:]= self.gap_function_1(gap_Squre_T[i], gap_Squre_B[i],
                                                                          parameters.pointsBackThroughParams.gap_Squre_T_nom, parameters.pointsBackThroughParams.gap_Squre_B_nom)

        gap = self.cycle_of_calculate_gaps(delta_chord_T_B_array[:,0], delta_chord_T_B_array[:,1], arrayNumberOfBlades_num.shape[0])

        assemblyGaps = AllCalculationAssemblyConditionParameter(delta_chord_T_B_array[:,0], delta_chord_T_B_array[:,1],gap)

        return assemblyGaps

    def model_blade_error_2D_B(self,thickness_B_array,angle_array,angle,k0B,b0B, P_B1, calcSquare):
        #Функция для расчета площади со стороны спинки
        P_B = copy.deepcopy(P_B1)
        # Увеличиваем координаты задающих точек и умножаем их на угол разворота
        rotate_matrix = np.zeros((2,2))
        rotate_matrix[0][0], rotate_matrix[0][1] = np.cos(angle_array), -np.sin(angle_array)
        rotate_matrix[1,0], rotate_matrix[1,1]= np.sin(angle_array), np.cos(angle_array)

        # Смещение точек
        P_B.P = P_B.P + np.full((P_B.P.shape[0],P_B.P.shape[1]), thickness_B_array/np.cos(angle))

        # Поворот точек

        P_B.P = P_B.P.dot(rotate_matrix)


        # Новые точки пересечения номинальной линии и четырехугольника
        k1 = (P_B.P[1,1]-P_B.P[2,1])/(P_B.P[1,0]-P_B.P[2,0])
        b1 = P_B.P[1,1]-k1*P_B.P[1,0]

        Point_02_B = np.zeros(2)
        Point_02_B[0], Point_02_B[1] = (b1-b0B)/(k0B-k1), k0B*((b1-b0B)/(k0B-k1))+b0B

        Point_01_B = np.zeros(2)
        if (abs(P_B.P[0,0]-P_B.P[3,0])>0.0001):
            k2 = (P_B.P[0,1]-P_B.P[3,1])/(P_B.P[0,0]-P_B.P[3,0])
            b2 = P_B.P[0,1]-k2*P_B.P[0,0]
            Point_01_B[0], Point_01_B[1] = (b2-b0B)/(k0B-k2), k0B*((b2-b0B)/(k0B-k2))+b0B
        else:
            Point_01_B[0], Point_01_B[1] = P_B.P[0,0], k0B*P_B.P[0,0]+b0B

        # Расчет площади четырехугольника
        Square_B = calcSquare.square_calculate(P_B)

        P_B0 = PointsForSquare(P_B.P[2,:], P_B.P[3,:],Point_01_B, Point_02_B)

        Square_B_nom0 = calcSquare.square_calculate(P_B0)

        # Превышение для расчета номинальных площадей натяга
        gap_Squre_B = Square_B - Square_B_nom0
        #print('Square_B: ' + str(Square_B) + '; Square_B_nom0: ' + str(Square_B_nom0))
        #print('P_B0: ', str(P_B0.P))
        return gap_Squre_B

    def model_blade_error_2D_T(self,thickness_T_array,angle_array,angle,k0T,b0T, P_T1, calcSquare):
        #Функция для расчета площади со стороны корыта
        P_T = copy.deepcopy(P_T1)
        # Увеличиваем координаты задающих точек и умножаем их на угол разворота
        rotate_matrix = np.zeros((2,2))
        rotate_matrix[0][0], rotate_matrix[0][1] = np.cos(angle_array), -np.sin(angle_array)
        rotate_matrix[1,0], rotate_matrix[1,1]= np.sin(angle_array), np.cos(angle_array)

        # Смещение точек
        P_T.P = P_T.P - np.full((P_T.P.shape[0],P_T.P.shape[1]), thickness_T_array/np.cos(angle))

        # Поворот точек

        P_T.P = P_T.P.dot(rotate_matrix)


        # Новые точки пересечения номинальной линии и четырехугольника
        k1 = (P_T.P[1,1]-P_T.P[2,1])/(P_T.P[1,0]-P_T.P[2,0])
        b1 = P_T.P[1,1]-k1*P_T.P[1,0]

        Point_02_T = np.zeros(2)
        Point_02_T[0], Point_02_T[1] = (b1-b0T)/(k0T-k1), k0T*((b1-b0T)/(k0T-k1))+b0T

        Point_01_T = np.zeros(2)
        if (abs(P_T.P[0,0]-P_T.P[3,0])>0.0001):
            k2 = (P_T.P[0,1]-P_T.P[3,1])/(P_T.P[0,0]-P_T.P[3,0])
            b2 = P_T.P[0,1]-k2*P_T.P[0,0]
            Point_01_T[0], Point_01_T[1] = (b2-b0T)/(k0T-k2), k0T*((b2-b0T)/(k0T-k2))+b0T
        else:
            Point_01_T[0], Point_01_T[1] = P_T.P[0,0], k0T*P_T.P[0,0]+b0T

        # Расчет площади четырехугольника
        Square_T = calcSquare.square_calculate(P_T)

        P_T0 = PointsForSquare(P_T.P[2,:], P_T.P[3,:],Point_01_T, Point_02_T)

        Square_T_nom0 = calcSquare.square_calculate(P_T0)

        # Превышение для расчета номинальных площадей натяга
        gap_Squre_B = Square_T-Square_T_nom0
        #print('Square_T: ' + str(Square_T) + '; Square_T_nom0: ' + str(Square_T_nom0))
        #print('P_B0: ', str(P_T0.P))

        return gap_Squre_B

    def gap_function_1(self, chord_T,chord_B, chord_T_nom, chord_B_nom):
        #Первая самая упрощенная модель расчета погрешностей одной лопатки для
        #дальнейшего расчета натягов в соединении
        #chord_T - хорда со стороны корыта
        #chord_B - хорда со стороны спинки
        #chord_T_array_nom, chord_B_nom - номинальные значения хорды со стороны
        #спинки и корыта

        #delta_chord_T, delta_chord_B - отклонения хорд со стороны корыта и спинки
        delta_chord_T_B = np.zeros(2)
        delta_chord_T_B[0] = chord_T - chord_T_nom
        delta_chord_T_B[1] = chord_B - chord_B_nom

        return delta_chord_T_B

    def function_calculate_gaps_1(self, delta_chord_B, delta_chord_T):
        # Упрощенная функция расчета натягов - зазоров - сумма превышения длин по
        # хорде

        # delta_chord_B, delta_chord_T - отклонения хорд со стороны спинки и корыта

        # gap - зазор - натяг в соединении
        gap = delta_chord_B + delta_chord_T
        return gap

    def cycle_of_calculate_gaps(self, delta_chord_B_array, delta_chord_T_array, number_of_blades):
        # Расстановка лопаток по порядковым номерам, оценка зазоров - натягов
        gaps = np.zeros(number_of_blades)
        for i in range(number_of_blades):
            if i < number_of_blades-1:
                gaps[i] = self.function_calculate_gaps_1(delta_chord_B_array[i], delta_chord_T_array[i + 1])
            else:
                gaps[i] = self.function_calculate_gaps_1(delta_chord_B_array[i], delta_chord_T_array[1])

        return gaps