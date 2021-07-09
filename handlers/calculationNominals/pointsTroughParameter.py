from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class PointsThroughParameter(BaseCommandHandlerParameter):
    def __init__(self, k0T,b0T,Point_1_T,Point_2_T,Point_3_T,Point_4_T, Point_01_T, Point_02_T):
        self.k0T = k0T
        self.b0T = b0T
        self.Point_1_T = Point_1_T
        self.Point_2_T = Point_2_T
        self.Point_3_T = Point_3_T
        self.Point_4_T = Point_4_T
        self.Point_01_T = Point_01_T
        self.Point_02_T = Point_02_T