"""Utility functions."""

import base64
from typing import Any, Dict, Iterator, List, Optional, Tuple

import numpy as np
import sklearn
import srsly
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
    return export_serializable(obj)


def export_serializable(obj):
    """Export in serializable format (`pickle.dumps()` that is `base64`-encoded).."""
    return base64.b64encode(srsly.pickle_dumps(obj))


def export_dict(nested: dict) -> Iterator[Tuple]:
    """Export a normal dictionary recursively.

    Args:
        nested (dict): Dictionary to export

    Yields:
        Iterator[Tuple]: Current level of key-value pairs.
    """
    for key, value in nested.items():
        if isinstance(value, dict):
            yield key, dict(export_dict(value))
        else:
            yield key, export_safe(value)


def export_safe(obj):
    """Safely export to transform into JSON or YAML."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.str):
        return str(obj)
    elif isinstance(obj, (frozenset, set)):
        return [export_safe(o) for o in list(obj)]
    elif isinstance(obj, (list, tuple)):
        return [dict(recursive_to_dict(o)) if hasattr(o, '__dict__') else export_safe(o) for o in obj]
    elif isinstance(obj, dict):
        return dict(export_dict(obj))
    elif callable(obj):
        return export_serializable(obj)
    return obj


def recursive_to_dict(nested: Any,
                      exclude: Optional[List[str]] = None,
                      include_class: bool = True) -> Iterator[Tuple[str, Any]]:
    """Recursively transform objects into a dictionary representation.

    Args:
        nested (Any): Current object.
        exclude (Optional[List[str]], optional): Keys to exclude. Defaults to None.
        include_class (bool, optional): Whether to include `__class__` (True) or not (False). Defaults to True.

    Yields:
        Iterator[Tuple[str, Any]]: Current level of key-value pairs.
    """
    exclude = [] if exclude is None else exclude
    if include_class and hasattr(nested, '__class__'):
        yield '__class__', str(nested.__class__).split("'")[1]
    if hasattr(nested, '__dict__'):
        nested = nested.__dict__
    for key, value in nested.items():
        if (isinstance(key, str) and not key.startswith('__')) and key not in exclude:
            if isinstance(value, (AbstractClassifier, Environment, Instance, InstanceProvider, LabelProvider)):
                yield export_safe(key), export_instancelib(value)
            elif isinstance(value, (sklearn.base.BaseEstimator)):
                yield export_safe(key), export_serializable(value)
            elif hasattr(value, '__dict__'):
                yield export_safe(key), dict(recursive_to_dict(value, exclude=exclude, include_class=include_class))
            else:
                yield export_safe(key), export_safe(value)
