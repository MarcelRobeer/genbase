"""Data imports, sampling and generation."""

from typing import (Callable, Dict, Iterator, List, Literal, Optional, Tuple,
                    Union)

import instancelib as il
import pandas as pd
from instancelib.typehints import KT, VT

from ..utils import get_file_type, info

Method = Literal['infer', 'glob', 'pandas']


METHODS = ['infer', 'glob', 'pandas']
PANDAS_FILE_TYPES = ['.csv', '.tsv', '.txt', '.json', '.pkl', '.xls', '.xlsx']



def get_compressed_files(ioargs):
    handle = ioargs.filepath_or_buffer
    mode = ioargs.mode
    compression = ioargs.compression.pop('method', None)

    if compression == 'gzip':
        import gzip

        if isinstance(handle, str):
            return gzip.GzipFile(filename=handle, mode=mode)
        return gzip.GzipFile(fileobj=handle, mode=mode)
    elif compression == 'bz2':
        import bz2
        return bz2.BZ2File(handle, mode=mode)
    elif compression == 'xz':
        from pandas.compat import get_lzma_file
        return get_lzma_file()(handle, mode=mode)
    elif compression == 'zip':
        from pandas.io.common import _BytesZipFile

        handle = _BytesZipFile(handle, mode)
        if handle.mode == "r":
            zip_names = handle.namelist()

            if len(zip_names) == 0:
                raise ValueError(f'Empty ZIP file "{ioargs.filepath_or_buffer}"')
            return [handle.open(name) for name in zip_names]
    raise NotImplementedError(f'Unable to process "{handle}" with compressiong method "{compression}"!')


def pandas_to_instancelib(dataset, data_cols, label_cols, label_map=None):
    env = il.pandas_to_env(dataset, data_cols, label_cols)
    if label_map is not None:
        if isinstance(label_map, dict):
            label_map = {str(k): v for k, v in label_map.items()}
        env = rename_labels(env, label_map)
    return env


def import_data(dataset,
                data_cols: Union[KT, List[KT]],
                label_cols: Union[KT, List[KT]],
                label_map: Optional[Union[Callable, dict]] = None,
                method: Method = 'infer',
                _to_instancelib: bool = True,
                **read_kwargs) -> Union[il.Environment, pd.DataFrame]:
    """Import data in an instancelib Environment.

    Examples:
        Import from an online .csv file with data in the 'text' column and labels in 'category':
        >>> from genbase import import_data
        >>> ds = import_data('https://storage.googleapis.com/dataset-uploader/bbc/bbc-text.csv',
                             data_cols='text', label_cols='category')

        Convert a pandas DataFrame to instancelib Environment:
        >>> from genbase import import_data
        >>> import pandas as pd
        >>> df = pd.read_csv('https://storage.googleapis.com/dataset-uploader/bbc/bbc-text.csv')
        >>> ds = import_data(df, data_cols='text', label_cols='category')

        Download a .zip file and convert each file in the zip to an instancelib Environment:
        >>> from genbase import import_data
        >>> ds = import_data('https://archive.ics.uci.edu/ml/machine-learning-databases/00462/drugsCom_raw.zip',
                             data_cols='review', label_cols='rating')

        Convert a huggingface dataset (sst2) to an instancelib Environment:
        >>> from genbase import import_data
        >>> from datasets import load_dataset
        >>> ds = import_data(load_dataset('glue', 'sst2'), data_cols='sentence', label_cols='label')

    Args:
        dataset (_type_): Dataset to import.
        data_cols (Union[KT, List[KT]]): Name of column(s) containing data.
        label_cols (Union[KT, List[KT]]): Name of column(s) containing labels.
        label_map (Optional[Union[Callable, dict]], optional): Label renaming dictionary/function. Defaults to None.
        method (Method, optional): Method used to import data. Choose from 'infer', 'glob', 'pandas'.
            Defaults to 'infer'.
        _to_instancelib (bool, optional): Whether to convert the final result to instancelib. Defaults to True.
        **read_kwargs: Optional arguments passed to reading call.

    Raises:
        ImportError: Unable to import file.
        ValueError: Invalid type of method.
        NotImplementedError: Import not yet implemented.

    Returns:
        Union[il.Environment, pd.DataFrame]: Environment for each file or dataset provided.
    """
    if method not in METHODS:
        raise ValueError(f'Unknown method "{method}", choose from {METHODS}.')

    if isinstance(data_cols, (int, str)):
        data_cols = [data_cols]
    if isinstance(label_cols, (int, str)):
        label_cols = [label_cols]

    file_type = get_file_type(dataset)
    path_like = isinstance(dataset, str)

    # Unpack archived file
    if file_type in pd.io.common._compression_to_extension.values():
        ioargs = pd.io.common._get_filepath_or_buffer(dataset, compression=file_type.replace('.', ''))
        info(f'Unpacking file "{dataset}".')
        return import_from_key_values([(file.name, file) for file in get_compressed_files(ioargs)],
                                      data_cols=data_cols,
                                      label_cols=label_cols,
                                      label_map=label_map,
                                      method=method,
                                      **read_kwargs)

    # Infer method
    if method == 'infer':
        if path_like and '*' in dataset:
            method = 'glob'
        elif file_type in PANDAS_FILE_TYPES:
            method = 'pandas'

    # Multiple files
    if method == 'glob':
        import glob
        return import_from_key_values([(file, file) for file in glob.glob(dataset)],
                                      data_cols=data_cols,
                                      label_cols=label_cols,
                                      label_map=label_map,
                                      method=method,
                                      **read_kwargs)

    # Read one file with Pandas
    if method == 'pandas':
        if file_type is not None:
            info(f'Reading file "{dataset}".')
            if file_type in ['.csv', '.tsv', '.txt']:
                if 'sep' not in read_kwargs:
                    if file_type == '.csv':
                        read_kwargs['sep']= ','
                    elif file_type == '.tsv':
                        read_kwargs['sep']= '\t'
                dataset = pd.read_csv(dataset, **read_kwargs)
            elif file_type == '.json':
                dataset = pd.read_json(dataset, **read_kwargs)
            elif file_type == '.pkl':
                dataset = pd.read_pickle(dataset, **read_kwargs)
            elif file_type in ['.xls', '.xlsx']:
                dataset = pd.read_excel(dataset, **read_kwargs)
            else:
                raise ImportError(f'Unable to process file type "{file_type}" with method "pandas"!')

    if hasattr(dataset, 'to_pandas') and callable(dataset.to_pandas):
        info(f'Preparing "{dataset}" for import with Pandas.'.replace('\n', ' ').replace('\t', ''))
        dataset = dataset.to_pandas()
    elif isinstance(dataset, dict):
        return import_from_key_values(dataset.items(),
                                      data_cols=data_cols,
                                      label_cols=label_cols,
                                      label_map=label_map,
                                      **read_kwargs)

    if _to_instancelib:
        return pandas_to_instancelib(dataset, data_cols=data_cols, label_cols=label_cols, label_map=label_map)
    return dataset


