import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

import matplotlib.pyplot as plt

class DrawClass():
    def __init__(self,_VARS):
        self._VARS = _VARS

    def drawChart(self,param):
        self._VARS[param.pltFigName] = plt.figure(figsize=(5.5, 4))
        plt.plot(param.dataXY_init[0], param.dataXY_init[1], 'b', label='До комплектации')
        if param.init_gap == 0:
            plt.plot(param.dataXY[0], param.dataXY[1], 'g', label='После комплектации')
        color1 = 'r'
        self.tolerance_plot_chart(plt, param.tolerance,
                            param.N, color1, 3)
        plt.xlabel(param.x_lab)
        plt.ylabel(param.y_lab)
        plt.legend()
        self._VARS[param.fig_aggName] = self.draw_figure(
            self._VARS['window'][param.figCanvasName].TKCanvas, self._VARS[param.pltFigName])

    def drawHist(self,param):
        self._VARS[param.pltFigName] = plt.figure(figsize=(4, 4))
        plt.hist(param.dataXY_init, bins=6, histtype='stepfilled', color='steelblue', label='До комплектации')
        if param.init_gap == 0:
            plt.hist(param.dataXY, bins=6, histtype='stepfilled', color='green', label='После комплектации')
        color1 = 'r'
        self.tolerance_plot(plt, param.tolerance,
                            param.N / 3, color1, 3)
        plt.xlabel(param.x_lab)
        plt.ylabel(param.y_lab)
        plt.legend()
        self._VARS[param.fig_aggName] = self.draw_figure(
            self._VARS['window'][param.figCanvasName].TKCanvas, self._VARS[param.pltFigName])

    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def clearChart(self,param):
        self._VARS[param.fig_aggName].get_tk_widget().forget()
        self._VARS[param.pltFigName].clf()

    def tolerance_plot(self,plt, T, N,color,width):
        #Функция прорисоки границы поля допуска
        plt.plot([T[0], T[0]], [0, N], color, linewidth = width)
        plt.plot([T[1], T[1]], [0, N], color, linewidth = width)

    def tolerance_plot_chart(self,plt, T, N,color,width):
        #Функция прорисоки границы поля допуска
        plt.plot([0, N], [T[0], T[0]], color, linewidth = width)
        plt.plot([0, N], [T[1], T[1]], color, linewidth = width)