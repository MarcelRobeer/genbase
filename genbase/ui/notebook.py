"""Jupyter notebook rendering interface."""

import traceback
import uuid
from typing import List, Union

import srsly
from IPython import get_ipython

from .plot import plotly_available
from .svg import CLONE as CLONE_SVG

PACKAGE_LINK = 'https://git.science.uu.nl/m.j.robeer/genbase/'
MAIN_COLOR = '#000000'
CUSTOM_CSS = """
#--var(ui_id),
#--var(ui_id) + footer {
    -webkit-text-size-adjust: 100%;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
    margin: 1em;
    font-family: sans-serif;
    font-size: 1.2rem;
    line-height: 1.2;
}

#--var(ui_id) h1,
#--var(ui_id) h2,
#--var(ui_id) h3,
#--var(ui_id) h4,
#--var(ui_id) h5,
#--var(ui_id) h6 {
    color: #0d0d0d;
    line-height: 1.2;
}

#--var(ui_id) + footer a,
#--var(ui_id) + footer a:visited,
#--var(ui_id) a,
#--var(ui_id) a:visited {
    background-color: transparent;
    color: --var(ui_color);
    line-height: 1.6;
}

#--var(ui_id) + footer a:hover,
#--var(ui_id) + footer a:active,
#--var(ui_id) a:hover,
#--var(ui_id) a:active {
    border-bottom: none;
    outline: 0;
}

#--var(ui_id) + footer a:focus,
#--var(ui_id) a:focus {
    border-bottom: none;
    outline: thin dotted;
}

#--var(ui_id) + footer a img,
#--var(ui_id) a img {
    border: 0;
}

#--var(ui_id) + footer {
    text-align: right;
    margin: 0 1rem;
    font-size: 1rem;
    color: #999;
}

#--var(ui_id) .ui-container {
    padding: 0.2rem;
}

#--var(ui_id) .ui-block {
    display: flex;
    align-items: center;
    justify-content: center;
}

#--var(tabs_id) {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
    box-shadow: 0 8px 8px rgba(0, 0, 0, 0.4);
}

#--var(tabs_id) label {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem 2rem;
    margin-right: 0.0625rem;
    cursor: pointer;
    background-color: --var(ui_color);
    color: #fff;
    font-size: 1.2rem;
    font-weight: 700;
    transition: background-color ease 0.3s;
}

#--var(tabs_id) .tab {
    flex-grow: 1;
    width: 100%;
    height: 100%;
    display: none;
    padding: 1rem 2rem;
    color: #000;
    background-color: #fff;
}

#--var(tabs_id) .tab > *:not(:last-child) {
    margin-bottom: 0.8rem;
}

#--var(tabs_id) [type=radio] {
    display: none;
}

#--var(tabs_id) [type=radio]:checked + label {
    background-color: #fff;
    color: --var(ui_color);
    border-top: 4px solid --var(ui_color);
}

#--var(tabs_id) [type=radio]:checked + label + .tab {
    display: block;
}

#--var(tabs_id) .code > pre {
    color: #111;
    font-family: Consolas, monospace;
    background-color: #eee !important;
    box-sizing: content-box;
    padding: 0.5rem 0.3rem !important;
    max-height: 30rem;
    overflow-x: hidden;
    overflow-y: scroll;
    box-shadow: inset 0 4px 4px rgba(0, 0, 0, 0.15);
}

#--var(tabs_id) .code section {
    position: relative;
}

#--var(tabs_id) .code section:not(:first-child) {
    margin-top: 2rem;
}

#--var(tabs_id) .code h3 {
    font-size: 18px;
    display: inline;
}

#--var(tabs_id) .code .pre-buttons {
    position: inherit;
    float: right;
}

#--var(tabs_id) .code .pre-buttons > a {
    position: relative;
    all: unset;
    height: 20px;
    width: 20px;
    background: none;
    font: inherit;
    outline: inherit;
    display: block;
}

#--var(tabs_id) .code .pre-buttons > a:hover {
    color: --var(ui_color);
}

#--var(tabs_id) .code a > svg {
    position: absolute;
    top: 0px;
    left: 0px;
    height: 18px;
}

#--var(tabs_id) .code a.copy:before {
    content: 'Copied to clipboard!';
    opacity: 0;
    position: fixed;
    bottom: 8px;
    right: 8px;
    padding: 1rem;
    color: #fff;
    background-color: #28a745;
    box-shadow: 0 4px 4px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease-in-out 2s;
}

#--var(tabs_id) .code a:active::before {
    opacity: 1;
    transition: 0s;
}

#--var(tabs_id) .code a:hover > svg,
#--var(tabs_id) .code a:hover > svg > * {
    stroke: --var(ui_color);
}

#--var(tabs_id) .code a:active > svg,
#--var(tabs_id) .code a:active > svg > * {
    stroke: #28a745;
}

#--var(tabs_id) p.info {
    color: #898989;
}

#--var(tabs_id) .instances-wrapper {
    max-height: 40rem;
}

#--var(tabs_id) .table-wrapper {
    overflow-y: scroll;
    background:
    linear-gradient(white 30%, rgba(255, 255, 255, 0)),
    linear-gradient(rgba(255, 255, 255, 0), white 70%) 0 100%,
    radial-gradient(50% 0, farthest-side, rgba(0, 0, 0, .2), rgba(0, 0, 0, 0)),
    radial-gradient(50% 100%, farthest-side, rgba(0, 0, 0, .2), rgba(0, 0, 0, 0)) 0 100%;
    background:
    linear-gradient(white 30%, rgba(255, 255, 255, 0)),
    linear-gradient(rgba(255, 255, 255, 0), white 70%) 0 100%,
    radial-gradient(farthest-side at 50% 0, rgba(0, 0, 0, .2), rgba(0, 0, 0, 0)),
    radial-gradient(farthest-side at 50% 100%, rgba(0, 0, 0, .2), rgba(0, 0, 0, 0)) 0 100%;
    background-repeat: no-repeat;
    background-color: white;
    background-size: 100% 40px, 100% 40px, 100% 14px, 100% 14px;
    background-attachment: local, local, scroll, scroll;
}

#--var(tabs_id) .table-wrapper table {
    table-layout: auto;
    width: 100%;
    font-size: 1em;
    border-collapse: collapse;
}

#--var(tabs_id) .table-wrapper tr:nth-child(odd) {
    background-color: rgba(0, 0, 0, 0.05);
}

#--var(tabs_id) .table-wrapper tr:hover {
    background-color: rgba(66, 165, 245, 0.2);
}

#--var(tabs_id) .table-wrapper td:nth-child(2),
#--var(tabs_id) .table-wrapper th:nth-child(2) {
    width: 99%;
}

#--var(tabs_id) .table-wrapper tr > td {
    text-align: left;
    padding: 1em;
    text-align: left;
}

#--var(tabs_id) .table-wrapper th {
    color: #fff;
    background-color: --var(ui_color);
}

#--var(tabs_id) .table-wrapper tr > th {
    text-align: left;
    padding: 1em;
    margin: -0.5em;
}

@media (min-width: 768px) {
    #--var(ui_id) {
        font-size: 1.33rem;
    }

    .ui-container {
        padding: 2rem 2rem;
    }

    #--var(tabs_id) label {
        order: 1;
        width: auto;
    }

    #--var(tabs_id) label.wide {
        flex: 1;
        align-items: left;
        justify-content: left;
    }

    #--var(tabs_id) .tab {
        order: 9;
    }

    #--var(tabs_id) [type=radio]:checked + label {
        border-bottom: none;
    }
}
"""
CUSTOM_JS = """
function copy(elem){
    var content = document.getElementById(elem).innerHTML;

    navigator.clipboard.writeText(content)
        .then(() => {
        console.log("Text copied to clipboard!")
    })
        .catch(err => {
        console.log('Something went wrong', err);
    })
}
"""


