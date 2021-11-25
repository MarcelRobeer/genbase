"""Default classes for all to inherit from."""

from pathlib import Path
from typing import List, Optional

import srsly

from genbase.data import import_data, train_test_split
from genbase.decorator import add_callargs
from genbase.internationalization import (LOCALE_MAP, get_locale, set_locale,
                                          translate_list, translate_string)
from genbase.mixin import CaseMixin, SeedMixin
from genbase.model import from_sklearn
from genbase.utils import recursive_to_dict


class Readable:
    """Ensure that a class has a readable representation."""

    def __repr__(self):
        public_vars = ', '.join([f'{k}={v}' for k, v in vars(self).items() if not k.startswith('_')])
        return f'{self.__class__.__name__}({public_vars})'


class Configurable:
    @classmethod
    def from_config(cls, config: dict, **kwargs) -> 'Configurable':
        config = {**config, **kwargs}
        _ = config.pop('__class__', None)
        return cls(**config)

    @classmethod
    def read_json(cls, path: str, **read_args) -> 'Configurable':
        read_fn = srsly.read_json
        if path.endswith('.json.gz'):
            read_fn = srsly.read_gzip_json
        elif path.endswith('.jsonl'):
            read_fn = srsly.read_jsonl
        return cls.from_config(read_fn(path, **read_args))

    @classmethod
    def from_json(cls, json_or_path: str, **read_args) -> 'Configurable':
        if Path.is_file(json_or_path):
            cls.read_json(json_or_path, **read_args)
        return cls.from_config(srsly.json_loads(json_or_path))

    @classmethod
    def read_yaml(cls, path: str) -> 'Configurable':
        return srsly.read_yaml(path)

    @classmethod
    def from_yaml(cls, yaml_or_path: str) -> 'Configurable':
        if Path.is_file(yaml_or_path):
            return cls.from_config(cls.read_yaml(yaml_or_path))
        return cls.from_config(srsly.yaml_loads(yaml_or_path))

    def to_config(self, exclude: List[str]) -> dict:
        return dict(recursive_to_dict(self, exclude=exclude))

    def to_json(self, indent: int = 2) -> str:
        return srsly.json_dumps(self.to_config(), indent=indent)

    def to_yaml(self, **write_args) -> str:
        return srsly.yaml_dumps(self.to_config(), **write_args)

    def write_json(self, path: str, indent: int = 2) -> None:
        write_fn = srsly.write_json
        if path.endswith('.json.gz'):
            write_fn = srsly.write_gzip_json
        elif path.endswith('.jsonl'):
            write_fn = srsly.write_jsonl
        return write_fn(path, self.to_config(), indent=indent)

    def write_yaml(self, path: str, **write_args) -> None:
        return srsly.write_yaml(path, self.to_config(), **write_args)


class MetaInfo(Configurable):
    def __init__(self,
                 type: str,
                 subtype: Optional[str] = None,
                 fn_name: Optional[str] = None,
                 callargs: Optional[dict] = None,
                 **kwargs):
        """Meta information class.

        Args:
            type (str): Type description.
            subtype (Optional[str], optional): Subtype description. Defaults to None.
            **kwargs: Optional meta descriptors.
        """
        self._type = type
        self._subtype = subtype
        self._callargs = callargs
        self._dict = {'type': type}
        if self._subtype is not None:
            self._dict['subtype'] = self._subtype
        if fn_name is not None:
            self._callargs['__name__'] = fn_name
        if self._callargs is not None:
            self._dict['callargs'] = self._callargs
        self._dict = dict(self._dict, **kwargs)

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

    def to_config(self):
        content = self.content if hasattr(self, 'content') \
            else super().to_config(exclude=['_type', '_subtype', '_dict', '_callargs'])
        return {'META': self.meta, 'CONTENT': content() if callable(content) else content}


__version__ = '0.1.8'
