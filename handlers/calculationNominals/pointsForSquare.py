from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter
import numpy as np

class PointsForSquare(BaseCommandHandlerParameter):
    def __init__(self, Point_1_B,Point_2_B,Point_3_B,Point_4_B):
        self.P = np.zeros((4,2))
        self.P[0, 0], self.P[0, 1] = Point_1_B[0], Point_1_B[1]
        self.P[1, 0], self.P[1, 1] = Point_2_B[0], Point_2_B[1]
        self.P[2, 0], self.P[2, 1] = Point_3_B[0], Point_3_B[1]
        self.P[3, 0], self.P[3, 1] = Point_4_B[0], Point_4_B[1]