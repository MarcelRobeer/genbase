"Jupyter notebook rendering interface."

import importlib.util

import srsly
from IPython import get_ipython

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
    font-family: "Source Sans Pro", sans-serif;
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
    font-family: Roboto, sans-serif;
    line-height: 1.2;
}

ui a,
ui a:visited {
    background-color: transparent;
    color: #000;
    text-decoration: none;
    border-bottom: 1px dotted;
}

ui a:hover,
ui a:active {
    border-bottom: none;
    outline: 0;
}

ui a:focus {
    border-bottom: none;
    outline: thin dotted;
}

ui a img {
    border: 0;
}

footer {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 2rem;
}

footer .credits {
    font-size: 1rem;
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
    background-color: #000;
    color: #fff;
    font-family: Roboto, sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    transition: background-color ease 0.3s;
}

.tabs label .material-icons {
    margin-right: 0.3rem;
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
    color: #000;
    border-top: 4px solid #000;
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

        _ = meta.pop('callargs')
        return html + f'<p>{meta}</p>' + f'<p>{content}</p>'

    def as_html(self, **renderargs) -> str:
        config_ = ''.join(f'{config}' for config in self.configs)
        html = ''.join(self.__html(config, **renderargs) for config in self.configs)

        HTML = f"""
            <div class="ui">
                <section class="ui-wrapper">
                    <div class="ui-container">
                        <div class="ui-block">
                            <div class="tabs">
                                <input type="radio" name="tabs" id="tab1" checked="checked" />
                                <label class="wide" for="tab1">Explanation</label>
                                <div class="tab">{html}</div>

                                <input type="radio" name="tabs" id="tab2" />
                                <label for="tab2">Config</label>
                                <div class="tab code">
                                    <h3>JSON</h3>
                                    <pre>{srsly.json_dumps(config_, indent=2)}</pre>

                                    <h3>YAML</h3>
                                    <pre>{config_}</pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
            """

        return f'<style>{CUSTOM_CSS}</style>{HTML}'
