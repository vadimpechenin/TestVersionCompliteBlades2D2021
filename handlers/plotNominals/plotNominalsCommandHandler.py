from handlers.baseCommandHandler import BaseCommandHandler
import matplotlib.pyplot as plt

class PlotNominalsCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Прорисовка номинальной геометрии
        fig=plt.figure()
        ax=fig.add_subplot(1,1,1)
        color = 'black'
        self.plot_line(ax, parameters.pointsBackThroughParams.pointsBackParams.Point_1_B,
                       parameters.pointsBackThroughParams.pointsBackParams.Point_2_B, color)

        self.plot_line(ax, parameters.pointsBackThroughParams.pointsBackParams.Point_2_B,
                       parameters.pointsBackThroughParams.pointsBackParams.Point_3_B, color)

        self.plot_line(ax, parameters.pointsBackThroughParams.pointsBackParams.Point_3_B,
                       parameters.pointsBackThroughParams.pointsBackParams.Point_4_B, color)

        self.plot_line(ax, parameters.pointsBackThroughParams.pointsBackParams.Point_4_B,
                       parameters.pointsBackThroughParams.pointsBackParams.Point_1_B, color)
        color = 'blue'
        self.plot_line(ax, parameters.pointsBackThroughParams.pointsBackParams.Point_01_B,
                       parameters.pointsBackThroughParams.pointsBackParams.Point_02_B, color)

        self.plot_line(ax, parameters.pointsBackThroughParams.pointsTroughParams.Point_01_T,
                       parameters.pointsBackThroughParams.pointsTroughParams.Point_02_T, color)

        color = 'red'
        self.plot_line(ax, parameters.pointsBackThroughParams.pointsTroughParams.Point_1_T,
                       parameters.pointsBackThroughParams.pointsTroughParams.Point_2_T, color)

        self.plot_line(ax, parameters.pointsBackThroughParams.pointsTroughParams.Point_2_T,
                       parameters.pointsBackThroughParams.pointsTroughParams.Point_3_T, color)

        self.plot_line(ax, parameters.pointsBackThroughParams.pointsTroughParams.Point_3_T,
                       parameters.pointsBackThroughParams.pointsTroughParams.Point_4_T, color)

        self.plot_line(ax, parameters.pointsBackThroughParams.pointsTroughParams.Point_4_T,
                       parameters.pointsBackThroughParams.pointsTroughParams.Point_1_T, color)

        ax.axis('equal')
        ax.set_title('Сечение лопатки')
        fig.show()

    def plot_line(self, ax, P1, P2, color):
        x = [P1[0],
             P2[0]]
        y = [P1[1],
             P2[1]]
        ax.plot(x, y, 'k', color=color, linewidth=2)