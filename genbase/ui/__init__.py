"""Extensible user interfaces (UIs) for `genbase` dependencies."""

from typing import Sequence, Union

import matplotlib.cm
import matplotlib.colors

from genbase.ui.notebook import Render, format_instances, is_interactive
from genbase.ui.plot import matplotlib_available


def get_color(value: Union[float, Sequence[float]],
              min_value: float = -1.0,
              max_value: float = 1.0,
              colorscale: Union[list, str] = 'RdYlGn',
              format: str = 'hex') -> Union[str, Sequence[str]]:
    """Get color from a `matplotlib` colorscale.

    Args:
        value (Union[float, Sequence[float]]): Value(s) to convert. Will be clamped to `[min_value, max_value]`.
        min_value (float, optional): Minimum scale value. Defaults to -1.0.
        max_value (float, optional): Maximum scale value. Defaults to 1.0.
        colorscale (Union[list, str], optional): `matplotlib` scale definition or colorscale name. Defaults to 'RdYlGn'.
        format (str, optional): Return format 'hex'/'rgb'. Defaults to 'hex'.

    Raises:
        ValueError: `min_value` is not smaller than `max_value`, unknown format ().
        ImportError: Cannot import `matplotlib`.

    Returns:
        Union[str, Sequence[str]]: Named color(s) in selected format.
    """
    if min_value >= max_value:
        raise ValueError(f'min_value should be smaller than max_value, but is {min_value} ({max_value=})')

    is_float = False

    if isinstance(value, float):
        is_float = True
        value = [value]
    if not isinstance(value, list):
        value = list(value)

    if not matplotlib_available():
        raise ImportError('Currently requires `matplotlib` to be installed!')

    # Clamp value
    value = [min(max(v, min_value), max_value) for v in value]

    if isinstance(colorscale, str):
        cmap = matplotlib.cm.get_cmap(colorscale)
    else:
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list('', colorscale)

    res = [cmap(int((v - min_value) / (max_value - min_value) * cmap.N)) for v in value]
    if format == 'hex':
        res = [matplotlib.colors.rgb2hex(v) for v in res]
    return res[0] if is_float else res
