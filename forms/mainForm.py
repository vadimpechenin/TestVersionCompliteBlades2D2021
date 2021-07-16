"""
Класс для прорисовки формы
"""
from handlers.loadNominals.loadNominalsCommandHandlerParameter import LoadNominalsCommandHandlerParameter
from handlers.generateMeasure.generateMeasureCommandHandlerParameter import GenerateMeasureCommandHandlerParameter
from handlers.loadMeasure.loadMeasureCommandHandlerParameter import LoadMeasureCommandHandlerParameter
from handlers.calculationNominals.calculationNominalsСommandHandlerParameter import CalculationNominalscommandHandlerParameter
from handlers.plotNominals.plotNominalsCommandHandlerParameter import PlotNominalsCommandHandlerParameter
from handlers.сalculationAssemblyCondition.calculationAssemblyConditionCommandHandlerParameter import CalculationAssemblyConditionCommandHandlerParameter
from handlers.placementBlades.placementBladesCommandHandlerParameter import PlacementBladesCommandHandlerParameter
from handlers.calculationChordsOfBlades.calculationChordsOfBladesCommandHandlerParameter import CalculationChordsOfBladesCommandHandlerParameter
from handlers.saveNumbers.saveNumbersCommandHandlerParameter import SaveNumbersCommandHandlerParameter
from handlers.plotMeasures.plotMeasuresCommandHandlerParameter import PlotMeasuresCommandHandlerParameter
from forms.mplgraphParameter import MPLGraphParameter


from forms.mplgraph import DrawClass
import os
import math


import matplotlib as mpl
mpl.use("TkAgg")  # MUST be invoked prior to importing mpl backends!

import numpy as np
import PySimpleGUI as sg


