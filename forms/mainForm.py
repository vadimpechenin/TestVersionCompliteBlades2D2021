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
    def __init__(self,handler):
        self.handler = handler
        #Переменные, с которыми будет работать форма
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
                # window['_output_'].TKOut.output.config(wrap='word')  # set Output element word wrapping
                self.filedb = os.path.basename(values['-databasename-'])
                if len(self.filedb)==0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                parameters = LoadNominalsCommandHandlerParameter(self.filedb, 'nominal')
                window['_output_'].print('Load from database: ' + self.filedb)
                result_request = self.handler.initFunction(0, parameters)
                #Сохранение переменных формы
                self.T_thickness[0], self.T_thickness[1] = result_request[0]['T_thickness_lower'], \
                                                           result_request[0]['T_thickness_upper']
                self.T_angle[0], self.T_angle[1]  = result_request[0]['T_angle_lower'], \
                                                           result_request[0]['T_angle_upper']

                self.thickness = result_request[0]['thickness'] # Номинальное значение толщины, обеспечивающее натяг
                self.thickness_T = result_request[0]['thickness_T']  # толщина до точки вращения со стороны корыта
                self.thickness_B = result_request[0]['thickness_B']  # толщина до точки вращения со стороны спинки
                self.thickness_T_nom = result_request[0]['thickness_T_nom']
                self.thickness_B_nom = result_request[0]['thickness_B_nom']
                self.angle = result_request[0]['angle']  # Угол антивибрационной полки

                # Толщина полки со стороны корыта
                self.shelf_width_T = result_request[0]['shelf_width_T']
                self.shelf_width_half_T = result_request[0]['shelf_width_half_T']  #
                self.T_shelf_width_half_T[0], self.T_shelf_width_half_T[1] = \
                    result_request[0]['T_shelf_width_half_T_lower'], result_request[0]['T_shelf_width_half_T_upper']  #

                # Толщина полки со стороны спинки
                self.shelf_width_B = result_request[0]['shelf_width_B']
                self.shelf_width_half_B = result_request[0]['shelf_width_half_B']  #
                self.T_shelf_width_half_B[0], self.T_shelf_width_half_B[1] = \
                    result_request[0]['T_shelf_width_half_B_lower'], result_request[0]['T_shelf_width_half_B_upper']  #

                # Угол и расстояния для срезов лопаток
                self.angle_slice = result_request[0]['angle_slice']
                self.slice_B = result_request[0]['slice_B']  # со стороны спинки
                self.slice_T = result_request[0]['slice_T']  # со стороны корыта

                window['_output_'].print('Parameters: ' + str(result_request))

            if event == 'Вычислить номинальные параметры':
                if self.thickness==None:
                    sg.PopupAnnoying('Не загружены значения допусков')  # Просто запускает окно
                    continue
                parameters = CalculationNominalscommandHandlerParameter(self.thickness_B, self.angle, self.thickness_B_nom,
                                                                 self.shelf_width_B, self.shelf_width_half_B, self.slice_B,
                                                                 self.angle_slice, self.thickness_T, self.thickness_T_nom,
                                                                 self.shelf_width_T, self.shelf_width_half_T, self.slice_T)
                result_request = self.handler.initFunction(3, parameters)

            if event == 'Генерация измерений':
                self.filedb = os.path.basename(values['-databasename-'])
                if len(self.filedb)==0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                self.number_of_blades = int(values['-numberblades-'])
                if (self.T_thickness[0]==None):
                    sg.PopupAnnoying('Не загружены значения допусков')  # Просто запускает окно
                    continue
                self.delta_thickness = np.random.normal((self.T_thickness[1]+self.T_thickness[0])/2,
                                                   (self.T_thickness[1]-self.T_thickness[0])/6, size = self.number_of_blades)
                self.delta_angle = np.random.normal((self.T_angle[1] + self.T_angle[0])/2,
                                                   (self.T_angle[1] - self.T_angle[0])/6, size = self.number_of_blades)
                parameters = GenerateMeasureCommandHandlerParameter(self.filedb, 'measure', self.delta_thickness, self.delta_angle)
                result_request = self.handler.initFunction(1, parameters)
                window.FindElement('_output2_').Update('')
                window['_output2_']. print('You entered ', result_request)

            if event == 'Загрузить измерения':
                window.FindElement('_output_').Update('')
                self.filedb = os.path.basename(values['-databasename-'])
                if len(self.filedb)==0:
                    sg.PopupAnnoying('Не указана или отсутствует база данных')  # Просто запускает окно
                    continue
                parameters = LoadMeasureCommandHandlerParameter(self.filedb,'measure')
                window['_output2_'].print('Load from database: ' + self.filedb)
                result_request = self.handler.initFunction(2, parameters)
                window.FindElement('_output2_').Update('')
                window['_output2_'].print('Parameters: ' + str(result_request))
                #Вывод всплывающего окна и выход из запроса
                number_of_blades_dict = result_request.pop()
                self.number_of_blades = number_of_blades_dict[0]['Количество']
                window.FindElement('-numberblades-').Update(str(self.number_of_blades))
                if self.number_of_blades==0 or self.number_of_blades==None:
                    sg.PopupAnnoying('Нет данных по измеренным отклонениям')  # Просто запускает окно
                    continue
                #Сохранение отклонений
                self.delta_thickness = np.zeros(self.number_of_blades)
                self.delta_angle = np.zeros(self.number_of_blades)
                for i in range (self.number_of_blades):
                    deviation_dict = result_request.pop(0)
                    self.delta_thickness[i] = deviation_dict['delta_thickness']
                    self.delta_angle[i] = deviation_dict['delta_angle']
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