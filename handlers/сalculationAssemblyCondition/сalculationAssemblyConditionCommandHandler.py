from handlers.baseCommandHandler import BaseCommandHandler
from handlers.calculationNominals.calculationNominalsСommandHandler import CalculationNominalscommandHandler
from handlers.calculationNominals.pointsForSquare import PointsForSquare

import numpy as np



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
        for i in arrayNumberOfBlades_num:
            gap_Squre_B[i] = self.model_blade_error_2D_B(thickness_B_array[i], parameters.delta_angle[i],
                                                         parameters.angle, parameters.pointsBackThroughParams.pointsBackParams.k0B,
                                                         parameters.pointsBackThroughParams.pointsBackParams.b0B, P_B,calcSquare)

        return gap_Squre_B

    def model_blade_error_2D_B(self,thickness_B_array,angle_array,angle,k0B,b0B, P_B, calcSquare):
        #Функция для расчета площади со стороны спинки

        # Увеличиваем координаты задающих точек и умножаем их на угол разворота
        rotate_matrix = np.zeros((2,2))
        rotate_matrix[0,0],rotate_matrix[0,1],
        rotate_matrix[1,0],rotate_matrix[1,1]= np.cos(angle_array), -np.sin(angle_array),
        np.sin(angle_array), np.cos(angle_array)

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
        gap_Squre_B = Square_B-Square_B_nom0

        return gap_Squre_B