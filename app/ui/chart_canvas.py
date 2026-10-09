"""Small wrapper that embeds a Matplotlib figure in a Qt widget."""
from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class ChartCanvas(FigureCanvasQTAgg):
    def __init__(self, width=6, height=3.5):
        self.figure = Figure(figsize=(width, height))
        super().__init__(self.figure)

    def draw_with(self, chart_function, **kwargs):
        """Call one of the functions from app/charts.py and repaint."""
        chart_function(self.figure, **kwargs)
        self.draw()
