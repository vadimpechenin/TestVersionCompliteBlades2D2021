from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class MPLGraphParameter(BaseCommandHandlerParameter):
    def __init__(self, figCanvasName,pltFigName,fig_aggName, dataXY_init, dataXY, tolerance, x_lab, y_lab, init_gap, N):
        self.figCanvasName = figCanvasName
        self.pltFigName = pltFigName
        self.fig_aggName = fig_aggName
        self.dataXY_init = dataXY_init
        self.dataXY = dataXY
        self.tolerance = tolerance
        self.x_lab = x_lab
        self.y_lab = y_lab
        self.init_gap = init_gap
        self.N = N