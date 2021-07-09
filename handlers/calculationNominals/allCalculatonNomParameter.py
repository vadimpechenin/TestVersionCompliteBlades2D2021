from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class AllCalculationNomParameter(BaseCommandHandlerParameter):
    def __init__(self, pointsBackParams, pointsTroughParams,gap_Squre_B_nom,gap_Squre_T_nom):
        self.pointsBackParams = pointsBackParams
        self.pointsTroughParams = pointsTroughParams
        self.gap_Squre_B_nom = gap_Squre_B_nom
        self.gap_Squre_T_nom = gap_Squre_T_nom