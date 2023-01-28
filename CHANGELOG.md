# Changelog
All notable changes to `genbase` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.14] - 2023-01-28
### Added
- Ability to silence tqdm outputs with `genbase.silence_tqdm`

## [0.2.13] - 2023-01-26
### Fixed
- Dependency conflicts for `onnxruntime`

## [0.2.12] - 2023-01-26
### Added
- Support for `onnx` in Python 3.10

### Changed
- Styling of labels in UI

### Fixed
- Support for new `pandas` versions with `pd.io.common._compression_to_extension` to `pd.io.common.extension_to_compression`

## [0.2.11] - 2022-07-15
### Fixed
- Beter rendering of `raw_html` through the `use_plotly` option

## [0.2.10] - 2022-07-14
### Added
- Ability to directly access `raw_html` through `MetaInfo.raw_html`

## [0.2.9] - 2022-07-14
### Added
- Ability to directly access `html` through `MetaInfo.html`

### Fixed
- Prevent `DeprecationWarning` for use of `np.str` in `genbase.utils`

## [0.2.8] - 2022-04-06
### Added
- Direct import of instancelib model

### Changed
- Requires new instancelib version
- `instancelib-onnx` is optional for Python 3.10

### Fixed
- Config export fixes

## [0.2.7] - 2022-03-21
### Changed
- Lazy evaluation of internationalization functions

## [0.2.5] - 2022-03-17
### Fixed
- Pass on docstrings with `@add_callargs`

## [0.2.4] - 2022-03-16
### Fixed
- Various bugfixes

### Changed
- Updated styling
- Improved exports in `recursive_to_dict()`

## [0.2.3] - 2022-03-08
### Added
- Renaming of labels when importing data
- `extract_metric` from `text_sensitivity`

### Changed
- Updated to `instancelib>=0.4.2.0`

## [0.2.2] - 2022-03-04
### Changed
- Updated to `instancelib-onnx>=0.1.3`

### Fixed
- Security fix in `import_model()`

## [0.2.1] - 2022-03-04
### Added
- Added `model.import_model()` to import models
- `instancelib-onnx` as a dependency
- Information logging

### Changed
- `from_sklearn()` is part of `import_model()`
- Multiple part in `import_data()` now return a single Environment
- Updated README.md to include new functionalities
- Changed location of `model` subpackage

## [0.2.0] - 2022-03-03
### Added
- Examples to `import_data()`

### Changed
- Extended `import_data()` to handle more input types
- Requires `instancelib>=0.4.0.0`
- Train/test splits are added to the environment itself

### Fixed
- Bugfix in `Configurable.read_yaml()`

## [0.1.18] - 2022-02-03
### Fixed
- Bugfix in online rendering of `plotly` in notebook
- Bugfix in `import_data()`
- Added `ipython` as dependency

## [0.1.17] - 2021-12-08
### Changed
- Improved exports in `recursive_to_dict()`

## [0.1.16] - 2021-12-07
### Added
- Offline rendering for `plotly`

### Changed
- Requires `matplotlib>=3.5.0`

## [0.1.15] - 2021-12-07
### Changed
- Requires `instancelib>=0.3.6.2`

### Fixed
- Imports from `instancelib` in `utils`

## [0.1.14] - 2021-12-06
### Added
- Feedback that copy to clipboard was successful

### Fixed
- Bugfix in rendering `format_instance()`

## [0.1.13] - 2021-12-02
### Added
- Ability to add a custom second tab to `genbase.ui.notebook.Render`
- Optional columns to `format_instances()`

### Changed
- Improved table styling

## [0.1.12] - 2021-12-01
### Fixed
- Unique identifier of each `genbase.ui.notebook` element

## [0.1.11] - 2021-12-01
### Added
- Copy to clipboard button to `genbase.ui.notebook.Render`
- Ability to define a colorscale in `genbase.ui.get_color()`

### Changed
- Moved plotting to `genbase.ui.plot`

### Fixed
- Safe `np.str` exports
- Rendering of multiple UIs in `genbase.ui.notebook.Render`

## [0.1.10] - 2021-11-30
### Added
- Checking if `matplotlib_available()`
- `genbase.ui.get_color()`, getting colors with `matplotlib` 
- Ability to exclude `__class__` from `recursive_to_dict()`
- Subtitles to `genbase.ui.notebook.Render`
- Documentation to `genbase.ui.notebook.Render`

### Changed
- Better subclassing for `genbase.ui.notebook.Render` (e.g. setting UI color and hyperlink)

### Fixed
- Bugfixes in `recursive_to_dict()`

