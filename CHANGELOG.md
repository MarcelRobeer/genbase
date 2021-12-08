# Changelog
All notable changes to `genbase` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
