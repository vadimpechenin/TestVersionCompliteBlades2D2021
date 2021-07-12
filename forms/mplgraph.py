import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

class MPLgraph(FigureCanvasTkAgg):
    """The canvas-like matplotlib object used by View.
    """
    def __init__(self, figure, parent=None, **options):
        """
        argument:
            figure: a matplotlib.figure.Figure object
        """
        FigureCanvasTkAgg.__init__(self, figure, parent, **options)
        self.figure = figure
        self.add = figure.add_subplot(1,1,1)
        # .show() was deprecated and changed to .draw(). See:
        # https://github.com/matplotlib/matplotlib/pull/9275
        self.draw()
        self.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self, parent)
        self.toolbar.update()

    def plot(self, x, y, x_lab, y_lab):
        """Take two arrays for x and y coordinates and plot the data."""
        self.add.plot(x, y)
        self.add.set_xlabel(x_lab)
        self.add.set_ylabel(y_lab)
        self.figure.canvas.draw()  # DRAW IS CRITICAL TO REFRESH

    def plot_hist(self, data, x_lab, y_lab):
        """Take two arrays for x and y coordinates and plot the data."""
        self.add.hist(data, bins=6, histtype='stepfilled', color='steelblue')
        self.add.set_xlabel(x_lab)
        self.add.set_ylabel(y_lab)
        self.figure.canvas.draw()

    def clear(self):
        """Erase the plot."""
        self.add.clear()
        self.figure.canvas.draw()