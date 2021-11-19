"""Default classes for all to inherit from."""

from typing import Optional

from genbase.data import import_data, train_test_split
from genbase.internationalization import (LOCALE_MAP, get_locale, set_locale,
                                          translate_list, translate_string)
from genbase.mixin import CaseMixin, SeedMixin
from genbase.model import from_sklearn


class Readable:
    """Ensure that a class has a readable representation."""

    def __repr__(self):
        public_vars = ', '.join([f'{k}={v}' for k, v in vars(self).items() if not k.startswith('_')])
        return f'{self.__class__.__name__}({public_vars})'


class MetaInfo:
    def __init__(self,
                 type: str,
                 subtype: Optional[str] = None,
                 **kwargs):
        """Meta information class.

        Args:
            type (str): Type description.
            subtype (Optional[str], optional): Subtype description. Defaults to None.
            **kwargs: Optional meta descriptors.
        """
        self._type = type
        self._subtype = subtype
        self._dict = {'type': type}
        if self._subtype is not None:
            self._dict['subtype'] = self._subtype
        self._dict = dict(self._dict, **kwargs)

    @property
    def type(self):
        return self._type

    @property
    def subtype(self):
        return self._subtype

    @property
    def meta(self):
        return self._dict

    def to_json(self):
        content = self.content if hasattr(self, 'content') else ''
        return {'META': self.meta, 'CONTENT': content}


__version__ = '0.1.2'
