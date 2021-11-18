"""Data imports, sampling and generation."""

import os
from typing import Tuple, Union

from instancelib.ingest.spreadsheet import read_csv_dataset, read_excel_dataset
from instancelib.instances.base import InstanceProvider


def import_data(filename: str, *args, **kwargs) -> InstanceProvider:
    """Import dataset using instancelib, currently supporting CSV and Excel files.

    Example:
        Read `test.csv` from the folder `datasets`:

        >>> from text_explainability.data import import_data
        >>> env = import_data('./datasets/test.csv', data_cols=['fulltext'], label_cols=['label'])
        >>> env.dataset, env.labels

    Args:
        filename (str): Filename, relative to current file or absolute path.

    Raises:
        ImportError: Cannot import file, unknown filetype.

    Returns:
        InstanceProvider: instancelib InstanceProvider. Access dataset through `.dataset()` and `.labels()`
    """
    filepath = os.path.abspath(filename)
    _, extension = os.path.splitext(filepath)
    extension = str.lower(extension).replace('.', '')

    if extension == 'csv':
        return read_csv_dataset(filepath, *args, **kwargs)
    elif extension.startswith('xls'):
        return read_excel_dataset(filepath, *args, **kwargs)
    else:
        raise ImportError(f'Unknown {extension=} for {filepath=}')


def train_test_split(environment: InstanceProvider,
                     train_size: Union[int, float]) -> Tuple[InstanceProvider, InstanceProvider]:
    """Split a dataset into training and test data.

    Args:
        environment (InstanceProvider): Environment containing all data (`environment.dataset`), 
            including labels (`environment.labels`).
        train_size (Union[int, float]): Size of training data, as a proportion [0, 1] or number of instances > 1.

    Returns:
        Tuple[InstanceProvider, InstanceProvider]: Train dataset, test dataset.
    """
    return environment.train_test_split(environment.dataset, train_size=train_size)