init_gap = 1


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
                     }
    def show(self):
        global init_gap #Переменная для сохранения начального gap, до оптимальной расстановки

        AppFont = 'Any 16'
        sg.theme('black')
        figure_w, figure_h = 200, 200
        layout = [
            [sg.Text('Количество лопаток'), sg.InputText('84', key='-numberblades-')],
            [sg.Canvas(size=(figure_w, figure_h), key='figCanvas1'),
             sg.Canvas(size=(figure_w, figure_h), key='figCanvas2')],
            [sg.Multiline(size=(40, 10), key = '_output_'), sg.Multiline(size=(50, 10), key = '_output2_'), sg.Multiline(size=(35, 10), key = '_output3_')],
            [sg.Button('Выход', font=AppFont), sg.Button('Загрузить номинальные значения'), sg.Button('Вычислить номинальные параметры'), sg.Button('Загрузить измерения'), sg.Button('Генерация измерений'), sg.Button('2D Прорисовка')],#, sg.Output
            [sg.Input(key='-databasename-', size=(31, 1)), sg.FileBrowse(), sg.Button('Расчет сборочного состояния'), sg.Button('Расстановка лопаток'), sg.Button('Сохранение комплекта'), sg.Button('Гистограммы статистики')]
        ]
        self._VARS['window']  = sg.Window('MVC Test', layout, grab_anywhere=True, finalize=True,
                            resizable=True,background_color='#FDF6E3')
        drawClass = DrawClass(self._VARS)


        figCanvasName1 = 'figCanvas1'
        figCanvasName2 = 'figCanvas2'

        fig_aggName1 = 'fig_agg1'
        fig_aggName2 = 'fig_agg2'

        pltFigName1 = 'pltFig1'
        pltFigName2 = 'pltFig2'

        dataXY_init = (0, 0)
        dataXY= (0, 0)

        T_gap = [0.35, 0.45]
        T_gap = [0.05, 1.2]
        parameter_plot = MPLGraphParameter(figCanvasName1, pltFigName1, fig_aggName1,dataXY_init, dataXY, T_gap, '№ лопатки', 'Зазор, мм', init_gap, 84)
        drawClass.drawChart(parameter_plot)
        drawClass.clearChart(parameter_plot)

        parameter_plot = MPLGraphParameter(figCanvasName2, pltFigName2, fig_aggName2,dataXY_init, dataXY,T_gap,'Зазорб мм', 'Количество', init_gap, 84)
        drawClass.drawHist(parameter_plot)
        drawClass.clearChart(parameter_plot)


        while True:
            event, values = self._VARS['window'].Read()  # event = name of event; values = {0: str, 0: str} of entry values
            if event == sg.WIN_CLOSED or event == 'Выход':
                break
            if event == 'Загрузить номинальные значения':
                self._VARS['window'].FindElement('_output_').Update('')
                self.settings.SetValue(self.settings.filedb_name, os.path.basename(values['-databasename-']))
                if len(self.settings.GetValue(self.settings.filedb_name))==0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                parameters = LoadNominalsCommandHandlerParameter(self.settings.GetValue(self.settings.filedb_name), 'nominal')
                self._VARS['window']['_output_'].print('Загружено из базы данных: ' + self.settings.GetValue(self.settings.filedb_name))
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


                list_russian = ['тип лопатки', 'номинальная толщина', 'толщина', 'нижнее поле допуска толщины',
                                'верхнее поле допуска толщины','толщина со стороны корыта','толщина со стороны спинки',
                                'номинальная толщина со стороны корыта','номинальная толщина со стороны спинки',
                                'угол закрутки','нинее поле допуска угла','верхнее поле допуска угла',
                                'ширина полки со стороны корыта',
                                'ширина полки со стороны корыта до оси','нижнее поле допуска ширины','верхнее поле допуска ширины',
                                'ширина полки со стороны спинки',
                                'ширина полки со стороны спинки до оси', 'нижнее поле допуска ширины',
                                'верхнее поле допуска ширины',
                                'угол скоса', 'расстояние до скоса на спинке', 'расстояние до скоса на корыте']
                self._VARS['window']['_output_'].print('Конструкторские параметры: ')
                for key in result_request[0]:
                    self._VARS['window']['_output_'].print(list_russian.pop(0) +': ' + str(round(result_request[0][key],3)))

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

                init_gap = 1
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
                                                                    'measure', 'numbers', 'serial_number',
                                                                    self.settings.GetValue(self.settings.delta_thickness_name),
                                                                    self.settings.GetValue(self.settings.delta_angle_name))
                responce_dict = self.handler.initFunction(1, parameters)

                result_request = responce_dict['meas']

                self._VARS['window'].FindElement('_output2_').Update('')
                self._VARS['window']['_output2_'].print('Измеренные параметры: ')

                for i in range (self.settings.GetValue(self.settings.number_of_blades_name)):
                    deviation_dict = result_request.pop(0)
                    delta_thickness = deviation_dict['delta_thickness']
                    delta_angle = deviation_dict['delta_angle']
                    self._VARS['window']['_output2_'].print('№ лопатки: ' + str(i+1) + '; отклонение толщины: ' +
                                                            str(round(delta_thickness, 3)) + '; отклонение угла: '
                                                            + str(round(delta_angle*180/math.pi, 3)))

                #Массив порядоковых номеров лопаток в комплекте
                arrayNumberOfBlades = np.linspace(1, self.settings.GetValue(self.settings.number_of_blades_name),
                                                  self.settings.GetValue(self.settings.number_of_blades_name),
                                                  endpoint=True).astype('int64')
                arrayNumberOfBlades_list = responce_dict['number']
                for i in range (self.settings.GetValue(self.settings.number_of_blades_name)):
                    arrayNumberOfBlades_dict = arrayNumberOfBlades_list.pop(0)
                    arrayNumberOfBlades[i] = arrayNumberOfBlades_dict['serial_number']


                self.settings.SetValue(self.settings.arrayNumberOfBlades_name, arrayNumberOfBlades)
                self._VARS['window'].FindElement('_output3_').Update('')
                self._VARS['window']['_output3_'].print('Порядок лопаток: ', arrayNumberOfBlades)

                parameters = CalculationChordsOfBladesCommandHandlerParameter(self.settings.GetValue(self.settings.arrayNumberOfBlades_name),
                                                                                 self.settings.GetValue(self.settings.pointsBackThroughParams_name),
                                                                                 self.settings.GetValue(self.settings.delta_thickness_name),
                                                                                 self.settings.GetValue(self.settings.delta_angle_name),
                                                                                 self.settings.GetValue(
                                                                                     self.settings.angle_name),
                                                                                 self.settings.GetValue(self.settings.thickness_T_name),
                                                                                 self.settings.GetValue(self.settings.thickness_B_name),
                                                                                 self.settings.GetValue(self.settings.thickness_name))
                assemblyChord = self.handler.initFunction(6, parameters)
                self.settings.SetValue(self.settings.assemblyChord_name, assemblyChord)

            if event == 'Загрузить измерения':

                init_gap = 1
                self._VARS['window'].FindElement('_output2_').Update('')
                self.settings.SetValue(self.settings.filedb_name, os.path.basename(values['-databasename-']))
                if len(self.settings.GetValue(self.settings.filedb_name)) == 0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                parameters = LoadMeasureCommandHandlerParameter(self.settings.GetValue(self.settings.filedb_name),
                                                                'measure','numbers', 'serial_number')
                self._VARS['window']['_output2_'].print('Загружено из базы данных: ' + self.settings.GetValue(self.settings.filedb_name))


                responce_dict = self.handler.initFunction(2, parameters)

                result_request = responce_dict['meas']

                self._VARS['window']['_output2_'].print('Измеренные параметры: ')
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
                    self._VARS['window']['_output2_'].print('№ лопатки: ' + str(i+1) + '; отклонение толщины: ' +
                                                            str(round(delta_thickness[i], 3)) + '; отклонение угла: '
                                                            + str(round(delta_angle[i]*180/math.pi, 3)))

                self.settings.SetValue(self.settings.delta_thickness_name, delta_thickness)
                self.settings.SetValue(self.settings.delta_angle_name, delta_angle)

                #Массив порядоковых номеров лопаток в комплекте
                arrayNumberOfBlades = np.linspace(1, self.settings.GetValue(self.settings.number_of_blades_name),
                                                  self.settings.GetValue(self.settings.number_of_blades_name),
                                                  endpoint=True).astype('int64')

                arrayNumberOfBlades_list = responce_dict['number']
                for i in range (self.settings.GetValue(self.settings.number_of_blades_name)):
                    arrayNumberOfBlades_dict = arrayNumberOfBlades_list.pop(0)
                    arrayNumberOfBlades[i] = arrayNumberOfBlades_dict['serial_number']

                self.settings.SetValue(self.settings.arrayNumberOfBlades_name, arrayNumberOfBlades)
                self._VARS['window'].FindElement('_output3_').Update('')
                self._VARS['window']['_output3_'].print('Порядок лопаток: ', arrayNumberOfBlades)

                parameters = CalculationChordsOfBladesCommandHandlerParameter(self.settings.GetValue(self.settings.arrayNumberOfBlades_name),
                                                                                 self.settings.GetValue(self.settings.pointsBackThroughParams_name),
                                                                                 self.settings.GetValue(self.settings.delta_thickness_name),
                                                                                 self.settings.GetValue(self.settings.delta_angle_name),
                                                                                 self.settings.GetValue(
                                                                                     self.settings.angle_name),
                                                                                 self.settings.GetValue(self.settings.thickness_T_name),
                                                                                 self.settings.GetValue(self.settings.thickness_B_name),
                                                                                 self.settings.GetValue(self.settings.thickness_name))
                assemblyChord = self.handler.initFunction(6, parameters)
                self.settings.SetValue(self.settings.assemblyChord_name, assemblyChord)


            if event == 'Расчет сборочного состояния':

                # Рассчет сборки с учетом существующей расстановки
                if self.settings.GetValue(self.settings.number_of_blades_name) == 0 or self.settings.GetValue(
                        self.settings.number_of_blades_name) == None:
                    sg.PopupAnnoying('Нет данных по измеренным отклонениям')  # Просто запускает окно
                    continue
                if self.settings.GetValue(self.settings.assemblyChord_name) == None:
                    sg.PopupAnnoying('Не загружены значения допусков')  # Просто запускает окно
                    continue
                parameters = CalculationAssemblyConditionCommandHandlerParameter(self.settings.GetValue(self.settings.arrayNumberOfBlades_name),
                                                                                 self.settings.GetValue(self.settings.assemblyChord_name))
                assemblyGaps = self.handler.initFunction(5, parameters)

                self.settings.SetValue(self.settings.assemblyGaps_name,assemblyGaps)
                #Начальное состояние зазоров
                if init_gap == 1:
                    self.settings.SetValue(self.settings.assemblyGaps_init_name, assemblyGaps)

                x_array = np.linspace(1, parameters.arrayNumberOfBlades.shape[0],parameters.arrayNumberOfBlades.shape[0])


                #Отрисовка результатов
                parameter_plot = MPLGraphParameter(figCanvasName1, pltFigName1, fig_aggName1, (x_array, self.settings.GetValue(self.settings.assemblyGaps_init_name)), (x_array, assemblyGaps),
                                                   T_gap, '№ лопатки', 'Зазор, мм', init_gap,self.settings.GetValue(self.settings.number_of_blades_name))
                drawClass.clearChart(parameter_plot)
                drawClass.drawChart(parameter_plot)


                parameter_plot = MPLGraphParameter(figCanvasName2, pltFigName2, fig_aggName2, self.settings.GetValue(self.settings.assemblyGaps_init_name), assemblyGaps,
                                                   T_gap, 'Зазор, мм', 'Количество', init_gap,self.settings.GetValue(self.settings.number_of_blades_name))
                drawClass.clearChart(parameter_plot)
                drawClass.drawHist(parameter_plot)


            if event == 'Расстановка лопаток':

                init_gap = 0
                # Алгоритм расстановки лопаток методом сортировки
                if self.settings.GetValue(self.settings.number_of_blades_name) == 0 or self.settings.GetValue(
                        self.settings.number_of_blades_name) == None:
                    sg.PopupAnnoying('Нет данных по измеренным отклонениям')  # Просто запускает окно
                    continue
                parameters = PlacementBladesCommandHandlerParameter(
                    self.settings.GetValue(self.settings.arrayNumberOfBlades_name),
                    self.settings.GetValue(self.settings.assemblyChord_name),
                   )
                arrayNumberOfBlades_sort = self.handler.initFunction(7, parameters)
                self.settings.SetValue(self.settings.arrayNumberOfBlades_name, arrayNumberOfBlades_sort)
                self._VARS['window'].FindElement('_output3_').Update('')
                self._VARS['window']['_output3_'].print('Порядок лопаток после расстановки: ', arrayNumberOfBlades_sort)

            if event == 'Сохранение комплекта':
                self.settings.SetValue(self.settings.filedb_name, os.path.basename(values['-databasename-']))
                if len(self.settings.GetValue(self.settings.filedb_name)) == 0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                if self.settings.GetValue(self.settings.number_of_blades_name) == 0 or self.settings.GetValue(
                        self.settings.number_of_blades_name) == None:
                    sg.PopupAnnoying('Нет данных по измеренным отклонениям')  # Просто запускает окно
                    continue
                parameters = SaveNumbersCommandHandlerParameter(self.settings.GetValue(self.settings.filedb_name),
                                                                'numbers',
                                                                self.settings.GetValue(self.settings.arrayNumberOfBlades_name))

                self.handler.initFunction(8, parameters)
                sg.PopupAnnoying('Схема расстановки лопаток успешно сохранена')

            if  event == 'Гистограммы статистики':
                #Отрисовка измеренных отклонений хорд и углов
                if self.settings.GetValue(self.settings.number_of_blades_name) == 0 or self.settings.GetValue(
                        self.settings.number_of_blades_name) == None:
                    sg.PopupAnnoying('Нет данных по измеренным отклонениям')  # Просто запускает окно
                    continue
                parameters = PlotMeasuresCommandHandlerParameter(self.settings.GetValue(self.settings.T_thickness_name),
                                                                 self.settings.GetValue(self.settings.T_angle_name),
                                                                 self.settings.GetValue(self.settings.delta_thickness_name),
                                                                 self.settings.GetValue(self.settings.delta_angle_name),
                                                                'Отклонение хорды, мм','Отклонение угла закрутки, град')
                self.handler.initFunction(9, parameters)

        self._VARS['window'].close()


