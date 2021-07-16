from handlers.baseCommandHandler import BaseCommandHandler
import matplotlib.pyplot as plt

import math

class PlotMeasuresCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Прорисовка измеренных отклоенний
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        color = 'steelblue'
        color1 = 'r'
        ax1.hist(parameters.delta_thickness, bins=6, histtype='stepfilled', color=color)
        self.tolerance_plot(ax1, parameters.T_thickness, parameters.delta_thickness.shape[0]/3, color1,3)
        ax1.set_xlabel(parameters.name_thickness)
        ax1.set_ylabel('Количество')
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.hist(parameters.delta_angle*180/math.pi, bins=6, histtype='stepfilled', color=color)
        self.tolerance_plot(ax2, [parameters.T_angle[0]*180/math.pi,parameters.T_angle[1]*180/math.pi], parameters.delta_angle.shape[0] / 3, color1,3)
        ax2.set_xlabel(parameters.name_angle)
        ax2.set_ylabel('Количество')
        fig.show()
    def tolerance_plot(self,ax, T, N,color,width):
        #Функция прорисоки границы поля допуска
        ax.plot([T[0], T[0]], [0, N], color, linewidth = width)
        ax.plot([T[1], T[1]], [0, N], color, linewidth = width)