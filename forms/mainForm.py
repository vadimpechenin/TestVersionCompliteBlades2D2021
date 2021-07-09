"""
Класс для прорисовки формы
"""
from handlers.loadNominals.loadNominalsCommandHandlerParameter import LoadNominalsCommandHandlerParameter
from handlers.generateMeasure.generateMeasureCommandHandlerParameter import GenerateMeasureCommandHandlerParameter
from handlers.loadMeasure.loadMeasureCommandHandlerParameter import LoadMeasureCommandHandlerParameter
from handlers.calculationNominals.calculationNominalsСommandHandlerParameter import CalculationNominalscommandHandlerParameter

from forms.mplgraph import MPLgraph
import os
import tkinter as tk

import matplotlib as mpl
mpl.use("TkAgg")  # MUST be invoked prior to importing mpl backends!
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)  # NavigationToolbar2TkAgg was deprecated
import numpy as np
import PySimpleGUI as sg


class MainForm():
    def __init__(self,handler,settings):
        #Математика приложения
        self.handler = handler
        #Переменные, с которыми будет работать форма
        self.settings = settings


        self.number_of_blades = None
        self.T_thickness = [None, None] # Допуск на толщину
        self.T_angle = [None, None] # Допуск на угол
        self.delta_thickness = None
        self.delta_angle = None

        self.thickness = None  # Номинальное значение толщины, обеспечивающее натяг
        self.thickness_T = None   # толщина до точки вращения со стороны корыта
        self.thickness_B = None   # толщина до точки вращения со стороны спинки
        self.thickness_T_nom = None
        self.thickness_B_nom = None
        self.angle = None # Угол антивибрационной полки

        # Толщина полки со стороны корыта
        self.shelf_width_T = None
        self.shelf_width_half_T = None  #
        self.T_shelf_width_half_T = [None, None]  #

        # Толщина полки со стороны спинки
        self.shelf_width_B = None
        self.shelf_width_half_B = None  #
        self.T_shelf_width_half_B = [None, None] #

        # Угол и расстояния для срезов лопаток
        self.angle_slice = None
        self.slice_B = None # со стороны спинки
        self.slice_T = None # со стороны корыта

        self.filedb = ''

    def show(self):
        figure_w, figure_h = 300, 300
        layout = [
            [sg.Text('Количество лопаток'), sg.InputText('84', key='-numberblades-'), sg.Text('exponent'), sg.InputText('1', key='-null-')],
            [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-'),
             sg.Canvas(size=(figure_w, figure_h), key='-CANVAS2-')],
            [sg.Multiline(size=(40, 10), key = '_output_'), sg.Multiline(size=(40, 10), key = '_output2_')],
            [sg.Submit(), sg.Exit(), sg.Button('Загрузить номинальные значения'), sg.Button('Вычислить номинальные параметры'), sg.Button('Загрузить измерения'), sg.Button('Генерация измерений')],#, sg.Output
            [sg.Input(key='-databasename-'), sg.FileBrowse()]
        ]
        window = sg.Window('MVC Test', layout, grab_anywhere=True, finalize=True)
        figure = mpl.figure.Figure(figsize=(4, 3), dpi=100)  # 5, 4
        # Первое окно
        canvas = MPLgraph(figure, window['-CANVAS-'].TKCanvas)
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH)  # expand=tk.YES,
        canvas.plot(*self.powerplot(1, 1))
        # Второе окно
        canvas2 = MPLgraph(figure, window['-CANVAS2-'].TKCanvas)
        canvas2._tkcanvas.pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH)
        canvas2.plot(*self.powerplot(1, 1))

        while True:
            event, values = window.Read()  # event = name of event; values = {0: str, 0: str} of entry values
            if event in (None, 'Exit'):  # If user closed window with X or if user clicked "Exit" event then exit
                break
            if event == 'Submit':
                x, y = self.powerplot(float(values['-numberblades-']), float(values['-null-']))
                canvas.clear()
                canvas.plot(x, y)

            if event == 'Загрузить номинальные значения':
                window.FindElement('_output_').Update('')
                self.settings.SetValue(self.settings.filedb_name, os.path.basename(values['-databasename-']))
                if len(self.settings.GetValue(self.settings.filedb_name))==0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                parameters = LoadNominalsCommandHandlerParameter(self.settings.GetValue(self.settings.filedb_name), 'nominal')
                window['_output_'].print('Load from database: ' + self.settings.GetValue(self.settings.filedb_name))
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

                window['_output_'].print('Parameters: ' + str(result_request))

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
                result_request = self.handler.initFunction(3, parameters)

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
                window.FindElement('_output2_').Update('')
                window['_output2_']. print('You entered ', result_request)

            if event == 'Загрузить измерения':
                window.FindElement('_output_').Update('')
                self.settings.SetValue(self.settings.filedb_name, os.path.basename(values['-databasename-']))
                if len(self.settings.GetValue(self.settings.filedb_name)) == 0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                parameters = LoadMeasureCommandHandlerParameter(self.settings.GetValue(self.settings.filedb_name),
                                                                'measure')
                window['_output2_'].print('Load from database: ' + self.settings.GetValue(self.settings.filedb_name))
                result_request = self.handler.initFunction(2, parameters)
                window.FindElement('_output2_').Update('')
                window['_output2_'].print('Parameters: ' + str(result_request))
                #Вывод всплывающего окна и выход из запроса
                number_of_blades_dict = result_request.pop()
                self.settings.SetValue(self.settings.number_of_blades_name, number_of_blades_dict[0]['Количество'])
                window.FindElement('-numberblades-').Update(str(self.settings.GetValue(self.settings.number_of_blades_name)))
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
        window.close()

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

    def powerplot2(self,base, exponent):
        """
        Calculates data for plotting the function: y = (base * x) ** exponent,
        for x = 0...10.
        Arguments: base and exponent as floats
        Returns: two numpy arrays of x and y coordinates (length 800).
        """

        x = np.linspace(0, 10, 800)
        y = (x * base) ** exponent
        return x, y