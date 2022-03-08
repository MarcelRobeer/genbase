"""Wrap models using instancelib and instancelib-onnx."""

from pathlib import Path
from typing import Dict, Optional, Union

from instancelib.environment.base import Environment
from instancelib.instances.base import InstanceProvider
from instancelib.machinelearning import (AbstractClassifier,
                                         SkLearnDataClassifier)
from instancelib.typehints import LT
from sklearn.base import is_classifier
from sklearn.exceptions import NotFittedError
from sklearn.pipeline import Pipeline
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils.validation import check_is_fitted

from ..data import train_test_split
from ..utils import get_file_type, info, package_available


def sklearn_model(model) -> bool:
    """Check is a model is an scikit-learn model.

    Args:
        model: Model to check.

    Returns:
        bool: Model is a scikit-learn model (True) or not (False).
    """
    if isinstance(model, Pipeline):
        return True
    try:
        check_estimator(model)
        return True
    except:
        return False


def sklearn_fitted(model) -> bool:
    """Check if a scikit-learn model is fitted.

    Args:
        model: Model to check.

    Returns:
        bool: Model is fitted (True) or not (False).
    """
    try:
        if isinstance(model, Pipeline):
            if all(sklearn_fitted(part) for _, part in model.steps):
                return True
        check_is_fitted(model)
        return True
    except NotFittedError:
        return False


def import_model(model,
                 environment: Optional[Environment] = None,
                 train: Union[int, float, str, InstanceProvider] = 'train',
                 label_map: Optional[Dict[LT, LT]] = None) -> AbstractClassifier:
    """Import a model from file or from a Python object.

    Examples:
        Make a scikit-learn text classifier and train it on SST2
        >>> from genbase import import_data, import_model
        >>> from datasets import load_dataset
        >>> ds = import_data(load_dataset('glue', 'sst2'), data_cols='sentence', label_cols='label')
        >>> from sklearn.pipeline import Pipeline
        >>> from sklearn.naive_bayes import MultinomialNB
        >>> from sklearn.feature_extraction.text import TfidfVectorizer
        >>> pipeline = Pipeline([('tfidf', TfidfVectorizer()),
        ...                      ('clf', MultinomialNB())])
        >>> import_model(pipeline, ds, train='train')

        Load a pretrained ONNX model downloaded from 
            https://github.com/mpbron/instancelib-onnx/blob/main/example_models/data-model.onnx
        >>> from genbase import import_model
        >>> import_model('data-model.onnx', label_map={0: 'Bedrijfsnieuws', 1: 'Games', 2: 'Smartphones'})

    Args:
        model: Model or path to model to import.
        environment (Optional[Environment], optional): Environment corresponding to model (with dataset and ground-truth
            labels), used for importing models and/or training them.
        train (Union[int, float, str, InstanceProvider], optional): Train split size, name in environment or provider. 
            Defaults to 'train'.
        label_map (Optional[Dict[LT, LT]], optional): Conversion of label IDs to named labels. Defaults to None.

    Raises:
        ImportError: Unable to import model or file.
        NotImplementedError: Type of model is not yet supported.

    Returns:
        AbstractClassifier: Instancelib wrapped model.
    """
    if label_map is None and environment is not None:
        label_map = list(environment.labels.labelset)
    if isinstance(label_map, dict):
        label_map = {str(k): v for k, v in label_map.items()}

    if isinstance(model, str):
        if not Path(model).exists():
            raise ImportError(f'Unable to locate file "{model}"')
        file_type = get_file_type(model)
        if file_type == '.pkl':
            import pickle  # nosec
            info('Unpickling model (warning: be sure you trust a source before unpickling a model!)')
            model = pickle.load(model)  # nosec
        elif file_type == '.onnx':
            if not package_available('ilonnx'):
                raise ImportError('To import ONNX files install `instancelib-onnx`!')
            import ilonnx
            if label_map is None:
                info('Improve the informativeness of your predictions by providing the label_map')
            return ilonnx.build_data_model(model, classes=label_map)
    elif isinstance(model, AbstractClassifier):
        return model

    _no_train_msg = ''

    if environment is not None:
        if isinstance(train, (float, int)):
            _no_train_msg = 'Splitting dataset into train/test set...'
            environment = train_test_split(environment, train_size=train)
            train = environment['train']
        elif train in environment.keys():
            _no_train_msg = f'Using named_provider "{train}" as the training set...'
            train = environment[train]
        elif not isinstance(train, InstanceProvider):
            _no_train_msg = 'No training set provided, defaulting to all data as training set...'
            train = environment.dataset

    if sklearn_model(model):
        if not sklearn_fitted(model):
            if environment is None:
                raise ImportError('Untrained scikit-learn models require an environment to import!')   
            info('Model is not fitted yet, fitting model!')
            if _no_train_msg:
                info(_no_train_msg)
            if is_classifier(model):
                model = SkLearnDataClassifier.build(model, environment)
                model.fit_provider(train, environment.labels)
                return model
            else:
                NotImplementedError('Only classifiers are currently supported!')
        else:
            if is_classifier(model):
                classes = label_map if environment is None else environment
                return SkLearnDataClassifier.build_from_model(model, classes=classes)
            else:
                raise NotImplementedError('Only classifiers are currently supported!')
    elif 'torch' in str(type(model)):
        raise ImportError('Convert your PyTorch model with ONNX (https://pytorch.org/docs/stable/onnx.html)' +
                          ' before importing it with instancelib-onnx.')
    elif 'keras' in str(type(model)):
        raise ImportError('Convert your Keras model with ONNX (https://github.com/onnx/keras-onnx)' +
                          ' before importing it with instancelib-onnx.')
    elif 'tensorflow' in str(type(model)):
        raise ImportError('Convert your Tensorflow model with ONNX (https://github.com/onnx/tensorflow-onnx)' +
                          ' before importing it with instancelib-onnx.')        
    raise NotImplementedError(f'Unknown type of model "{model}!"')