def import_from_key_values(iterator: Iterator[Tuple[KT, VT]],
                           data_cols: Union[KT, List[KT]],
                           label_cols: Union[KT, List[KT]],
                           label_map: Optional[Union[Callable, dict]] = None,
                           method: Method = 'infer',
                           **read_kwargs) -> Dict[KT, il.Environment]:
    dataset = {k: import_data(v, data_cols=data_cols, label_cols=label_cols,
                              method=method, _to_instancelib=False, **read_kwargs)
               for k, v in iterator}
    return pandas_to_instancelib(dataset, data_cols=data_cols, label_cols=label_cols, label_map=label_map)


def train_test_split(environment: il.Environment,
                     train_size: Union[int, float],
                     train_name: str = 'train',
                     test_name: str = 'test') -> il.Environment:
    """Split an environment into training and test data, and save it to the original environment.

    Args:
        environment (instancelib.Environment): Environment containing all data (`environment.dataset`), 
            including labels (`environment.labels`).
        train_size (Union[int, float]): Size of training data, as a proportion [0, 1] or number of instances > 1.
        train_name (str, optional): Name of train split. Defaults to 'train'.
        test_name (str, optional): Name of train split. Defaults to 'test'.

    Returns:
        instancelib.Environment: Environment with named splits `train_name` (containing training data) and `test_name`
            (containing test data) 
    """
    environment[train_name], environment[test_name] = environment.train_test_split(environment.dataset,
                                                                                   train_size=train_size)
    return environment


def rename_labels(provider: Union[il.Environment, il.LabelProvider],
                  mapping: Union[Callable, dict]) -> Union[il.Environment, il.LabelProvider]:
    """Rename labels in a labelprovider or environment.

    Args:
        provider (Union[il.Environment, il.LabelProvider]): Provider to rename labels in.
        mapping (Union[Callable, dict]): Rename function or dictionary containing label mapping.

    Returns:
        Union[il.Environment, il.LabelProvider]: Original provider with labels remapped.
    """
    is_environment = isinstance(provider, il.Environment)
    _provider = provider.labels if is_environment else provider
    _provider = il.MemoryLabelProvider.rename_labels(_provider, mapping)
    if is_environment:
        provider._labelprovider = _provider
    else:
        provider = _provider
    return provider
