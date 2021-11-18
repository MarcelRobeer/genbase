"""Support for i18n internationalization."""

import os
from typing import List

import i18n

LOCALE_MAP = {'br': 'pt_BR',
              'cs': 'cs_CZ',
              'da': 'da_DK',
              'el': 'el_GR',
              'ph': 'fil_PH',
              'fr': 'fr_FR',
              'ga': 'ga_IE',
              'hi': 'hi_IN',
              'hr': 'hr_HR',
              'hu': 'hu_HU',
              'id': 'id_ID',
              'it': 'it_IT',
              'jp': 'ja_JP',
              'ka': 'ka_GE',
              'lt': 'lt_LT',
              'lv': 'lv_LV',
              'nl': 'nl_NL',
              'no': 'no_NO',
              'pl': 'pl_PL',
              'pt': 'pt_PT',
              'ro': 'ro_RO',
              'ru': 'ru_RU',
              'sk': 'sk_SK',
              'tr': 'tr_TR',
              'uk': 'uk_UA'}


FOLDER = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
if not os.path.isdir(f'{FOLDER}{os.path.sep}locale'):
    FOLDER = os.path.join(FOLDER, 'genbase')

i18n.load_path.append(os.path.join(FOLDER, 'locale'))
i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'json')
i18n.set('locale', 'nl')
i18n.set('fallback', 'en')
i18n.set('skip_locale_root_data', True)
i18n.resource_loader.init_json_loader()


def translate_string(id: str) -> str:
    """Get a string based on `locale`, as defined in the './locale' folder.

    Args:
        id (str): Identifier of string in `lang.{locale}.yml` file.

    Returns:
        str: String corresponding to locale.
    """
    return i18n.t(f'{id}')


def translate_list(id: str, sep: str = ';') -> List[str]:
    """Get a list based on `locale`, as defined in the './locale' folder.

    Args:
        id (str): Identifier of list in `lang.{locale}.yml` file.
        sep (str, optional): Separator to split elements of list. Defaults to ';'.

    Returns:
        List[str]: List corresponding to locale.
    """
    return i18n.t(f'{id}').split(sep)


def set_locale(locale: str) -> None:
    """Set current locale (choose from `en`, `nl`).

    Args:
        locale (str): Locale to change to.
    """
    return i18n.set('locale', locale)


def get_locale() -> str:
    """Get current locale.

    Returns:
        str: Current locale.
    """
    return i18n.get('locale')