def format_label(label: str, label_name: str = 'Label', h: str = 'h3') -> str:
    """Format label as title.

    Args:
        label (str): Name of label
        label_name (str, optional): Label name. Defaults to 'Label'.
        h (str, optional): h-tag (h1, h2, ...). Defaults to 'h1'.

    Returns:
        str: Formatted label title.
    """
    return f'<{h}>{label_name.title()}: <kbd>{label}</kbd></{h}>'


def format_instance(instance: dict, **kwargs) -> str:
    """Format an `instancelib` instance.

    Args:
        instance (dict): `instancelib` instance exported to config.

    Returns:
        str: Formatted instance.
    """
    repr = instance['_representation'] if '_representation' in instance else instance['_data']
    identifier = instance['_identifier']
    instance_title = instance.get('__class__', '')
    optional_columns = ''.join(f'<td>{v}</td>' for v in kwargs.values())
    return f'<tr title="{instance_title}"><td>{identifier}</td><td>{repr}</td>{optional_columns}</tr>'


def format_instances(instances: Union[dict, List[dict]], **kwargs) -> str:
    """Format multiple `instancelib` instances.

    Args:
        instances (Union[dict, List[dict]]): instances.
        **kwargs: Optional named columns.

    Returns:
        str: Formatted instances.
    """
    if isinstance(instances, dict):
        instances = [instances]
    for k, v in kwargs.items():
        if isinstance(v, str):
            kwargs[k] = [v] * len(instances)
        elif isinstance(v, dict) and 'labelset' in v and 'labeldict' in v:
            kwargs[k] = {k_: ', '.join([f'<kbd>{v__}</kbd>' for v__ in v_]) for k_, v_ in v['labeldict'].items()}
        elif not isinstance(v, list):
            raise ValueError(f'Unable to parse {type(v)} ({v})')

    content = ''.join([format_instance(instance, **{k: v[i] if isinstance(v, list) else v[instance['_identifier']]
                                                    for k, v in kwargs.items()})
                       for i, instance in enumerate(instances)])
    header = ''.join([f'<th>{h}</th>' for h in ['ID', 'Instance'] + [str(k).title() for k in kwargs.keys()]])

    return f'<div class="instances-wrapper table-wrapper"><table><tr>{header}</tr>{content}</table></div>'


