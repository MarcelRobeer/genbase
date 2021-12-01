"""Static & interactive plotting functions."""

import os
from typing import Callable

import pandas as pd
import plotly
import plotly.io as pio

ROOT_DIR = os.path.dirname(os.path.abspath(plotly.__file__))
PACKAGE_DIR = os.path.join(ROOT_DIR, 'package_data')
PLOTLYJS_FILE = os.path.join(PACKAGE_DIR, 'plotly.min.js')


def matplotlib_available() -> bool:
    """Check if `matplotlib` is installed.

    Returns:
        bool: True if available, False if not.
    """
    import importlib.util
    return importlib.util.find_spec('matplotlib') is not None


def plotly_available() -> bool:
    """Check if `plotly` is installed.

    Returns:
        bool: True if available, False if not.
    """
    import importlib.util
    return importlib.util.find_spec('plotly') is not None


class ExpressPlot:
    def __init__(self, df: pd.DataFrame, px_fn: Callable, *args, **kwargs):
        self.plot = px_fn(df, *args, **kwargs)

    @property
    def static(self):
        return self.to_png()

    @property
    def interactive(self) -> str:
        return self._repr_html_()

    def to_html(self, **kwargs) -> str:
        return pio.to_html(self.plot, **kwargs)

    def write_html(self, **kwargs):
        return pio.write_html(self.plot, **kwargs)

    def to_image(self, **kwargs):
        return pio.to_image(self.plot, **kwargs)

    def write_image(self, file: str, **kwargs):
        return pio.write_image(self.plot, file, **kwargs)

    def to_png(self, **kwargs):
        return pio.to_image(self.plot, format='png', **kwargs)

    def write_png(self, file: str, **kwargs):
        return pio.write_image(self.plot, file, **kwargs)

    def __str__(self) -> str:
        return str(self.plot)

    def _repr_html_(self) -> str:
        return pio.to_html(self.plot, full_html=False, include_plotlyjs='require')  # TODO: 'require' when offline
