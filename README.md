*<p align="center">
  <img src="https://github.com/MarcelRobeer/genbase/blob/0b6bb7e9cf715954ab0eeb419b6fe2d8459a23c8/img/genbase.png" alt="genbase logo" width="50%">*
</p>

**<h3 align="center">
Generation base dependency**
</h3>

[![PyPI](https://img.shields.io/pypi/v/genbase)](https://pypi.org/project/genbase/)
[![Python_version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/genbase/)
[![License](https://img.shields.io/pypi/l/genbase)](https://www.gnu.org/licenses/lgpl-3.0.en.html)
[![Lint, Security & Tests](https://github.com/MarcelRobeer/genbase/actions/workflows/check.yml/badge.svg)](https://github.com/MarcelRobeer/genbase/actions/workflows/check.yml)

---

Base functions, generation functions and generic wrappers.

&copy; Marcel Robeer, 2021

## Module overview
| Module | Description |
|--------|-------------|
| [`genbase`](#genbase) | Readable data representations and meta information class. |
| [`genbase.data`](#genbase-data) | Wrapper functions for working with data. |
| [`genbase.decorator`](#genbase-decorator) | Base support for decorators. |
| [`genbase.internationalization`](#genbase-i18n) | `i18n` internationalization. |
| [`genbase.mixin`](#genbase-mixin) | Mixins for seeding (reproducibility) and state machines. |
| [`genbase.model`](#genbase-model) | Wrapper functions for working with machine learning models. |
| [`genbase.ui`](#genbase-ui) | Extensible user interfaces (UIs) for `genbase` dependencies. |

## Installation
| Method | Instructions |
|--------|--------------|
| `pip` | Install from [PyPI](https://pypi.org/project/genbase/) via `pip3 install genbase`. |
| Local | Clone this repository and install via `pip3 install -e .` or locally run `python3 setup.py install`.

## Releases
`genbase` is officially released through [PyPI](https://pypi.org/project/genbase/).

See [CHANGELOG.md](CHANGELOG.md) for a full overview of the changes for each version.

## Packages using `genbase`

---

<a href="https://explabox.readthedocs.io/" target="_blank"><img src="https://explabox.readthedocs.io/en/latest/_static/explabox-logo-text.png" alt="Explabox logo" width="180px"></a><p>The `explabox` aims to support data scientists and machine learning (ML) engineers in explaining, testing and documenting AI/ML models, developed in-house or acquired externally. The explabox turns your _ingestibles_ (AI/ML model and/or dataset) into _digestibles_ (statistics, explanations or sensitivity insights)! The `text_explainability` package is available through [PyPI](https://pypi.org/project/explabox/) and fully documented at [https://explabox.readthedocs.io/](https://explabox.readthedocs.io/).</p>

---

<a href="https://text-explainability.readthedocs.io/" target="_blank"><img src="https://github.com/MarcelRobeer/text_explainability/blob/6e5bb5d6f521ec2f02a95b42e33f83a7d61ae962/img/te-logo_large.png" alt="T_xt explainability logo" width="230px"></a><p>`text_explainability` provides a _generic architecture_ from which well-known state-of-the-art explainability approaches for text can be composed. This modular architecture allows components to be swapped out and combined, to quickly _develop new types of explainability approaches_ for (natural language) text, or to _improve a plethora of approaches_ by improving a single module. The `text_explainability` package is available through [PyPI](https://pypi.org/project/text-explainability/) and fully documented at [https://text-explainability.readthedocs.io/](https://text-explainability.readthedocs.io/).</p>

---

<a href="https://text-sensitivity.readthedocs.io/" target="_blank"><img src="https://github.com/MarcelRobeer/text_sensitivity/blob/08e44ca2d1b1806fcf316c646ff665157184ba61/img/ts-logo_large.png" alt="Text sensitivity logo" width="200px"></a><p>`text_explainability` can be extended to also perform _sensitivity testing_, checking for machine learning model safety, robustness and fairness. The `text_sensitivity` package is available through [PyPI](https://pypi.org/project/text-sensitivity/) and fully documented at [https://text-sensitivity.readthedocs.io/](https://text-sensitivity.readthedocs.io/).</p>

---

## API

<a name="genbase"></a>
### `genbase`
Readable data representations and meta information class.

| Class | Description |
|-------|-------------|
| `Readable` | Ensure that a class has a readable representation. |
| `Configurable` | Adds working with configs (`.from_config()`, `from_json()`, `from_yaml()`, ..., `read_json()`, ..., `to_yaml()`) to a class. |
| `MetaInfo` | Adds `type`, `subtype`, `callargs` and other meta descriptors to a class (subclass of `Configurable`). |
| `silence_tqdm` | Silence output of `tqdm` in a module. |

_Examples_:
```python
>>> from genbase import MetaInfo

>>> class ReturnCls(MetaInfo):
...     def __init__(self, value, **kwargs):
...         super().__init__(self,
...                          type='special_test',
...                          subtype='special',
...                          **kwargs)
...         self.value = value
...
...     @property
...     def content(self):
...          return {'value': self.value}

>>> obj = ReturnCls(value=5)
>>> obj.to_config()
{'META': {'type': 'special_test',
          'subtype': 'special'},
 'CONTENT': {'value': 5}}
```

Silence the output of `tqdm` in a `with` statement.

```python
>>> import instancelib
>>> from genbase import silence_tqdm

>>> with silence_tqdm(instancelib):
...    model.predict(instances)
```

<a name="genbase-data"></a>
### `genbase.data`
Wrapper functions for working with data.

| Function | Description |
|----------|-------------|
| `import_data()` | Import dataset into an `instancelib.Environment` (containing instances and ground-truth labels). |
| `train_test_split()` | Split a dataset into training and test data. |

_Examples_:
Import from an online .csv file for the [BBC News dataset](http://mlg.ucd.ie/datasets/bbc.html) with data in the 'text' column and labels in 'category':
```python
>>> from genbase import import_data
>>> import_data('https://storage.googleapis.com/dataset-uploader/bbc/bbc-text.csv',
...             data_cols='text', label_cols='category')
TextEnvironment()
```

Convert a pandas DataFrame to instancelib Environment:
```python
>>> from genbase import import_data
>>> import pandas as pd
>>> df = pd.read_csv('./Downloads/bbc-text.csv')
>>> import_data(df, data_cols=['text'], label_cols=['category'])
TextEnvironment()
```

Download a .zip file of the [Drugs.com review dataset](https://archive.ics.uci.edu/ml/datasets/Drug+Review+Dataset+%28Drugs.com%29#) and convert each file in the ZIP to an instancelib Environment:
```python
>>> from genbase import import_data
>>> import_data('https://archive.ics.uci.edu/ml/machine-learning-databases/00462/drugsCom_raw.zip',
...             data_cols='review', label_cols='rating')
TextEnvironment(named_providers=['drugsComTest_raw.tsv', 'drugsComTrain_raw.tsv'])
```

Convert a huggingface Dataset ([SST2 in Glue](https://huggingface.co/datasets/glue)) to an instancelib Environment:
```python
>>> from genbase import import_data
>>> from datasets import load_dataset
>>> import_data(load_dataset('glue', 'sst2'), data_cols='sentence', label_cols='label')
TextEnvironment(named_providers=['test', 'train', 'validation'])
```

<a name="genbase-decorator"></a>
### `genbase.decorator`
Base support for decorators.

| Decorator | Description |
|----------|-------------|
| `@add_callargs` | Decorator that passes `__callargs__`  to a function if available. Useful in conjunction with `MetaInfo`. |

_Example_:
```python
>>> from genbase import MetaInfo, add_callargs

>>> class ReturnCls(MetaInfo):
...     def __init__(self, value, callargs=None, **kwargs):
...         super().__init__(self,
...                          type='special_test',
...                          subtype='special',
...                          callargs=callargs,
...                          **kwargs)
...         self.value = value
...
...     @property
...     def content(self):
...          return {'value': self.value}

>>> @add_callargs
... def example_fn(x: int, y: int, z: int = 5, t='str', **kwargs):
...     callargs = kwargs.pop('__callargs__', None)
...     return ReturnCls(value=x + y + z, callargs=callargs)

>>> example_fn(x=1, y=2).callargs
{'x': 1, 'y': 2, 'z': 5, 't': 'str'}
```

<a name="genbase-i18n"></a>
### `genbase.internationalization`
`i18n` internationalization.

| Function | Description |
|----------|-------------|
| `get_locale()` | Get current locale. |
| `set_locale()` | Set current locale . |
| `translate_list()` | Get a list based on `locale`, as defined in the './locale' folder. |
| `translate_string()` | Get a string based on `locale`, as defined in the './locale' folder. |

_Example_:
```python
>>> from genbase.internationalization import set_locale, translate_list
>>> set_locale('en')
>>> translate_list('stopwords')
['a', 'an', 'the']

>>> set_locale('nl')
>>> translate_list('stopwords')
['de', 'het', 'een']
```

<a name="genbase-mixin"></a>
### `genbase.mixin`
Mixins for seeding (reproducibility) and state machines.

| Class | Description |
|-------|-------------|
| `SeedMixin` | Adds working with ._seed and ._original_seed for reproducibility. |
| `CaseMixin` | Adds working with title-, sentence-, upper- and lowercase for random data generation. |

_Example_:
```python
>>> from genbase.mixin import SeedMixin
>>> class RandomCls(SeedMixin):
...     def __init__(self, seed: int = 0):
...         self._seed = self._original_seed = seed

>>> rc = RandomCls(seed=10)
>>> rc.seed
10

>>> rc._seed += 20
>>> rc.seed
30

>>> rc._original_seed
10
```

<a name="genbase-model"></a>
### `genbase.model`
Wrapper functions for working with machine learning models.

| Function | Description |
|----------|-------------|
| `import_data()` | Import a model with instancelib or instancelib-onnx. |

_Examples_:
Make a scikit-learn text classifier and train it on SST2
```python
>>> from genbase import import_data, import_model
>>> from datasets import load_dataset
>>> ds = import_data(load_dataset('glue', 'sst2'), data_cols='sentence', label_cols='label')
>>> from sklearn.pipeline import Pipeline
>>> from sklearn.naive_bayes import MultinomialNB
>>> from sklearn.feature_extraction.text import TfidfVectorizer
>>> pipeline = Pipeline([('tfidf', TfidfVectorizer()),
...                      ('clf', MultinomialNB())])
>>> import_model(pipeline, ds, train='train')
SklearnDataClassifier()
```

Load a [pretrained ONNX model](https://github.com/mpbron/instancelib-onnx/blob/main/example_models/data-model.onnx) 
with labels 'Bedrijfsnieuws', 'Games' and 'Smartphones'
```python
>>> from genbase import import_model
>>> import_model('data-model.onnx', label_map={0: 'Bedrijfsnieuws', 1: 'Games', 2: 'Smartphones'})
SklearnDataClassifier()
```

<a name="genbase-ui"></a>
### `genbase.ui`
Extensible user interfaces (UIs) for `genbase` dependencies.

| Function | Description |
|----------|-------------|
| `get_color()` | Get color from a `matplotlib` colorscale. |
| `plot.matplotlib_available()` | Check if `matplotlib` is installed. |
| `plot.plotly_available()` | Check if `plotly` is installed. |
| `notebook.format_label()` | Format label as title. |
| `notebook.format_instances()` | Format multiple `instancelib` instances. |
| `notebook.is_colab()` | Check if environment is Google Colab. |
| `notebook.is_interactive()` | Check if the environment is interactive (Jupyter Notebook). |

| Class | Description |
|-------|-------------|
| `plot.ExpressPlot` | Plotter for `plotly.express`. |
| `notebook.Render` | Base class for rendering configs (configuration dictionaries). |

_Example_:
```python
>>> from genbase.ui.notebook import Render
>>> class CustomRender(Render):
...     def __init__(self, *configs):
...         super().__init__(*configs)
...         self.default_title = 'My Custom Explanation'
...         self.main_color = '#ff00000'
...         self.package_link = 'https://git.io/text_explainability'
...
...     def format_title(self, title: str, h: str = 'h1', **renderargs) -> str:
...         return f'<{h} style="color: red;">{title}</{h}>'
...
...     def render_content(self, meta: dict, content: dict, **renderargs):
...         type = meta['type'] if 'type' in meta else ''
...         return type.replace(' ').title() if 'explanation' in type else type

>>> from genbase import MetaInfo
>>> NiceCls(MetaInfo):
...     def __init__(self, **kwargs):
...         super().__init__(renderer=CustomRenderer, **kwargs)
```
