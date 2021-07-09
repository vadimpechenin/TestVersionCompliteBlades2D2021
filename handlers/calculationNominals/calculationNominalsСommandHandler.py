from handlers.baseCommandHandler import BaseCommandHandler

from .pointsBackParameter import PointsBackParameter
from .pointsTroughParameter import PointsThroughParameter
from .allCalculatonNomParameter import AllCalculationNomParameter
from .pointsForSquare import PointsForSquare

import numpy as np

class CalculationNominalscommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Вычисление необходимых номинальных значений
        # Вычисление всех (4) задающих точек и поиск площади превышения номинальной стыковки
        # Со стороны спинки
        pointsBackParams = self.function_poisk_points_back_2D(parameters)
        # Со стороны корыта
        pointsTroughParams = self.function_poisk_points_trough_2D(parameters)
        # Расчет площадей
        params = PointsForSquare(pointsBackParams.Point_1_B, pointsBackParams.Point_2_B,
                                 pointsBackParams.Point_3_B, pointsBackParams.Point_4_B)
        Square_B_nom = self.square_calculate(params)
        params = PointsForSquare(pointsTroughParams.Point_1_T, pointsTroughParams.Point_2_T,
                                 pointsTroughParams.Point_3_T, pointsTroughParams.Point_4_T)
        Square_T_nom = self.square_calculate(params)
        params = PointsForSquare(pointsBackParams.Point_3_B, pointsBackParams.Point_4_B,
                                 pointsBackParams.Point_01_B, pointsBackParams.Point_02_B)
        Square_B_nom0 = self.square_calculate(params)
        params = PointsForSquare(pointsTroughParams.Point_3_T, pointsTroughParams.Point_4_T,
                                 pointsTroughParams.Point_01_T, pointsTroughParams.Point_02_T)
        Square_T_nom0 = self.square_calculate(params)
        #Номинальное превышение для расчета номинальных площадей натяга
        gap_Squre_B_nom = Square_B_nom-Square_B_nom0
        gap_Squre_T_nom = Square_T_nom-Square_T_nom0

        ciphers = AllCalculationNomParameter(pointsBackParams, pointsTroughParams, gap_Squre_B_nom, gap_Squre_T_nom)
        #Наборы точек для смещения и разворота
        return ciphers

    def square_calculate(self,parameters):
        # Формула расчета площади  произвольного четырехугольника, информации о его вершинах
        d1 = np.sqrt((parameters.P[0][0] - parameters.P[2][0])**2 + (parameters.P[0][1] - parameters.P[2][1]) ** 2)
        d2 = np.sqrt((parameters.P[1, 0] - parameters.P[3, 0]) ** 2 + (parameters.P[1, 1] - parameters.P[3, 1]) **2)

        k1 = (parameters.P[0, 1] - parameters.P[2, 1]) / (parameters.P[0, 0] - parameters.P[2, 0])

        k2 = (parameters.P[1, 1] - parameters.P[3, 1]) / (parameters.P[1, 0] - parameters.P[3, 0])


        fi = np.arccos((k1 * k2 + 1) / (np.sqrt(k1 ** 2 + 1) * np.sqrt(k2 ** 2 + 1)))

        Square_B_nom = d1 * d2 * np.sin(fi) / 2

        return Square_B_nom

    def function_poisk_points_back_2D(self, parameters):
        # Поиск всей геометрии на спинке для решения задачи
        Point0 = np.zeros(2)
        Point0[0], Point0[1] = 0, parameters.thickness_B / np.cos(parameters.angle)
        Point0nom = np.zeros(2)
        Point0nom[0], Point0nom[1] = 0, parameters.thickness_B_nom / np.cos(parameters.angle)

        # Уравнение типа y = kx + b
        b1 = parameters.thickness_B / np.cos(parameters.angle)
        k1 = -np.tan(parameters.angle)
        k0B = -np.tan(parameters.angle)
        b0B = parameters.thickness_B_nom / np.cos(parameters.angle)
        Point_1_B = np.zeros(2)
        Point_1_B[0], Point_1_B[1]= parameters.shelf_width_B - parameters.shelf_width_half_B, \
                                    k1*(parameters.shelf_width_B - parameters.shelf_width_half_B) + b1

        Point_2d_B = np.zeros(2)
        Point_2d_B[0], Point_2d_B[1] = -parameters.shelf_width_half_B, k1 * (-parameters.shelf_width_half_B) + b1

        Point0slice = np.zeros(2)
        Point0slice[0], Point0slice[1]  = -parameters.slice_B / np.cos(parameters.angle_slice), 0
        b2 = parameters.slice_B / np.cos(parameters.angle_slice)
        k2 = np.tan(parameters.angle_slice)
        # Точки пересечения скоса и линий лопаток
        # С вертикальной
        Point_3_B = np.zeros(2)
        Point_3_B[0], Point_3_B[1] = -parameters.shelf_width_half_B, k2 * (-parameters.shelf_width_half_B) + b2
        Point_2_B = np.zeros(2)
        Point_2_B[0], Point_2_B[1] = (b2 - b1) / (k1 - k2), k1 * ((b2 - b1) / (k1 - k2)) + b1
        b4 = Point_3_B[1] - k1 * Point_3_B[0]
        Point_4_B = np.zeros(2)
        Point_4_B[0], Point_4_B[1] = (parameters.shelf_width_B - parameters.shelf_width_half_B),\
                                     k1 * (parameters.shelf_width_B - parameters.shelf_width_half_B) + b4

        # Точки пересечения с фигурой
        Point_01_B = np.zeros(2)
        Point_01_B[0], Point_01_B[1]= parameters.shelf_width_B - parameters.shelf_width_half_B, \
                                    k0B * (parameters.shelf_width_B - parameters.shelf_width_half_B) + b0B
        Point_02_B = np.zeros(2)
        Point_02_B[0],  Point_02_B[1] = (b2 - b0B) / (k0B - k2), \
                                         k0B * ((b2 - b0B) / (k0B - k2)) + b0B
        pointsBackParams = PointsBackParameter(k0B,b0B,Point_1_B,Point_2_B,Point_3_B,Point_4_B, Point_01_B, Point_02_B)
        return pointsBackParams

    def function_poisk_points_trough_2D(self, parameters):
        # Поиск всей геометрии на спинке для решения задачи
        Point0 = np.zeros(2)
        Point0[0], Point0[1] = 0, -parameters.thickness_T / np.cos(parameters.angle)
        Point0nom = np.zeros(2)
        Point0nom[0], Point0nom[1] = 0, -parameters.thickness_T_nom / np.cos(parameters.angle)

        # Уравнение типа y = kx + b
        b1 = -parameters.thickness_T / np.cos(parameters.angle)
        k1 = -np.tan(parameters.angle)
        k0B = -np.tan(parameters.angle)
        b0B = -parameters.thickness_T_nom / np.cos(parameters.angle)
        Point_1_B = np.zeros(2)
        Point_1_B[0], Point_1_B[1] = -(parameters.shelf_width_T - parameters.shelf_width_half_T), \
                                     k1 * (-(parameters.shelf_width_T - parameters.shelf_width_half_T)) + b1

        Point_2d_B = np.zeros(2)
        Point_2d_B[0], Point_2d_B[1] = parameters.shelf_width_half_T, k1 * (parameters.shelf_width_half_T) + b1

        Point0slice = np.zeros(2)
        Point0slice[0], Point0slice[1] = parameters.slice_T / np.cos(parameters.angle_slice), 0
        b2 = -parameters.slice_T / np.cos(parameters.angle_slice)
        k2 = np.tan(parameters.angle_slice)
        # Точки пересечения скоса и линий лопаток
        # С вертикальной
        Point_3_B = np.zeros(2)
        Point_3_B[0], Point_3_B[1] = parameters.shelf_width_half_T, k2 * (parameters.shelf_width_half_T) + b2
        Point_2_B = np.zeros(2)
        Point_2_B[0], Point_2_B[1] = (b2 - b1) / (k1 - k2), k1 * ((b2 - b1) / (k1 - k2)) + b1
        b4 = Point_3_B[1] - k1 * Point_3_B[0]
        Point_4_B = np.zeros(2)
        Point_4_B[0], Point_4_B[1] = (-(parameters.shelf_width_T - parameters.shelf_width_half_T)), \
                                     k1 * (-(parameters.shelf_width_T - parameters.shelf_width_half_T)) + b4

        # Точки пересечения с фигурой
        Point_01_B = np.zeros(2)
        Point_01_B[0], Point_01_B[1] = -(parameters.shelf_width_T - parameters.shelf_width_half_T), \
                                       k0B * (-(parameters.shelf_width_T - parameters.shelf_width_half_T)) + b0B
        Point_02_B = np.zeros(2)
        Point_02_B[0], Point_02_B[1] = (b2 - b0B) / (k0B - k2), \
                                       k0B * ((b2 - b0B) / (k0B - k2)) + b0B
        pointsTroughParams = PointsThroughParameter(k0B,b0B,Point_1_B,Point_2_B,Point_3_B,Point_4_B, Point_01_B, Point_02_B)
        return pointsTroughParams