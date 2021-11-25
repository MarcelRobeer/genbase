"""Utility functions."""

from typing import Any, Dict, Iterator, List, Optional, Tuple

import numpy as np
from instancelib import (AbstractClassifier, Environment, Instance,
                         InstanceProvider, LabelProvider)


def export_instancelib(obj) -> Dict[str, Any]:
    """`instancelib`-specific safe exports."""
    if isinstance(obj, Environment):
        return {'dataset': export_instancelib(obj.dataset),
                'labels': export_instancelib(obj.labels)}
    elif isinstance(obj, Instance):
        return {k.lstrip('_'): export_safe(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, LabelProvider):
        return {'labelset': export_safe(obj._labelset),
                'labeldict': {k: export_safe(v) for k, v in obj._labeldict.items()}}
    elif hasattr(obj, 'all_data'):
        return list(obj.all_data())
    elif hasattr(obj, '__dict__'):
        return dict(recursive_to_dict(obj))
    return None  # TODO: update


def export_safe(obj):
    """Safely export to transform into .json or .yaml."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (frozenset, set)):
        return list(obj)
    elif isinstance(obj, (list, tuple)):
        return [dict(recursive_to_dict(o)) if hasattr(o, '__dict__') else export_safe(o) for o in obj]
    return obj


def recursive_to_dict(nested: Any, exclude: Optional[List[str]] = None) -> Iterator[Tuple[str, Any]]:
    """Recursively transform objects into a dictionary representation.

    Args:
        nested (Any): Current object.
        exclude (Optional[List[str]], optional): Keys to exclude. Defaults to None.

    Yields:
        Iterator[Tuple[str, Any]]: Current level of key-value pairs.
    """
    exclude = [] if exclude is None else exclude
    if hasattr(nested, '__class__'):
        yield '__class__', str(nested.__class__).split("'")[1]
    if hasattr(nested, '__dict__'):
        nested = nested.__dict__
    for key, value in nested.items():
        if not key.startswith('__') and key not in exclude:
            if isinstance(value, (AbstractClassifier, Environment, Instance, InstanceProvider, LabelProvider)):
                yield key, export_instancelib(value)
            elif hasattr(value, '__dict__'):
                yield key, dict(recursive_to_dict(value, exclude=exclude))
            else:
                yield key, export_safe(value)
