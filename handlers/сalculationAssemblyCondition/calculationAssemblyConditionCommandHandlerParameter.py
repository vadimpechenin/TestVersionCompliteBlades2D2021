from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class CalculationAssemblyConditionCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self, arrayNumberOfBlades, assemblyChord):
        self.arrayNumberOfBlades = arrayNumberOfBlades
        self.assemblyChord = assemblyChord