def is_interactive() -> bool:
    """Check whether the environment is interactive (Jupyter Notebook) and plotly is available for rendering.

    Returns:
        bool: True if interactive, False if not.
    """
    try:
        if 'interactive' in str.lower(get_ipython().__class__.__name__):
            return True
        return False
    except:  # noqa: E722
        return False


def internet_connection(url: str = 'http://www.pypi.org', timeout: int = 5) -> bool:
    """Check whether there is an active internet connection, by trying to reach an URL within timeout.

    Args:
        url (str, optional): URL to connect to. Defaults to 'http://www.pypi.org'.
        timeout (int, optional): Timeout. Defaults to 5.

    Returns:
        bool: True if has internet connection, else False.
    """
    import requests

    try:
        requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


class Render:
    main_color = MAIN_COLOR
    package_link = PACKAGE_LINK
    extra_css = ''

    def __init__(self, *configs):
        """Base class for rendering configs (configuration dictionaries).

        Example:
            Writing your own custom rendering functions `format_title()` and `render_content()`, and give the tab 
            a custom title `tab_title`, set the main UI color to red (`#ff0000`) and package link (URL in footer):

            >>> from genbase.ui.notebook import Render
            >>> class CustomRender(Render):
            ...     def __init__(self, *configs):
            ...         super().__init__(*configs)
            ...         self.tab_title = 'My Custom Explanation'
            ...         self.main_color = '#ff00000'
            ...         self.package_link = 'https://git.io/text_explainability'
            ...
            ...     def format_title(self, title: str, h: str = 'h1', **renderargs) -> str:
            ...         return f'<{h} style="color: red;">{title}</{h}>
            ...
            ...     def render_content(self, meta: dict, content: dict, **renderargs):
            ...         type = meta['type'] if 'type' in meta else ''
            ...         return type.replace(' ').title() if 'explanation' in type else type
        """
        self.configs = self.__validate_configs(configs)
        self.config_title = 'Config'
        self.main_color = Render.main_color
        self.package_link = Render.package_link
        self.extra_css = Render.extra_css

    def __validate_configs(self, *configs):
        configs = [li for subli in configs for li in subli]
        for config in configs:
            assert isinstance(config, dict), 'Config should be dict'  # nosec
            assert 'META' in config, 'Config should contain "META" key'  # nosec
            assert 'CONTENT' in config, 'Config should contain "CONTENT" key'  # nosec
        return configs

    @property
    def tab_title(self, **renderargs) -> str:
        """Title of content tab."""
        title = 'Explanation'
        titles = [config['META']['title'] for config in self.configs if 'title' in config['META']]
        if titles:
            title = ' | '.join(list(set(titles)))
        if 'title' in renderargs:
            title = renderargs['title']
        return title

    @property
    def custom_tab_title(self, **renderargs) -> str:
        """Title of custom tab."""
        return ''

    @property
    def package_name(self) -> str:
        if hasattr(self, '_package_name'):
            return self._package_name
        return self.package_link.rstrip('/').split('/')[-1]

    @package_name.setter
    def package_name(self, package_name: str):
        self._package_name = package_name

    def css(self, **replacement_kwargs):
        css_ = CUSTOM_CSS + '\n' + self.extra_css
        for k, v in replacement_kwargs.items():
            css_ = css_.replace(f'--var({k})', v)
        return css_

    def format_title(self, title: str, h: str = 'h1', **renderargs) -> str:
        """Format title in HTML format.

        Args:
            title (str): Title contents.
            h (str, optional): h-tag (h1, h2, ...). Defaults to 'h1'.

        Returns:
            str: Formatted title.
        """
        return f'<{h}>{title}</{h}>'

    def format_subtitle(self, subtitle: str) -> str:
        """Format the subtitle in HTML format.

        Args:
            subtitle (str): Subtitle contents.

        Returns:
            str: Formatted subtitle.
        """
        return f'<p class="info">{subtitle}</p>'

    def render_title(self, meta: dict, content: dict, **renderargs) -> str:
        """Render the title as HTML. Overwrite this when subclassing for your custom implementation.

        Args:
            meta (dict): Meta config.
            content (dict): Content config.
            **renderags: Optional arguments for rendering.

        Returns:
            str: Formatted title.
        """
        title = renderargs.pop('title', None)
        if title is None:
            if 'title' in meta:
                title = meta['title']
            elif 'type' in meta:
                title = meta['type']
                if 'subtype' in meta:
                    title += f' ({meta["subtype"]})'

        return self.format_title(title, **renderargs) if title else ''

    def render_subtitle(self, meta: dict, content: dict, **renderargs) -> str:
        return self.format_subtitle(renderargs['subtitle']) if 'subtitle' in renderargs else ''

    def get_renderer(self, meta: dict):
        """Get a render function (Callable taking `meta`, `content` and `**renderargs` and returning a `str`).

        Args:
            meta (dict): Meta information to decide on appropriate renderer.
        """
        def default_renderer(meta, content, **renderargs):
            return f'<p>{meta}</p>' + f'<p>{content}</p>'
        return default_renderer

    def render_content(self, meta: dict, content: dict, **renderargs) -> str:
        """Render content as HTML. Overwrite this when subclassing for your custom implementation.

        Args:
            meta (dict): Meta config.
            content (dict): Content config.
            **renderags: Optional arguments for rendering.

        Returns:
            str: Formatted content.
        """
        renderer = self.get_renderer(meta)
        return renderer(meta, content, **renderargs)

    def render_elements(self, config: dict, **renderargs) -> str:
        """Render HTML title and content.

        Args:
            config (dict): Config meta & content.
            **renderags: Optional arguments for rendering.

        Returns:
            str: Formatted title and content.
        """
        meta, content = config['META'], config['CONTENT']
        return self.render_title(meta, content, **renderargs) + \
            self.render_subtitle(meta, content, **renderargs) + \
            self.render_content(meta, content, **renderargs)

    def custom_tab(self, config: dict, **renderargs) -> str:
        return ''

    def as_html(self, **renderargs) -> str:
        """Get HTML element for interactive environments (e.g. Jupyter notebook).

        Args:
            **renderags: Optional arguments for rendering.

        Returns:
            str: HTML element.
        """
        def fmt_exception(e: Exception, fmt_type: str = 'JSON') -> str:
            res = f'ERROR IN PARSING {fmt_type}\n'
            res += '=' * len(res) + '\n'
            return res + '\n'.join(traceback.TracebackException.from_exception(e).format())

        try:
            json = '\n'.join(srsly.json_dumps(config, indent=2) for config in self.configs)
        except TypeError as e:
            json = fmt_exception(e, fmt_type='JSON')

        try:
            yaml = '\n'.join(srsly.yaml_dumps(config) for config in self.configs)
        except srsly.ruamel_yaml.representer.RepresenterError as e:
            yaml = fmt_exception(e, fmt_type='YAML')

        html = ''.join(self.render_elements(config, **renderargs) for config in self.configs)
        id = str(uuid.uuid4())
        tabs_id = f'tabs-{id}'
        ui_id = f'ui-{id}'

        CUSTOM_TAB = ''.join(self.custom_tab(config, **renderargs) for config in self.configs)
        if CUSTOM_TAB:
            CUSTOM_TAB = f"""<input type="radio" name="{tabs_id}" id="{tabs_id}-tab2"/>
                             <label class="wide" for="{tabs_id}-tab2">{self.custom_tab_title}</label>
                             <div class="tab">{CUSTOM_TAB}</div>"""

        HTML = f"""
        <div id="{ui_id}">
            <section class="ui-wrapper">
                <div class="ui-container">
                    <div class="ui-block">
                        <div id="{tabs_id}">
                            <input type="radio" name="{tabs_id}" id="{tabs_id}-tab1" checked="checked" />
                            <label class="wide" for="{tabs_id}-tab1">{self.tab_title}</label>
                            <div class="tab">{html}</div>
                            {CUSTOM_TAB}
                            <input type="radio" name="{tabs_id}" id="{tabs_id}-tab{'3' if CUSTOM_TAB else '2'}" />
                            <label for="{tabs_id}-tab{'3' if CUSTOM_TAB else '2'}">{self.config_title}</label>
                            <div class="tab code">
                                <section>
                                    <div class="pre-buttons">
                                <a class='copy' onclick="copy('json-output')" href="#" title="Copy JSON to clipboard">
                                    {CLONE_SVG}
                                </a>
                                    </div>
                                    <h3>JSON</h3>
                                </section>
                                <pre id="json-output">{json}</pre>

                                <section>
                                    <div class="pre-buttons">
                                <a class='copy' onclick="copy('yaml-output')" href="#" title="Copy YAML to clipboard">
                                    {CLONE_SVG}
                                </a>
                                    </div>
                                    <h3>YAML</h3>
                                </section>
                                <pre id="yaml-output">{yaml}</pre>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        """

        JS = f'<script type="text/javascript">{CUSTOM_JS}</script>' if CUSTOM_JS else ''

        main_color = renderargs.pop('main_color', self.main_color)
        package = renderargs.pop('package_link', self.package_link)
        package_name = self.package_name

        CSS = self.css(ui_color=main_color, ui_id=ui_id, tabs_id=tabs_id)
        FOOTER = f'<footer>Generated with <a href="{package}" target="_blank">{package_name}</a></footer>'

        return f'<style>{CSS}</style>{HTML}{FOOTER}{JS}'


if is_interactive() and not internet_connection() and plotly_available():
    from plotly.offline import init_notebook_mode
    init_notebook_mode(connected=False)