## [0.1.9] - 2021-11-27
### Added
- Base rendering behavior for Jupyter notebook
- Add render when `is_interactive()`
- Ability to pass render arguments with `**renderargs`
- Rendering of element in Jupyter notebook
- Add check for `plotly_available()`
- `export_serializable()` for Python inner objects (e.g. `scikit-learn`)

### Fixed
- `recursive_to_dict()` can also iterate over lists/tuples

## [0.1.8] - 2021-11-25
### Added
- `instancelib`-specific exports for `recursive_to_dict()`

### Changed
- Added `recursive_to_dict()` to `@add_callargs`

### Fixed
- Bugfix in top-level export of `@add_callargs`

## [0.1.7] - 2021-11-24
### Fixed
- Generalization of `**kwargs` argument in `@add_callargs`

## [0.1.6] - 2021-11-24
### Added
- Added `genbase.decorator` to README.md
- Base support for decorator `@add_callargs`

## [0.1.5] - 2021-11-24
### Added
- `callargs` to `MetaInfo` class, for future work on rerunning (class) methods

## [0.1.4] - 2021-11-24
### Added
- `Configurable` for reading/writing classes from a `config`, or `json`/`yaml` file

## [0.1.3] - 2021-11-19
### Added
- `MetaInfo` for future work with user interfaces (UI)

### Changed
- Moved internationalization tests to `genbase`

## [0.1.2] - 2021-11-18
### Fixed
- Bugfix in internationalization

## [0.1.1] - 2021-11-18
### Added
- Logo
- Moved `Readable` from `text_explainability` to `genbase`
- Moved `internationalization` to `genbase`

### Changed
- Refactor of `genbase.data`

## [0.1.0] - 2021-11-18
### Added
- CI/CD Pipeline
- `flake8` linting
- `README.md`
- `LICENSE`
- `CHANGELOG.md`
- `git` setup
- Moved mixins from `text_sensitivity` to `genbase`
- Moved machine learning model imports from `text_explainability` to `genbase`
- Moved data wrappers from `text_explainability` to `genbase`

[Unreleased]: https://git.science.uu.nl/m.j.robeer/genbase
[0.2.14]: https://pypi.org/project/genbase/0.2.14/
[0.2.13]: https://pypi.org/project/genbase/0.2.13/
[0.2.12]: https://pypi.org/project/genbase/0.2.12/
[0.2.11]: https://pypi.org/project/genbase/0.2.11/
[0.2.10]: https://pypi.org/project/genbase/0.2.10/
[0.2.9]: https://pypi.org/project/genbase/0.2.9/
[0.2.8]: https://pypi.org/project/genbase/0.2.8/
[0.2.7]: https://pypi.org/project/genbase/0.2.7/
[0.2.6]: https://pypi.org/project/genbase/0.2.6/
[0.2.5]: https://pypi.org/project/genbase/0.2.5/
[0.2.4]: https://pypi.org/project/genbase/0.2.4/
[0.2.3]: https://pypi.org/project/genbase/0.2.3/
[0.2.2]: https://pypi.org/project/genbase/0.2.2/
[0.2.1]: https://pypi.org/project/genbase/0.2.1/
[0.2.0]: https://pypi.org/project/genbase/0.2.0/
[0.1.18]: https://pypi.org/project/genbase/0.1.18/
[0.1.17]: https://pypi.org/project/genbase/0.1.17/
[0.1.16]: https://pypi.org/project/genbase/0.1.16/
[0.1.15]: https://pypi.org/project/genbase/0.1.15/
[0.1.14]: https://pypi.org/project/genbase/0.1.14/
[0.1.13]: https://pypi.org/project/genbase/0.1.13/
[0.1.12]: https://pypi.org/project/genbase/0.1.12/
[0.1.11]: https://pypi.org/project/genbase/0.1.11/
[0.1.10]: https://pypi.org/project/genbase/0.1.10/
[0.1.9]: https://pypi.org/project/genbase/0.1.9/
[0.1.8]: https://pypi.org/project/genbase/0.1.8/
[0.1.7]: https://pypi.org/project/genbase/0.1.7/
[0.1.6]: https://pypi.org/project/genbase/0.1.6/
[0.1.5]: https://pypi.org/project/genbase/0.1.5/
[0.1.4]: https://pypi.org/project/genbase/0.1.4/
[0.1.3]: https://pypi.org/project/genbase/0.1.3/
[0.1.2]: https://pypi.org/project/genbase/0.1.2/
[0.1.1]: https://pypi.org/project/genbase/0.1.1/
[0.1.0]: https://pypi.org/project/genbase/0.1.0/
