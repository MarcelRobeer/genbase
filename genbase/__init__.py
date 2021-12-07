"""Default classes for all to inherit from."""

import builtins
from pathlib import Path
from typing import List, Optional

import srsly

from genbase.data import import_data, train_test_split
from genbase.decorator import add_callargs
from genbase.internationalization import (LOCALE_MAP, get_locale, set_locale,
                                          translate_list, translate_string)
from genbase.mixin import CaseMixin, SeedMixin
from genbase.model import from_sklearn
from genbase.ui import Render, is_interactive
from genbase.utils import recursive_to_dict


class Readable:
    """Ensure that a class has a readable representation."""

    def __repr__(self):
        public_vars = ', '.join([f'{k}={v}' for k, v in vars(self).items() if not k.startswith('_')])
        return f'{self.__class__.__name__}({public_vars})'


class Configurable:
    """Add working with configs (configuration dictionaries) to a class."""

    @classmethod
    def from_config(cls, config: dict, **kwargs) -> 'Configurable':
        config = {**config, **kwargs}
        _ = config.pop('__class__', None)
        return cls(**config)

    @classmethod
    def read_json(cls, path: str, **read_args) -> 'Configurable':
        """Read config from JSON file (GZIP JSON, JSONL or JSON).

        Args:
            path (str): File path.
            **read_args: Optional arguments passed to `srsly.read_json()`/`srsly.read_jsonl()`/`srsly.read_gzip_json`.
        """
        read_fn = srsly.read_json
        if path.endswith('.json.gz'):
            read_fn = srsly.read_gzip_json
        elif path.endswith('.jsonl'):
            read_fn = srsly.read_jsonl
        return cls.from_config(read_fn(path, **read_args))

    @classmethod
    def from_json(cls, json_or_path: str, **read_args) -> 'Configurable':
        """Get config from JSON string or filepath.

        Args:
            json_or_path (str): File path or JSON string.
            **read_args: Optional arguments passed to `srsly.read_json()`/`srsly.read_jsonl()`/`srsly.read_gzip_json`.
        """
        if Path.is_file(json_or_path):
            cls.read_json(json_or_path, **read_args)
        return cls.from_config(srsly.json_loads(json_or_path))

    @classmethod
    def read_yaml(cls, path: str) -> 'Configurable':
        """Read config from YAML file.

        Args:
            path (str): File path.
        """
        return srsly.read_yaml(path)

    @classmethod
    def from_yaml(cls, yaml_or_path: str) -> 'Configurable':
        """Get config from YAML string or filepath.

        Args:
            yaml_or_path (str): File path or YAML string.
        """
        if Path.is_file(yaml_or_path):
            return cls.from_config(cls.read_yaml(yaml_or_path))
        return cls.from_config(srsly.yaml_loads(yaml_or_path))

    def to_config(self, exclude: List[str]) -> dict:
        """Convert class information into config (configuration dictionary).

        Args:
            exclude (List[str]): Names of variables to exclude.

        Returns:
            dict: [description]
        """
        return dict(recursive_to_dict(self, exclude=exclude))

    def to_json(self, indent: int = 2) -> str:
        """Convert config to JSON-formatted string.

        Args:
            indent (int, optional): Number of spaces to indent JSON. Defaults to 2.

        Returns:
            str: Config formatted as JSON.
        """
        return srsly.json_dumps(self.to_config(), indent=indent)

    def to_yaml(self, **write_args) -> str:
        """Convert config to YAML-formatted string.

        Args:
            **write_args: Optional arguments passed to `srsly.yaml_dumps()`

        Returns:
            str: Config formatted as YAML.
        """
        return srsly.yaml_dumps(self.to_config(), **write_args)

    def write_json(self, path: str, indent: int = 2) -> None:
        """Write class config to JSON.

        Args:
            path (str): Path to save to. If ends in `.json.gz` saves as GZIP JSON, `.jsonl` as JSONL or JSON by default.
            indent (int, optional): Number of spaces to indent JSON. Defaults to 2.
        """
        write_fn = srsly.write_json
        if path.endswith('.json.gz'):
            write_fn = srsly.write_gzip_json
        elif path.endswith('.jsonl'):
            write_fn = srsly.write_jsonl
        write_fn(path, self.to_config(), indent=indent)

    def write_yaml(self, path: str, **write_args) -> None:
        """Write class config to YAML.

        Args:
            path (str): Path to save to.
            **write_args: Optional arguments passed to `srsly.write_yaml()`
        """
        srsly.write_yaml(path, self.to_config(), **write_args)


class MetaInfo(Configurable):
    def __init__(self,
                 type: str,
                 subtype: Optional[str] = None,
                 fn_name: Optional[str] = None,
                 callargs: Optional[dict] = None,
                 renderargs: Optional[dict] = None,
                 renderer = Render,
                 **kwargs):
        """Meta information class.

        Args:
            type (str): Type description.
            subtype (Optional[str], optional): Subtype description. Defaults to None.
            callargs (Optional[dict], optional): Arguments used when the function was called. Defaults to None.
            renderargs (Optional[dict], optional): Custom arguments passed to renderer. Defaults to None.
            renderer
            **kwargs: Optional meta descriptors.
        """
        self._type = type
        self._subtype = subtype
        self._callargs = callargs
        self._renderargs = renderargs
        self._dict = {'type': type}
        if self._subtype is not None:
            self._dict['subtype'] = self._subtype
        if fn_name is not None:
            self._callargs['__name__'] = fn_name
        if self._callargs is not None:
            self._dict['callargs'] = self._callargs
        if self._renderargs is not None:
            self._dict['renderargs'] = self._renderargs
        self._dict = dict(self._dict, **kwargs)
        self._renderer = renderer if isinstance(renderer, builtins.type) else renderer.__class__

    @property
    def type(self):
        return self._type

    @property
    def subtype(self):
        return self._subtype

    @property
    def callargs(self):
        return self._callargs

    @property
    def meta(self):
        return self._dict

    @property
    def renderargs(self):
        return self._renderargs if self._renderargs is not None else {}

    def to_config(self):
        if hasattr(self, 'content'):
            _content = self.content() if callable(self.content) else self.content
            content = dict(recursive_to_dict(_content, include_class=False))
        else:
            content = super().to_config(exclude=['_type', '_subtype', '_dict', '_callargs'])

        return {'META': self.meta, 'CONTENT': content}

    def _repr_html_(self) -> str:
        return self._renderer(self.to_config()).as_html(**self.renderargs) if is_interactive() else repr(self)


__version__ = '0.1.16'
