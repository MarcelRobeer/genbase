"""Base support for decorators."""

import inspect


def add_calldict(function):
    """Decorator that passes `__call_dict__`  to a function if available. Useful in conjunction with `MetaInfo`."""

    def inner(*args, **kwargs):
        ba = inspect.signature(function).bind(*args, **kwargs)
        ba.apply_defaults()

        # Do not decorate the function if we are unable to pass __call_dict__ as an argument
        if 'kwargs' not in ba.arguments and '__call_dict__' not in ba.arguments:
            return function(*ba.args, **ba.kwargs)

        # Construct __call_dict__ (including introspection of the self argument)
        call_dict = {'__name__': function.__name__, **ba.arguments}
        if hasattr(function, '__self__') and 'self' not in call_dict.keys():
            call_dict['self'] = function.__self__
        if 'self' in call_dict.keys():
            self = call_dict.pop('self')
            call_dict['self'] = self.to_config() if hasattr(self, 'to_config') and hasattr(self, '_dict') \
                else self.__dict__
            if '__name__' not in call_dict['self'] and hasattr(self, '__class__') or hasattr(self, '__name__'):
                call_dict['self']['__name__'] = self.__class__.__name__ if hasattr(self, '__class__') \
                    else self.__name__
        return function(*ba.args, __call_dict__=call_dict, **ba.kwargs)
    return inner
