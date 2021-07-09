from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class AllCalculationNomParameter(BaseCommandHandlerParameter):
    def __init__(self, pointsBackParams, pointsTroughParams):
        self.pointsBackParams = pointsBackParams
        self.pointsTroughParams = pointsTroughParams