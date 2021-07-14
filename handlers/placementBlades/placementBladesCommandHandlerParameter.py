from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class PlacementBladesCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, arrayNumberOfBlades, assemblyGaps):
        self.arrayNumberOfBlades = arrayNumberOfBlades
        self.assemblyGaps = assemblyGaps