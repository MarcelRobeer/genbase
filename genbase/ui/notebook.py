from IPython import get_ipython


def is_interactive() -> bool:
    """Check whether the environment is interactive (Jupyter Notebook).

    Returns:
        bool: True if interactive, False if not.
    """
    try:
        if 'interactive' in str.lower(get_ipython().__class__.__name__):
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

    def show(self):
        print("RENDERING GOES HERE!")
