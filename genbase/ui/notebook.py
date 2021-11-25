"Jupyter notebook rendering interface."

import importlib.util

from IPython import get_ipython


def is_interactive() -> bool:
    """Check whether the environment is interactive (Jupyter Notebook) and plotly is available for rendering.

    Returns:
        bool: True if interactive, False if not.
    """
    try:
        if ('interactive' in str.lower(get_ipython().__class__.__name__) and 
           importlib.util.find_spec('plotly') is not None):
            return True
        return False
    except:  # noqa: E722
        return False


class Render:
    def __init__(self, *configs):
        self.configs = self.__validate_configs(configs)

    def __validate_configs(self, *configs):
        configs = [li for subli in configs for li in subli]
        for config in configs:
            assert isinstance(config, dict), 'Config should be dict'
            assert 'META' in config, 'Config should contain "META" key'
            assert 'CONTENT' in config, 'Config should contain "CONTENT" key'
        return configs

    def __html(self, config, **renderargs) -> str:
        meta, content = config['META'], config['CONTENT']

        title = renderargs.pop('title', None)
        if title is None:
            if 'title' in meta:
                title = meta['title']
            elif 'type' in meta:
                title = meta['type']
                if 'subtype' in meta:
                    title += f' ({meta["subtype"]})'

        html = ''

        if title is not None:
            html += f'<h1>{title}</h1>'

        return html + f'meta={meta}<br>content={content}'

    def as_html(self, **renderargs) -> str:
        return ''.join(self.__html(config, **renderargs) for config in self.configs)
