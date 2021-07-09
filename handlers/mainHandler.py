"""
Описывает базовый класс для тестирования комплектации лопаток
"""

from handlers.loadNominals.loadNominalsCommandHandler import LoadNominalsCommandHandler
from handlers.generateMeasure.generateMeasureCommandHandler import GenerateMeasureCommandHandler
from handlers.loadMeasure.loadMeasureCommandHandler import LoadMeasureCommandHandler
from handlers.calculationNominals.calculationNominalsСommandHandler import CalculationNominalscommandHandler

class MainHandler():
    def __init__(self):
        self.dict = {}
        self.dict[0] = LoadNominalsCommandHandler()
        self.dict[1] = GenerateMeasureCommandHandler()
        self.dict[2] = LoadMeasureCommandHandler()
        self.dict[3] = CalculationNominalscommandHandler()


    def initFunction(self,code_request, parameter):
        result = None
        if code_request in self.dict:
            handler = self.dict[code_request]
            result = handler.execute(parameter)

        return result