"""
Класс для прорисовки формы
"""
from handlers.loadNominals.loadNominalsCommandHandlerParameter import LoadNominalsCommandHandlerParameter
from handlers.generateMeasure.generateMeasureCommandHandlerParameter import GenerateMeasureCommandHandlerParameter
from handlers.loadMeasure.loadMeasureCommandHandlerParameter import LoadMeasureCommandHandlerParameter
from handlers.calculationNominals.calculationNominalsСommandHandlerParameter import CalculationNominalscommandHandlerParameter
from handlers.plotNominals.plotNominalsCommandHandlerParameter import PlotNominalsCommandHandlerParameter
from handlers.сalculationAssemblyCondition.calculationAssemblyConditionCommandHandlerParameter import CalculationAssemblyConditionCommandHandlerParameter


from forms.mplgraph import DrawClass
import os


import matplotlib as mpl
mpl.use("TkAgg")  # MUST be invoked prior to importing mpl backends!

import numpy as np
import PySimpleGUI as sg


class MainForm():
    def __init__(self,handler,settings):
        #Математика приложения
        self.handler = handler
        #Переменные, с которыми будет работать форма
        self.settings = settings
        # Переменные для прорисовки
        self._VARS = {'window': False,
                     'fig_agg1': False,
                     'pltFig1': False,
                     'fig_agg2': False,
                     'pltFig2': False,
                     'fig_agg3': False,
                     'pltFig3': False,
                      'fig_agg4': False,
                      'pltFig4': False
                     }
    def show(self):
        figure_w, figure_h = 200, 200
        layout = [
            [sg.Text('Количество лопаток'), sg.InputText('84', key='-numberblades-')],
            [sg.Canvas(size=(figure_w, figure_h), key='figCanvas1'),
             sg.Canvas(size=(figure_w, figure_h), key='figCanvas2'),
             sg.Canvas(size=(figure_w, figure_h), key='figCanvas3'),
             sg.Canvas(size=(figure_w, figure_h), key='figCanvas4')],
            [sg.Multiline(size=(30, 10), key = '_output_'), sg.Multiline(size=(30, 10), key = '_output2_'), sg.Multiline(size=(60, 10), key = '_output3_')],
            [sg.Exit(), sg.Button('Загрузить номинальные значения'), sg.Button('Вычислить номинальные параметры'), sg.Button('Загрузить измерения'), sg.Button('Генерация измерений'), sg.Button('2D Прорисовка')],#, sg.Output
            [sg.Input(key='-databasename-'), sg.FileBrowse(), sg.Button('Расчет сборочного состояния'), sg.Button('Расстановка лопаток'), sg.Button('Сохранение комплекта')]
        ]
        self._VARS['window']  = sg.Window('MVC Test', layout, grab_anywhere=True, finalize=True,
                            resizable=True,background_color='#FDF6E3')
        drawClass = DrawClass(self._VARS)


        figCanvasName1 = 'figCanvas1'
        figCanvasName2 = 'figCanvas2'
        figCanvasName3 = 'figCanvas3'
        figCanvasName4 = 'figCanvas4'

        fig_aggName1 = 'fig_agg1'
        fig_aggName2 = 'fig_agg2'
        fig_aggName3 = 'fig_agg3'
        fig_aggName4 = 'fig_agg4'

        pltFigName1 = 'pltFig1'
        pltFigName2 = 'pltFig2'
        pltFigName3 = 'pltFig3'
        pltFigName4 = 'pltFig4'

        dataXY = (0, 0)
        drawClass.drawChart(figCanvasName1, pltFigName1, fig_aggName1,dataXY,'№ лопатки', 'Зазор')
        drawClass.drawHist(figCanvasName2, pltFigName2, fig_aggName2,dataXY,'Зазор', 'Количество')
        drawClass.drawHist(figCanvasName3, pltFigName3, fig_aggName3,dataXY[0], 'Отклонение толщины', 'Количество')
        drawClass.drawHist(figCanvasName4, pltFigName4, fig_aggName4, dataXY[0], 'Отклонение толщины', 'Количество')
        drawClass.clearChart(figCanvasName1, pltFigName1, fig_aggName1)
        drawClass.clearChart(figCanvasName2, pltFigName2, fig_aggName2)
        drawClass.clearChart(figCanvasName3, pltFigName3, fig_aggName3)
        drawClass.clearChart(figCanvasName4, pltFigName4, fig_aggName4)

        while True:
            event, values = self._VARS['window'].Read()  # event = name of event; values = {0: str, 0: str} of entry values
            if event in (None, 'Exit'):  # If user closed window with X or if user clicked "Exit" event then exit
                break

            if event == 'Загрузить номинальные значения':
                self._VARS['window'].FindElement('_output_').Update('')
                self.settings.SetValue(self.settings.filedb_name, os.path.basename(values['-databasename-']))
                if len(self.settings.GetValue(self.settings.filedb_name))==0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                parameters = LoadNominalsCommandHandlerParameter(self.settings.GetValue(self.settings.filedb_name), 'nominal')
                self._VARS['window']['_output_'].print('Load from database: ' + self.settings.GetValue(self.settings.filedb_name))
                result_request = self.handler.initFunction(0, parameters)
                #Сохранение переменных формы
                self.settings.SetValue(self.settings.T_thickness_name, [result_request[0]['T_thickness_lower'],
                                                                                  result_request[0]['T_thickness_upper']])
                self.settings.SetValue(self.settings.T_angle_name, [result_request[0]['T_angle_lower'],
                                                                        result_request[0]['T_angle_upper']])

                self.settings.SetValue(self.settings.thickness_name, result_request[0]['thickness']) # Номинальное значение толщины, обеспечивающее натяг
                self.settings.SetValue(self.settings.thickness_T_name, result_request[0]['thickness_T']) # толщина до точки вращения со стороны корыта
                self.settings.SetValue(self.settings.thickness_B_name, result_request[0]['thickness_B']) # толщина до точки вращения со стороны спинки
                self.settings.SetValue(self.settings.thickness_T_nom_name, result_request[0]['thickness_T_nom'])
                self.settings.SetValue(self.settings.thickness_B_nom_name, result_request[0]['thickness_B_nom'])
                self.settings.SetValue(self.settings.angle_name, result_request[0]['angle']) # Угол антивибрационной полки

                # Толщина полки со стороны корыта
                self.settings.SetValue(self.settings.shelf_width_T_name, result_request[0]['shelf_width_T'])
                self.settings.SetValue(self.settings.shelf_width_half_T_name, result_request[0]['shelf_width_half_T'])
                self.settings.SetValue(self.settings.T_shelf_width_half_T_name, [result_request[0]['T_shelf_width_half_T_lower'],
                                                                        result_request[0]['T_shelf_width_half_T_upper']])

                # Толщина полки со стороны спинки
                self.settings.SetValue(self.settings.shelf_width_B_name, result_request[0]['shelf_width_B'])
                self.settings.SetValue(self.settings.shelf_width_half_B_name, result_request[0]['shelf_width_half_B'])
                self.settings.SetValue(self.settings.T_shelf_width_half_B_name,
                                       [result_request[0]['T_shelf_width_half_B_lower'],
                                        result_request[0]['T_shelf_width_half_B_upper']])

                # Угол и расстояния для срезов лопаток
                self.settings.SetValue(self.settings.angle_slice_name, result_request[0]['angle_slice'])
                self.settings.SetValue(self.settings.slice_B_name, result_request[0]['slice_B'])# со стороны спинки
                self.settings.SetValue(self.settings.slice_T_name, result_request[0]['slice_T'])# со стороны корыта

                self._VARS['window']['_output_'].print('Parameters: ' + str(result_request))

            if event == 'Вычислить номинальные параметры':
                if self.settings.GetValue(self.settings.thickness_name)==None:
                    sg.PopupAnnoying('Не загружены значения допусков')  # Просто запускает окно
                    continue
                parameters = CalculationNominalscommandHandlerParameter(self.settings.GetValue(self.settings.thickness_B_name),
                            self.settings.GetValue(self.settings.angle_name), self.settings.GetValue(self.settings.thickness_B_nom_name),
                                                                        self.settings.GetValue(
                                                                            self.settings.shelf_width_B_name),
                                                                        self.settings.GetValue(
                                                                            self.settings.shelf_width_half_B_name),
                                                                        self.settings.GetValue(
                                                                            self.settings.slice_B_name),
                                                                        self.settings.GetValue(
                                                                            self.settings.angle_slice_name),
                                                                        self.settings.GetValue(
                                                                            self.settings.thickness_T_name),
                                                                        self.settings.GetValue(
                                                                            self.settings.thickness_T_nom_name),
                                                                        self.settings.GetValue(
                                                                            self.settings.shelf_width_T_name),
                                                                        self.settings.GetValue(
                                                                            self.settings.shelf_width_half_T_name),
                                                                        self.settings.GetValue(
                                                                            self.settings.slice_T_name))
                pointsBackThroughParams = self.handler.initFunction(3, parameters)
                self.settings.SetValue(self.settings.pointsBackThroughParams_name, pointsBackThroughParams)

            if event == '2D Прорисовка':
                if self.settings.GetValue(self.settings.pointsBackThroughParams_name) == None:
                    sg.PopupAnnoying('Не рассчитаны производные параметры')  # Просто запускает окно
                    continue
                parameters = PlotNominalsCommandHandlerParameter(self.settings.GetValue(self.settings.pointsBackThroughParams_name))
                self.handler.initFunction(4, parameters)

            if event == 'Генерация измерений':
                self.settings.SetValue(self.settings.filedb_name, os.path.basename(values['-databasename-']))
                if len(self.settings.GetValue(self.settings.filedb_name)) == 0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue

                self.settings.SetValue(self.settings.number_of_blades_name, int(values['-numberblades-']))
                #self.number_of_blades = int(values['-numberblades-'])
                if (self.settings.GetValue(self.settings.shelf_width_B_name)==None):
                    sg.PopupAnnoying('Не загружены значения допусков')  # Просто запускает окно
                    continue
                T_thickness = self.settings.GetValue(self.settings.T_thickness_name)
                self.settings.SetValue(self.settings.delta_thickness_name, np.random.normal((T_thickness[1]+T_thickness[0])/2,
                                                   (T_thickness[1]-T_thickness[0])/6, size = self.settings.GetValue(self.settings.number_of_blades_name)))
                T_angle_name = self.settings.GetValue(self.settings.T_angle_name)
                self.settings.SetValue(self.settings.delta_angle_name, np.random.normal((T_angle_name[1] + T_angle_name[0])/2,
                                                   (T_angle_name[1] - T_angle_name[0])/6, size = self.settings.GetValue(self.settings.number_of_blades_name)))

                parameters = GenerateMeasureCommandHandlerParameter(self.settings.GetValue(self.settings.filedb_name),
                                                                    'measure',
                                                                    self.settings.GetValue(self.settings.delta_thickness_name),
                                                                    self.settings.GetValue(self.settings.delta_angle_name))
                result_request = self.handler.initFunction(1, parameters)
                self._VARS['window'].FindElement('_output2_').Update('')
                self._VARS['window']['_output2_']. print('You entered ', result_request)

                #Массив порядоковых номеров лопаток в комплекте
                arrayNumberOfBlades = np.linspace(1, self.settings.GetValue(self.settings.number_of_blades_name),
                                                  self.settings.GetValue(self.settings.number_of_blades_name),
                                                  endpoint=True).astype('int64')
                self.settings.SetValue(self.settings.arrayNumberOfBlades_name, arrayNumberOfBlades)
                self._VARS['window'].FindElement('_output3_').Update('')
                self._VARS['window']['_output3_'].print('Порядок лопаток: ', arrayNumberOfBlades)

            if event == 'Загрузить измерения':
                self._VARS['window'].FindElement('_output2_').Update('')
                self.settings.SetValue(self.settings.filedb_name, os.path.basename(values['-databasename-']))
                if len(self.settings.GetValue(self.settings.filedb_name)) == 0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                parameters = LoadMeasureCommandHandlerParameter(self.settings.GetValue(self.settings.filedb_name),
                                                                'measure')
                self._VARS['window']['_output2_'].print('Load from database: ' + self.settings.GetValue(self.settings.filedb_name))
                result_request = self.handler.initFunction(2, parameters)

                self._VARS['window']['_output2_'].print('Parameters: ' + str(result_request))
                #Вывод всплывающего окна и выход из запроса
                number_of_blades_dict = result_request.pop()
                self.settings.SetValue(self.settings.number_of_blades_name, number_of_blades_dict[0]['Количество'])
                self._VARS['window'].FindElement('-numberblades-').Update(str(self.settings.GetValue(self.settings.number_of_blades_name)))
                if self.settings.GetValue(self.settings.number_of_blades_name)==0 or self.settings.GetValue(self.settings.number_of_blades_name)==None:
                    sg.PopupAnnoying('Нет данных по измеренным отклонениям')  # Просто запускает окно
                    continue
                #Сохранение отклонений
                delta_thickness = np.zeros(self.settings.GetValue(self.settings.number_of_blades_name))
                delta_angle = np.zeros(self.settings.GetValue(self.settings.number_of_blades_name))
                for i in range (self.settings.GetValue(self.settings.number_of_blades_name)):
                    deviation_dict = result_request.pop(0)
                    delta_thickness[i] = deviation_dict['delta_thickness']
                    delta_angle[i] = deviation_dict['delta_angle']

                self.settings.SetValue(self.settings.delta_thickness_name, delta_thickness)
                self.settings.SetValue(self.settings.delta_angle_name, delta_angle)

                #Массив порядоковых номеров лопаток в комплекте
                arrayNumberOfBlades = np.linspace(1, self.settings.GetValue(self.settings.number_of_blades_name),
                                                  self.settings.GetValue(self.settings.number_of_blades_name),
                                                  endpoint=True).astype('int64')
                self.settings.SetValue(self.settings.arrayNumberOfBlades_name, arrayNumberOfBlades)
                self._VARS['window'].FindElement('_output3_').Update('')
                self._VARS['window']['_output3_'].print('Порядок лопаток: ', arrayNumberOfBlades)

            if event == 'Расчет сборочного состояния':
                # Рассчет сборки с учетом существующей расстановки
                if self.settings.GetValue(self.settings.number_of_blades_name) == 0 or self.settings.GetValue(
                        self.settings.number_of_blades_name) == None:
                    sg.PopupAnnoying('Нет данных по измеренным отклонениям')  # Просто запускает окно
                    continue
                if self.settings.GetValue(self.settings.thickness_name) == None:
                    sg.PopupAnnoying('Не загружены значения допусков')  # Просто запускает окно
                    continue
                parameters = CalculationAssemblyConditionCommandHandlerParameter(self.settings.GetValue(self.settings.arrayNumberOfBlades_name),
                                                                                 self.settings.GetValue(self.settings.pointsBackThroughParams_name),
                                                                                 self.settings.GetValue(self.settings.delta_thickness_name),
                                                                                 self.settings.GetValue(self.settings.delta_angle_name),
                                                                                 self.settings.GetValue(
                                                                                     self.settings.angle_name),
                                                                                 self.settings.GetValue(self.settings.thickness_T_name),
                                                                                 self.settings.GetValue(self.settings.thickness_B_name),
                                                                                 self.settings.GetValue(self.settings.thickness_name))
                assemblyGaps = self.handler.initFunction(5, parameters)

                self.settings.SetValue(self.settings.assemblyGaps_name,assemblyGaps)


                x_array = np.linspace(1,parameters.arrayNumberOfBlades.shape[0],parameters.arrayNumberOfBlades.shape[0])

                drawClass.clearChart(figCanvasName1, pltFigName1, fig_aggName1)
                drawClass.clearChart(figCanvasName2, pltFigName2, fig_aggName2)
                drawClass.clearChart(figCanvasName3, pltFigName3, fig_aggName3)
                drawClass.clearChart(figCanvasName4, pltFigName4, fig_aggName4)
                drawClass.drawChart(figCanvasName1, pltFigName1, fig_aggName1, (x_array, assemblyGaps.gap),'№ лопатки', 'Зазор')
                drawClass.drawHist(figCanvasName2, pltFigName2, fig_aggName2, assemblyGaps.gap, 'Зазор', 'Количество')
                drawClass.drawHist(figCanvasName3, pltFigName3, fig_aggName3, parameters.delta_thickness, 'Отклонение толщины',
                                   'Количество')
                drawClass.drawHist(figCanvasName4, pltFigName4, fig_aggName4, parameters.delta_angle, 'Отклонение угла',
                                   'Количество')


            if event == 'Расстановка лопаток':
                pass
            if event == 'Сохранение комплекта':
                pass

        self._VARS['window'].close()


    def plot_gap(self,number_of_blades,gap):
        pass

    def powerplot(self,base, exponent):
        """
        Calculates data for plotting the function: y = (base * x) ** exponent,
        for x = 0...10.
        Arguments: base and exponent as floats
        Returns: two numpy arrays of x and y coordinates (length 800).
        """

        x = np.linspace(0, 10, 800)
        y = (x * base) ** exponent
        return x, y
