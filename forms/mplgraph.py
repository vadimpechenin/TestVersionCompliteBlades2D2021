import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

import matplotlib.pyplot as plt

class DrawClass():
    def __init__(self,_VARS):
        self._VARS = _VARS

    def drawChart(self,figCanvasName,pltFigName,fig_aggName, dataXY, x_lab, y_lab):
        self._VARS[pltFigName] = plt.figure(figsize=(5.5, 4))
        plt.plot(dataXY[0], dataXY[1], 'k')
        plt.xlabel(x_lab)
        plt.ylabel(y_lab)
        self._VARS[fig_aggName] = self.draw_figure(
            self._VARS['window'][figCanvasName].TKCanvas, self._VARS[pltFigName])

    def drawHist(self,figCanvasName,pltFigName,fig_aggName,dataXY, x_lab, y_lab):
        self._VARS[pltFigName] = plt.figure(figsize=(4, 4))
        plt.hist(dataXY, bins=6, histtype='stepfilled', color='steelblue')
        plt.xlabel(x_lab)
        plt.ylabel(y_lab)
        self._VARS[fig_aggName] = self.draw_figure(
            self._VARS['window'][figCanvasName].TKCanvas, self._VARS[pltFigName])

    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def clearChart(self,figCanvasName,pltFigName,fig_aggName):
        self._VARS[fig_aggName].get_tk_widget().forget()
        self._VARS[pltFigName].clf()