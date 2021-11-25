*<p align="center">
  <img src="https://git.science.uu.nl/m.j.robeer/genbase/-/raw/master/img/genbase.png" alt="genbase logo" width="50%">*
</p>

**<h3 align="center">
Generation base dependency**
</h3>

[![PyPI](https://img.shields.io/pypi/v/genbase)](https://pypi.org/project/genbase/)
[![Python_version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)](https://pypi.org/project/genbase/)
[![Build_passing](https://img.shields.io/badge/build-passing-brightgreen)](https://git.science.uu.nl/m.j.robeer/genbase/-/pipelines)
[![License](https://img.shields.io/pypi/l/genbase)](https://www.gnu.org/licenses/lgpl-3.0.en.html)

---

Base functions, generation functions and generic wrappers.

&copy; Marcel Robeer, 2021

## Module overview
| Module | Description |
|--------|-------------|
| `genbase` | Readable data representations and meta information class. |
| `genbase.data` | Wrapper functions for working with data. |
| `genbase.decorator` | Base support for decorators. |
| `genbase.internationalization` | `i18n` internationalization. |
| `genbase.mixin` | Mixins for seeding (reproducibility) and state machines. |
| `genbase.model` | Wrapper functions for working with machine learning models. |
| `genbase.ui` | Exstensible user interfaces (UIs) for `genbase` dependencies |

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

<a href="https://marcelrobeer.github.io/text_explainability/" target="_blank"><img src="https://git.science.uu.nl/m.j.robeer/text_explainability/-/raw/main/img/TextLogo-Logo large.png" alt="T_xt explainability logo" width="230px"></a><p>`text_explainability` provides a _generic architecture_ from which well-known state-of-the-art explainability approaches for text can be composed. This modular architecture allows components to be swapped out and combined, to quickly _develop new types of explainability approaches_ for (natural language) text, or to _improve a plethora of approaches_ by improving a single module. The `text_explainability` package is available through [PyPI](https://pypi.org/project/text-explainability/) and fully documented at [https://marcelrobeer.github.io/text_explainability/](https://marcelrobeer.github.io/text_explainability/).</p>

---

<a href="https://marcelrobeer.github.io/text_sensitivity/" target="_blank"><img src="https://git.science.uu.nl/m.j.robeer/text_sensitivity/-/raw/main/img/TextLogo-Logo_large_sensitivity.png" alt="T_xt sensitivity logo" width="200px"></a><p>`text_explainability` can be extended to also perform _sensitivity testing_, checking for machine learning model robustness and fairness. The `text_sensitivity` package is available through [PyPI](https://pypi.org/project/text-sensitivity/) and fully documented at [https://marcelrobeer.github.io/text_sensitivity/](https://marcelrobeer.github.io/text_sensitivity/).</p>

---
