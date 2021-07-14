from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class PlacementBladesCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, arrayNumberOfBlades, assemblyChord):
        self.arrayNumberOfBlades = arrayNumberOfBlades
        self.assemblyChord = assemblyChord