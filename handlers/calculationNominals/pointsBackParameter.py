from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class PointsBackParameter(BaseCommandHandlerParameter):
    def __init__(self, k0B,b0B,Point_1_B,Point_2_B,Point_3_B,Point_4_B, Point_01_B, Point_02_B):
        self.k0B = k0B
        self.b0B = b0B
        self.Point_1_B = Point_1_B
        self.Point_2_B = Point_2_B
        self.Point_3_B = Point_3_B
        self.Point_4_B = Point_4_B
        self.Point_01_B = Point_01_B
        self.Point_02_B = Point_02_B