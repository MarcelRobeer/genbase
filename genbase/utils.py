"""Utility functions."""

import base64
import importlib.util
import warnings
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple
from zipfile import ZipExtFile

import numpy as np
import sklearn
import srsly
from instancelib.analysis.base import (BinaryModelMetrics,
                                       MulticlassModelMetrics)
from instancelib.environment.base import Environment
from instancelib.instances.base import Instance, InstanceProvider
from instancelib.labels.base import LabelProvider
from instancelib.machinelearning import AbstractClassifier

ModelMetrics = (BinaryModelMetrics, MulticlassModelMetrics)


def export_instancelib(obj) -> Dict[str, Any]:
    """`instancelib`-specific safe exports."""
    if isinstance(obj, Environment):
        return {'dataset': export_instancelib(obj.dataset),
                'labels': export_instancelib(obj.labels),
                'named_providers': export_instancelib(obj.named_providers)}
    elif isinstance(obj, Instance):
        return {k: export_safe(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, LabelProvider):
        return {'labelset': export_safe(obj._labelset),
                'labeldict': {k: export_safe(v) for k, v in obj._labeldict.items()}}
    elif isinstance(obj, InstanceProvider):
        return [export_instancelib(o) for o in obj.get_all()]
    elif isinstance(obj, ModelMetrics):
        return {k: export_safe(getattr(obj, k)) for k in dir(obj)
                if not k.startswith('_') and not callable(getattr(obj, k))}
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
    elif 'pandas' in str(type(obj)).lower() and hasattr(obj, 'to_dict') and callable(obj.to_dict):
        return obj.to_dict()
    elif isinstance(obj, np.str):
        return str(obj)
    elif isinstance(obj, (frozenset, set)):
        return [export_safe(o) for o in list(obj)]
    elif isinstance(obj, (list, tuple)):
        return [dict(recursive_to_dict(o)) if hasattr(o, '__dict__') else export_safe(o) for o in obj]
    elif isinstance(obj, dict):
        return dict(export_dict(obj))
    elif 'tensorflow.' in str(type(obj)).lower() or 'torch.' in str(type(obj)).lower():
        return 'TODO-EXPORT-TF-TORCH'
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
        cls = str(nested.__class__).split("'")[1]
        if cls == 'type':
            yield '__name__', str(nested.__qualname__)
            return
        elif 'blackboxclassifier' in str.lower(cls):
            yield 'BLACKBOX', 'HAS_CONTENTS_HIDDEN_<3_SO_STOP_PEEKING_:)'
            return
        elif cls != 'dict':
            yield '__class__', cls
    if hasattr(nested, '__qualname__') and hasattr(nested, '__annotations__'):
        yield '__name__', str(nested.__qualname__)
        nested = nested.__annotations__
    elif hasattr(nested, '__dict__'):
        nested = nested.__dict__
    if not hasattr(nested, 'items'):
        nested = dict(nested)
    for key, value in nested.items():
        if (isinstance(key, str) and not key.startswith('__')) and key not in exclude:
            if isinstance(value, (AbstractClassifier, Environment, Instance,
                                  InstanceProvider, LabelProvider, ModelMetrics)):
                yield export_safe(key), export_instancelib(value)
            elif isinstance(value, (sklearn.base.BaseEstimator)):
                yield export_safe(key), export_serializable(value)
            elif hasattr(value, '__dict__') or isinstance(value, dict):
                yield export_safe(key), dict(recursive_to_dict(value, exclude=exclude, include_class=include_class))
            else:
                yield export_safe(key), export_safe(value)


def get_file_type(pathlike: str) -> Optional[str]:
    """Get file type of a pathlike string.

    Args:
        pathlike (str): Pathlike string.

    Returns:
        Optional[str]: File extension or None.
    """
    if isinstance(pathlike, ZipExtFile):
        pathlike = pathlike.name
    if isinstance(pathlike, str):
        return str.lower(Path(pathlike).suffix)
    return None


def package_available(package: str) -> bool:
    """Check if package is installed.

    Args:
        package (str): Name of package.

    Returns:
        bool: Whether the package is available (True) or not (False).
    """
    return importlib.util.find_spec(package) is not None


def extract_metrics(metrics: dict) -> Tuple[dict, list]:
    # Get all unique property names
    properties = []

    def safe_getattr(obj, name):
        try:
            return getattr(obj, name, None)
        except Exception as e:
            warning(e)
            return type(e).__name__

    for v in metrics.values():
        for p in dir(v):
            if not p.startswith('_') and not callable(safe_getattr(v, p)) and p not in properties:
                properties.append(p)

    # Extract property values
    def extract_property(m, p):
        res = safe_getattr(m, p)
        if isinstance(res, frozenset):
            res = len(res)
        return res

    return {k: {p: extract_property(v, p) for p in properties} for k, v in metrics.items()}, properties


def info(message):
    """Print an informational message."""
    warnings.formatwarning = lambda msg, *args, **kwargs: f'{msg}\n'
    warnings.warn(f'[INFO] {message}')


def warning(message):
    """Print a warning message."""
    warnings.formatwarning = lambda msg, *args, **kwargs: f'{msg}\n'
    warnings.warn(f'[EXCEPTION] {message}')
