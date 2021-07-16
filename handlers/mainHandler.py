"""
Описывает базовый класс для тестирования комплектации лопаток
"""

from handlers.loadNominals.loadNominalsCommandHandler import LoadNominalsCommandHandler
from handlers.generateMeasure.generateMeasureCommandHandler import GenerateMeasureCommandHandler
from handlers.loadMeasure.loadMeasureCommandHandler import LoadMeasureCommandHandler
from handlers.calculationNominals.calculationNominalsСommandHandler import CalculationNominalscommandHandler
from handlers.plotNominals.plotNominalsCommandHandler import PlotNominalsCommandHandler
from handlers.сalculationAssemblyCondition.сalculationAssemblyConditionCommandHandler import CalculationAssemblyConditionCommandHandler
from handlers.placementBlades.placementBladesCommandHandler import PlacementBladesCommandHandler
from handlers.calculationChordsOfBlades.calculationChordsOfBladesCommandHandler import CalculationChordsOfBladesCommandHandler
from handlers.saveNumbers.saveNumbersCommandHandler import SaveNumbersCommandHandler
from handlers.plotMeasures.plotMeasuresCommandHandler import PlotMeasuresCommandHandler

class MainHandler():
    def __init__(self):
        self.dict = {}
        self.dict[0] = LoadNominalsCommandHandler()
        self.dict[1] = GenerateMeasureCommandHandler()
        self.dict[2] = LoadMeasureCommandHandler()
        self.dict[3] = CalculationNominalscommandHandler()
        self.dict[4] = PlotNominalsCommandHandler()
        self.dict[5] = CalculationAssemblyConditionCommandHandler()
        self.dict[6] = CalculationChordsOfBladesCommandHandler()
        self.dict[7] = PlacementBladesCommandHandler()
        self.dict[8] = SaveNumbersCommandHandler()
        self.dict[9] = PlotMeasuresCommandHandler()

    def initFunction(self,code_request, parameter):
        result = None
        if code_request in self.dict:
            handler = self.dict[code_request]
            result = handler.execute(parameter)

        return result