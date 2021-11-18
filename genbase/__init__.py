"""Default classes for all to inherit from."""

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


__version__ = '0.1.2'
