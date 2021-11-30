"""Jupyter notebook rendering interface."""

import traceback

import srsly
from IPython import get_ipython

PACKAGE_LINK = 'https://git.science.uu.nl/m.j.robeer/genbase/'
MAIN_COLOR = '#000000'
CUSTOM_CSS = """
ui {
    -webkit-text-size-adjust: 100%;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    padding: 0;
    margin: 0;
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
    background-color: #e5e5e5;
    color: #1a1a1a;
    font-family: sans-serif;
    font-size: 1rem;
    line-height: 1.6;
}

ui h1,
ui h2,
ui h3,
ui h4,
ui h5,
ui h6 {
    color: #0d0d0d;
    line-height: 1.2;
}

footer a,
footer a:visited,
ui a,
ui a:visited {
    background-color: transparent;
    color: --var(ui_color);
    border-bottom: 1px dotted;
    line-height: 1.6;
}

footer a:hover,
footer a:active,
ui a:hover,
ui a:active {
    border-bottom: none;
    outline: 0;
}

footer a:focus,
ui a:focus {
    border-bottom: none;
    outline: thin dotted;
}

footer a img,
ui a img {
    border: 0;
}

footer {
    text-align: right;
    margin: 0 1rem;
    font-size: 1rem;
    color: #999;
}

.ui-container {
    padding: 0.2rem;
}

.ui-block {
    display: flex;
    align-items: center;
    justify-content: center;
}

.tabs {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
    box-shadow: 0 8px 8px rgba(0, 0, 0, 0.4);
}

.tabs label {
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

.tabs .tab {
    flex-grow: 1;
    width: 100%;
    height: 100%;
    display: none;
    padding: 1rem 2rem;
    color: #000;
    background-color: #fff;
}

.tabs .tab > *:not(:last-child) {
    margin-bottom: 0.8rem;
}

.tabs [type=radio] {
    display: none;
}

.tabs [type=radio]:checked + label {
    background-color: #fff;
    color: --var(ui_color);
    border-top: 4px solid --var(ui_color);
}

.tabs [type=radio]:checked + label + .tab {
    display: block;
}

.code pre {
    font-family: Consolas, monospace;
    background-color: #eff5f6;
    box-sizing: content-box;
    padding: 2rem 1.5rem;
    max-height: 30rem;
    overflow-x: hidden;
    overflow-y: scroll;
    box-shadow: inset 0 4px 4px rgba(0, 0, 0, 0.15);
}

p.info {
    color: #aaa;
}

@media (min-width: 768px) {
    body.home {
        font-size: 1.125rem;
    }

    .ui-container {
        padding: 2rem 2rem;
    }

    .tabs label {
        order: 1;
        width: auto;
    }

    .tabs label.wide {
        flex: 1;
        align-items: left;
        justify-content: left;
    }

    .tabs .tab {
        order: 9;
    }

    .tabs [type=radio]:checked + label {
        border-bottom: none;
    }
}
"""


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


def matplotlib_available() -> bool:
    """Check if `matplotlib` is installed.

    Returns:
        bool: True if available, False if not.
    """
    import importlib.util
    return importlib.util.find_spec('matplotlib') is not None


def plotly_available() -> bool:
    """Check if `plotly` is installed.

    Returns:
        bool: True if available, False if not.
    """
    import importlib.util
    return importlib.util.find_spec('plotly') is not None


class Render:
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
        self.main_color = MAIN_COLOR
        self.package_link = PACKAGE_LINK
        self.extra_css = ''

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

    def render_content(self, meta: dict, content: dict, **renderargs) -> str:
        """Render content as HTML. Overwrite this when subclassing for your custom implementation.

        Args:
            meta (dict): Meta config.
            content (dict): Content config.
            **renderags: Optional arguments for rendering.

        Returns:
            str: Formatted content.
        """
        return f'<p>{meta}</p>' + f'<p>{content}</p>'

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

        HTML = f"""
            <div class="ui">
                <section class="ui-wrapper">
                    <div class="ui-container">
                        <div class="ui-block">
                            <div class="tabs">
                                <input type="radio" name="tabs" id="tab1" checked="checked" />
                                <label class="wide" for="tab1">{self.tab_title}</label>
                                <div class="tab">{html}</div>

                                <input type="radio" name="tabs" id="tab2" />
                                <label for="tab2">{self.config_title}</label>
                                <div class="tab code">
                                    <h3>JSON</h3>
                                    <pre>{json}</pre>

                                    <h3>YAML</h3>
                                    <pre>{yaml}</pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
            """

        main_color = renderargs.pop('main_color', self.main_color)
        package = renderargs.pop('package_link', self.package_link)
        package_name = self.package_name

        CSS = self.css(ui_color=main_color)
        FOOTER = f'<footer>Generated with <a href="{package}" target="_blank">{package_name}</a></footer>'

        return f'<style>{CSS}</style>{HTML}{FOOTER}'
